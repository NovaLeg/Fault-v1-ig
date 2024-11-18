import discord
from discord.ext import commands
import sqlite3
import asyncio
from .interface import VoiceMasterControlPanel

conn = sqlite3.connect('voice.db')
c = conn.cursor()

def setup_database():
    c.execute('''
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTEGER PRIMARY KEY,
        setup BOOLEAN,
        category_id INTEGER,
        join_to_create_id INTEGER,
        text_channel_id INTEGER
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS temp_channels (
        user_id INTEGER PRIMARY KEY,
        channel_id INTEGER
    )
    ''')

    conn.commit()

setup_database()

class VoiceMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}
        self.user_cooldowns = {}
        self.cooldown_time = 10
        self.control_panel = VoiceMasterControlPanel(self)
        self.bot.add_view(self.control_panel)
        self.load_data()

    @commands.hybrid_command(name="setup", with_app_command=True, description="Setup temporary voice channels for your server.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def setup(self, ctx: commands.Context):
        guild_data = self.get_guild_data(ctx.guild.id)

        if guild_data:
            setup_embed = discord.Embed(
                description="<:warn:1285428592460824587> **Temporary Vc** is already enabled in this server. " +
                            "Use the **button** below to reset the setup.",
                color=discord.Color(0x654CB1)
            )

            reset_button = discord.ui.Button(label="Reset Setup", style=discord.ButtonStyle.blurple)

            async def reset_callback(interaction):
                await interaction.message.delete()
                await self.reset_setup(ctx.guild)

            reset_button.callback = reset_callback

            view = discord.ui.View()
            view.add_item(reset_button)

            await ctx.send(embed=setup_embed, view=view)
            return

        guild = ctx.guild

        setup_embed = discord.Embed(
            description="Setting up **Temporary Vc**. Please wait...",
            color=discord.Color(0x654CB1)
        )
        setup_message = await ctx.send(embed=setup_embed)

        setup_embed.description = "Creating **voice category**..."
        await setup_message.edit(embed=setup_embed)
        voice_category = await guild.create_category(name="FAULT CATEGORY")
        setup_embed.description = "**Voice category** created."
        await setup_message.edit(embed=setup_embed)
        await asyncio.sleep(2)

        setup_embed.description = "Creating **join-to-create** voice channel..."
        await setup_message.edit(embed=setup_embed)
        join_to_create = await voice_category.create_voice_channel(name="➕ Creator Channel", user_limit=False)
        setup_embed.description = "**Join-to-create** voice channel created."
        await setup_message.edit(embed=setup_embed)
        await asyncio.sleep(2)

        setup_embed.description = "Creating **control text** channel..."
        await setup_message.edit(embed=setup_embed)
        text_channel = await voice_category.create_text_channel(name="💜・interface")
        setup_embed.description = "**Control text channel** created."
        await setup_message.edit(embed=setup_embed)
        await asyncio.sleep(2)

        setup_embed.description = "<:tick:1285428638765813780> **Temporary Vc** setup complete."
        await setup_message.edit(embed=setup_embed)

        embed = discord.Embed(color=discord.Color(0x654CB1))
        embed.set_image(url="https://media.discordapp.net/attachments/1284893886925242439/1285233188331061268/Extreme_Exorcism.gif?ex=66e9862e&is=66e834ae&hm=833520b78b211f24cf708c35802981da4cc57b332229720140b7361c38c3e10d&")
        await text_channel.send(embed=embed, view=self.control_panel)

        self.insert_guild_data(
            guild.id, True, voice_category.id, join_to_create.id, text_channel.id
        )

    @setup.error
    async def setup_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            no_perm_embed = discord.Embed(
                description="You do not have the required permissions to use this command. You need the `Administrator` permission to run the setup command.",
                color=discord.Color(0x654CB1)
            )
            await ctx.send(embed=no_perm_embed)

    async def reset_setup(self, guild):
        guild_data = self.get_guild_data(guild.id)
        if not guild_data:
            return

        category_id = guild_data[2]
        join_to_create_id = guild_data[3]
        text_channel_id = guild_data[4]

        status_embed = discord.Embed(
            description="Starting the **reset process**. Please wait...",
            color=discord.Color(0x654CB1)
        )
        status_message = await guild.system_channel.send(embed=status_embed)

        category = discord.utils.get(guild.categories, id=category_id)
        if category:
            status_embed.description = "Deleting **channels** in the category..."
            await status_message.edit(embed=status_embed)
            for channel in category.channels:
                try:
                    await channel.delete()
                except discord.HTTPException as e:
                    await status_message.edit(
                        description=f"Failed to delete channel **{channel.name}: {e}**"
                    )
            status_embed.description = "Category **deleted.**"
            await status_message.edit(embed=status_embed)
            await asyncio.sleep(2)
            try:
                await category.delete()
            except discord.HTTPException as e:
                await status_message.edit(
                    description=f"Failed to delete **category: {e}**"
                )

        text_channel = guild.get_channel(text_channel_id)
        if text_channel:
            status_embed.description = "Deleting **control text channel**..."
            await status_message.edit(embed=status_embed)
            try:
                await text_channel.delete()
            except discord.HTTPException as e:
                await status_message.edit(
                    description=f"Failed to delete text **channel: {e}**"
                )

        self.delete_guild_data(guild.id)
        self.temp_channels = {}
        self.delete_temp_channels()

        status_embed.description = "<:tick:1285428638765813780> **Temporary Vc** setup has been reset."
        await status_message.edit(embed=status_embed)

    def load_data(self):
        c.execute('SELECT * FROM temp_channels')
        rows = c.fetchall()
        for row in rows:
            self.temp_channels[row[0]] = row[1]

    def insert_guild_data(self, guild_id, setup, category_id, join_to_create_id, text_channel_id):
        with conn:
            c.execute('''
            INSERT OR REPLACE INTO guilds (guild_id, setup, category_id, join_to_create_id, text_channel_id)
            VALUES (?, ?, ?, ?, ?)
            ''', (guild_id, setup, category_id, join_to_create_id, text_channel_id))

    def get_guild_data(self, guild_id):
        c.execute('SELECT * FROM guilds WHERE guild_id = ?', (guild_id,))
        return c.fetchone()

    def delete_guild_data(self, guild_id):
        with conn:
            c.execute('DELETE FROM guilds WHERE guild_id = ?', (guild_id,))

    def delete_temp_channels(self):
        with conn:
            user_ids = list(self.temp_channels.keys())
            if user_ids:
                placeholders = ', '.join('?' for _ in user_ids)
                c.execute(f'DELETE FROM temp_channels WHERE user_id IN ({placeholders})', user_ids)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild_data = self.get_guild_data(member.guild.id)

        if not guild_data:
            return

        category_id = guild_data[2]
        join_to_create_id = guild_data[3]

        if before.channel is None and after.channel and after.channel.id == join_to_create_id:
            current_time = discord.utils.utcnow().timestamp()

            if member.id in self.user_cooldowns:
                last_join_time = self.user_cooldowns[member.id]
                if current_time - last_join_time < self.cooldown_time:
                    remaining_time = int(self.cooldown_time - (current_time - last_join_time))
                    await member.send(f"You must wait {remaining_time} seconds before creating a new voice channel.")
                    return

            temp_channel = await after.channel.category.create_voice_channel(name=f"{member.display_name}'s Vc")
            await member.move_to(temp_channel)

            self.temp_channels[member.id] = temp_channel.id
            self.user_cooldowns[member.id] = current_time
            
            with conn:
                c.execute('INSERT INTO temp_channels (user_id, channel_id) VALUES (?, ?)', (member.id, temp_channel.id))

        elif after.channel is None and before.channel and before.channel.id in self.temp_channels.values():
            temp_channel = discord.utils.get(member.guild.voice_channels, id=before.channel.id)
            if temp_channel:
                await temp_channel.delete()

            del self.temp_channels[member.id]
            with conn:
                c.execute('DELETE FROM temp_channels WHERE user_id = ?', (member.id,))

async def setup(bot):
    await bot.add_cog(VoiceMaster(bot))
