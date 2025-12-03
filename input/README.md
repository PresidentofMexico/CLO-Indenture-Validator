# Input Directory

This directory is for placing your input files:

- **PDF Documents**: Place CLO indenture documents and related PDFs here
- **Stipulations**: Upload your stipulations file (stips.xlsx or stips.csv)
- **Metadata**: Any supporting metadata files

## Example Files

You can create files like:
- `indenture.pdf` - Your CLO indenture document
- `stips.xlsx` - Excel file with compliance stipulations
- `pdf_metadata.xlsx` - Metadata about your documents

## Stipulations Format

Your stipulations Excel/CSV file should have these columns:
- `id` - Unique identifier for the stipulation
- `category` - Category (e.g., "Coverage Test", "Concentration Limit")
- `description` - The rule or requirement to check
- `section` - Document section where this applies (optional)
