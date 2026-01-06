import json
from openai import AsyncOpenAI
from typing import List, Dict
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_ai_response(messages_history: List[Dict[str, str]]) -> dict:
    """
    Calls the OpenAI API with the given message history and returns the structured JSON response.
    """
    completion = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages_history,
        response_format={"type": "json_object"}
    )
    
    ai_response_str = completion.choices[0].message.content
    try:
        ai_data = json.loads(ai_response_str)
    except json.JSONDecodeError:
        # Fallback if the AI doesn't return valid JSON
        ai_data = {"reply": ai_response_str}
        
    return ai_data

async def ask_ai(prompt: str) -> str:
    """
    Sends a direct prompt to the AI and returns the text response. Used for scoring.
    """
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that provides numerical scores based on context."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content