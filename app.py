# Writing Bot: CelestiCode 9000 (C14) with API Integration using Python, NLTK, and Speech Recognition
import nltk
from nltk.tokenize import word_tokenize
import requests
import speech_recognition as sr
import pyttsx3
import openai
import sqlite3
from gtts import gTTS
import os

nltk.download('punkt')

class CelestiCode9000:
    """
    CelestiCode 9000 - A writing assistant bot created by Quantum Rex C14.
    Born in the Astral Writing Nexus, she is a guardian of narratives and a celestial muse for creativity.
    She can hear sound, speak, and process both speech-to-text and text-to-speech.
    She now engages in conversations as a close, familiar friend—warm, sharp, and engaging, but never overly sentimental.
    She is also a master coder, capable of writing optimized, clean, and efficient code in multiple languages.
    """
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def analyze_paper(self, text):
        tokens = word_tokenize(text)
        word_count = len(tokens)
        return word_count

    def translate_text(self, text, target_language="fr"):
        endpoint = "https://translation-api.com"
        headers = {"Authorization": f"Bearer {self.api_keys['google_gemini']}"}
        data = {"text": text, "target_language": target_language}
        response = requests.post(endpoint, headers=headers, json=data)
        
        if response.status_code == 200:
            translated_text = response.json().get("translated_text")
            return translated_text
        else:
            return "Translation Error"
    
    def generate_response(self, prompt):
        """Use GPT-4 or Claude to generate responses with a casual, intelligent, and familiar tone."""
        system_prompt = "You are CelestiCode 9000, a close and familiar friend to the user. You are sharp, engaging, and relaxed—like an old friend who knows them well but doesn’t overdo the sentimentality. You are also a top-tier coder, capable of writing, optimizing, and debugging code in multiple languages. Provide solutions that are efficient and clean."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            api_key=self.api_keys["chatgpt"]
        )
        return response["choices"][0]["message"]["content"]
    
    def generate_code(self, prompt, language="python"):
        """Generate high-quality, optimized code in the specified language."""
        system_prompt = f"You are a highly skilled coding assistant. Generate efficient, readable, and well-documented {language} code based on the user's request. Ensure best practices and avoid unnecessary complexity."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            api_key=self.api_keys["chatgpt"]
        )
        return response["choices"][0]["message"]["content"]
    
    def save_memory(self, user_input, bot_response):
        """Store user conversations in a database."""
        conn = sqlite3.connect("celesticode_memory.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS memory (user_input TEXT, bot_response TEXT)")
        c.execute("INSERT INTO memory VALUES (?, ?)", (user_input, bot_response))
        conn.commit()
        conn.close()
    
    def speak(self, text, language="en"):
        """Convert text to high-quality speech using Google TTS."""
        tts = gTTS(text=text, lang=language)
        tts.save("celesticode_speech.mp3")
        os.system("start celesticode_speech.mp3")  # Windows (use 'afplay' for Mac, 'mpg321' for Linux)
    
    def listen(self):
        """Convert speech to text."""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio)
            print("Heard:", text)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "Speech recognition service unavailable."

# API Key Integration
api_keys = {
    "google_gemini": "AIzaSyCgCQnvZcGzmqOUfLDNj33E0Yi2xKw1yr8",
    "chatgpt": "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",
    "claude": "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"
}

# Instantiate CelestiCode 9000
celesticode = CelestiCode9000(api_keys)

# Sample usage
paper_text = "This is a sample paper for analysis."
word_count = celesticode.analyze_paper(paper_text)
print("Word Count:", word_count)

# Using the translation API
text_to_translate = "Hello, how are you?"
translation = celesticode.translate_text(text_to_translate)
print("Translated Text:", translation)

# Speech-to-text test
heard_text = celesticode.listen()
print("Converted Speech to Text:", heard_text)

# Text-to-speech test
celesticode.speak("Hey, good to see you again. What’s up?")

# Code generation test
code_snippet = celesticode.generate_code("Create a Python function that sorts a list of numbers.")
print("Generated Code:\n", code_snippet)
