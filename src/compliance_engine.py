import json
import os
from openai import OpenAI
from config.settings import SYSTEM_PROMPT, OPENAI_MODEL_NAME

class ComplianceEngine:
    def __init__(self):
        # Initialize Standard OpenAI Client
        # It automatically looks for "OPENAI_API_KEY" in environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

        self.client = OpenAI(api_key=api_key)
        self.model = OPENAI_MODEL_NAME

    def evaluate_stipulation(self, stip_text, category, evidence_text):
        """
        Sends the Stipulation + Evidence to the LLM for a verdict.
        """
        user_message = f"""
        --- STIPULATION INFO ---
        CATEGORY: {category}
        REQUIREMENT: "{stip_text}"
        
        --- EVIDENCE FROM INDENTURE ---
        (Extracted Text Segment):
        {evidence_text[:15000]} 
        
        (Note: Text limited to 15k chars for token optimization)
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"},
                temperature=0 # Deterministic output is key for compliance
            )
            
            result_json = json.loads(response.choices[0].message.content)
            return result_json

        except Exception as e:
            print(f"Error evaluating stip: {e}")
            return {
                "status": "ERROR",
                "evidence_quote": "N/A",
                "reasoning": f"System Error: {str(e)}",
                "discrepancy_details": "See logs"
            }