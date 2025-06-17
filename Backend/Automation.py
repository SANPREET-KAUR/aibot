from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
env_vars = dotenv_values("../.env")

GroqAPIKey = env_vars.get("GROQ_API_KEY") or "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"

if not GroqAPIKey:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

client = Groq(api_key=GroqAPIKey)

# Define CSS classes for parsing specific elements in HTML content.
classes = ["ZcZubb", "hgKElc", "LTKOO SY7ric", "ZOLOW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "I26fcd", "OSr6Id tL9QX", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWfRfe", "VQF4g", "vQ3w9e", "kno-desc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq Client with the API key.
# client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I’m at your service for any additional questions or support you may need—don’t hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {env_vars.get('Username', 'User')}, You're a content writer. You have to write content like letter"
}]

def GoogleSearch(Topic):
    search(Topic)
    return True
# GoogleSearch("ahemadabad doctor family")
def Content(Topic):

    
    def OpenNotepad(File):
        default_text_editor='notepad.exe'
        subprocess.Popen([default_text_editor,File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user","content":f"{prompt}"})

        completion=client.chat.completions.create(
            model="llama3-8b-8192",
            messages=SystemChatBot+messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer=""
        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response.
        return Answer

    Topic: str = Topic.replace("Content ", "")  # Remove "Content " from the topic.
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

    # Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True
# Content("application for sick leave ")
def YoutubeSearch(Topic):
    Url4Search=f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True
# PlayYoutube("Triggered Insaan")
def OpenApp(app,sess=requests.session()):
    try:
        appopen(app,match_closest=True,output=True,throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup =BeautifulSoup(html,'html.parser')
            links=soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href')for link in links]
        def search_google(query):
            url=f"https://www.google.com/search?q={query}"
            headers={"User-Agent":useragent}
            response=sess.get(url,headers=headers)

            if response.status_code==200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None
        html=search_google(app)

        if html:
            link=extract_links(html)[0]
            webopen(link)
        return True
# OpenApp("Google Chrome")
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app,match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False
        
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume mute")
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")
    if command=="mute":
        mute()
    elif command=="unmute":
        unmute()
    elif command=="volume up":
        volume_up()
    elif command=="volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs=[]
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file"==command:
                pass
            else:
                fun=asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun=asyncio.to_thread(CloseApp,command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun=asyncio.to_thread(PlayYoutube,command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun=asyncio.to_thread(Content,command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun=asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun=asyncio.to_thread(YoutubeSearch,command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun=asyncio.to_thread(System,command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")
    results=await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__=='__main__':
    asyncio.run(Automation(["open facebook","open instagram","open telegram","play afsanay","content song for me"]))