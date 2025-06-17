import cohere

from rich import print
from dotenv import dotenv_values
import os
env_path = os.path.join(os.path.dirname(__file__), '.env')
env_vars = dotenv_values(env_path)


CohereAPIKey =env_vars.get("CohereAPIKey")
# assert CohereAPIKey, "CohereAPIKey not found in .env file"

co = cohere.Client(api_key=CohereAPIKey)
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Initialize an empty list to store user messages.
messages = []

# Define the preamble that guides the AI model on how to categorize queries.
preamble = """ 
You are a very accurate Decision-Making Model that classifies queries into specific categories.

You must classify the given query into:
- 'general' → if it can be answered by a language model without needing real-time or external information.
- 'realtime' → if it requires up-to-date, real-world, or internet-based data (e.g. current events, live scores, trending news).
- task categories like 'open', 'close', 'play', 'generate image', 'system', 'reminder', etc.

*** Do NOT answer the query. Only classify it. ***
*** Always use lowercase category names. ***

---
👉 Examples:
- "who was akbar?" → general who was akbar?
- "how can I study more effectively?" → general how can I study more effectively?
- "what is python programming language?" → general what is python programming language?
- "thank you!" → general thank you!
- "how are you?" → general how are you?

---
🕒 Realtime Examples:
- "who is elon musk?" → realtime who is elon musk?
- "latest news today" → realtime latest news today
- "current weather in delhi" → realtime current weather in delhi
- "stock price of tesla" → realtime stock price of tesla

---
⚙️ Task Examples:
- "open chrome and tell me about india" → open chrome, general tell me about india
- "open notepad" → open notepad
- "remind me to drink water at 5pm" → reminder 5pm drink water
- "generate an image of a sunset on mars" → generate image of a sunset on mars
- "play music" → play music
- "exit" → exit
"""


# Define a chat history with predefined user-chatbot interactions for context.
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": " what is today's date and by the way remind me that i have a dancing performance on"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]

# Define the main function for decision-making on queries.
def FirstLayerDMM(prompt: str = "test"):
    # Add the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})

    stream=co.chat_stream(
        model='command-r-plus',
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )
    response=""
    for event in stream:
        if event.event_type=="text-generation":
            response+=event.text
    
    response=response.replace("\n","")
    response=response.split(",")
    response=[i.strip() for i in response]

    temp=[]
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
    
    response=temp
    if "(query)" in response:
        newresponse=FirstLayerDMM(prompt=prompt)
        return newresponse
    else:
        return response
    
if __name__ == "__main__":
    try:
        while True:
            print(FirstLayerDMM(input(">>> ")))
    except KeyboardInterrupt:
        print("\nExiting...")
