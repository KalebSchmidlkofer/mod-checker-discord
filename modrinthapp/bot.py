import hikari
import arc
from arc.errors import NotOwnerError
import miru
from os import path, environ, getcwd, name

activity_types = {
    'Watching': hikari.ActivityType.WATCHING,
    'Listening': hikari.ActivityType.LISTENING,
    'Streaming': hikari.ActivityType.STREAMING,
    'Playing': hikari.ActivityType.PLAYING
}

StatusTypes = {
  'Online': hikari.Status.ONLINE,
  'Offline': hikari.Status.OFFLINE,
  'Do Not Disturb': hikari.Status.DO_NOT_DISTURB,
  'Idle': hikari.Status.IDLE,
}

gateway = hikari.GatewayBot(environ['BOT_TOKEN'], intents=hikari.Intents.ALL, banner=None)
client = arc.GatewayClient(gateway)

PluginPath=path.join('modrinthapp', 'extensions')
client.load_extensions_from(PluginPath)
miru.Client(gateway)

@client.listen()
async def set_presence(event: arc.StartedEvent):
  await gateway.update_presence(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(name=f'Mee6 Screw Up', type=hikari.ActivityType.WATCHING)
    )
  
@client.include
@arc.with_hook(arc.owner_only)
@arc.slash_command('presence', 'Changes Discord bots presence')
async def change_presence(
  ctx: arc.GatewayContext,
  message: arc.Option[str, arc.StrParams('The message to display')],
  activity: arc.Option[int, arc.IntParams (choices=activity_types, description='What activity eg. watching, playing')], # type: ignore
  status: arc.Option[str, arc.StrParams(choices=StatusTypes, description='What Status eg. Online, idle, do not disturb')]
  ) -> None:  
  
  await gateway.update_presence(
    status=status, #type: ignore
    activity=hikari.Activity(name=message, type=activity)
  )
  await ctx.respond('Done Changing', flags=hikari.MessageFlag.EPHEMERAL)

@change_presence.set_error_handler
async def error_handler(ctx: arc.GatewayContext, exc: Exception) -> None:
  if isinstance(exc, NotOwnerError):
    await ctx.respond('Only the bot Owner can run this command!', flags=hikari.MessageFlag.EPHEMERAL)
  
def run() -> None:
  if not name == 'nt':
    import uvloop
    uvloop.install
