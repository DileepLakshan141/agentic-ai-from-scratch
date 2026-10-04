import json
import re
from pydantic import BaseModel, Field
from typing import List

class SentimentAnalysis(BaseModel):
    sentiment: str = Field(description="තක්සේරුව: 'POSITIVE', 'NEGATIVE', හෝ 'NEUTRAL'")
    confidence_score: float = Field(description="විශ්වාසනීයත්ව මට්ටම 0.0 සිට 1.0 දක්වා")
    key_topics: List[str] = Field(description="ඡේදයේ සඳහන් වන ප්‍රධාන මාතෘකා ලැයිස්තුව")
    summary: str = Field(description="සිංහලෙන් සපයා ඇති සාරාංශය")


json_schema = SentimentAnalysis.model_json_schema()


system_prompt = f"""
You are an expert AI Data Extractor. 
Extract information from the provided text and output ONLY a JSON object matching this schema:

{json.dumps(json_schema, indent=2)}

Do NOT include any markdown formatting, thoughts, or extra text. Output ONLY pure JSON.
"""

user_text = "I really loved using Next.js and NestJS for building my web platform! The setup was smooth, though the database migrations took a bit of time."

raw_llm_output = """
{
    "sentiment": "POSITIVE",
    "confidence_score": 0.92,
    "key_topics": ["Next.js", "NestJS", "Database Migrations"],
    "summary": "Next.js සහ NestJS භාවිතය ඉතා පහසු වූ අතර Database migration සඳහා මඳ වේලාවක් ගතවිය."
}
"""

try:
    # Regex extract (Safety measure)
    json_str = re.search(r"\{.*\}", raw_llm_output, re.DOTALL).group(0)
    
    # Validation & Instantiation
    result = SentimentAnalysis.model_validate_json(json_str)
    
    print("✅ Parsed Successfully!")
    print(f"Sentiment: {result.sentiment}")
    print(f"Topics: {result.key_topics}")
    print(f"Confidence: {result.confidence_score * 100}%")

except Exception as e:
    print(f"❌ Validation Failed: {e}")