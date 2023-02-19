from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import pandas as pd

def get_jobs(verbose, path, sleep_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.co.in/Job/data-scientist-jobs-SRCH_KO0,14.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520scientist&typedLocation=&context=Jobs&dropdown=0'
    driver.get(url)
    job_buttons = driver.find_elements(By.XPATH,'.//il[@class="react-job-listing css-wp148e eigr9kq3"]')
    for job_button in job_buttons:  
        print("Iteration: ",job_button)