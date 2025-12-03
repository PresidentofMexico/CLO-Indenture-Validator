import json
import os
from openai import AzureOpenAI
from config.settings import SYSTEM_PROMPT

class ComplianceEngine:
    def __init__(self):
        # Initialize Azure OpenAI Client
        # Assumes env variables are set: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

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
        
        (Note: Text limited to 15k chars for token optimization if massive definition)
        """
        # Note: In production, you'd want a token counter here to handle massive definition sections
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
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
