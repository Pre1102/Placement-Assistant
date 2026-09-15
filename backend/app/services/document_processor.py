import fitz  # PyMuPDF
import re

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> list[dict]:
        """
        Extracts text page by page from PDF file.
        Returns a list of dicts: [{"page_number": 1, "text": "..."}]
        """
        pages_content = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                raw_text = page.get_text("text")
                # Clean extra whitespace while keeping sentence structure
                cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
                if cleaned_text:
                    pages_content.append({
                        "page_number": page_num + 1,
                        "text": cleaned_text
                    })
            doc.close()
        except Exception as e:
            print(f"[DocumentProcessor] Error processing PDF {pdf_path}: {e}")
        return pages_content
