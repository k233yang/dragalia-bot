import discord
import os
import requests
import urllib.request

import stats
import unit
import data
import skills

from bs4 import BeautifulSoup
from discord.ext import commands

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
        length = len(message.content)
        #if message.content == "hello":
        #        await message.channel.send("hey dirtbag")
        if message.content[0:3] == "dl!":
                charName = message.content[3:length]
                if message.content[3] == ' ':
                        charName = message.content[4:length]
                
                if charName.strip() == "help":
                        await message.channel.send("uhuh")
                elif charName.strip() == "hello":
                        
                        await message.channel.send("<:farren:896826606662877194>")

                # Congregated both conditions
                else:
                        if not(' ' in charName):
                                URL = data.characterUrl+ message.content[3:length].lstrip()
                                

                        elif ' ' in charName:
                                character = charName
                                character = character.replace(' ', '_').lstrip()
                                URL = data.characterUrl + character

                        # Scraping Skill Names and Details
                        page = requests.get(URL)

                        soup = BeautifulSoup(page.content, "html.parser")
                        results = soup.find(id="mw-content-text")
                        spans = soup.find_all('img', alt=True)

                        Element = ""
                        Weapon = "Dragon"
                        
                        thisChar = unit.Unit(results, spans)
                        charStats = thisChar.charStats

                        HP = charStats.hp
                        Str = charStats.str
                        Element = charStats.element
                        Weapon = charStats.weapon         

                        s = skills.Skills(results)
                        skillDesc = []
                        skillDetails = []
                        skillDesc = s.skillDescription
                        skillDetails = s.skillDet

                        # Scraping Icon
                        altURL = ""
                        for a in soup.find_all('a', href=True):
                                # ADVENTURER ID
                                if('r05' in a['href'] or 'r04'in a['href'] or 'r03' in a['href']):
                                        #print("Found the URL:", a['href'])
                                        title = soup.find('title').get_text().replace("- Adventurer", '')
                                        charID = a['href'].replace("/w", '')[:-17]
                                        charID = charID[6:]
                                        #print("CharID: " + charID)
                                        iconURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+".png"
                                        break
                                # DRAGON ID
                                elif('_01' in a['href']):
                                        #print("Found the URL:", a['href'])
                                        title = soup.find('title').get_text().replace("- Dragon", '')
                                        charID = a['href'].replace("/w", '')[:-13]
                                        charID = charID[6:]
                                        #print("CharID: " + charID)
                                        iconURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+".png"
                                        # Sometimes URL above breaks, for contingency
                                        altURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+"_parts_c000.png"
                                        break
                        epithet = soup.find("div", class_="panel-heading").get_text().replace(charName, '')

                        # GENERATING THE EMBEDDED FILE
                        # Character Details

                        embed = discord.Embed(title = title, url = URL, description = "**HP: **" + HP + "  " + "**Str: **" + Str + "\n" + "**Element: **" + Element + "  " + "**Weapon: **" + Weapon, color = data.Color[Element])
                        embed.set_author(name = epithet)
                        if requests.get((iconURL)).status_code == 200:
                                embed.set_thumbnail(url=iconURL)
                        else:
                                embed.set_thumbnail(url=altURL)

                        await message.channel.send(embed=embed)

                        # Skills
                        embed = discord.Embed(title = "Skills", color = data.Color[Element])
                        for i in range(len(skillDesc)):
                                #Checks if skill is Shareable
                                sharedIndex = skillDetails[i][2].find('Shared')
                                #Adds a line break between SP Cost and Shared SP Cost
                                if sharedIndex != -1:
                                        formatted_line = skillDetails[i][2][:sharedIndex] + "\n" + skillDetails[i][2][sharedIndex:]
                                #Skill listed isn't shareable
                                else:
                                        formatted_line = skillDetails[i][2]
                                embed.add_field(name = "__**" + skillDetails[i][1] + "**__", value = skillDesc[i][:-12] + "\n" + "**" + formatted_line + "**", inline = True)
                        await message.channel.send(embed=embed)


bot.run(DISCORD_TOKEN)
