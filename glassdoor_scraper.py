from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, sleep_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.co.in/Job/' + keyword + '-jobs-SRCH_KO0,14.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=&context=Jobs&dropdown=0'
    driver.get(url)
    jobs = []
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        done = False
        while not done:
            #Going through each job in this page
            job_buttons = driver.find_elements(By.XPATH,".//article[@id='MainCol']//ul/li[@data-test='jobListing']")  #These are the buttons we're going to click.
            for job_button in job_buttons:  
                #Let the page load. Change this number based on your internet speed.
                # Or, wait until the webpage is loaded, instead of hardcoding it.
                # time.sleep(sleep_time)

                #Test for the "Sign Up" prompt and get rid of it.
##---------------- Simpler code to close the pop-up prompts-------##
                try:
                    
                    signup_element = driver.find_element(By.XPATH,".//div[@class='background-overlay']//span[@alt='Close']")
                    WebDriverWait(driver,sleep_time).until(EC.presence_of_element_located(signup_element)).click()
                    # driver.execute_script("arguments[0].click();",signup_element)
                except:
                    NoSuchElementException
                #To Click "Refresh Page Button"
                # try:
                #     element_1 = driver.find_element(By.XPATH,".//div[@id='JDCol']//button[@type='button']")
                #     driver.execute_script("arguments[0].click()",element_1)
                # except:
                #     NoSuchElementException

                time.sleep(0.1)
##---------------------------- Print the Progess of each job --------------------------##
                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break
##------------------------------ Click each job posting ------------------------------##               
                # try:
                    # WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, ".//div[@class='background-overlay']")))
                target_element = WebDriverWait(driver,1).until(EC.element_to_be_clickable(job_button))
                ActionChains(driver).move_to_element(target_element).click().perform()
                time.sleep(1)
                # except:   
                #     if ElementClickInterceptedException:
                #         actions = ActionChains(driver)
                #         actions.move_to_element(job_button).click().perform()

                #To Click "Refresh Page Button"
                try:
                    element_1 = driver.find_element(By.XPATH,".//div[@id='JDCol']//button[@type='button']")
                    driver.execute_script("arguments[0].click()",element_1)
                except:
                    NoSuchElementException
                
##-------------------------- Collect necessary data from each job posting --------------------------##
                collected_successfully = False
                while not collected_successfully:
                    try:
                        company_name = driver.find_element(By.XPATH,".//div[@data-test='employerName']").text
                        location = driver.find_element(By.XPATH,".//div[@data-test='location']").text
                        job_title = driver.find_element(By.XPATH,".//div[@data-test='jobTitle']").text

                    # click on the "Show more" button
                        show_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//div[@class='css-t3xrds e856ufb4']")))
                        show_more_button.click()
                        # wait for the text to load
                        element_with_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@id='JobDescriptionContainer']")))
                        job_description = element_with_text.text
                    except:
                        time.sleep(5)

                    try:
                        salary_estimate = driver.find_element(By.XPATH,".//div[@class='css-w04er4 e1tk4kwz6']//span[@data-test='detailSalary']").text
                    except NoSuchElementException:
                        salary_estimate = -1 #You need to set a "not found value. It's important."
                
                    try:
                        rating = driver.find_element(By.XPATH,'.//span[@data-test="detailRating"]').text
                    except NoSuchElementException:
                        rating = -1 #You need to set a "not found value. It's important."

                # Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    # print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))

                #Going to the Company tab...
                #clicking on this:
                #<div class="tab" data-tab-type="overview"><span>Company</span></div>
                
                try:
            # #         #<div class="infoEntity">
            # #         #    <label>Headquarters</label>
            # #         #    <span class="value">San Francisco, CA</span>
            # #         #</div>
                    headquarters = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(By.XPATH,'//div[@id="CompanyContainer"]//span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH,'.//div[@id="CompanyContainer"]//span[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1
                    
                if verbose:
                    print("Headquarters: {}".format(headquarters))
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("Competitors: {}".format(competitors))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    
##--------------------------------- Store every collected data as a dictionary --------------------##
                jobs.append({"Job Title" : job_title,
                "Salary Estimate" : salary_estimate,
                "Job Description" : job_description,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Headquarters" : headquarters,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue,
                "Competitors" : competitors
                })
                #add job to jobs
                
                done = True

##-------------------- Move to next page after clicking all job posting in a page ---------------##
        #Clicking on the "next page" button
            if done:
                try:
                    element = driver.find_element(By.XPATH,".//span[@alt='Close']")
                    driver.execute_script("arguments[0].click();",element)
                except:
                    NoSuchElementException
                driver.find_element(By.XPATH,"//span[@alt='next-icon']").click()   
                time.sleep(sleep_time)
            else:
                break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.