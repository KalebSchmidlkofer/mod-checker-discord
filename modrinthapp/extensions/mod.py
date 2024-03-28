from modrinth import modrinthProjects
import asyncio
import hikari
import miru
import arc
import os
from ..bot import gateway
plugin = arc.GatewayPlugin('mod', default_permissions=hikari.Permissions.ADMINISTRATOR)



project=modrinthProjects.Data()

mc_version='1.20.1'
mc_loader='forge'

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
  
  channel = int(os.environ['CHANNEL'])
  
  if mc_version in game_version and mc_loader in loaders:
    await ctx.respond(f'valid Mod!', flags=hikari.MessageFlag.EPHEMERAL)
    modDataEmbed=hikari.Embed(title=await project.get_slug(), url=modid, color=0x1eb37c)
    modDataEmbed.set_image(icon)
    modDataEmbed.add_field('Client Side', value=client, inline=True)
    modDataEmbed.add_field('Server Side', value=server, inline=True)
    modDataEmbed.set_footer(f'Requested by, {ctx.user.global_name}', icon=ctx.user.avatar_url)
    await gateway.rest.create_message(channel, modDataEmbed)
  else:
    if not mc_version in game_version:
      await ctx.respond(f"Doesn't have a {mc_version} version!", flags=hikari.MessageFlag.EPHEMERAL)
    if not mc_loader in loaders:
      await ctx.respond(f'Not built for {mc_loader}', flags=hikari.MessageFlag.EPHEMERAL)
      
      


@arc.loader
def load(client: arc.GatewayClient) -> None:
  client.add_plugin(plugin)
  
@arc.unloader
def unload(client: arc.GatewayClient) -> None:
  client.remove_plugin(plugin)
