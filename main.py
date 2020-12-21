import os
import time
import logging
import requests
import yagmail
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()
email_address = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')

def email(name, url):
    """ 
         email myself if item is in stock
    """
    user = email_address
    app_password = password
    to = email_address

    subject = 'PS5 is in baby!'
    content = f"""
            Click below to buy
            {name}
            {url}
    """

    try:
        with yagmail.SMTP(user, app_password) as yag:
            yag.send(to, subject, content)
        logging.info(f'{key} - email success')
    except:
        logging.critical(f'{key} - email failed')



def check_walmart():
    """ 
         check if the button text 'Add to cart' exists
    """
    logging.info('Start bot')
    
    urls = {
        'PS5 Digital Edition': 'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815',
        'PS5 Console': 'https://www.walmart.com/ip/PlayStation-5-Console/363472942'
    }

    driver = webdriver.Chrome()
    class_name = 'prod-product-cta-add-to-cart'

    for key in urls:
        driver.get(urls[key])
        logging.info(f'{urls[key]} - downloaded')
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(driver, 5).until(element_present)
            item_message = driver.find_element_by_class_name(class_name).text
            if 'Add to cart' in item_message:
                logging.info(f'{key} - In Stock')
                email(key, urls[key])
        except TimeoutException:
            logging.info(f'{key} - Not in stock')    
    driver.quit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="./logs/main.log", format='%(asctime)s:%(levelname)s:%(message)s')
    scheduler = BlockingScheduler()
    scheduler.add_job(check_walmart, 'interval', minutes=1)
    scheduler.start()