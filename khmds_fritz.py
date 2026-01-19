#Legacy solution to the extraction problem via text
#The problem was solved via pypdf annotations
import sys
import re
import fitz  # PyMuPDF
from typing import Optional

# Regex to identify the digital signature block
SIGNATURE_PATTERN = (
    r"Ministry of\s+Digital\s+Governance\s+Digitally signed by.*?Location:\s*Athens"
)


def extract_contract_id(pdf_path: str) -> Optional[str]:
    """
    Opens the PDF, sanitizes the text by removing the signature, and returns the ID.
    """
    try:
        # Use context manager for safe file handling
        with fitz.open(pdf_path) as doc:
            if len(doc) == 0:
                raise ValueError("PDF file is empty.")

            # Extract text from the first page
            text = doc[0].get_text("text")

            # Remove the digital signature block to avoid parsing errors
            clean_text = re.sub(
                SIGNATURE_PATTERN, "", text, flags=re.DOTALL | re.IGNORECASE
            )

            # Tokenize and extract the target ID (2nd to last element)
            tokens = clean_text.split()

            if len(tokens) < 2:
                return None

            return tokens[-2].strip()

    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    # Ensure correct usage
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]

    result = extract_contract_id(pdf_file)

    if result:
        print(result)
    else:
        print("ID not found.")
        sys.exit(1)
