import discord
import os
import requests
import urllib.request

import data
import stats
import unit
import skills

from bs4 import BeautifulSoup
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()

advList = []
dragonList = []

@bot.event
async def on_ready():
        guild_count = 0
        text_channel_list = []

        # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
        for guild in bot.guilds:
                print(f"- {guild.id} (name: {guild.name})")
                guild_count = guild_count + 1

        print("DragaliaBot is in " + str(guild_count) + " guilds.")

        # PRELIMINARY
        advlistURL = "https://dragalialost.wiki/w/Adventurer_List"
        dragonlistURL = "https://dragalialost.wiki/w/Dragon_List"

        # UPDATES LIST OF ADVENTURERS
        newAdv = []
        
        # GRABS LIST OF EXISTING ADVENTURERS
        advFile = open('advList.txt', 'r')
        Lines = advFile.readlines()

        for line in Lines:
            advList.append(line.strip())
        print(advList)

        page = requests.get(advlistURL)
        soup = BeautifulSoup(page.content, "html.parser")
        advTable = soup.find('table',{'class':'wikitable sortable'})
        
        # CHECKS FOR NEW ADVENTURERS
        rows = advTable.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if (len(cols) > 0):
                if cols[1] not in advList:
                    advList.append(cols[1])
                    newAdv.append(cols[1])
                    print("New Adventurer: " + cols[1])
        if (len(newAdv) > 0):
            with open("advList.txt", "a") as advOutput: 
                for i in newAdv:
                    if i is not None:
                        advOutput.write(str(i) + "\n")
                advOutput.close()

        # UPDATES LIST OF DRAGONS
        newDragon = []
        
        # GRABS LIST OF EXISTING DRAGONS
        dragonFile = open('dragonList.txt', 'r')
        Lines = dragonFile.readlines()

        for line in Lines:
            dragonList.append(line.strip())
        print(dragonList)

        page = requests.get(dragonlistURL)
        soup = BeautifulSoup(page.content, "html.parser")
        dragonTable = soup.find('table',{'class':'wikitable sortable'})
        
        # CHECKS FOR NEW DRAGONS
        rows = dragonTable.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if (len(cols) > 0):
                if cols[1] not in dragonList:
                    newDragon.append(cols[1])
                    dragonList.append(cols[1])
                    print("New Dragon: " + cols[1])

        # ADDS NEW DRAGONS(IF ANY)
        if(len(newDragon) > 0):
            with open("dragonList.txt", "a") as dragonOutput: 
                for i in newDragon  :
                    if i is not None:
                        dragonOutput.write(str(i).replace(u"\u02bb", '') + "\n")
                dragonOutput.close()

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
                    links = soup.find_all('a', href=True)

                    element = ""
                    weapon = "Dragon"
                    
                    thisChar = unit.Unit(results, spans, links, soup)
                    charStats = thisChar.charStats
                    charSkills = thisChar.charSkills
                    charAbilities = thisChar.charAbilities

                    HP = charStats.hp
                    Str = charStats.str
                    element = charStats.element
                    weapon = charStats.weapon     
                    skillDesc = charSkills.skillDescription
                    skillDetails = charSkills.skillDet 

                    iconURL = thisChar.charStats.iconURL
                    altURL = thisChar.charStats.altURL 
                    title = thisChar.charStats.title

                    abilities = charAbilities.abilityDescription
                    abilityNames = charAbilities.abilityName

                    epithet = soup.find("div", class_="panel-heading").get_text().replace(charName, '')

                    # GENERATING THE EMBEDDED FILE
                    # Character Details

                    if weapon is not None:
                        embed = discord.Embed(title = title, url = URL, description = "**HP: **" + HP + "  " + "**Str: **" + Str + "\n" + "**Element: **" + element + "  " + "**Weapon: **" + weapon, color = data.Color[element])
                    else:
                        embed = discord.Embed(title = title, url = URL, description = "**HP: **" + HP + "  " + "**Str: **" + Str + "\n" + "**Element: **" + element,color = data.Color[element])
                    embed.set_author(name = epithet)
                    if requests.get((iconURL)).status_code == 200:
                            embed.set_thumbnail(url=iconURL)
                    else:
                            embed.set_thumbnail(url=altURL)

                    await message.channel.send(embed=embed)

                    # Skills
                    embed = discord.Embed(title = "Skills", color = data.Color[element])
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

                    #Co-abilities
                    abilityCounter = 0
                    embed = discord.Embed(title = "Co-abilities" if charName in advList else "Abilities", color = data.Color[element])
                    for i in range (len(abilities)):
                        if (i+1)%5 == 0 and i <= 9:
                            embed.add_field(name = "__**" + abilityNames[abilityCounter] + "**__", value = abilities[i])
                            abilityCounter += 1
                    await message.channel.send(embed=embed)

                    #Abilities
                    if charName in advList:
                        embed = discord.Embed(title = "Abilities", color = data.Color[element])
                        for i in range (len(abilities)):
                            if i> 9 and (i+1)%2 == 0:
                                embed.add_field(name = "__**" + abilityNames[abilityCounter] + "**__", value = abilities[i])
                                abilityCounter += 1
                        await message.channel.send(embed=embed)


bot.run(DISCORD_TOKEN)