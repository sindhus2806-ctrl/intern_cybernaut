import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

url = "https://www.imdb.com/chart/top/"
driver.get(url)
rows = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//ul[contains(@class,'ipc-metadata-list')]/li")
    )
)

titles = []
years = []
ratings = []
rankings = []
for i, movie in enumerate(rows):
    try:
        title = movie.find_element(By.XPATH, ".//h3").text
        year = movie.find_element(By.XPATH, ".//span[contains(@class,'cli-title-metadata-item')]").text
        rating = movie.find_element(By.XPATH, ".//span[@class='ipc-rating-star--rating']").text

        titles.append(title)
        years.append(year)
        ratings.append(rating)
        rankings.append(i + 1)

    except Exception as e:
        print(f"Skipping row {i + 1}: {e}")

driver.quit()

df = pd.DataFrame({
    "Rank": rankings,
    "Title": titles,
    "Year": years,
    "IMDb Rating": ratings
})

df.to_csv("imdb_top_250_movies.csv", index=False)

print("Data extracted successfully! Saved as imdb_top_250_movies.csv")
