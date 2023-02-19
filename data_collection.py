import glassdoor_scraper as gs
import pandas as pd

path = "/Users/venkatj/Projects/Glassdor_Salary_predict/chromedriver"
df = gs.get_jobs('data-scientist',5,False, path, 5)
df