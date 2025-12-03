"""
Centralized Regex Patterns and Configuration Settings
The "CLO Logic" - Contains all regex patterns and compliance rules
"""

import re

# Regex patterns for CLO document parsing
REGEX_PATTERNS = {
    # Common CLO document patterns
    'section_header': r'^(?:SECTION|Article)\s+(\d+(?:\.\d+)*)\s*[-\u2013\u2014]\s*(.+?)$',
    'covenant_trigger': r'(?:if|when|in the event that)\s+([^,]+?)\s+(?:exceeds?|falls? below|is less than|is greater than)\s+(\d+(?:\.\d+)?%?)',
    'percentage': r'(\d+(?:\.\d+)?)\s*%',
    'dollar_amount': r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
    'date_pattern': r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',
    
    # CLO-specific patterns
    'oc_ratio': r'(?:overcollateralization|o/c)\s+(?:ratio|test)\s*(?:of)?\s*(\d+(?:\.\d+)?%?)',
    'ic_ratio': r'(?:interest coverage|i/c)\s+(?:ratio|test)\s*(?:of)?\s*(\d+(?:\.\d+)?%?)',
    'concentration_limit': r'concentration\s+limit\s*(?:of)?\s*(\d+(?:\.\d+)?%?)',
    'rating_threshold': r'(?:rated|rating)\s+(?:of\s+)?([A-Z][a-z]*[-+]?)',
}

# Compliance thresholds
COMPLIANCE_THRESHOLDS = {
    'min_oc_ratio': 100.0,  # Minimum overcollateralization ratio (%)
    'min_ic_ratio': 100.0,  # Minimum interest coverage ratio (%)
    'max_concentration': 10.0,  # Maximum single asset concentration (%)
    'min_rating': 'BBB-',  # Minimum acceptable rating
}

# Document sections to extract
DOCUMENT_SECTIONS = [
    'Definitions',
    'Covenants',
    'Events of Default',
    'Collateral',
    'Payment Priority',
    'Coverage Tests',
    'Concentration Limits',
    'Rating Requirements',
]

# LLM prompt templates
PROMPT_TEMPLATES = {
    'compliance_check': """
You are a CLO compliance expert. Analyze the following document section and determine if it complies with the given rule.

Document Section:
{document_section}

Rule/Stipulation:
{rule}

Please provide:
1. Compliance Status: PASS/FAIL/UNCLEAR
2. Explanation: Brief reasoning for your determination
3. Relevant Excerpts: Quote specific text from the document that supports your conclusion
""",
    
    'covenant_extraction': """
Extract all financial covenants and their thresholds from the following text:

{text}

Format your response as:
- Covenant Name: [name]
  Threshold: [value]
  Condition: [trigger condition]
""",
}

# API Configuration
API_CONFIG = {
    'model': 'gpt-4',
    'temperature': 0.1,  # Lower temperature for more consistent compliance checking
    'max_tokens': 2000,
}

# File paths
DEFAULT_PATHS = {
    'input_dir': 'input/',
    'output_dir': 'output/',
    'stips_file': 'input/stips.xlsx',
    'report_output': 'output/compliance_report.xlsx',
}

# Logging configuration
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
}
