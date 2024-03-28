from modrinth.py import modrinthProjects
import asyncio
import hikari
import miru
import arc

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
  await ctx.respond(f"""{game_version}, {loaders}""")
  if '1.20.1' in game_version and 'forge' in loaders:
    await ctx.respond('valid Mod!')
     


@arc.loader
def load(client: arc.GatewayClient) -> None:
  client.add_plugin(plugin)
  
@arc.unloader
def unload(client: arc.GatewayClient) -> None:
  client.remove_plugin(plugin)