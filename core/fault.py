import discord
import os
from discord.ext import commands
import sqlite3

class Fault(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=discord.Intents.all()
        )
        self.owner_ids = [1212431696381612132]
        self.remove_command('help')
        self.config = sqlite3.connect('prefix.db')
        self.cursor = self.config.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS config (guild INTEGER PRIMARY KEY, prefix TEXT)")
        self.config.commit()

    async def on_ready(self):
        print(f"{self.user.display_name} is now online!")

    async def setup_hook(self):
        await self.load_extension('jishaku')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'[Loaded] `{filename}`')
                except Exception as e:
                    print(f'Failed to load {filename}: {e}')
        
        await self.tree.sync()

    async def get_prefix(self, message: discord.Message):
        cursor = self.config.cursor()
        cursor.execute("SELECT prefix FROM config WHERE guild = ?", (message.guild.id,))
        guild_row = cursor.fetchone()
        prefix = guild_row[0] if guild_row and guild_row[0] else ";"
        return commands.when_mentioned_or(prefix)(self, message)

fault = Fault()

fault.run('token')
