import fitz  # PyMuPDF
import re
from config.settings import SECTION_MAPPING

class DocumentProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = None
        self.full_text = ""

    def load_and_slice(self, start_page, end_page):
        """
        Loads the PDF and extracts text only from the specified page range.
        Note: PDF pages are 0-indexed in code, but 1-indexed for humans.
        """
        print(f"Loading PDF: {self.pdf_path} (Pages {start_page}-{end_page})...")
        self.doc = fitz.open(self.pdf_path)
        
        extracted_text = []
        
        # Safety check for page range
        total_pages = len(self.doc)
        if end_page > total_pages:
            end_page = total_pages
            
        for page_num in range(start_page - 1, end_page):
            page = self.doc.load_page(page_num)
            extracted_text.append(page.get_text())
            
        self.full_text = "\n".join(extracted_text)
        print(f"Extraction complete. {len(self.full_text)} characters loaded.")
        return self.full_text

    def extract_section_by_category(self, category):
        """
        Uses Regex patterns from config to pull specific Articles/Sections.
        """
        mapping = SECTION_MAPPING.get(category)
        
        if not mapping or not mapping["regex_pattern"]:
            print(f"No specific mapping for '{category}'. Returning full sliced text.")
            return self.full_text

        print(f"Scanning for section: {category}...")
        pattern = mapping["regex_pattern"]
        match = re.search(pattern, self.full_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            # Group 2 usually contains the content between the headers
            clean_content = match.group(0) 
            print(f"Found section for {category} ({len(clean_content)} chars).")
            return clean_content
        else:
            print(f"WARNING: Could not find section for {category}. Using full text fallback.")
            return self.full_text
