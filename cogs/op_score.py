import requests
import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from statistics import mean

##
# TODO: Look at only specified number of games.
# TODO: Implement testing
# TODO: Multiple requests lags the command, outputting the results all at the end.
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

    try:
        flexBtn[0].find_elements_by_class_name('Link')[0].click()
    except ElementClickInterceptedException:
        raise ElementClickInterceptedException
    except:
        raise Exception("Something went wrong")

    # Locating the "Match Detail" button that is connected to javascript
    buttons = driver.find_elements_by_class_name('MatchDetail')
    print("Number of matches: " + str(len(buttons)))

    # Click on the match detail buttons to expand and reveal the op scores
    for el in buttons:
        try:
            el.click()
        except ElementClickInterceptedException:
            raise ElementClickInterceptedException
        except:
            raise Exception("Something went wrong")
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
        username = ctx.message.content[3:] # Users with spaces

        # Empty usernames
        if not username:
            await ctx.send("Please provide a summoner name."
                           "Example: !op <name>")
            return

        driver = driver_init(username)
        try:
            _, _, scoreList = get_score(driver)
        except ElementClickInterceptedException:
            await ctx.send("There was an overlay ad problem. Please try again.")
        except Exception:
            await ctx.send("Something went wrong. Please try again.")
        else:
            if not scoreList:
                await ctx.send("Not enough flex games. Better queue up!")
            else:
                await ctx.send(f'{username}\'s average OP score from '
                f'last {str(len(scoreList))} games is {mean(scoreList):.2f}.')
        finally:
            driver.quit()


def setup(bot):
    bot.add_cog(OPScore(bot))
