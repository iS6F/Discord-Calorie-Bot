import discord, asyncio, requests, os
from discord.ext import commands
from bs4 import BeautifulSoup as bs

token = '' #Bot Token (str)
prefix = '' #Bot Prefix (str)
color = 000000 #Embed Color Hex (int)

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    os.system('cls')
    await bot.change_presence(status=discord.Status.idle)
    print(f'Bot Started [{bot.user}]')
    print(f'Latency [{bot.latency}]')
    await asyncio.sleep(2)
    os.system('cls')

@bot.command()
async def calorie(ctx, *, arg):
    print(ctx.author, "[Calorie]")
    siteurl = f'https://www.calorieking.com/us/en/foods/search?keywords={arg}'
    siterequest = requests.get(siteurl)
    sitesoup = bs(siterequest.content, 'lxml')
    siteclass = sitesoup.find('a', class_="MuiButtonBase-root MuiListItem-root MuiListItem-dense MuiListItem-gutters MuiListItem-button")
    try:
        href = str(siteclass['href'])
        foodurl = f'https://www.calorieking.com{href}'
        foodrequest = requests.get(foodurl)
        foodsoup = bs(foodrequest.content, 'lxml')
        calorieclass = foodsoup.find('h2', class_="MuiTypography-root MuiCardHeader-title MuiTypography-h4 MuiTypography-colorInherit MuiTypography-gutterBottom MuiTypography-displayBlock")
        nameclass = foodsoup.find('a', class_="MuiTypography-root MuiLink-root MuiLink-underlineHover jss367 MuiTypography-body2 MuiTypography-colorInherit")
        calorie = calorieclass.text
        name = nameclass.text
        embed = discord.Embed(title=name, description=calorie , color=color)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title='Error!', description='Inccorect Food Name!' , color=color)
        await ctx.send(embed=embed)

bot.run(token)
