from pypdf import PdfReader
from backend.utils.text_utils import clean_text


def extract_resume_text(uploaded_file):
    """
    Extracts and cleans text from an uploaded PDF resume.
    """

    try:
        reader = PdfReader(uploaded_file)

        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        cleaned_text = clean_text(extracted_text)

        return {
            "success": True,
            "text": cleaned_text,
            "page_count": len(reader.pages),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": str(e)
        }