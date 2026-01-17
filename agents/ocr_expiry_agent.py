from langchain_ollama import OllamaLLM
from datetime import datetime

def ocr_expiry_agent(extracted_text, detected_expiry_date, food_status):
    """
    AI agent that analyzes OCR-extracted text and provides food safety recommendations.
    Uses Ollama for reasoning and recommendations.
    """
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    prompt = f"""You are a food waste prevention assistant.
    
You receive text extracted from food labels using OCR (text recognition only).
Based on this information, provide practical food safety advice.

EXTRACTED TEXT FROM LABEL:
{extracted_text}

DETECTED EXPIRY DATE: {detected_expiry_date if detected_expiry_date else 'Not found in text'}
FOOD STATUS: {food_status}
CURRENT DATE: {current_date}

Please provide:
1. A brief explanation of the expiry status
2. Is it safe to consume?
3. What should the user do?
4. How to use this food to reduce waste?

Keep recommendations practical and safety-focused.
If expiry date is missing or unclear, advise caution."""
    
    return llm.invoke(prompt)
