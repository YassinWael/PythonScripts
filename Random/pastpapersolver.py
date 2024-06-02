from time import sleep
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from os import startfile



print("""


$$\      $$\                 $$\           
$$$\    $$$ |                $$ |          
$$$$\  $$$$ | $$$$$$\   $$$$$$$ | $$$$$$\  
$$\$$\$$ $$ | \____$$\ $$  __$$ |$$  __$$\ 
$$ \$$$  $$ | $$$$$$$ |$$ /  $$ |$$$$$$$$ |
$$ |\$  /$$ |$$  __$$ |$$ |  $$ |$$   ____|
$$ | \_/ $$ |\$$$$$$$ |\$$$$$$$ |\$$$$$$$\ 
\__|     \__| \_______| \_______| \_______|
                                           
                                           
                                           

$$$$$$$\            
$$  __$$\           
$$ |  $$ |$$\   $$\ 
$$$$$$$\ |$$ |  $$ |
$$  __$$\ $$ |  $$ |
$$ |  $$ |$$ |  $$ |
$$$$$$$  |\$$$$$$$ |
\_______/  \____$$ |
          $$\   $$ |
          \$$$$$$  |
           \______/ 

      

$$\     $$\                             $$\                 
\$$\   $$  |                            \__|                
 \$$\ $$  /$$$$$$\   $$$$$$$\  $$$$$$$\ $$\ $$$$$$$\        
  \$$$$  / \____$$\ $$  _____|$$  _____|$$ |$$  __$$\       
   \$$  /  $$$$$$$ |\$$$$$$\  \$$$$$$\  $$ |$$ |  $$ |      
    $$ |  $$  __$$ | \____$$\  \____$$\ $$ |$$ |  $$ |      
    $$ |  \$$$$$$$ |$$$$$$$  |$$$$$$$  |$$ |$$ |  $$ |      
    \__|   \_______|\_______/ \_______/ \__|\__|  \__|      
                                                            
                                                            
                                                            

""")




def get_link(subject="chemistry",question=" Acid-base reactions are examples of proton transfer. (a) Ethylamine is a weak base and sodium hydroxide is a strong base.(i) In terms of proton transfer, explain what is meant by the term weak base."):
    question = question.replace(" ","+")
    link = f"https://caiefinder.com/search/?subs={subject}&zone=&search={question}+"
    ("Getting Link...")
    return(link)

def download_file(link):
    try:
        file_data = get(link).content
        past_paper_name = link.split("/")[-1]
        with open(f"{past_paper_name}","wb") as file:
            file.write(file_data)
        return past_paper_name
    except Exception as e:
        return None
    
def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach",True)
    chrome_options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options=chrome_options)
    print("Running Chrome In The Background...")
    return driver

def main():
    driver = setup_driver()
    subject = input("Please enter your prefered subject: ").capitalize()
    while True:
        try:
            
            
                
                question = input("Please enter your question (Doesn't need to be full, just consecutive EXACT words): ")
                if question == "d":
                        pdf_link = driver.find_element(By.XPATH,"/html/body/div[2]/div/center[3]/h3/a")
                        pdf_link.click()
                        sleep(1)
                        driver.switch_to.window(driver.window_handles[1])
                        print("Downloading Mark Scheme...")
                        file_name = download_file(driver.current_url)
                        if file_name:
                            startfile(file_name)
                            continue
                if question == "l":
                        print(driver.current_url)
                        continue
                link = get_link(subject,question)
                # link = get_link()
                driver.get(link)


                WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/pre"))
                )

                answer = driver.find_element(By.XPATH,"/html/body/div[2]/div/pre")
                print("------------------------------------------------------------------------------------------------------------------------")
                print("------------------------------------------------------------------------------------------------------------------------")
                print("------------------------------------------------------------------------------------------------------------------------")
                print(answer.text)
                print("------------------------------------------------------------------------------------------------------------------------")
                print("------------------------------------------------------------------------------------------------------------------------")
                print("------------------------------------------------------------------------------------------------------------------------")
        except Exception as e:
            print(f"Failed due to: {e}")
            print("No search results found, Please try again...")


if __name__ == "__main__":
    main()
# https://caiefinder.com/pastpapers/pdf/IGCSE/Chemistry%20(0620)/2015/0620_s15_ms_31.pdf