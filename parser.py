import fitz
import os

def parse_pdf(pdf_path):
    doc=fitz.open(pdf_path)
    full_text=""

    for page_num, page in enumerate(doc):
        text=page.get_text()
        full_text += f"\n--- Page {page_num + 1} ---\n"
        full_text += text
    doc.close()
    return full_text

if __name__ == "__main__":
    text=parse_pdf("arrays.pdf")
    print(text[:500])
    print(f"\n total characters extracted:{len(text)}")
