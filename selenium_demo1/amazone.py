from selenium import webdriver
from selenium.webdriver.common.by import By
import time
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser=webdriver.Chrome(options=options)
browser.get('https://www.amazon.in')
#get the input elemets
input_search=browser.find_element(By.ID,'twotabsearchtextbox')
search_button=browser.find_element(By.XPATH,"(//input[@type='submit'])[1]")
#send the input
input_search.send_keys('smartphones under 10000')
time.sleep(1)
search_button.click()
u=browser.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[5]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span[@class="a-size-medium a-color-base a-text-normal"]').text
time.sleep(1)
browser.quit()
print(u)
#product_class='a-size-medium a-color-base a-text-normal'
#next_button='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'

#scrapp product from amazone
'''product=[]
for i in range(10):
    print('scraping page ',i+1 )
    product=browser.find_element(By.CLASS_NAME,product_class).text
    product.extend(product)
    next_button=browser.find_element(By.CLASS_NAME,'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')
    next_button.click()
    time.sleep(3)
    '''