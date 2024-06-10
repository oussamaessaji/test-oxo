"""Asset of type IP.
This module takes care of preparing an IP asset, either single address, a range with mask for both v4 and v6."""

import ipaddress
import logging
from typing import List

import click

from ostorlab.assets import ipv4
from ostorlab.assets import ipv6
from ostorlab.cli import console as cli_console
from ostorlab.cli.scan.run import run
from ostorlab import exceptions
from ostorlab.runtimes.local.models import models
from ostorlab.runtimes.local import runtime as runtime_local

logger = logging.getLogger(__name__)

console = cli_console.Console()


@run.run.command(name="ip")
@click.argument("ips", required=True, nargs=-1)
@click.pass_context
def ip_cli(ctx: click.core.Context, ips: List[str]) -> None:
    """Run scan for IP asset."""
    runtime = ctx.obj["runtime"]
    try:
        assets = []
        for ip in ips:
            ip_network = ipaddress.ip_network(ip, strict=False)
            if ip_network.version == 4:
                assets.append(
                    ipv4.IPv4(
                        host=ip_network.network_address.exploded,
                        mask=str(ip_network.prefixlen),
                    )
                )
            elif ip_network.version == 6:
                assets.append(
                    ipv6.IPv6(
                        host=ip_network.network_address.exploded,
                        mask=str(ip_network.prefixlen),
                    )
                )
            else:
                console.error(f"Invalid Ip address {ip}")

        logger.debug("scanning assets %s", assets)
        try:
            created_scan = runtime.scan(
                title=ctx.obj["title"],
                agent_group_definition=ctx.obj["agent_group_definition"],
                assets=assets,
            )

            if isinstance(ctx.obj["runtime"], runtime_local.LocalRuntime) is True:
                with models.Database() as session:
                    agent_group_db = models.AgentGroup.create_from_agent_group_def(
                        ctx.obj["agent_group_definition"]
                    )
                    created_scan.agent_group_id = agent_group_db.id
                    session.add(created_scan)
                    session.commit()

                    if assets is not None:
                        models.Asset.create_from_assets_def(
                            scan_id=created_scan.id, assets=assets
                        )

        except exceptions.OstorlabError as e:
            console.error(f"An error was encountered while running the scan: {e}")

    except ValueError as e:
        console.error(f"{e}")
        raise click.Abort()
