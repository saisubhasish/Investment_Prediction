import os
import sys
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from investment_prediction.exception import InvestmentPredictionException
from investment_prediction.logger import logging



class Data_scraper:
    @staticmethod
    def scraper(company, start_date, end_date, driver_path, raw_file_path):
        '''
        To automate the process of changing start date and end date in the code, 
        We can create a function that takes start date and end date as input parameters and formats them as Unix timestamps. 
        We can then construct the URL with the formatted timestamps as query parameters.
        '''
        logging.info(f"{'>>'*20} Web Scrapping {'<<'*20}")
        logging.info("Creating raw file path if not exists")
        if not os.path.exists(raw_file_path):
            os.makedirs(raw_file_path)

        logging.info(f"Scrapping for {company} company data")
        logging.info("Step 1: Create a session and load the page")
        logging.info("Preparing time-stamp for start and end interval")
        start_timestamp = int(time.mktime(time.strptime(start_date, '%Y-%m-%d')))
        end_timestamp = int(time.mktime(time.strptime(end_date, '%Y-%m-%d')))

        logging.info("Preparing url with company name and time interva")
        url = f'https://in.investing.com/equities/{company}-historical-data?end_date={end_timestamp}&st_date={start_timestamp}'
        
        logging.info(f"Requesting {company} company url in Chrome browser")
        try:
            driver = webdriver.Chrome(driver_path)
            driver.get(url)

        except Exception as e:
            raise InvestmentPredictionException(e, sys)
        
        driver.implicitly_wait(2)
        
        logging.info("Scrolling to the end of the page")
        driver.maximize_window()
        driver.implicitly_wait(2) 
        
        driver.execute_script("window.scrollBy(0,500)","")
        time.sleep(3)
        
        driver.execute_script("window.scrollBy(0,2000)","")
        time.sleep(3)
        
        driver.execute_script("window.scrollBy(0,5000)","")
        time.sleep(3)
        
        driver.execute_script("window.scrollBy(0,5000)","")
        time.sleep(3)
        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        driver.execute_script("window.scrollBy(0,-2000)","")
        time.sleep(5)

        logging.info("Step 2: Close the pop-up if it appears")
        try:
            maybe_later_button = driver.find_element_by_xpath("//button[contains(text(),'Maybe later')]")
            maybe_later_button.click()
        except:
            pass

        logging.info("Step 3: Parse lxml code and grab tables with Beautiful Soup")
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            tables = soup.find_all('table')
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

        logging.info("Step 4: Read tables with Pandas read_html()")
        dfs = pd.read_html(str(tables))

        print(f'Total tables: {len(dfs)}')
        print(dfs[0])

        driver.close()

        logging.info(f"Saving scrapped data to: {raw_file_path}")
        dfs[0].to_csv(os.path.join(raw_file_path, f"{company}.csv"))


