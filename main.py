import os
import pandas as pd
from dotenv import load_dotenv
from src.document_processor import DocumentProcessor
from src.compliance_engine import ComplianceEngine

# Load environment variables
load_dotenv()

def main():
    # --- INPUT CONFIGURATION ---
    # In a real app, these would come from the UI/CLI args
    PDF_PATH = "input/Draft_Indenture_v3.pdf"
    STIPS_PATH = "input/structured_stips.csv" # Pre-processed stips
    START_PAGE = 146
    END_PAGE = 385
    
    # 1. Initialize Components
    if not os.path.exists(PDF_PATH):
        print(f"Error: File {PDF_PATH} not found. Please place a dummy PDF in input folder.")
        return

    processor = DocumentProcessor(PDF_PATH)
    engine = ComplianceEngine()
    
    # 2. Load and Slice PDF (The "Associate" Step)
    processor.load_and_slice(START_PAGE, END_PAGE)
    
    # 3. Load Stipulations
    # We assume columns: [Category, Requirement]
    try:
        stips_df = pd.read_csv(STIPS_PATH)
        print(f"Loaded {len(stips_df)} stipulations to check.")
    except Exception as e:
        print(f"Could not load stips CSV: {e}")
        return

    results = []

    # 4. The Analysis Loop
    for index, row in stips_df.iterrows():
        category = row['Category']
        requirement = row['Requirement']
        
        print(f"\nProcessing Stip {index+1}: [{category}] {requirement[:30]}...")
        
        # A. Route to relevant text
        relevant_text = processor.extract_section_by_category(category)
        
        # B. Analyze
        verdict = engine.evaluate_stipulation(requirement, category, relevant_text)
        
        # C. Store Result
        results.append({
            "Stipulation": requirement,
            "Category": category,
            "Status": verdict.get("status"),
            "Discrepancy Details": verdict.get("discrepancy_details"),
            "Reasoning": verdict.get("reasoning"),
            "Evidence": verdict.get("evidence_quote")
        })

    # 5. Generate Report
    results_df = pd.DataFrame(results)
    output_path = "output/Compliance_Matrix.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nJob Complete. Report generated at: {output_path}")

if __name__ == "__main__":
    main()
