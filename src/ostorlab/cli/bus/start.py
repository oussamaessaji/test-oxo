import asyncio
import dataclasses
import logging
from typing import List

from ostorlab.apis import scanner_config
from ostorlab.apis.runners import authenticated_runner

WAIT_SCHEDULE_SCAN = 60  # seconds


from ostorlab.cli.bus import handler


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


@dataclasses.dataclass
class SubjectBusConfigs:
    subject: str
    queue: str


@dataclasses.dataclass
class ScannerConfig:
    bus_url: str
    bus_cluster_id: str
    bus_client_name: str
    subject_bus_configs: List[SubjectBusConfigs]

    @classmethod
    def from_json(cls, config):
        subject_configs = config["data"]["scanners"]["scanners"][0]["config"]
        bus_configs = []
        for subject_config in subject_configs["subjectBusConfigs"]["subjectBusConfigs"]:
            bus_configs.append(SubjectBusConfigs(subject=subject_config["subject"], queue=subject_config["queue"]))
        return cls(
            bus_url=config["data"]["scanners"]["scanners"][0]["config"]["busUrl"],
            bus_cluster_id=config["data"]["scanners"]["scanners"][0]["config"]["busClusterId"],
            bus_client_name=config["data"]["scanners"]["scanners"][0]["config"]["busClientName"],
            subject_bus_configs=bus_configs
        )


def _handle_exception(loop, context):
    logger.error(f"Caught Loop Exception: {context}")


class ScanHandler:
    def __init__(self):
        self._bus_handlers = []

    async def close(self):
        for handler in self._bus_handlers:
            await handler.close()

    async def _subscribe(self, config, subject, queue, cb, stream, start_at="first"):
        bus_handler = await self._create_bus_handler(config)
        asyncio.create_task(bus_handler.ensure_running_handler())
        await bus_handler.connect()
        await bus_handler.add_stream(name=stream, subjects=[subject])
        await bus_handler.subscribe(
            subject=subject, queue=queue, cb=cb, start_at=start_at
        )
        self._bus_handlers.append(bus_handler)

    async def subscribe_all(self, config):
        for bus_conf in config.subject_bus_configs:
            if bus_conf.subject == "scan.startAgentScan":
                await self._subscribe(
                    config=config,
                    subject=bus_conf.subject,
                    queue=bus_conf.queue,
                    cb=self._persist_agent_scan,
                    start_at="last_received",
                    stream=bus_conf.queue,
                )
            elif bus_conf.subject in ["scan_engine.scan_saved", "scan_engine.scan_done", "scan_engine.scan_start_request"]:
                await self._subscribe(
                    config=config,
                    subject=f"scan_engine.scan_done",
                    queue=bus_conf.queue,
                    cb=self._start_scan_scheduling,
                    start_at="last_received",
                    stream=bus_conf.queue,
                )

            logger.info(f"subscribing to scan_engine.scan_saved")
            return

    async def _message_handler(self, subject, request, cb):
        loop = asyncio.get_event_loop()
        scan = await loop.run_in_executor(None, cb, request)
        logger.info("publishing scan_saved event")

        bus_handler = await self._create_bus_handler()
        await bus_handler.connect()
        await bus_handler.publish(
            "scan_engine.scan_saved",
            {"scan_id": scan.id, "reference_scan_id": request.reference_scan_id},
            stream="engine_saved",
        )
        logger.info("done persisting scan")
        await bus_handler.close()

    async def _persist_agent_scan(self, subject, request):

        await self._message_handler(
            subject, request, None
        )

    async def _create_bus_handler(self, config):
        bus_handler = handler.BusHandler(
            bus_url=config.bus_url, cluster_id=config.bus_cluster_id, name=config.bus_client_name
        )
        return bus_handler

    async def _start_scan_scheduling(self, subject, request):
        logger.info(f"scheduling scan from request {request.scan_id}")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, None)
        logger.info("done scheduling scan")


async def connect_nats(config: ScannerConfig, scanner_id: str):
    try:
        logger.info(
            f"starting bus runner for scanner {scanner_id}"
        )
        scan_handler = ScanHandler()
        logger.info("connected, subscribing to plans channels ...")
        await scan_handler.subscribe_all(config)
        logger.info("subscribed")
        return scan_handler
    except Exception as e:
        logger.exception("run exception %s", e)


async def subscribe_to_nats(api_key: str, scanner_id: str):
    import nest_asyncio
    nest_asyncio.apply()
    runner = authenticated_runner.AuthenticatedAPIRunner(
        api_key=api_key
    )
    data = runner.execute(scanner_config.ScannerConfigAPIRequest(scanner_id=scanner_id))
    config = ScannerConfig.from_json(data)
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(_handle_exception)
    loop.run_until_complete(connect_nats(config, scanner_id))
    try:
        logger.info("starting forever loop")
        loop.run_forever()
    finally:
        logger.info("closing loop")
        loop.close()



