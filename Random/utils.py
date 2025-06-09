from os import environ
from json import loads
from icecream import ic
from pprint import pprint
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
from requests import get,exceptions
from bs4 import BeautifulSoup
from ratelimit import sleep_and_retry,limits
import google.generativeai as genai
from time import sleep
from pickle import dump,load
from coinpaprika import client as Coinpaprika
import difflib
def find_most_similar(word,word_list):
    matched_word = difflib.get_close_matches(word,word_list,n=1,cutoff=0.68)
    return matched_word[0] if matched_word else None


client = Coinpaprika.Client()





load_dotenv()
genai_api_key = environ.get("genai_api_key")
units = [("KH/s",1000),("MH/s",1e6),("GH/s",1e9),("TH/s",1000000000000),("PH/s",1000000000000000),("EH/s",1000000000000000000)]
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",  # Do Not Track – optional but polite
}


def get_coin_exchange_details(coin_name="",past_exchanges = [],coin_id=""):
    coin_data = {}
    if not coin_id:
        coin_name = coin_name.replace(" ","").replace("(","").replace(")","").strip(" ").lower()
        if past_exchanges:
            past_names = [exchange[0] for exchange in past_exchanges]
            if find_most_similar(coin_name,past_names):
                return "Past"
        coin_id = find_most_similar(coin_name,exchanges)
        coin_data = {}
        if not coin_id:
            ic(exchanges)
            ic(coin_id)
            
        
            return None
    
       
    try:    
        data = client.exchange(coin_id)
        ic(f"Found: {coin_name}")
        ic(data)
        sleep(5)
        if not data['id']:
            ic("NO ID")
            ic(data)
        coin_data['Exchange Name'] = data['name']
        coin_data['Direct URL'] = data['links'].get('website',None)[0] if data['links'].get('website',None) else None

        coin_data['24h Volume'] = round(data['quotes'].get("USD")['adjusted_volume_24h'],2)
        coin_data['Fiat On-ramps'] = str([fiat.get('symbol') for fiat in data['fiats']]).replace("[","").replace("]","") if data.get('fiats') else None
        coin_data['Markets Served'] = data.get('markets')
        coin_data['Analysis (Paprika)'] = f"https://coinpaprika.com/exchanges/{data['id']}/"
        ic(coin_data)
    except Exception as e:
        ic(e)
        ic(data)
    return(coin_data)


def convert_hashrate_to_difficulty(raw_hashrate,unit):
    unit = "H/s" if not unit else unit
    i = 0
   
    ic(raw_hashrate)
    while (raw_hashrate / units[i][1]) > 1:
        i += 1
        ic(i)
    raw_hashrate /= units[i-1][1]

    return f"{round(raw_hashrate,2)} {units[i-1][0]}"

def safe_update(original, updates):
    for key,value in updates.items():
        if value is not None:
            original[key] = value


def convert_timestamp_to_readable(timestamp):
    eastern = timezone('US/Eastern')
    timestamp = datetime.fromtimestamp(int(timestamp),tz=eastern)
       
    return datetime.isoformat(timestamp)


def get_coin_algos(coin_name,coins):
        all_algos = [coin['algo'] for coin in coins if coin['name'] == coin_name]
        return all_algos


def get_coin_socials(coin):
    socials = {}
    coin = coin.lower().replace(" ","")
    ic(f"https://miningpoolstats.stream/{coin}")
    request = get(f"https://miningpoolstats.stream/{coin}",timeout=30)
    ic(request.status_code)
    ic(f"Getting socials for {coin}")
    soup = BeautifulSoup(request.text,"lxml")

    links = ([link['href'] for link in soup.find_all('a') if "https" in link['href']])
    
    socials['telegram'] = next((link for link in links if "t.me" in link), None)
    socials['github'] = next((link for link in links if "github" in link), None)
    socials['reddit'] = next((link for link in links if "reddit" in link), None)
    socials['twitter'] = next((link for link in links if "twitter" in link), None)
    socials['discord'] = next((link for link in links if "discord" in link), None)
    socials['website'] = next((link for link in links if coin in link and link not in socials.values() and 'github' not in link and 'reddit' not in link and 'twitter' not in link and 'discord' not in link), None)
    pprint(socials)
    return socials


def get_project_rating_coinpaprika(coin,symbol):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://coinpaprika.com',
        'referer': 'https://coinpaprika.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    }
    response = get(f'https://api-frontend.coinpaprika.com/coin/{symbol}-{coin}/markets?per_page=30000&page=1',headers=headers,timeout=30)
    ic(f'https://api-frontend.coinpaprika.com/coin/{symbol}-{coin}/markets?per_page=30000&page=1')
    

    try:
        project_rating = ""
        ic("project rating",response.status_code)
        data = response.json().get('data').get('data') if response.status_code == 200 else None
        if not data:
            ic("none",data)
            return "C"
        exchanges_length = max([exchange['rank'] for exchange in data],default=0)
        ic(exchanges_length)
        if exchanges_length:
            if exchanges_length > 5:
                project_rating = "A"
            elif exchanges_length > 2:
                project_rating = "B"
            else:
                project_rating = "C"
            return project_rating
        else:
            ic(f"Project rating not found, {coin}")
            pprint(data)
            return None
    except Exception as e:
        ic(e)
        ic(data)
     



def get_coin_details_coinpaprika(coin="",symbol="",url=""):
    print(f"Getting details for {coin}")
    coin = coin.lower().replace(" ","-")
    symbol = symbol.lower()
    url = f"https://coinpaprika.com/coin/{symbol}-{coin}" if not url else url
    ic(url)

    request = get(url,stream=False,headers=headers,timeout=30)
    ic(request.status_code)
    if request.status_code == 404:
        print("Coin not found: ",coin)
        return {
            "Liquidity":"",
            "Exchanges":"",
            "Code Progress":"",
            "Overview":"",
            "Project Rating":"",
        }
    
    

    coin_details = {}
    soup = BeautifulSoup(request.text,"lxml")
    all_links = [a.get("href") for a in soup.find_all("a", href=True)]
    all_links = [link for link in all_links if link.startswith("http")]
   
   
 
    # coin_details['description'] = soup.find("p",{"class":"cp-content-intro"}).text
    coin_details['Whitepaper'] = next((link for link in all_links if "whitepapers" in link), None)
    coin_details['Explorer'] = next((link for link in all_links if "explore" in link), None)
    coin_details['Liquidity'] = f"{url}/liquidity"
    coin_details['Exchanges'] = f"{url}/exchanges"
    coin_details['Code Progress'] = f"{url}/code-progress"
    coin_details['Overview'] = url
    coin_details['Project Rating'] = get_project_rating_coinpaprika(coin,symbol)

    pprint(coin_details)
    return coin_details

def clean_sheet(sheet):
    """Deletes any row that starts with None"""
    rows_to_delete = [row[0].row for row in sheet.rows if not row[0].value]
    for row_idx in sorted(rows_to_delete,reverse=True):
        sheet.delete_rows(row_idx)

def get_coin_details_from_website(website):
    genai.configure(api_key=genai_api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")


    main_prompt = "You will be passed the entire text of a webpage that is for a crypto coin, your purpose is to extract the description of the coin from the website text and send back the data ONLY JSON, ONLY REPSOND WITH JSON. In the following format. KEEP IT TO 150 WORDS MAXIMUM, MAKE SURE TO PROVIDE THE DESCRIPTION IN A WAY THAT IS PARSABALE BY THE PYTHON .loads() FUNCTION. {'description':''}"
    headers = {
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        }

    request = get(website,headers=headers,timeout=30)
    soup = BeautifulSoup(request.text,"lxml")
    all_text = "".join([div.text.replace("\n","") for div in soup.find_all("div") if (len(div.text) > 10)])
    try:
        response = model.generate_content(f"{main_prompt}: {all_text}")
    
        

        print(len(all_text))
        json_content = response.text.lstrip("```json").rstrip("```")
        pprint(json_content)
    
        return loads(json_content)
    except Exception as e:
        ic(e)
        return {"description":""}
    


def query_gemini(prompt,text,scheme):
    genai.configure(api_key=genai_api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")
    json_only = f'YOU WILL ONLY RETURN THE RESULT AS A JSON, MAKE SURE THE JSON WILL NOT RAISE AN JSONDecodeError WHEN LOADED BY THE .loads() FUNCTION IN PYTHON, NOTHING MORE NOTHING LESS. YOU SHOULD MAKE SURE YOUR TEXT AND RESPONSE DO NOT VIOLATE THE SCHEMA: {str(scheme)}'

    try:
        response = model.generate_content(f"{prompt}, {json_only}. {text}")
    
        json_content = response.text.lstrip("```json").rstrip("```")
        ic(json_content)
        return loads(json_content)
    except Exception as e:
        ic(e)
        return {"description":""}


def save_data_from_airtable_to_pkl(table,fields=[]):
    all_data = table.all(fields=fields) if fields else table.all()
    with open("table.pkl","wb") as f:
        dump(all_data,f)

@sleep_and_retry
@limits(calls=1, period=1)
def check_link_validity(link):
    ic(f"Checking {link}")
    try:
        request = get(link,headers=headers,timeout=30)
        ic(request.status_code)
        return (True,request.status_code)
    except exceptions.RequestException:
        ic("ConnectionError")
        ic(request.status_code)
        return (False,request.status_code)
    

def get_all_links_from_website(website):
    request = get(website,timeout=30,headers=headers)
    if request.status_code != 200:
        ic(f"Error getting links from {website}")
        return []
    soup = BeautifulSoup(request.text,"lxml")
    all_links = [a.get("href") for a in soup.find_all("a", href=True) if not a.get("href").startswith("/") and not a.get("href").startswith("#")]
    all_links = [link for link in all_links if len(link) > 5]
    return all_links

def get_all_text_from_website(website):
    request = get(website,timeout=30,headers=headers)
    request.raise_for_status()
    soup = BeautifulSoup(request.text,"lxml")
    all_text = "".join([div.text.replace("\n","") for div in soup.find_all("div") if (len(div.text) > 10)])
    return all_text


def get_coin_wallet(links="",coin_url=""):
    wallet = ""
    if not links:
        links = get_all_links_from_website(coin_url)
        pprint(links)
    wallet = next((link for link in links if "wallet" in link), None)
      
    if not wallet:
        response = query_gemini(prompt="Extract any crypto coin wallet links from the following list of links. If there are multiple return the best one of them ONLY ONE, if there is none then just return 'None'. Make sure it is an actual wallet page and not just anything. a minimal example is https://www.bnbchain.org/en/wallets or https://coinpaprika.com/coins-wallet/btc-bitcoin/ it does not need to have 'wallet' in the link, but it should NOT be the website's page itself (bitcoin.org for example is NOT a wallet link)",text=str(links))
        ic(response)
        wallet = response.get("wallet")
    ic("Returning", wallet)
    return wallet
