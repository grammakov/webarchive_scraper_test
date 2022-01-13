import json

input_file = open("input.json")
input = json.load(input_file)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

urls = input[0]["Got input"]["input"]

results = []
with webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub", options=options) as driver:
    for url in urls:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@fill, string('139'))]"))).click()
        #date = driver.find_element(By.CLASS_NAME, "popup-of-day").find_element(By.CLASS_NAME, "day-tooltip-title").text
        link = driver.find_element(By.CLASS_NAME, "popup-of-day").find_element(By.TAG_NAME, "a").get_attribute('href')
        r = link.split('/')[-2]
        year = r[2:4]
        month = r[4:6]
        day = r[6:8]
        date = f"{day}.{month}.{year}"

        output = {
          "URL": url.split('/')[-1],
          "Date": date,
        }
        results.append(output)
        
output_file = open("output.json", 'w')
output_file.write(json.dumps(results))

input_file.close()
output_file.close()
