"""Text Normalization Domain Service."""
import re
import unicodedata
from typing import Optional


class TextNormalizer:
    """
    Domain service for text normalization.
    Handles text cleaning and preprocessing for consistent embedding generation.
    """

    @staticmethod
    def normalize(
        text: str,
        normalize_whitespace: bool = True,
        normalize_unicode: bool = True,
        remove_special_chars: bool = False,
        lowercase: bool = False,
        max_length: Optional[int] = None
    ) -> str:
        """
        Apply text normalization pipeline.

        Args:
            text: Input text to normalize
            normalize_whitespace: Collapse multiple spaces/newlines
            normalize_unicode: Convert to NFKC form
            remove_special_chars: Remove non-alphanumeric chars
            lowercase: Convert to lowercase
            max_length: Truncate to max length if specified

        Returns:
            Normalized text string
        """
        if not text:
            return ""

        result = text

        if normalize_unicode:
            result = unicodedata.normalize("NFKC", result)

        if normalize_whitespace:
            result = re.sub(r'\s+', ' ', result)
            result = result.replace('\r\n', '\n').replace('\r', '\n')
            result = result.strip()

        if remove_special_chars:
            result = re.sub(r'[^\w\s.,!?;:\'"()-]', '', result)

        if lowercase:
            result = result.lower()

        if max_length and len(result) > max_length:
            result = result[:max_length]

        return result

    @staticmethod
    def normalize_for_embedding(text: str) -> str:
        """
        Standard normalization for embedding generation.
        Optimized for semantic similarity.
        """
        return TextNormalizer.normalize(
            text,
            normalize_whitespace=True,
            normalize_unicode=True,
            remove_special_chars=False,
            lowercase=False  # Preserve case for proper nouns
        )

    @staticmethod
    def normalize_for_keyword_search(text: str) -> str:
        """
        Normalization optimized for keyword search.
        More aggressive normalization for matching.
        """
        return TextNormalizer.normalize(
            text,
            normalize_whitespace=True,
            normalize_unicode=True,
            remove_special_chars=True,
            lowercase=True
        )

    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> list:
        """
        Extract meaningful keywords from text.

        Args:
            text: Input text
            min_length: Minimum keyword length

        Returns:
            List of keywords
        """
        normalized = TextNormalizer.normalize_for_keyword_search(text)

        words = normalized.split()

        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'it', 'its', 'as', 'if', 'not', 'no', 'yes'
        }

        keywords = [
            word for word in words
            if len(word) >= min_length and word not in stop_words
        ]

        return keywords

    @staticmethod
    def clean_pdf_text(text: str) -> str:
        """
        Special cleaning for PDF-extracted text.
        Handles common PDF extraction artifacts.
        """
        if not text:
            return ""

        result = text

        result = re.sub(r'\n\s*\d+\s*\n', '\n', result)
        result = re.sub(r'^\d+\s*$', '', result, flags=re.MULTILINE)
        result = re.sub(r'(\w)-\n(\w)', r'\1\2', result)
        result = re.sub(r'\n{3,}', '\n\n', result)

        result = re.sub(r'(\w)\s+(\w)', lambda m:
            m.group(1) + m.group(2) if len(m.group(0)) <= 3 else m.group(0),
            result
        )

        result = TextNormalizer.normalize(result)

        return result
