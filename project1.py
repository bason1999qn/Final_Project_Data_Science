from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

with webdriver.Chrome(options=options) as browser:
    data = pd.DataFrame(columns=['Date', 'Close/Last', 'Volume', 'Open', 'High', 'Low', 'Company'])
    urls = ['https://www.nasdaq.com/market-activity/stocks/googl/historical',
            'https://www.nasdaq.com/market-activity/stocks/aapl/historical',
            'https://www.nasdaq.com/market-activity/stocks/amzn/historical',
            'https://www.nasdaq.com/market-activity/stocks/fb/historical',
            'https://www.nasdaq.com/market-activity/stocks/tsla/historical',
            'https://www.nasdaq.com/market-activity/stocks/msft/historical'
            ]
    companies = ['Alphabet', 'Apple', 'Amazon', 'Facebook', 'Tesla', 'Microsoft']
    for index in range(len(urls)):
        browser.get(urls[index])
        # browser.get(urls[i])
        time.sleep(4)
        try:
            close = browser.find_element_by_id('_evh-ric-c')
            ActionChains(browser).click(close).perform()
        except NoSuchElementException:
            pass
        expand = browser.find_element_by_xpath('//button[text()="MAX"]')
        ActionChains(browser).click(expand).perform()
        browser.execute_script("window.scrollTo(0, 450)")
        i = 0
        while i < 70:
            rows = browser.find_elements_by_class_name('historical-data__row')
            for row in rows:
                row_data = row.text.split(' ')
                row_data.append(companies[index])
                data.loc[len(data), :] = row_data
            print(data)

            next_button = browser.find_element_by_class_name('pagination__next')
            ActionChains(browser).click(next_button).perform()
            time.sleep(5)
            i += 1

    data.to_csv('stock_data.csv', sep='\t', index=False)
