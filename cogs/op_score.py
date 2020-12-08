import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def get_score(username):
    print("Starting...")

    time.perf_counter()
    # Initializing the website
    URL = "https://na.op.gg/summoner/userName={q}"


    # Headless(browser-less) website instance
    options = webdriver.ChromeOptions()
    # options.set_headless()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    print("Entering Website...")
    driver.implicitly_wait(10)
    driver.get(URL.format(q=username))

    element = driver.find_element_by_css_selector("html")
    element.send_keys(Keys.CONTROL, Keys.SUBTRACT)

    print("Locating elements...")
    buttons = driver.find_elements_by_class_name('MatchDetail')
    print("Number of matches: " + str(len(buttons)))

    for el in buttons:
        el.click()
        time.sleep(.5)

    print("Locating more elements...")
    detailedEl = driver.find_elements_by_class_name('isRequester')
    print("Number of requesters: " + str(len(detailedEl)))

    for el in detailedEl:
        try:
            opEl = el.find_elements_by_css_selector('div.OPScore.Text')
            if opEl:
                print(opEl[0].text)
            else:
                continue
        except: continue

    # detailedEl = driver.find_elements_by_xpath(".//tr[@class='Row']")
    # print(len(detailedEl))
    # for el in detailedEl:
    #     print(el)

    driver.quit()
    print(time.perf_counter())

    return None

if __name__ == "__main__":
    get_score("GoodMentalGamer")
