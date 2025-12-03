"""
CLO Compliance AI - Main Orchestrator
Coordinates document processing, compliance checking, and report generation
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent / 'config'))

# Import configuration
from settings import (
    REGEX_PATTERNS,
    COMPLIANCE_THRESHOLDS,
    DOCUMENT_SECTIONS,
    PROMPT_TEMPLATES,
    API_CONFIG,
    DEFAULT_PATHS,
    LOG_CONFIG
)

# Import modules
from document_processor import DocumentProcessor
from compliance_engine import ComplianceEngine
from data_loader import DataLoader

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['level']),
    format=LOG_CONFIG['format'],
    datefmt=LOG_CONFIG['date_format']
)
logger = logging.getLogger(__name__)


class CLOComplianceOrchestrator:
    """
    Main orchestrator for CLO compliance checking workflow.
    """
    
    def __init__(self):
        """Initialize the orchestrator and all components."""
        logger.info("Initializing CLO Compliance AI Orchestrator")
        
        # Initialize components
        self.doc_processor = DocumentProcessor(REGEX_PATTERNS)
        self.compliance_engine = ComplianceEngine(
            model=API_CONFIG['model'],
            temperature=API_CONFIG['temperature']
        )
        self.data_loader = DataLoader(
            input_dir=DEFAULT_PATHS['input_dir'],
            output_dir=DEFAULT_PATHS['output_dir']
        )
        
        logger.info("All components initialized successfully")
    
    def run_compliance_check(
        self,
        pdf_path: str,
        stips_path: str = None
    ) -> Dict[str, any]:
        """
        Run the complete compliance checking workflow.
        
        Args:
            pdf_path: Path to the PDF document to check
            stips_path: Path to stipulations file (optional)
            
        Returns:
            Dictionary with compliance results and summary
        """
        logger.info("=" * 60)
        logger.info("Starting CLO Compliance Check Workflow")
        logger.info("=" * 60)
        
        # Step 1: Load stipulations
        logger.info("\n[Step 1] Loading stipulations...")
        stips = self.data_loader.load_stips(stips_path)
        logger.info(f"Loaded {len(stips)} stipulations")
        
        # Validate stips format
        if not self.data_loader.validate_stips_format(stips):
            logger.error("Stipulations format validation failed")
            return {'error': 'Invalid stipulations format'}
        
        # Step 2: Process PDF document
        logger.info("\n[Step 2] Processing PDF document...")
        document_text = self.doc_processor.load_pdf(pdf_path)
        
        # Extract relevant sections
        sections = self.doc_processor.extract_sections(
            document_text,
            DOCUMENT_SECTIONS
        )
        logger.info(f"Extracted {len(sections)} sections from document")
        
        # Step 3: Run compliance checks
        logger.info("\n[Step 3] Running compliance checks...")
        results = []
        
        for i, stip in enumerate(stips, 1):
            logger.info(f"Checking stipulation {i}/{len(stips)}: {stip.get('description', 'N/A')[:50]}...")
            
            # Find relevant section
            section_name = stip.get('section', DOCUMENT_SECTIONS[0])
            section_text = sections.get(section_name, document_text[:1000])
            
            # Check compliance
            check_result = self.compliance_engine.check_compliance(
                document_section=section_text,
                rule=stip.get('description', ''),
                prompt_template=PROMPT_TEMPLATES['compliance_check']
            )
            
            # Add metadata to result
            result = {
                'stip_id': stip.get('id', ''),
                'category': stip.get('category', ''),
                'description': stip.get('description', ''),
                'section': section_name,
                **check_result
            }
            results.append(result)
        
        # Step 4: Generate summary
        logger.info("\n[Step 4] Generating summary...")
        summary = self.data_loader.create_summary_report(results)
        
        # Step 5: Save report
        logger.info("\n[Step 5] Saving compliance report...")
        report_path = self.data_loader.save_compliance_report(results)
        logger.info(f"Report saved to: {report_path}")
        
        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("COMPLIANCE CHECK COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total Checks: {summary['total_checks']}")
        logger.info(f"Passed: {summary['passed']}")
        logger.info(f"Failed: {summary['failed']}")
        logger.info(f"Unclear: {summary['unclear']}")
        logger.info("=" * 60)
        
        return {
            'results': results,
            'summary': summary,
            'report_path': report_path
        }
    
    def extract_covenants(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Extract financial covenants from a document.
        
        Args:
            pdf_path: Path to the PDF document
            
        Returns:
            List of extracted covenants
        """
        logger.info("Extracting covenants from document...")
        
        # Load document
        document_text = self.doc_processor.load_pdf(pdf_path)
        
        # Extract covenants section
        sections = self.doc_processor.extract_sections(
            document_text,
            ['Covenants', 'Financial Covenants']
        )
        covenant_text = sections.get('Covenants', document_text)
        
        # Use LLM to extract covenants
        covenants = self.compliance_engine.extract_covenants(
            covenant_text,
            PROMPT_TEMPLATES['covenant_extraction']
        )
        
        logger.info(f"Extracted {len(covenants)} covenants")
        return covenants


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='CLO Compliance AI - Automated compliance checking for CLO documents'
    )
    parser.add_argument(
        '--pdf',
        type=str,
        help='Path to PDF document to check'
    )
    parser.add_argument(
        '--stips',
        type=str,
        help='Path to stipulations file (Excel/CSV)'
    )
    parser.add_argument(
        '--extract-covenants',
        action='store_true',
        help='Extract covenants from document instead of compliance check'
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = CLOComplianceOrchestrator()
    
    if args.extract_covenants:
        if not args.pdf:
            print("Error: --pdf argument required for covenant extraction")
            sys.exit(1)
        
        # Extract covenants
        covenants = orchestrator.extract_covenants(args.pdf)
        
        # Print results
        print("\nExtracted Covenants:")
        print("=" * 60)
        for i, covenant in enumerate(covenants, 1):
            print(f"\n{i}. {covenant.get('name', 'Unknown')}")
            print(f"   Threshold: {covenant.get('threshold', 'N/A')}")
            print(f"   Condition: {covenant.get('condition', 'N/A')}")
    
    else:
        if not args.pdf:
            print("Error: --pdf argument required")
            print("\nUsage examples:")
            print("  python main.py --pdf input/indenture.pdf")
            print("  python main.py --pdf input/indenture.pdf --stips input/stips.xlsx")
            print("  python main.py --pdf input/indenture.pdf --extract-covenants")
            sys.exit(1)
        
        # Run compliance check
        results = orchestrator.run_compliance_check(
            pdf_path=args.pdf,
            stips_path=args.stips
        )
        
        if 'error' in results:
            print(f"\nError: {results['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
