import os
from app.config import settings

class LLMService:
    @classmethod
    def generate_grounded_answer(cls, query: str, category: str, context_chunks: list[dict], unknown_flag: bool = False) -> str:
        """
        Generates grounded response using Google Gemini API if key is present,
        or grounded context synthesis fallback if key is unprovided.
        """
        if unknown_flag or not context_chunks:
            return "I couldn't find this information in the available placement knowledge base. Please check with the placement cell or upload the relevant authorized document."

        # System prompt instructions
        prompt_system = (
            "You are CareerCampusAI, a placement and career guidance assistant.\n"
            "For institutional placement questions, use ONLY the retrieved knowledge provided in the context.\n"
            "Do NOT invent company eligibility, CGPA criteria, backlog limits, salaries, dates, or procedures.\n"
            "If the answer is not supported by the retrieved context, explicitly state that the information was not found in the placement knowledge base.\n\n"
        )
        
        context_str = "RETRIEVED CONTEXT:\n"
        for i, c in enumerate(context_chunks):
            doc = c.get("document_name", "Document")
            pg = c.get("page_number", 1)
            txt = c.get("text", "")
            context_str += f"[Source {i+1}: {doc} (Page {pg})]\n{txt}\n\n"
            
        user_prompt = f"{prompt_system}{context_str}USER QUESTION: {query}\n\nPROVIDE A GROUNDED, CLEAR RESPONSE:"

        # Try Google Gemini if API key present
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(user_prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[LLMService] Gemini API call failed: {e}. Falling back to context synthesis.")

        # Grounded Context Synthesis Fallback (guarantees offline demo works perfectly)
        return cls._synthesize_context_fallback(query, category, context_chunks)

    @classmethod
    def _synthesize_context_fallback(cls, query: str, category: str, chunks: list[dict]) -> str:
        """
        Directly synthesizes answer from retrieved context chunks without external API call.
        """
        primary_text = " ".join([c["text"] for c in chunks[:3]])
        doc_names = list(set([f"{c['document_name']} (Page {c['page_number']})" for c in chunks]))
        
        lines = []
        lines.append(f"Based on the official placement knowledge base:")
        lines.append("")
        
        # Format key sentences
        sentences = [s.strip() for s in primary_text.split(".") if len(s.strip()) > 10]
        for s in sentences[:5]:
            lines.append(f"• {s}.")
            
        lines.append("")
        lines.append(f"**Verified Sources:** {', '.join(doc_names)}")
        return "\n".join(lines)
