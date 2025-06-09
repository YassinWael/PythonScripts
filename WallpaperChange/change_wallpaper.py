from requests import get
from os import environ,getlogin
import ctypes
from time import sleep
from sys import exit
from random import choice
from icecream import ic
from dotenv import load_dotenv
load_dotenv()
user_name = getlogin()
google = environ.get("google")

url = "https://api.pexels.com/v1/search"

key = "Mif8qLZbhi91nUxyd04BizIjwiRlOWmfZRpOleFwltCgN1V3VWe68plc"
headers = {
    "Authorization":key,
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
#DO NOT REMOVE THE USER AGENT, OR A 403 ERROR WILL BE RETURNED.
queries = ["night", "landscape","magnifent", "nature", "city", "animals", "sea", "space", "mountains", "forest", "architecture", "food", "weather", "transportation","history", "skyline", "sunset", "beach", "waterfall", "galaxy", "clouds", "desert", "countryside"]

input("""Hello, and welcome to Wallpaper Changer 1.0,
   1. Y Sets wallpaper and closes the script
   2. N Finds another wallpaper from the same keyword
   3. Q Changes the keyword (Randomized and no chance of being the same twice)
   Press Enter to start...""")

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


def get_next_page(request_data):
    try:
        print("Found next page.")
        return request_data["next_page"]
    except KeyError:
        print("No more images lol (Skill issue)")
        exit()

def download_photo(url, file_name=rf"C:\Users\{user_name}\wallpaper.png"):
    try:
        response = get(url, stream=True,headers=headers)
        response.raise_for_status()  # Ensure the request was successful

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded image and saved to {file_name}")

    except Exception as e:
        print(f"Image downloading failed due to: {e}")


def get_photo(url=url,next_page=0):
    
    global req # to get next page when needed
    if bool(next_page): 
        print(f"retrieved photo from next page.")
        req = get(url,headers=headers).json()
    else:
        params = {
    "query":f"{choice(queries)}",
    "orientation":"landscape"
    }  #defined it inside the function, so that the query gets randomized
        print(f"retrieved photo from {params['query']}")
        ic(url)
        req = get(url,headers=headers,params=params).json()
    return req.get("photos")[0]["src"]["original"]

def get_photo_google(query=choice(queries)):
    params = {
        "imgSize":"xxlarge",
        "fileType":"JPEG, PNG, WebP",
        "cx":"2714eb689a4f24a53",
        "searchType":"image",
        "siteSearch":"https://www.tiktok.com/",
        "siteSearchFilter":"e"

    }
    request = get(f"https://www.googleapis.com/customsearch/v1?key={google}&q={query}",params=params).json()
    image_link = (request['items'][0]['link'])

    ic(image_link)
    return image_link
def set_wallpaper(image=rf"C:\Users\{user_name}\wallpaper.png"):
    ctypes.windll.user32.SystemParametersInfoW(20,0,image,3)
    print("Wallpaper changed successfully.")

image_url = get_photo()
download_photo(image_url)
sleep(1) #just for the file to be saved
set_wallpaper()

while True:
    user_response = input("Is it good? Y/N/Q ").lower()
    if  user_response == "n" or user_response == "no":
        print("Getting another photo from the same keyword...")
        next_page = get_next_page(req)
        new_image = get_photo(url=next_page,next_page=1) #next_page 1 so no query type is printed, since its the same one. just the next page
        download_photo(new_image)
        set_wallpaper()
    elif user_response == "q" or "query" in user_response:
        print("Randomizing new query choice...")
        new_image = get_photo()
        download_photo(new_image)
        set_wallpaper()
    else:
        quit()
    











