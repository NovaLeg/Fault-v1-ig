import discord
from discord.ext import commands
import aiohttp
import random

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_gif(self, search_term):
        api_key = 'kyQCz27OyTf0FYOiGFYonHNPbGgW7NmG'
        url = f"https://api.giphy.com/v1/gifs/search?q={search_term}&api_key={api_key}&limit=20"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return random.choice(data['data'])['images']['original']['url']
                return None

    @commands.hybrid_command(name="kiss", usage="kiss <user>", help="Kiss a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime kiss")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} kisses {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a kiss GIF right now.")

    @commands.hybrid_command(name="hug", usage="hug <user>", help="Hug a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime hug")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} hugs {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a hug GIF right now.")

    @commands.hybrid_command(name="slap", usage="slap <user>", help="Slap a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime slap")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} slaps {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a slap GIF right now.")

    @commands.hybrid_command(name="handholding", usage="handholding <user>", help="Hold hands with a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def handholding(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime handholding")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} holds hands with {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a handholding GIF right now.")

    @commands.hybrid_command(name="kick", usage="kick <user>", help="Kick a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime kick")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} kicks {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a kick GIF right now.")

    @commands.hybrid_command(name="cuddle", usage="cuddle <user>", help="Cuddle a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime cuddle")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} cuddles {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a cuddle GIF right now.")

    @commands.hybrid_command(name="lick", usage="lick <user>", help="Lick a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime lick")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} licks {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a lick GIF right now.")

    @commands.hybrid_command(name="highfive", usage="highfive <user>", help="Give a high five to a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime high five")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} high fives {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a high five GIF right now.")

    @commands.hybrid_command(name="bite", usage="bite <user>", help="Bite a user")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bite(self, ctx, user: discord.Member):
        gif_url = await self.fetch_gif("anime bite")
        if gif_url:
            embed = discord.Embed(description=f"{ctx.author.mention} bites {user.mention} <:heart:1285527071912886366>", color=0x654CB1)
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a bite GIF right now.")

async def setup(bot):
    await bot.add_cog(Anime(bot))
