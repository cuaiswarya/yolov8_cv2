from selenium import webdriver
from selenium.webdriver.common.by import By
import time
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver=webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://pythonbasics.org/selenium-get-html/")
html = driver.page_source
time.sleep(2)
print(html)
driver.close()
print(type(html))