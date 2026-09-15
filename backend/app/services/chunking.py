import uuid

class TextChunker:
    @staticmethod
    def chunk_document(
        pages: list[dict],
        document_id: int,
        document_name: str,
        category: str,
        company: str = None,
        chunk_size: int = 400,
        overlap: int = 50
    ) -> list[dict]:
        """
        Splits page text into overlapping chunks and attaches full metadata.
        """
        chunks = []
        
        for page in pages:
            page_num = page["page_number"]
            text = page["text"]
            
            if len(text) <= chunk_size:
                chunk_id = f"doc_{document_id}_p{page_num}_{uuid.uuid4().hex[:8]}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "document_id": document_id,
                    "document_name": document_name,
                    "page_number": page_num,
                    "category": category,
                    "company": company,
                    "text": text
                })
            else:
                start = 0
                while start < len(text):
                    end = start + chunk_size
                    chunk_text = text[start:end].strip()
                    
                    if chunk_text:
                        chunk_id = f"doc_{document_id}_p{page_num}_{uuid.uuid4().hex[:8]}"
                        chunks.append({
                            "chunk_id": chunk_id,
                            "document_id": document_id,
                            "document_name": document_name,
                            "page_number": page_num,
                            "category": category,
                            "company": company,
                            "text": chunk_text
                        })
                    start += (chunk_size - overlap)

        return chunks
