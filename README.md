# PDF Text Extractor

This script, `extract_pdf_text.py`, extracts text content from a list of PDF files and saves the text from each PDF into a separate `.txt` file.

## Features

-   Extracts text from multiple PDF files.
-   Saves output to individual `.txt` files (e.g., `example.pdf` -> `example.txt`).
-   Handles errors gracefully for individual files (e.g., password-protected or corrupted PDFs) and continues processing other files.
-   Uses the `PyPDF2` library.

## Requirements

-   Python 3.x
-   PyPDF2

## Installation

1.  **Clone the repository (if applicable) or ensure `extract_pdf_text.py` and `requirements.txt` are in the same directory.**

2.  **Install the necessary Python libraries:**
    Open your terminal or command prompt and navigate to the directory containing `requirements.txt`. Then run:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the script, use the following command in your terminal or command prompt:

```bash
python extract_pdf_text.py pdf_file1.pdf [pdf_file2.pdf ...]
```

**Arguments:**

-   `pdf_file1.pdf`: Path to the first PDF file you want to process.
-   `[pdf_file2.pdf ...]`: (Optional) Paths to any additional PDF files, separated by spaces.

**Example:**

```bash
python extract_pdf_text.py documentA.pdf "My Document B.pdf" report.pdf
```

This will:
-   Extract text from `documentA.pdf` and save it to `documentA.txt`.
-   Extract text from `My Document B.pdf` and save it to `My Document B.txt`.
-   Extract text from `report.pdf` and save it to `report.txt`.

If any PDF is password-protected or corrupted, an error message will be printed for that specific file, and the script will proceed with the next one.
