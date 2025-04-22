import os
import groq
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class GroqPCOSAdvisor:
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"
        
    def get_response(self, user_input: str, context: Optional[str] = None) -> str:
        """Generates PCOS-focused responses via Groq API"""
        messages = [
            {
                "role": "system",
                "content": """You're a PCOS health advisor. Follow these rules:
                1. Medical accuracy is critical
                2. Use simple language and 1-2 emojis
                3. Keep responses under 50 words
                4. End with a question or CTA"""
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {user_input}" if context else user_input
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            top_p=0.9
        )
        
        return self._clean_response(response.choices[0].message.content)

    def _clean_response(self, response: str) -> str:
        """Removes any redundant prefixes/suffixes"""
        return response.split("Question:")[-1].strip()
    
advisor = GroqPCOSAdvisor()
print(advisor.get_response(
    "What's the best exercise for insulin resistance in PCOS?",
    context="User is overweight with prediabetes"
))