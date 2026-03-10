"""Chunking Domain Service."""
from typing import List, Optional
from uuid import uuid4
import re

from ..entities.chunk import Chunk
from ..entities.document import Document
from ..value_objects.chunking_config import ChunkingConfig, ChunkingStrategy
from .text_normalizer import TextNormalizer


class ChunkingService:
    """
    Domain service for document chunking.
    Implements various chunking strategies with overlap support.
    """

    def __init__(self, config: Optional[ChunkingConfig] = None):
        """Initialize chunking service with configuration."""
        self.config = config or ChunkingConfig()
        self.normalizer = TextNormalizer()

    def chunk_document(self, document: Document) -> List[Chunk]:
        """
        Split document into chunks based on configured strategy.

        Args:
            document: Document to chunk

        Returns:
            List of Chunk entities
        """
        text = document.content

        if not text:
            return []

        if self.config.strategy == ChunkingStrategy.FIXED_SIZE:
            raw_chunks = self._chunk_fixed_size(text)
        elif self.config.strategy == ChunkingStrategy.SENTENCE:
            raw_chunks = self._chunk_by_sentence(text)
        elif self.config.strategy == ChunkingStrategy.PARAGRAPH:
            raw_chunks = self._chunk_by_paragraph(text)
        elif self.config.strategy == ChunkingStrategy.RECURSIVE:
            raw_chunks = self._chunk_recursive(text)
        else:
            raw_chunks = self._chunk_fixed_size(text)

        chunks = []
        for idx, (content, start, end) in enumerate(raw_chunks):
            normalized = self.normalizer.normalize_for_embedding(content)

            if len(normalized) < self.config.min_chunk_size:
                continue

            chunk = Chunk(
                id=uuid4(),
                document_id=document.id,
                content=content,
                normalized_content=normalized,
                chunk_index=idx,
                start_char=start,
                end_char=end,
                chunk_size=self.config.chunk_size,
                overlap_size=self.config.chunk_overlap,
                metadata={
                    **document.metadata.custom_fields,
                    "source": document.filename,
                    "strategy": self.config.strategy.value
                }
            )
            chunks.append(chunk)

        return chunks

    def _chunk_fixed_size(self, text: str) -> List[tuple]:
        """
        Fixed-size chunking with overlap.

        Returns:
            List of (content, start_pos, end_pos) tuples
        """
        chunks = []
        chunk_size = self.config.chunk_size
        overlap = self.config.chunk_overlap

        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                space_pos = text.rfind(' ', start, end)
                if space_pos > start + (chunk_size // 2):
                    end = space_pos

            chunk_content = text[start:end].strip()
            if chunk_content:
                chunks.append((chunk_content, start, end))

            # Move start position with overlap
            start = end - overlap
            if start <= chunks[-1][1] if chunks else 0:
                start = end  # Avoid infinite loop

        return chunks

    def _chunk_by_sentence(self, text: str) -> List[tuple]:
        """
        Sentence-based chunking with overlap.
        Groups sentences until chunk size is reached.
        """

        sentence_pattern = r'(?<=[.!?])\s+'
        sentences = re.split(sentence_pattern, text)

        chunks = []
        current_chunk = []
        current_size = 0
        chunk_start = 0
        pos = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            sentence_len = len(sentence)

            if current_size + sentence_len > self.config.chunk_size and current_chunk:
                chunk_content = ' '.join(current_chunk)
                chunk_end = pos
                chunks.append((chunk_content, chunk_start, chunk_end))

                overlap_sentences = []
                overlap_size = 0
                for s in reversed(current_chunk):
                    if overlap_size + len(s) <= self.config.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_size += len(s)
                    else:
                        break

                current_chunk = overlap_sentences
                current_size = overlap_size
                chunk_start = chunk_end - overlap_size

            current_chunk.append(sentence)
            current_size += sentence_len
            pos += sentence_len + 1

        if current_chunk:
            chunk_content = ' '.join(current_chunk)
            chunks.append((chunk_content, chunk_start, len(text)))

        return chunks

    def _chunk_by_paragraph(self, text: str) -> List[tuple]:
        """
        Paragraph-based chunking.
        Splits on double newlines, groups small paragraphs.
        """
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = []
        current_size = 0
        chunk_start = 0
        pos = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                pos += 2
                continue

            para_len = len(para)

            if current_size + para_len > self.config.chunk_size and current_chunk:
                chunk_content = '\n\n'.join(current_chunk)
                chunks.append((chunk_content, chunk_start, pos))

                current_chunk = []
                current_size = 0
                chunk_start = pos

            current_chunk.append(para)
            current_size += para_len
            pos += para_len + 2

        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            chunks.append((chunk_content, chunk_start, len(text)))

        return chunks

    def _chunk_recursive(
        self,
        text: str,
        separators: Optional[tuple] = None
    ) -> List[tuple]:
        """
        Recursive chunking using hierarchy of separators.
        Best balance of semantic coherence and chunk size control.
        """
        if separators is None:
            separators = self.config.separators

        if not separators:
            return self._chunk_fixed_size(text)

        separator = separators[0]
        remaining_seps = separators[1:]

        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)

        chunks = []
        current_chunk = []
        current_size = 0
        chunk_start = 0
        pos = 0

        for split in splits:
            split_len = len(split) + len(separator)

            if current_size + len(split) > self.config.chunk_size:
                if current_chunk:
                    chunk_content = separator.join(current_chunk)
                    chunks.append((chunk_content, chunk_start, pos))

                    current_chunk = []
                    current_size = 0
                    chunk_start = pos

                if len(split) > self.config.chunk_size and remaining_seps:
                    sub_chunks = self._chunk_recursive(split, remaining_seps)
                    for content, s, e in sub_chunks:
                        chunks.append((content, chunk_start + s, chunk_start + e))
                    pos += len(split) + len(separator)
                    chunk_start = pos
                    continue

            current_chunk.append(split)
            current_size += len(split)
            pos += split_len

        if current_chunk:
            chunk_content = separator.join(current_chunk)
            chunks.append((chunk_content, chunk_start, len(text)))

        return chunks

    def estimate_chunk_count(self, text: str) -> int:
        """
        Estimate number of chunks without actually chunking.
        Useful for progress tracking.
        """
        if not text:
            return 0

        text_len = len(text)
        effective_chunk_size = self.config.chunk_size - self.config.chunk_overlap

        if effective_chunk_size <= 0:
            effective_chunk_size = self.config.chunk_size

        return max(1, (text_len // effective_chunk_size) + 1)
