import glassdoor_scraper as gs
import pandas as pd

path = "/Users/venkatj/Projects/Glassdor_Salary_predict/chromedriver"
df = gs.get_jobs('data-scientist',3,False, path, 10)
df.to_csv('glassdoor_jobs_1k.csv')