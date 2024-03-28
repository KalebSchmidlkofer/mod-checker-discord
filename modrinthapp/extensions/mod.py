from modrinth.py import modrinthProjects
import asyncio
import hikari
import miru
import arc
from ..bot import gateway
plugin = arc.GatewayPlugin('mod', default_permissions=hikari.Permissions.ADMINISTRATOR)



project=modrinthProjects.Data()


@plugin.include
@arc.slash_command('modsuggest', 'Suggest a mod')
async def modsuggest(
  ctx:arc.GatewayContext,
  modid: arc.Option[str, arc.StrParams(description='What Mod to fetch')],
  ) -> None:
  await project.request(modid)
  game_version = await project.get_game_versions()
  loaders = await project.get_loaders()
  client = await project.get_client_side()  
  server = await project.get_server_side()  
  icon=await project.get_icon_url()
  
  if '1.20.1' in game_version and 'forge' in loaders:
    await ctx.respond('valid Mod!', flags=hikari.MessageFlag.EPHEMERAL)
    modDataEmbed=hikari.Embed(title=await project.get_slug(), url=modid, color=0x1eb37c)
    modDataEmbed.set_image(icon)
    modDataEmbed.add_field('Client Side', value=client, inline=True)
    modDataEmbed.add_field('Server Side', value=server, inline=True)
    await gateway.rest.create_message(1221744548213030922, modDataEmbed)
  else:
    await ctx.respond('Invalid Mod! if you think this is wrong, ping naterfute', flags=hikari.MessageFlag.EPHEMERAL)
     


@arc.loader
def load(client: arc.GatewayClient) -> None:
  client.add_plugin(plugin)
  
@arc.unloader
def unload(client: arc.GatewayClient) -> None:
  client.remove_plugin(plugin)
