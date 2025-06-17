from groq import Groq  # Importing the Groq library to use its API
from json import load, dump  # Importing functions to read and write JSON
import datetime  # Importing the datetime module for real-time operations
from dotenv import dotenv_values  # Importing dotenv_values to read .env variables
import os
# Load environment variables from the .env file.
env_vars = dotenv_values("Backend/.env")

# Retrieve specific environment variables for username, assistantname, and API key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY")
if not GroqAPIKey:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot.
System = f"""Hello, I am {Username}, "You are a highly accurate and knowledgeable chatbot named {Assistantname}. You have access to current system date and time, but not the live internet."
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
# A list of system instructions for the chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a JSON file.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)  # Load existing messages from the chat log.
except FileNotFoundError:
    # If the file doesn't exist, create an empty JSON file to store chat log.
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # Get the current date and time
    day = current_date_time.strftime("%A")       # Day of the week.
    date = current_date_time.strftime("%d")      # Day of the month.
    month = current_date_time.strftime("%B")     # Full month name.
    year = current_date_time.strftime("%Y")      # Year.
    hour = current_date_time.strftime("%H")      # Hour in 24-hour format.
    minute = current_date_time.strftime("%M")    # Minute.
    second = current_date_time.strftime("%S")    # Second.

    # Format the information into a string.
    data = "Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer='\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """

    try:
        # Load the existing chat log from the JSON file.
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Specify the AI model to use.
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer =""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer+=chunk.choices[0].delta.content

        Answer=Answer.replace("</s>","")
            # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log to the JSON file.
        with open(r"Data\ChatLog.json", "w") as f:
             dump(messages, f, indent=4)

    # Return the formatted response.
        return AnswerModifier(Answer=Answer)

    except Exception as e:
    # Handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Retry the query after resetting the log.

# Main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        print(ChatBot(user_input))


