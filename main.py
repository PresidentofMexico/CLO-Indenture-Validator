import os
import pandas as pd
from dotenv import load_dotenv
from src.document_processor import DocumentProcessor
from src.compliance_engine import ComplianceEngine

# Load environment variables
load_dotenv()

def main():
    # --- CONFIGURATION ---
    # 1. Filename Configuration
    PDF_FILENAME = "Elmwood CLO 19 Second Reset - Final Offering Circular (as printed 10.03.25).pdf"
    STIPS_CSV_FILENAME = "structured_stips.csv"
    
    # 2. PAGE RANGE (Update this manually!)
    # Open your PDF, find the "Indenture" section, and enter the start/end pages.
    START_PAGE = 1   
    END_PAGE = 100   

    # Derived Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_PATH = os.path.join(BASE_DIR, "input", PDF_FILENAME)
    
    # UPDATED: Points to the CSV in the 'input' folder now
    STIPS_CSV_PATH = os.path.join(BASE_DIR, "input", STIPS_CSV_FILENAME)
    
    # --- EXECUTION ---
    print("--- CLO INDENTURE VALIDATOR STARTING ---")

    # 1. Initialize Engine
    if not os.path.exists(PDF_PATH):
        print(f"Error: PDF not found at {PDF_PATH}")
        print("Please check the filename in the 'input' folder.")
        return

    processor = DocumentProcessor(PDF_PATH)
    engine = ComplianceEngine()
    
    # 2. Load and Slice PDF
    try:
        processor.load_and_slice(START_PAGE, END_PAGE)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return
    
    # 3. Load Stipulations (Directly from CSV)
    if not os.path.exists(STIPS_CSV_PATH):
        print(f"Error: Stips CSV not found at {STIPS_CSV_PATH}")
        return

    try:
        stips_df = pd.read_csv(STIPS_CSV_PATH)
        print(f"Loaded {len(stips_df)} stipulations to check.")
    except Exception as e:
        print(f"Could not load stips CSV: {e}")
        return

    results = []

    # 4. The Analysis Loop
    print("\n--- BEGINNING ANALYSIS ---\n")
    for index, row in stips_df.iterrows():
        # Flexible column names in case your CSV headers vary
        category = row.get('Category') or row.get('category')
        requirement = row.get('Requirement') or row.get('requirement') or row.get('Description')
        
        if not category or not requirement:
            print(f"Skipping Row {index}: Missing 'Category' or 'Requirement' column.")
            continue
            
        print(f"Checking Stip {index+1}/{len(stips_df)}: [{category}]")
        
        # A. Route to relevant text
        relevant_text = processor.extract_section_by_category(category)
        
        # B. Analyze
        verdict = engine.evaluate_stipulation(requirement, category, relevant_text)
        
        # C. Store Result
        print(f"  -> Verdict: {verdict.get('status')}")
        results.append({
            "Category": category,
            "Stipulation": requirement,
            "Status": verdict.get("status"),
            "Evidence Quote": verdict.get("evidence_quote"),
            "Reasoning": verdict.get("reasoning"),
            "Discrepancy Details": verdict.get("discrepancy_details")
        })

    # 5. Generate Report
    results_df = pd.DataFrame(results)
    output_path = os.path.join(BASE_DIR, "output", "Compliance_Matrix.csv")
    results_df.to_csv(output_path, index=False)
    print(f"\nJob Complete. Report generated at: {output_path}")

if __name__ == "__main__":
    main()