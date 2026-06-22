# This program will be responsible for reading PDF and TXT files from the documents/ folder

# PyPDF2 is used for extracting text from PDF files, while standard file I/O is used for reading plain text files. The extracted text is then cleaned and formatted for use in the chatbot's knowledge base. This allows the chatbot to provide accurate and up-to-date information based on the content available in the documents.

# The document loading process is done in 3 steps:
# 1. Check if the documents/ folder exists. If not, create it and prompt the user to add PDF/TXT files.
# 2. Iterate through all files in the documents/ folder, and for each file:
#    - If it's a PDF, use PyPDF2 to extract text from each page.
#    - If it's a TXT, read the content directly.
# 3. Combine the extracted text from all documents and return it for further processing, such as feeding into an AI model for question-answering or summarization tasks.


import os
import PyPDF2

DOCUMENTS_FOLDER = "documents"

def load_pdf(filepath):
    """Extract text from a PDF file."""
    try:
        print(f"  Reading PDF: {os.path.basename(filepath)}...")
        text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n[Page {page_num + 1}]\n{page_text}"

        if not text.strip():
            return f"[{os.path.basename(filepath)}: No readable text found]\n"

        return text

    except Exception as e:
        print(f"  Could not read {filepath}: {e}")
        return f"[{os.path.basename(filepath)}: Could not be read]\n"


def load_txt(filepath):
    """Read a plain text file."""
    try:
        print(f"  Reading TXT: {os.path.basename(filepath)}...")
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"  Could not read {filepath}: {e}")
        return f"[{os.path.basename(filepath)}: Could not be read]\n"


def load_all_documents():
    """Load all PDFs and TXTs from the documents/ folder."""

    # Create folder if it doesn't exist yet
    if not os.path.exists(DOCUMENTS_FOLDER):
        os.makedirs(DOCUMENTS_FOLDER)
        print(f"   Created '{DOCUMENTS_FOLDER}/' folder.")
        print(f"   Add your PDF/TXT files there and rerun.\n")
        return ""

    files = os.listdir(DOCUMENTS_FOLDER)
    if not files:
        print(f"   No documents found in '{DOCUMENTS_FOLDER}/'.")
        return ""

    print(f"\n   Loading documents from '{DOCUMENTS_FOLDER}/'...")
    all_text = []

    for filename in files:
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        ext = filename.lower().split(".")[-1]

        if ext == "pdf":
            text = load_pdf(filepath)
            label = filename.replace(".pdf", "").replace("_", " ").upper()
            all_text.append(f"=== DOCUMENT: {label} ===\n{text}\n")

        elif ext == "txt":
            text = load_txt(filepath)
            label = filename.replace(".txt", "").replace("_", " ").upper()
            all_text.append(f"=== DOCUMENT: {label} ===\n{text}\n")

        else:
            print(f"  Skipping unsupported file: {filename}")

    print("  Document loading complete.\n")
    return "\n".join(all_text)


# Run standalone to test
if __name__ == "__main__":
    result = load_all_documents()
    print(result[:2000] if result else "No documents loaded.")