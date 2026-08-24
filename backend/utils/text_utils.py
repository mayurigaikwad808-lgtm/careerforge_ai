#What this file does

#When text is extracted from a PDF, it may contain:

#Extra spaces
#Extra empty lines
#Unnecessary formatting

#This function cleans the text before we send it to our AI system later.

import re


def clean_text(text):
    """
    Cleans extracted resume text.
    """

    if not text:
        return ""

    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple empty lines with a single newline
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text