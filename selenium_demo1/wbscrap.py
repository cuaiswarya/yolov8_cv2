from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver=webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.google.com/")  
time.sleep(3)
#waiting for element appear on scsreen-------------
element = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.NAME,"q")))
element.send_keys("bmw")
element.submit()
for i in range(3):
  print(driver.find_element(By.XPATH,'//*[@id="rso"]/div[6]/div/div/div[1]/div/a/div/div/span').text)
#img=driver.find_element(By.CLASS_NAME,'gb_ie')
#img.click()
driver.quit()

