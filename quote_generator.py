import os
from openai import AsyncOpenAI
import random

async def generate_hinglish_quote(mood: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Fallback quotes in case API is not configured or fails
    fallback_quotes = {
        "sad": [
            "Log badal jaate hain, yaadein wahin reh jaati hain.",
            "Dil toota hai, par umeed abhi baaki hai.",
            "Akele pan ki aadat si ho gayi hai ab."
        ],
        "romantic": [
            "Tum meri wo khushi ho, jiska mujhe hamesha se intezaar tha.",
            "Ishq woh nahi jo tujhe mera kar de, ishq woh hai jo tujhe kisi aur ka na hone de.",
            "Teri aankhon mein mujhe apna kal dikhta hai."
        ],
        "real": [
            "Waqt sabki asliyat dikha deta hai, bas thoda sabr rakho.",
            "Jo log tumhari value nahi karte, unke liye time waste mat karo.",
            "Success is the best revenge. Mehnat karte raho."
        ],
        "deep": [
            "Zindagi mein kuch dard aise hote hain, jo hum kisi ko samjha nahi sakte.",
            "Samundar ki gehrai toh sabko dikhti hai, par dil ki gehrai koi nahi samajhta.",
            "Khamoshi mein bhi bohot kuch chupa hota hai, bas sunne wala chahiye."
        ]
    }
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("Warning: OPENAI_API_KEY is not set. Using fallback quotes.")
        mood_lower = mood.lower()
        if mood_lower in fallback_quotes:
            return random.choice(fallback_quotes[mood_lower])
        else:
            return random.choice(fallback_quotes["real"])

    try:
        client = AsyncOpenAI(api_key=api_key)
        
        prompt = f"""
        Write a short (1-2 lines), emotional, relatable, and Gen Z style quote in Hinglish (a mix of Hindi and English) based on the mood: '{mood}'.
        Do not use any hashtags or emojis.
        Do not wrap the text in quotes.
        Make it profound and perfect for an Instagram post. Avoid cringe.
        """
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", # Can be changed to gpt-4 if preferred
            messages=[
                {"role": "system", "content": "You are an expert Instagram content creator who writes deep, relatable Hinglish quotes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=60
        )
        
        quote = response.choices[0].message.content.strip()
        # Remove any surrounding quotes if the AI added them despite instructions
        quote = quote.strip('"\'')
        return quote
        
    except Exception as e:
        print(f"Error generating quote with OpenAI: {e}")
        mood_lower = mood.lower()
        if mood_lower in fallback_quotes:
            return random.choice(fallback_quotes[mood_lower])
        else:
            return random.choice(fallback_quotes["real"])
