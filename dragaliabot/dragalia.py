import discord
import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()

@bot.event
async def on_ready():
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")

		guild_count = guild_count + 1

	print("DragaliaBot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("hey dirtbag")

bot.run(DISCORD_TOKEN)
