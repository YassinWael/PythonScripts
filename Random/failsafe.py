import google.generativeai as genai
from dotenv import load_dotenv
from os import environ
from pprint import pprint
from PIL import Image
from json import loads
from pyautogui import screenshot
from time import sleep
import winsound
import pyttsx3
from os import system
load_dotenv()
genai.configure(api_key=environ.get("genai_api_key"))
print("Google Generative AI is configured with the provided API key.")

engine = pyttsx3.init()
model = genai.GenerativeModel(model_name="gemini-2.0-flash")


def take_screenshot_and_check_nsfw(image_path=""):
    """
    Takes a screenshot and checks if the image is NSFW using Google Generative AI.
    
    Args:
        image_path (str): The path to the image file to be checked.
        
    Returns:
        dict: A dictionary containing the NSFW status and explanation.
    """
    if not image_path:
        screenshot("nsfw_check.png")
        winsound.PlaySound("click.wav", winsound.SND_ALIAS)
        image_path = "nsfw_check.png"

    response = model.generate_content(["All I need from you is to return a json following this schema {'NSFW':'boolean','Explanation':'why it is or why it is not'} if the image infront of you is nsfw (18+, sex, porn...etc) or has text that is nsfw roleplay. do NOT return anything else. make sure the output you return can be parsed with the python .loads() function withotu returning any errors.",Image.open(image_path)])

    if response.text:
        try:
            result = loads(response.text.lstrip("```json").rstrip("```"))

            # pprint(result)
        except Exception as e:
            pprint(response)
            result = {"NSFW": False, "Explanation": "Error parsing JSON"}
            print(f"Error parsing JSON: {e}")
    return result


while True:
    nsfw_status = take_screenshot_and_check_nsfw()
    print(f"Explanation: {nsfw_status['Explanation']}")

    if nsfw_status["NSFW"]:
        print("NSFW content detected!")
        print(f"Explanation: {nsfw_status['Explanation']}")
        winsound.PlaySound("alert.wav", winsound.SND_ALIAS)
        engine.say("NSFW content detected! You have 10 seconds to close the app before a shutdown is initiated.")
        engine.runAndWait()
        sleep(10)

        nsfw_status_repeat = take_screenshot_and_check_nsfw()
        if nsfw_status_repeat["NSFW"]:
            print("NSFW content still detected after 10 seconds. Shutting down the system.")
            engine.say("Shutting down the system due to NSFW content.")
            engine.runAndWait()
            system("shutdown /s /t 10")
        else:
            engine.say("Content is now safe after 10 seconds.")
            engine.runAndWait()


    else:
        print("Content is safe.")
    print("Taking another screenshot in 15 minutes...")
    sleep(800)  # Wait for 15 minutes before taking another screenshot