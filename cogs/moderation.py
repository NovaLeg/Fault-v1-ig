import discord
from discord.ext import commands
import re
import datetime

time_regex = re.compile(r'(\d+)([smhd])')


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}

    async def send_embed_dm(self, member, title, description):
        embed = discord.Embed(title=title, description=description, color=0x654CB1)
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.hybrid_command(name="role", with_app_command=True, description="Add/Remove a role from a user")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        bot_owner_id = self.bot.owner_id

        if ctx.author.id == bot_owner_id:
            pass
        elif not ctx.author.guild_permissions.manage_roles:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        if ctx.guild.me.top_role.position > role.position:
            if role in member.roles:
                await member.remove_roles(role)
                await self.send_embed_dm(member, "Role Removed", f"You have had the role **{role.name}** removed in **{ctx.guild.name}**.")
            else:
                await member.add_roles(role)
                await self.send_embed_dm(member, "Role Added", f"You have been given the role **{role.name}** in **{ctx.guild.name}**.")
            await ctx.message.add_reaction('<:tick:1285428638765813780>')
        else:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')

    @commands.hybrid_command(name="ban", with_app_command=True, description="Ban a member")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: discord.User, *, reason=None):
        bot_owner_id = self.bot.owner_id

        if ctx.author.id == bot_owner_id:
            pass
        elif not ctx.author.guild_permissions.ban_members:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        try:
            await self.send_embed_dm(member, "You Have Been Banned", f"You have been banned from **{ctx.guild.name}** for: {reason}")
        except discord.Forbidden:
            pass

        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.message.add_reaction('<:tick:1285428638765813780>')
        except discord.Forbidden:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')

    @commands.hybrid_command(name="unban", with_app_command=True, description="Unban a member")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban(self, ctx, *, member):
        bot_owner_id = self.bot.owner_id

        if ctx.author.id == bot_owner_id:
            pass
        elif not ctx.author.guild_permissions.ban_members:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        banned_users = await ctx.guild.bans()

        if member.isdigit():
            member_id = int(member)
            for ban_entry in banned_users:
                if ban_entry.user.id == member_id:
                    await ctx.guild.unban(ban_entry.user)
                    await ctx.message.add_reaction('<:tick:1285428638765813780>')
                    return
        elif len(member.split('#')) == 2:
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                if (ban_entry.user.name, ban_entry.user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(ban_entry.user)
                    await ctx.message.add_reaction('<:tick:1285428638765813780>')
                    return

        await ctx.message.add_reaction('<:warn:1285428592460824587>')

    @commands.hybrid_command(name="mute", with_app_command=True, description="Timeout a user for a specific time")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timeout(self, ctx, member: discord.Member, duration: str, reason: str = None):
        bot_owner_id = self.bot.owner_id

        if ctx.author.id == bot_owner_id:
            pass
        elif not ctx.author.guild_permissions.moderate_members:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        total_seconds = 0
        matches = time_regex.findall(duration)

        for amount, unit in matches:
            amount = int(amount)
            if unit == 's':
                total_seconds += amount
            elif unit == 'm':
                total_seconds += amount * 60
            elif unit == 'h':
                total_seconds += amount * 3600
            elif unit == 'd':
                total_seconds += amount * 86400

        if total_seconds <= 0:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        timeout_duration = datetime.timedelta(seconds=total_seconds)

        try:
            await member.timeout(timeout_duration, reason=reason)
            await ctx.message.add_reaction('<:tick:1285428638765813780>')
        except discord.Forbidden:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')

    @commands.hybrid_command(name="unmute", with_app_command=True, description="Unmute a member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def untimeout(self, ctx, member: discord.Member):
        bot_owner_id = self.bot.owner_id

        if ctx.author.id == bot_owner_id:
            pass
        elif not ctx.author.guild_permissions.moderate_members:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        if member.timed_out_until:
            try:
                await member.edit(timed_out_until=None)
                await ctx.message.add_reaction('<:tick:1285428638765813780>')
            except Exception:
                await ctx.message.add_reaction('<:warn:1285428592460824587>')
        else:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')

    @commands.hybrid_command(name="warn", with_app_command=True, description="Warn a member")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        bot_owner_id = self.bot.owner_id

        if ctx.author.id == bot_owner_id:
            pass
        elif not ctx.author.guild_permissions.manage_messages:
            await ctx.message.add_reaction('<:warn:1285428592460824587>')
            return

        if member.id not in self.warns:
            self.warns[member.id] = []

        self.warns[member.id].append(reason)

        await self.send_embed_dm(member, "You Have Been Warned", f"You have been warned in **{ctx.guild.name}** for: {reason}")
        await ctx.message.add_reaction('<:tick:1285428638765813780>')

async def setup(bot):
    await bot.add_cog(Moderation(bot))
