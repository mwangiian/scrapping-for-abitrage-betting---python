import discord
from dotenv import load_dotenv
from discord.ext import commands

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from scrapping import *
import datetime 
import time
from dateutil.relativedelta import relativedelta
import re
import os


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



bot = commands.Bot(command_prefix='!')

@bot.command(name='showOpps',help="shows Available abitrage opportunities")
async def abitrage_opp(ctx,amount:int = 0):
    if(amount != 0 ):
        message =" Hello "+ str(ctx.message.author)+'\n'
        message += "For Amount :"+str(amount)+" Bet as follows : \n"
        mess = entry_prog(amount)
        if(mess == "There aren't abitrage opportunities currently keep trying"):
            message = mess
        else:
            message += mess
        await ctx.send(message[0:2000])
    else:
        await ctx.send("Pass an amount you wish to stake i.e. \n !showOpps 100 or !showOpps 1000")



bot.run(TOKEN)