import discord
import os
import requests
import urllib.request

from bs4 import BeautifulSoup

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
                input = message.content[3:length]
                if message.content[3] == ' ':
                        input = message.content[4:length]
                
                if input.strip() == "help":
                        await message.channel.send("uhuh")
                elif input.strip() == " hello":
                        await message.channel.send("smh")

                # Congregated both conditions
                else:
                        if not(' ' in input):
                                URL = "https://dragalialost.wiki/w/" + message.content[3:length].lstrip()
                                

                        elif ' ' in input:
                                character = input
                                character = character.replace(' ', '_').lstrip()
                                URL = "https://dragalialost.wiki/w/" + character

                        iconURL = URL+"/Misc"
                        iconlocation = ""

                        # Scraping Skill Names and Details
                        page = requests.get(URL)

                        soup = BeautifulSoup(page.content, "html.parser")
                        results = soup.find(id="mw-content-text")

                        title = soup.find('title').get_text().replace("- Adventurer", '')
                        epithet = soup.find("div", class_="panel-heading").get_text().replace(input, '')


                        elements = results.find_all("div", class_="skill-display-content")

                        skillname = results.find_all("div", class_="skill-display-header")


                        skillList = []

                        skillNames = []

                        for skill in skillname:
                                skills = skill.find("a")
                                if skills.text not in skillNames:
                                        skillNames.append(skills.text)
                                #print(skills.text)

                        print(skillNames)

                        for element in elements:
                                paragraph = element.find("p")
                                skillList.append(paragraph.text)
                                #print(paragraph.text)

                        desc = ""

                        for i in range(len(skillNames)):
                                desc += skillNames[i] + "\n" + skillList[i]

                        # Scraping Icon
                        page = requests.get(iconURL)

                        soup = BeautifulSoup(page.content, "html.parser")
                        for a in soup.find_all('a', href=True):
                                if('r05' in a['href']):
                                        print("Found the URL:", a['href'])
                                        charID = a['href'].replace("/w", '')[:-8]
                                        charID = charID[6:]
                                        print(charID)
                                        iconURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+".png"
                                        break
                        print(iconURL)
                        
                        embed = discord.Embed(title = title, url = URL, description = desc,)
                        embed.set_author(name = epithet, icon_url = iconURL)
                        await message.channel.send(embed=embed)
                                


bot.run(DISCORD_TOKEN)
