import sys
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
#from datetime import datetime
from investment_prediction.exception import InvestmentPredictionException


save_file_to_path = "D:/FSDS-iNeuron/10.Projects-DS/Investment_Prediction/raw_dataset/"
start_date = '2016-03-19'
end_date = '2023-03-19'
driver_path = r"D:\FSDS-iNeuron\10.Projects-DS\Investment_Prediction\selenium\chromedriver.exe"
company = 'itc'

#britannia-industries --> Britannia Inductries
#itc --> ITC
#reliance-industries --> Reliance Industries
#tata-consultancy-services  -->  TCS
#tata-motors-ltd --> TATA Motors

class data_scraper:
        
    def scraper(self, company, start_date, end_date, driver_path):
        '''
        To automate the process of changing start date and end date in the code, 
        We can create a function that takes start date and end date as input parameters and formats them as Unix timestamps. 
        We can then construct the URL with the formatted timestamps as query parameters.
        '''
        # Step 1: Create a session and load the page
        # Preparing time-stamp
        start_timestamp = int(time.mktime(time.strptime(start_date, '%Y-%m-%d')))
        end_timestamp = int(time.mktime(time.strptime(end_date, '%Y-%m-%d')))

        # Preparing url with company name and time interval
        url = f'https://in.investing.com/equities/{company}-historical-data?end_date={end_timestamp}&st_date={start_timestamp}'
        
        # Requesting url in Chrome browser
        try:
            driver = webdriver.Chrome(driver_path)
            driver.get(url)

        except Exception as e:
            raise InvestmentPredictionException(e, sys)
        
        driver.implicitly_wait(2)
        
        
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

        # Step 2: Close the pop-up if it appears

        try:
            maybe_later_button = driver.find_element_by_xpath("//button[contains(text(),'Maybe later')]")
            maybe_later_button.click()
        except:
            pass

        # Step 3: Parse HTML code and grab tables with Beautiful Soup
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            tables = soup.find_all('table')
        except Exception as e:
            raise InvestmentPredictionException(e, sys)

        # Step 4: Read tables with Pandas read_html()
        dfs = pd.read_html(str(tables))

        print(f'Total tables: {len(dfs)}')
        print(dfs[0])

        driver.close()

        # Saving data to directory
        dfs[0].to_csv(f'{save_file_to_path}{company}.csv')

# example usage
scraper = data_scraper()
scraper.scraper(company, start_date, end_date, driver_path)
