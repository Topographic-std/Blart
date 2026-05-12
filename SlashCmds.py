import discord
from discord import app_commands
from discord.ext import commands


class SlashCmds(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="vietnam", description="They're in the trees!")
    async def vietnam(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"*Fortunate Son Intensifies* {interaction.user.mention}!"
        )
        
    @app_commands.command(name="contact", description="Contact the bot owner.")
    async def contact(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"Contacting the bot owner... {interaction.user.mention}"
        )
        owner = await self.bot.fetch_user(self.bot.owner_id)
        if owner:
            try:
                await owner.send(
                    f"{interaction.user} used the contact command in {interaction.guild} ({interaction.channel})."
                )
            except Exception as e:
                await interaction.followup.send(
                    f"Failed to contact the owner: {e}", ephemeral=True
                )
        else:
            None


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SlashCmds(bot))
