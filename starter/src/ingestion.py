"""Read and normalize source data."""
from pathlib import Path
import unicodedata
import re
import pypdf
from .models import DocumentPage


def normalize_text(text: str) -> str:
    """Normalize Unicode (NFC) and clean up excessive whitespace while keeping structure."""
    if not text:
        return ""
    # Normalize unicode to NFC
    text = unicodedata.normalize("NFC", text)
    # Standardize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace non-breaking spaces
    text = text.replace("\xa0", " ")
    # Clean up multiple horizontal spaces
    text = re.sub(r"[ \t]+", " ", text)
    # Clean up empty lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    """Extract physical pages from PDF, detect chapters/sections, and record metadata."""
    reader = pypdf.PdfReader(str(path))
    pages: list[DocumentPage] = []
    
    current_chapter = "Chương I"
    
    # Chapter title mappings for reference
    chapter_pattern = re.compile(r"^\s*(Chương\s+[IVXLCDM]+)", re.IGNORECASE)
    
    for idx, raw_page in enumerate(reader.pages):
        page_number = idx + 1
        raw_text = raw_page.extract_text() or ""
        clean_text = normalize_text(raw_text)
        
        # Detect if a new chapter starts on this page
        for line in clean_text.split("\n"):
            m = chapter_pattern.match(line.strip())
            if m:
                current_chapter = m.group(1).title()
        
        metadata = {
            "chapter": current_chapter,
            "char_count": len(clean_text),
            "is_empty": len(clean_text) == 0
        }
        
        pages.append(DocumentPage(
            document_id=document_id,
            source=source,
            page=page_number,
            text=clean_text,
            metadata=metadata
        ))
        
    return pages
