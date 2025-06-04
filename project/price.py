from bs4 import BeautifulSoup
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import time
import json

options = uc.ChromeOptions()
options.add_argument('--user-data-dir=/home/ashish.chaudhary@simform.dom/.config/google-chrome/Default')

browser = uc.Chrome(options=options)

amazon_url = 'https://www.amazon.in/'
flipkart_url = 'https://www.flipkart.com/'
# snapdeal_url = 'https://www.snapdeal.com/'
# walmart_url = 'https://www.walmart.com/'


data = {'amazon':[], 'flipkart': []}


def get_amazon_price(product_name):
    browser.get(amazon_url)
    time.sleep(2)
    search_box = browser.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys(product_name)
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    listed_items = soup.find_all(role = 'listitem', attrs={'data-index' : True})
    for item in listed_items:
        amazon_items = {}
        try:
            anchor = item.find(class_='a-link-normal s-line-clamp-2 s-link-style a-text-normal')
            price = item.find(class_='a-price-whole')
            if anchor and price:
                amazon_items['name'] = anchor.string
                amazon_items['price'] = price.string
                data['amazon'].append(amazon_items)
        except Exception as e:
            print(f"Error fetching item: {e}")
            continue


def get_flipkart_price(product_name):
    browser.get(flipkart_url)
    time.sleep(2)
    search_box = browser.find_element(By.NAME, 'q')
    search_box.send_keys(product_name)
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    items_page = soup.find(class_='DOjaWF gdgoEp')
    listed_items = items_page.find_all(class_='cPHDOP col-12-12')
    for item in listed_items:
        flipkart_items = {}
        try:
            section = item.find(class_='yKfJKb row')
            if section:
                item_name = section.find(class_='KzDlHZ')
                item_price = section.find(class_='Nx9bqj _4b5DiR')
                if item_name and item_price:
                    flipkart_items['name'] = item_name.string
                    flipkart_items['price'] = item_price.get_text(strip=True)
                    data['flipkart'].append(flipkart_items)
        except Exception as e:
            print(f"Error fetching item: {e}")
            continue




# product_name = input("Enter the product name: ")
# print("Fetching prices...")
# get_amazon_price(product_name)
# get_flipkart_price(product_name)







if __name__ =="__main__":
    start_time = time.perf_counter()
    product_name = input("Enter the product name: ")
    print("Fetching prices...")

    t1 = threading.Thread(get_amazon_price, args=(product_name,))
    t2 = threading.Thread(get_flipkart_price, args=(product_name,))
#     t3 = threading.Thread(get_snapdeal_price, args=(product_name,))
#     t4 = threading.Thread(get_walmart_price, args=(product_name,))

    t1.start()
    t2.start()
#     t3.start()
#     t4.start()

    t1.join()
    t2.join()
#     t3.join()
#     t4.join()
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    
    stop_time = time.perf_counter()
    print(f"Time taken: {stop_time - start_time} seconds")
    print("Data fetched successfully!")

    browser.close()