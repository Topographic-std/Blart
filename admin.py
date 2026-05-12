"""
Owner-only admin commands for managing cogs at runtime.
"""

from discord.ext import commands
import discord
import logging

log = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        # Restrict every command in this cog to the bot owner.
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="reload", help="Reload a cog. Usage: !reload general")
    async def reload(self, ctx: commands.Context, extension: str) -> None:
        ext = f"cogs.{extension}"
        try:
            await self.bot.reload_extension(ext)
            try:
                guild = discord.Object(id=780251364735057990)
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                log.info("Synced %d application command(s).", len(synced))
            except Exception as e:
                log.exception("Slash command sync failed: %s", e)
                await ctx.send(f"Reloaded `{ext}`.")
        except Exception as e:
            await ctx.send(f"Failed to reload `{ext}`: `{e}`")

    @commands.command(name="load", help="Load a cog. Usage: !load general")
    async def load(self, ctx: commands.Context, extension: str) -> None:
        ext = f"cogs.{extension}"
        try:
            await self.bot.load_extension(ext)
            await ctx.send(f"Loaded `{ext}`.")
        except Exception as e:
            await ctx.send(f"Failed to load `{ext}`: `{e}`")

    @commands.command(name="unload", help="Unload a cog. Usage: !unload general")
    async def unload(self, ctx: commands.Context, extension: str) -> None:
        ext = f"cogs.{extension}"
        try:
            await self.bot.unload_extension(ext)
            await ctx.send(f"Unloaded `{ext}`.")
        except Exception as e:
            await ctx.send(f"Failed to unload `{ext}`: `{e}`")

    @commands.command(name="sync", help="Re-sync slash commands.")
    async def sync(self, ctx: commands.Context) -> None:
        synced = await self.bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} application command(s).")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
