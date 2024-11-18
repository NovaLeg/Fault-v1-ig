from discord import Embed, Interaction, ButtonStyle
from discord.ext import commands
import discord
import asyncio
import time

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.hybrid_command(aliases=['latency'], usage="shows the bot's latency", help="Bot latency")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        embed = Embed(color=0x654CB1)
        embed.description = f"My latency: **{round(self.bot.latency * 1000)}ms**"
        embed.set_author(name="Fault", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text="Fault", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(usage="shows this help menu", help="Help menu")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def help(self, ctx: Interaction):
        embed = Embed(title="Fault - Help", color=0x654CB1)
        embed.description = "👋 Hey, I'm Fault and I'm here to help you! Let me explain how I work <3\n\nSelect a category from the drop down below to learn more about my commands and features!"
        embed.set_footer(text="Fault", icon_url=self.bot.user.avatar.url)

        options = [
            discord.SelectOption(label="VoiceMaster", description="Learn more about voicemaster on fault", emoji="➕", value="voicemaster"),
            discord.SelectOption(label="Welcome & Leave Messages", description="Learn more about welcome/leave messages", emoji="👋", value="welcome"),
            discord.SelectOption(label="Moderation", description="Learn about fault's moderation features", emoji="🛠️", value="moderation"),
            discord.SelectOption(label="Truth or Dare", description="Learn about truth & dare", emoji="🎲", value="truth_or_dare"),
            discord.SelectOption(label="Anime Images", description="Learn related to anime images", emoji="🖼️", value="images"),
            discord.SelectOption(label="Economy", description="Learn and play economy on fault", emoji="💵", value="economy"),
            discord.SelectOption(label="Minigames", description="Learn about minigames", emoji="🎮", value="minigame"),
            discord.SelectOption(label="Info", description="Get extra information", emoji="ℹ️", value="info"),
        ]

        select = discord.ui.Select(placeholder="I want to learn about...", options=options)

        async def callback(interaction: Interaction):
            if select.values[0] == "voicemaster":
                embed = Embed(title="➕ Voicemaster Commands", color=0x654CB1)
                embed.description = "`;setup` - Create temporary voice channel."
            elif select.values[0] == "welcome":
                embed = Embed(title="👋 Welcome & Leave Messages Commands", color=0x654CB1)
                embed.description = "`;setwlc`, `;setlv`, `;resetwlc`, `;resetlv`, `;setwlcmsg`, `;setlvmsg`, `;settingsview` - Set up welcome messages & leave messages."
            elif select.values[0] == "moderation":
                embed = Embed(title="🛠️ Moderation Commands", color=0x654CB1)
                embed.description = "`;mute`, `;unmute`, `;ban`, `;unban`, `;role`, `warn` - Moderation commands."
            elif select.values[0] == "truth_or_dare":
                embed = Embed(title="🎲 Truth or Dare Commands", color=0x654CB1)
                embed.description = "`;truth`, `;dare`, `;random` - Play the Truth or Dare game."
            elif select.values[0] == "images":
                embed = Embed(title="🖼️ Anime images Commands", color=0x654CB1)
                embed.description = "`;kiss`, `;hug`, `;slap`, `;handholding`, `;kick`, `;cuddle`, `;lick`, `;highfive`, `;bite` - Image-related commands."
            elif select.values[0] == "economy":
                embed = Embed(title="💵 Economy Commands", color=0x654CB1)
                embed.description = "`;shop`, `;buy`, `;marry`, `;divorce`, `;marriage`, `;work`, `;balance`, `;deposit`, `;withdraw`, `;pay`, `;leaderboard` - Manage your economy in the server."
            elif select.values[0] == "minigame":
                embed = Embed(title="🎮 Minigame Commands", color=0x654CB1)
                embed.description = "`;coinflip`, `;doubledice`, `;minesweeper` - Play fun minigames."
            elif select.values[0] == "info":
                embed = Embed(title="ℹ️ Info Commands", color=0x654CB1)
                embed.description = "`;help`, `;ping`, `;setprefix`, `stats` - Get information about the bot."

            await interaction.response.send_message(embed=embed, ephemeral=True)

        select.callback = callback

        view = discord.ui.View()
        view.add_item(select)

        support_button = discord.ui.Button(label="Support Server", style=ButtonStyle.link, url="https://discord.gg/aHxv8TpuCY", emoji="❓")
        add_bot_button = discord.ui.Button(label="Add To Server", style=ButtonStyle.link, url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8", emoji="➕")

        view.add_item(support_button)
        view.add_item(add_bot_button)

        message = await ctx.send(embed=embed, view=view)

        await asyncio.sleep(300)

        for item in view.children:
            item.disabled = True

        await message.edit(view=view)

    @commands.hybrid_command(aliases=['botinfo', 'st', 'bi'], usage="shows bot statistics", help="Bot statistics")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):
        uptime = time.time() - self.start_time
        embed = Embed(title="**__Bot Info__**", color=0x654CB1)
        embed.add_field(name="Total Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Total Users", value=sum(guild.member_count for guild in self.bot.guilds), inline=True)
        embed.add_field(name="Total Channels", value=sum(len(guild.channels) for guild in self.bot.guilds), inline=True)
        embed.add_field(name="Bot Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Uptime", value=f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m {int(uptime % 60)}s", inline=True)
        embed.add_field(name="Developer", value="**[Nitrix](https://discord.com/users/1269276489820672042)\n[Miox](https://discord.com/users/1178572441367363615)**", inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
