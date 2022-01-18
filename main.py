import json

input_file = open("input.json")
input = json.load(input_file)

import os
os.system('pip install selenium')


from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

urls = input["input"]

results = []
with webdriver.Chrome(options=options) as driver:
    for url in urls:
        date = None
        driver.get(f"https://web.archive.org/web/changes/{url}")
        a = ActionChains(driver)
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((("xpath", "//*[contains(@fill, 'rgb')]"))))
            driver.execute_script("window.scrollTo(0, '600');")
            day_squares = driver.find_elements(by="xpath", value="//*[contains(@fill, 'rgb')]")
            for day_square in day_squares:
                a.move_to_element(day_square).perform()
                hour_squares = day_square.find_elements('xpath', "//div[@class='popup-of-day-content']//div[@class='popup-of-day-with-heatmap-item']/div")
                for line in hour_squares:
                    rgb_number = line.get_attribute("style").split(')')[0].split()[-1]
                    if int(rgb_number) > 230:
                        date = day_square.find_element('xpath', "//div[@class='popup-of-day-content']//header[@class='day-tooltip-title']").text
                        date = datetime.strptime(date, '%B %d, %Y').strftime('%d.%m.%Y')
                        break
                if date:
                    break
        except:
            pass

        output = {
            "URL": url,
            "Date": date,
            }
        results.append(output)


output_file = open("output.json", 'w')
output_file.write(json.dumps(results))

input_file.close()
output_file.close()
