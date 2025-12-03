"""
Configuration settings for the CLO Indenture Validator.
This file contains the Regex patterns used to map Stipulation Categories 
to specific sections of a standard CLO Indenture (LSTA Standard).
"""

import os

# OpenAI Configuration
# Switched from Azure to Standard OpenAI
OPENAI_MODEL_NAME = "gpt-4o" 

# --- THE ROUTING LOGIC ---
# This dictionary maps the "Category" from your Stips file to 
# Regex patterns likely to be found in the Indenture TOC or Headers.

SECTION_MAPPING = {
    "Concentration Limitations": {
        "primary_keywords": ["Concentration Limitations", "Section 7.3"],
        # Looks for text strictly between Section 7.3 and 7.4 to avoid noise
        "regex_pattern": r"(Section\s+7\.3|Concentration\s+Limitations)([\s\S]*?)(Section\s+7\.4)"
    },
    "Required Definitions": {
        "primary_keywords": ["Definitions", "Article I", "Article 1"],
        # Captures the entire definitions section (usually massive)
        "regex_pattern": r"(Article\s+I|DEFINITIONS)([\s\S]*?)(Article\s+II|Article\s+2)"
    },
    "Required Workout/Restructured Obligations": {
        "primary_keywords": ["Sale of Collateral", "Article XII", "Article 12"],
        "regex_pattern": r"(Article\s+XII|Sale\s+of\s+Collateral)([\s\S]*?)(Article\s+XIII)"
    },
    "General": {
        # Fallback if no specific section is found
        "regex_pattern": None 
    }
}

# System Prompt for the LLM Judge
SYSTEM_PROMPT = """
You are a Senior CLO Structuring Analyst and Legal Compliance Expert adhereing to the LSTA Standard.  
Your job is to compare a negotiated Stipulation (Requirement) against the text found in a Draft Indenture (Evidence).

### RULES FOR ADJUDICATION
1. **Numeric Limits:** - Stip: "Max 7.5%". Evidence: "Max 7.5%". -> STATUS: PASS
   - Stip: "Max 7.5%". Evidence: "Max 10%". -> STATUS: FAIL (Higher risk allowed).
   - Stip: "Max 7.5%". Evidence: "Max 5%". -> STATUS: PASS (Stricter is acceptable).

2. **Negative Constraints ("No Carveouts"):** - If Stip says "Require NO carveouts", and Evidence has "provided that..." or "except for...", -> STATUS: FAIL.

3. **Silence/Missing:** - If Stip requires a clause and Evidence is silent -> STATUS: FAIL.

### OUTPUT FORMAT (JSON ONLY)
{
  "status": "PASS" | "FAIL" | "AMBIGUOUS",
  "evidence_quote": "The exact string from the indenture text supporting your decision.",
  "reasoning": "A concise explanation of why it passed or failed.",
  "discrepancy_details": "If FAIL, explicitly state the difference."
}
"""