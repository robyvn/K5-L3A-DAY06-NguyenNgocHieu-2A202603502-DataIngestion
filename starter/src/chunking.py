"""Implement fixed-size and structure-aware chunking."""
import re
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping fixed-size windows while preserving page and chapter metadata."""
    text = page.text
    if not text:
        return []
    
    chunks: list[Chunk] = []
    start = 0
    chunk_index = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + size, text_len)
        chunk_text = text[start:end].strip()
        
        if chunk_text:
            chunk_id = f"{page.document_id}_p{page.page}_fix_{chunk_index:03d}"
            metadata = dict(page.metadata)
            metadata["chunk_strategy"] = "fixed_size"
            metadata["chunk_index"] = chunk_index
            metadata["start_char"] = start
            metadata["end_char"] = end
            
            chunks.append(Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=metadata
            ))
            chunk_index += 1
            
        if end >= text_len:
            break
        start += (size - overlap)
        
    return chunks


def by_paragraph(page: DocumentPage, max_size: int = 800) -> list[Chunk]:
    """Split text by legal articles and paragraphs, preserving semantic completeness."""
    text = page.text
    if not text:
        return []
        
    chunks: list[Chunk] = []
    
    # Split by legal article pattern or double newline
    # Matches 'Điều 1.', 'Điều 2.' or section numbers
    paragraphs = re.split(r"\n\s*\n|(?=\n\s*Điều\s+\d+\.)", text)
    
    chunk_index = 0
    current_buffer = []
    current_length = 0
    
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
            
        p_len = len(p_clean)
        
        # If single paragraph is oversized, split into sentences
        if p_len > max_size:
            if current_buffer:
                combined_text = "\n\n".join(current_buffer)
                chunk_id = f"{page.document_id}_p{page.page}_struct_{chunk_index:03d}"
                meta = dict(page.metadata)
                meta["chunk_strategy"] = "by_paragraph"
                meta["chunk_index"] = chunk_index
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=combined_text,
                    metadata=meta
                ))
                chunk_index += 1
                current_buffer = []
                current_length = 0
                
            sentences = re.split(r"(?<=[.;])\s+", p_clean)
            sub_buf = []
            sub_len = 0
            for s in sentences:
                s_strip = s.strip()
                if not s_strip:
                    continue
                if sub_len + len(s_strip) > max_size and sub_buf:
                    chunk_id = f"{page.document_id}_p{page.page}_struct_{chunk_index:03d}"
                    meta = dict(page.metadata)
                    meta["chunk_strategy"] = "by_paragraph"
                    meta["chunk_index"] = chunk_index
                    chunks.append(Chunk(
                        chunk_id=chunk_id,
                        document_id=page.document_id,
                        source=page.source,
                        page=page.page,
                        text=" ".join(sub_buf),
                        metadata=meta
                    ))
                    chunk_index += 1
                    sub_buf = [s_strip]
                    sub_len = len(s_strip)
                else:
                    sub_buf.append(s_strip)
                    sub_len += len(s_strip)
            if sub_buf:
                chunk_id = f"{page.document_id}_p{page.page}_struct_{chunk_index:03d}"
                meta = dict(page.metadata)
                meta["chunk_strategy"] = "by_paragraph"
                meta["chunk_index"] = chunk_index
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=" ".join(sub_buf),
                    metadata=meta
                ))
                chunk_index += 1
        elif current_length + p_len > max_size and current_buffer:
            combined_text = "\n\n".join(current_buffer)
            chunk_id = f"{page.document_id}_p{page.page}_struct_{chunk_index:03d}"
            meta = dict(page.metadata)
            meta["chunk_strategy"] = "by_paragraph"
            meta["chunk_index"] = chunk_index
            chunks.append(Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=combined_text,
                metadata=meta
            ))
            chunk_index += 1
            current_buffer = [p_clean]
            current_length = p_len
        else:
            current_buffer.append(p_clean)
            current_length += p_len
            
    if current_buffer:
        combined_text = "\n\n".join(current_buffer)
        chunk_id = f"{page.document_id}_p{page.page}_struct_{chunk_index:03d}"
        meta = dict(page.metadata)
        meta["chunk_strategy"] = "by_paragraph"
        meta["chunk_index"] = chunk_index
        chunks.append(Chunk(
            chunk_id=chunk_id,
            document_id=page.document_id,
            source=page.source,
            page=page.page,
            text=combined_text,
            metadata=meta
        ))
        
    return chunks
