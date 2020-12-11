import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from statistics import mean

##
# TODO: Look at only specified number of games.
# TODO: Implement testing
##

def driver_init(username):
    # Initializing the website driver
    options = webdriver.ChromeOptions()
    options.set_headless()    # Headless(browser-less) website instance
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # Accessing the website
    URL = "https://na.op.gg/summoner/userName={q}"
    print("Entering Website...")
    driver.implicitly_wait(1)
    driver.get(URL.format(q=username))

    return driver


# Inputs: driver - Chrome webdriver intialized in driver_init
# Outputs: Average score of the recent games.
def get_score(driver):

    # Locating the "FlexRanked" button that is connected to javascript
    print("Locating elements...")
    flexBtn = driver.find_elements_by_id('right_gametype_flexranked')
    flexBtn[0].find_elements_by_class_name('Link')[0].click()

    # Locating the "Match Detail" button that is connected to javascript
    buttons = driver.find_elements_by_class_name('MatchDetail')
    print("Number of matches: " + str(len(buttons)))

    # Click on the match detail buttons to expand and reveal the op scores
    for el in buttons:
        el.click()
        time.sleep(0.45)  # Selenium is kinda slow, so explicit wait

    # Trying to find user block
    print("Locating more elements...")
    detailedEl = driver.find_elements_by_class_name('isRequester')
    print("Number of requesters: " + str(len(detailedEl)))

    # Extracting User op scores
    opList = []
    for el in detailedEl:
        tempEl = el.find_elements_by_class_name('OPScore.Text')
        if tempEl:
            opList.append(float(tempEl[0].text))

    return len(buttons), len(detailedEl), opList

# OPScore class for discord bot
class OPScore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def op(self, ctx):
        username = ctx.message.content[3:]
        driver = driver_init(username)
        _, _, scoreList = get_score(driver)
        driver.quit()
        await ctx.send(f'{username}\'s average OP score from '
            f'last {str(len(scoreList))} games is {mean(scoreList):.2f}.')


def setup(bot):
    bot.add_cog(OPScore(bot))
