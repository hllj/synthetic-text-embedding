import os
import time

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient():
    def __init__(self, model_name="gemini-1.5-flash"):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
        # Create the model
        # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
        self.generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }
    
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
    
    def generate(self, message):
        chat = self.model.start_chat(history=[])
    
        response = chat.send_message(
            message,
            safety_settings=self.safety_settings,
            generation_config=self.generation_config
        )
        return response.text