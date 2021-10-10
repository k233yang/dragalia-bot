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
                charName = message.content[3:length]
                if message.content[3] == ' ':
                        charName = message.content[4:length]
                
                if charName.strip() == "help":
                        await message.channel.send("uhuh")
                elif charName.strip() == " hello":
                        await message.channel.send("smh")

                # Congregated both conditions
                else:
                        if not(' ' in charName):
                                URL = "https://dragalialost.wiki/w/" + message.content[3:length].lstrip()
                                

                        elif ' ' in charName:
                                character = charName
                                character = character.replace(' ', '_').lstrip()
                                URL = "https://dragalialost.wiki/w/" + character

                        # Scraping Skill Names and Details
                        page = requests.get(URL)

                        soup = BeautifulSoup(page.content, "html.parser")
                        results = soup.find(id="mw-content-text")

                        # Previous Way


                        #elements = results.find_all("div", class_="skill-display-content")

                        #skillname = results.find_all("div", class_="skill-display-header")

                        #skillList = []

                        #skillNames = []

                        #skillCost = []

                        # Get Skill Names
                        #for skill in skillname:
                                #skills = skill.find("a")
                                #f skills.text not in skillNames:
                                        #skillNames.append(skills.text)
                                #print(skills.text)

                        #print(elements)

                        # Get Skill Descs
                        #for element in elements:
                                #paragraph = element.find("p")
                                #killList.append(paragraph.text)
                                #print(paragraph.text)

                        #desc = ""

                        #for i in range(len(skillNames)):
                                #desc += "__**" + skillNames[i] + "**__" + "\n" + skillList[i]

                        HP = results.find(id='adv-hp').text
                        #print(HP.text)

                        Str = results.find(id='adv-str').text
                        #print(Str.text)

                        Element = ""

                        Weapon = "Dragon"
                        
                        spans = soup.find_all('img', alt=True)
                        for line in spans:
                                if "Element" in line['alt']:
                                        Element = line['alt'].split(" ")[2][:-4]
                                if "Weapon" in line['alt']:
                                        Weapon = line['alt'].split(" ")[2][:-4]

                        Color = {
                        "Flame" : 15158332,
                        "Water" : 1752220,
                        "Wind" : 3066993,
                        "Shadow" : 800080,
                        "Light" : 16776960
                        }

                        # VERY MESSY

                        #To Parse
                        skillTable = []

                        #Contains Skill Description
                        skillDesc = []

                        #Contains Skill SP Cost
                        skillDetails = []
                        temp = []

                        test = results.find_all("div", class_="skill-table")
                        for res in test:
                                skillTable.append(res.text.split('\n\n'))


                        #Skill Desciption & Details
                        for i in range(len(skillTable)):
                                temp.append(skillTable[i][-4])

                                #Removes preceding skill details
                                desc = skillTable[i][-3].split('\n')
                                skillDesc.append(desc[-1])
                        

                        #Cleaning
                        for i in temp:
                                skillDetails.append(i.split('\n'))


                        #Formatting Skill Desc
                        for i in range(len(skillDesc)):
                                skillDesc[i] = skillDesc[i].replace(".If", ".\n\nIf")
                                skillDesc[i] = skillDesc[i].replace(". If", ".\n\nIf")
                                skillDesc[i] = skillDesc[i].replace(".  If", ".\n\nIf")

                                skillDesc[i] = skillDesc[i].replace(". This", ".\n\nThis")
                                skillDesc[i] = skillDesc[i].replace(".This", ".\n\nThis")

                                skillDesc[i] = skillDesc[i].replace(".When", ".\n\nWhen")
                                skillDesc[i] = skillDesc[i].replace(". When", ".\n\nWhen")

                                skillDesc[i] = skillDesc[i].replace(". Also", ".\n\nAlso")
                                
                                skillDesc[i] = skillDesc[i].replace("・", "\n\n・")
                                
                                skillDesc[i] = skillDesc[i].replace(".Lv", ".\n\nLv")
                                skillDesc[i] = skillDesc[i].replace(".In", ".\n\nIn")
                                
                                skillDesc[i] = skillDesc[i].replace("%The", "%\n\nThe")
                                skillDesc[i] = skillDesc[i].replace(". The", ".\n\nThe")

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
                        embed = discord.Embed(title = title, url = URL, description = "**HP: **" + HP + "  " + "**Str: **" + Str + "\n" + "**Element: **" + Element + "  " + "**Weapon: **" + Weapon, color = Color[Element])
                        embed.set_author(name = epithet)
                        if requests.get((iconURL)).status_code == 200:
                                embed.set_thumbnail(url=iconURL)
                        else:
                                embed.set_thumbnail(url=altURL)

                        await message.channel.send(embed=embed)

                        # SKills
                        embed = discord.Embed(title = "Skills", color = Color[Element])
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
