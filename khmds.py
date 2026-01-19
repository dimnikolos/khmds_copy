import sys
import re
import pypdf
import pyperclip
from typing import Optional

# Pre-compile the regex for better performance if run in loops/batches
CONTRACT_PATTERN = re.compile(r"\d{2}(REQ|AWRD|PROC|SYMV|PAY)\d+")


def extract_contract_id(pdf_path: str) -> Optional[str]:
    """
    Scans the annotations of the first page for a specific contract ID pattern.
    Returns the ID if found, otherwise None.
    """
    try:
        reader = pypdf.PdfReader(pdf_path)

        # Ensure the PDF has pages
        if len(reader.pages) == 0:
            print("Error: PDF is empty.", file=sys.stderr)
            return None

        first_page = reader.pages[0]

        # Check if annotations exist
        if "/Annots" not in first_page:
            return None

        # Iterate through annotations
        for annot_ref in first_page["/Annots"]:
            # .get_object() ensures we resolve the IndirectObject safely
            annot = annot_ref.get_object()

            # Defensive coding: Check structure before accessing
            if "/AP" in annot and "/N" in annot["/AP"]:
                # Get raw bytes
                ap_stream = annot["/AP"]["/N"].get_object().get_data()

                # Decode bytes to string (Latin-1 is standard for PDF internal names)
                # We use errors='ignore' to handle binary garbage safely
                text_content = ap_stream.decode("latin-1", errors="ignore")

                # Search for the pattern
                match = CONTRACT_PATTERN.search(text_content)
                if match:
                    return match.group(0)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return None

    return None


def main():
    # 1. Argument Validation
    if len(sys.argv) < 2:
        print("Usage: python script.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]

    # 2. Execution
    result = extract_contract_id(pdf_file)

    # 3. User Feedback & Action
    if result:
        pyperclip.copy(result)
        print(f"✅ Success! Copied to clipboard: {result}")
    else:
        print("⚠️ No contract ID found in annotations.")
        sys.exit(1)


if __name__ == "__main__":
    main()
