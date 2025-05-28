import argparse
import sys
import os
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

def extract_text_from_pdf(pdf_path, output_txt_path):
    """
    Extracts text from a single PDF file and saves it to a .txt file.

    Args:
        pdf_path (str): The path to the input PDF file.
        output_txt_path (str): The path to save the extracted text.
    
    Returns:
        bool: True if text extraction was successful, False otherwise.
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            
            # Check if the PDF is encrypted (password-protected)
            if reader.is_encrypted:
                # Attempt to decrypt with an empty password (common for non-password protected but encrypted files)
                # More complex password handling would require user input or a password list
                try:
                    reader.decrypt('') 
                except Exception as decrypt_error:
                     # If decryption fails (e.g. needs a password)
                    sys.stderr.write(f"Error: Could not decrypt '{pdf_path}'. It might be password-protected. Error: {decrypt_error}\n")
                    return False

            text_content = []
            # Iterate through each page and extract text
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text_content.append(page.extract_text())
            
            # Join the text from all pages
            full_text = "\n".join(text_content)
            
            # Save the extracted text to the output file
            with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(full_text)
            
            print(f"Successfully extracted text from '{pdf_path}' to '{output_txt_path}'")
            return True

    except FileNotFoundError:
        sys.stderr.write(f"Error: PDF file not found at '{pdf_path}'\n")
        return False
    except PdfReadError as e:
        # This can catch various issues, including some forms of password protection or corrupted files
        sys.stderr.write(f"Error: Could not read PDF '{pdf_path}'. It may be password-protected or corrupted. Details: {e}\n")
        return False
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred while processing '{pdf_path}': {e}\n")
        return False

def main():
    """
    Main function to handle command-line arguments and orchestrate PDF text extraction.
    """
    parser = argparse.ArgumentParser(
        description="Extracts text from PDF files and saves it to .txt files.",
        usage="%(prog)s <pdf_file1.pdf> [pdf_file2.pdf ...]"
    )
    parser.add_argument(
        "pdf_files",
        metavar="pdf_file.pdf",
        nargs='*',  # Allows zero or more arguments
        help="One or more PDF files to process."
    )
    
    args = parser.parse_args()
    
    if not args.pdf_files:
        # If no PDF files are provided, print the usage message.
        # argparse default help message is quite good, or we can print custom.
        # For this task, printing parser's help is fine for usage.
        parser.print_help(sys.stdout)
        sys.exit(0) # Exit gracefully
        
    processed_count = 0
    error_count = 0

    for pdf_path in args.pdf_files:
        if not pdf_path.lower().endswith('.pdf'):
            sys.stderr.write(f"Warning: Skipping non-PDF file '{pdf_path}'\n")
            continue

        # Construct the output .txt file path
        base_name = os.path.splitext(pdf_path)[0]
        output_txt_path = base_name + ".txt"
        
        if extract_text_from_pdf(pdf_path, output_txt_path):
            processed_count += 1
        else:
            error_count += 1
            
    print(f"\nProcessing complete. Successfully processed {processed_count} files.")
    if error_count > 0:
        print(f"Encountered errors with {error_count} files.")

if __name__ == "__main__":
    main()
```
