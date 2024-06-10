"""Asset of type .IPA (IOS App Store Package).
This module takes care of preparing a file of type .IPA before injecting it to the runtime instance.
"""

import io
import logging
from typing import Tuple, Optional

import click

from ostorlab.assets import ios_ipa as ios_ipa_asset
from ostorlab.cli.scan.run import run
from ostorlab.cli import console as cli_console
from ostorlab import exceptions
from ostorlab.runtimes.local.models import models
from ostorlab.runtimes.local import runtime as runtime_local

console = cli_console.Console()
logger = logging.getLogger(__name__)


@run.run.command()
@click.option("--file", type=click.File(mode="rb"), multiple=True, required=False)
@click.option("--url", multiple=True, required=False)
@click.pass_context
def ios_ipa(
    ctx: click.core.Context,
    file: Optional[Tuple[io.FileIO]] = (),
    url: Optional[Tuple[str]] = (),
) -> None:
    """Run scan for .IPA package file."""
    runtime = ctx.obj["runtime"]
    assets = []

    if url != () and file != ():
        console.error("Command accepts either path or source url of the ipa file.")
        raise click.exceptions.Exit(2)
    if url == () and file == ():
        console.error("Command missing either file path or source url of the ipa file.")
        raise click.exceptions.Exit(2)

    if file != ():
        for f in file:
            assets.append(ios_ipa_asset.IOSIpa(content=f.read(), path=str(f.name)))
    if url != ():
        for u in url:
            assets.append(ios_ipa_asset.IOSIpa(content_url=u))

    logger.debug("scanning assets %s", [str(asset) for asset in assets])
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
