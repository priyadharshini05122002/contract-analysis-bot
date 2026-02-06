# file_loader.py
from typing import Optional
from io import BytesIO

def load_contract_text(uploaded_file) -> Optional[str]:
    """
    Extract text from uploaded contract files.
    Supports: PDF, DOCX, TXT.
    Works on Streamlit Cloud.
    """

    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    try:
        # ---------- TXT ----------
        if file_name.endswith(".txt"):
            content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            return content.strip() if content else None

        # ---------- PDF (FIXED) ----------
        elif file_name.endswith(".pdf"):
            from PyPDF2 import PdfReader

            # IMPORTANT: use getvalue() not read()
            pdf_bytes = uploaded_file.getvalue()
            reader = PdfReader(BytesIO(pdf_bytes))

            text_pages = []

            for page in reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_pages.append(page_text.strip())
                except:
                    pass

            full_text = "\n".join(text_pages)

            # DEBUG (optional)
            if not full_text:
                return None

            return full_text

        # ---------- DOCX ----------
        elif file_name.endswith(".docx"):
            import docx

            doc = docx.Document(BytesIO(uploaded_file.getvalue()))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)

        # ---------- FALLBACK ----------
        else:
            content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            return content.strip() if content else None

    except Exception as e:
        print("FILE LOAD ERROR:", e)
        return None
