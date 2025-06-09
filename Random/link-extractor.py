from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from icecream import ic

chrome_options = Options()


driver = webdriver.Chrome()

driver.get(url="https://www.youtube.com/results?search_query=half+life+2+trailer")


driver.implicitly_wait(10)

 # Find all <a> elements on the page
links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')]
        
        # Filter out None or invalid links
links = [link for link in links if link]

ic(links)