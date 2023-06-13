#!/usr/bin/env python
#coding: utf-8

# In[19]:
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.amazon.com")
driver.maximize_window()
time.sleep(10)

search_box = driver.find_element(By.ID,"twotabsearchtextbox")
search_box.send_keys("xiamo charger yellow watch red")
search_button = driver.find_element(By.ID, 'nav-search-submit-button')
search_button.click()

product_name = []
product_price = []
product_rating = []
product_ratings_num = []
product_category = []
product_url = []
list_of_reviews = []
final_list = []

is_last_page = False
while not is_last_page:
    laptops = driver.find_elements(By.XPATH,'//div[@data-component-type="s-search-result"]')
    for laptop in laptops:
        product_category.append('laptop')
        names = laptop.find_elements(By.XPATH,".//span[@class='a-size-medium a-color-base a-text-normal']")
        ratings_num = laptop.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']")
        product_name.extend([name.text for name in names])
        product_ratings_num.extend([rating_num.text for rating_num in ratings_num])
        time.sleep(10)
        linkprop = laptop.find_element(By.CSS_SELECTOR,".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
        link = linkprop.get_attribute("href")
        print(link)
        product_url.append(link)
        driver.execute_script('''window.open("'''+link+'''","_blank");''')
        time.sleep(4)
        # scraping code inside the product page.
        
        try:
            if len(laptop.find_elements(By.XPATH,".//span[@class='a-price-whole']")) > 0:
                prices = laptop.find_elements(By.XPATH,".//span[@class='a-price-whole']")
                for price in prices:
                    product_price.append(price.text)
                    time.sleep(10)
            else:
                product_price.append("0")
        except NoSuchElementException as e:
            # Handle the exception if an element is not found
            print("Element not found:", e)
        except Exception as e:
            # Handle any other exceptions that may occur during scraping
            print("An error occurred during scraping:", e)
        
        try:
            if len(laptop.find_elements(By.XPATH,".//span[@class='reviewCountTextLinkedHistogram noUnderline']")) > 0:
                ratings = laptop.find_elements(By.XPATH,".//span[@class='reviewCountTextLinkedHistogram noUnderline']")
                for rating in ratings:
                    rating2 = rating.get_attribute('title')
                    product_rating.append(rating2)
                    time.sleep(10)
            else:
                product_rating.append("0")
        except NoSuchElementException as e:
            # Handle the exception if an element is not found
            print("Element not found:", e)
        except Exception as e:
            # Handle any other exceptions that may occur during scraping
            print("An error occurred during scraping:", e)
        
        # closing of the window that shows the product page.
        
        time.sleep(2)
        # switching to the parent window
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        link1 = driver.current_url.split("/")[0] + "//" + driver.current_url.split("/")[2] + "/" + driver.current_url.split("/")[3]
        print(link1)
        print(driver.current_url)
        link2 = link1 + "/product-reviews/" + driver.current_url.split("/")[5] + "/reviewerType=all_reviews"
        print(link2)
        list_of_reviews.append(link2)
        driver.execute_script('''window.open("'''+link2+'''","_blank");''')
        time.sleep(4)
        
        ratings = driver.find_elements(By.XPATH,".//span[@class='a-size-medium a-color-base']")
        product_rating.extend([rating.text for rating in ratings])
        time.sleep(4)
        parent = driver.window_handles[0]
        chld = driver.window_handles[1]
        chld2 = driver.window_handles[2]
        print(len(driver.window_handles))
        driver.switch_to.window(chld)
        print(len(driver.window_handles))
        driver.close()
        driver.switch_to.window(chld2)
        print(len(driver.window_handles))
        driver.close()
        driver.switch_to.window(parent)

    try:
        next_page = driver.find_element(By.XPATH,".//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
        next_page.click()
        time.sleep(10)
    except NoSuchElementException:
        is_last_page = True

print('no of laptops==>', len(product_name))
print('no of prices==>', len(product_price))

driver.quit()




# %%
import pandas as pd
df = pd.DataFrame(zip(product_name, product_category, product_price, product_rating, product_ratings_num, product_url, list_of_reviews), columns=['product_name', 'product_category', 'product_price', 'product_rating', 'product_ratings_num', 'product_url', 'list_of_reviews'])
df.to_excel("/Users/SalmaDkier/Desktop/PFA/scrap/scrap.xlsx", index=False)

# %%
