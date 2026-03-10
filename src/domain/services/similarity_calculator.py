"""Similarity Calculation Domain Service."""
import math
from typing import List, Tuple

from ..value_objects.search_config import SimilarityMetric


class SimilarityCalculator:
    """
    Domain service for vector similarity calculations.
    Implements various similarity metrics for vector comparison.

    Cosine vs Dot Product:
    ---------------------
    COSINE SIMILARITY:
    - Measures the angle between vectors, ignoring magnitude
    - Best for normalized embeddings (most text embedding models)
    - Range: -1 to 1 (1 = identical direction)
    - Recommended for: semantic similarity, text matching
    - Formula: cos(θ) = (A·B) / (||A|| × ||B||)

    DOT PRODUCT:
    - Measures both angle and magnitude
    - Faster computation (no normalization step)
    - Range: unbounded
    - Only equivalent to cosine if vectors are normalized
    - Recommended for: when vectors are pre-normalized or magnitude matters
    - Formula: A·B = Σ(ai × bi)

    EUCLIDEAN DISTANCE:
    - Measures straight-line distance in vector space
    - Lower = more similar (inverse of similarity)
    - Best for dense, low-dimensional embeddings
    - Formula: d = √(Σ(ai - bi)²)
    """

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Best for:
        - Text embeddings from models like OpenAI, Cohere, etc.
        - When semantic similarity matters more than magnitude
        - Variable-length or unnormalized embeddings

        Args:
            vec_a: First vector
            vec_b: Second vector

        Returns:
            Similarity score between -1 and 1
        """
        if len(vec_a) != len(vec_b):
            raise ValueError("Vectors must have same dimensions")

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = math.sqrt(sum(a * a for a in vec_a))
        magnitude_b = math.sqrt(sum(b * b for b in vec_b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    @staticmethod
    def dot_product(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculate dot product between two vectors.

        Best for:
        - Pre-normalized vectors (L2 normalized)
        - When computation speed is critical
        - When using vector DBs that expect dot product (e.g., Pinecone with dotproduct metric)

        Note: For unnormalized vectors, this is NOT equivalent to cosine similarity.
        If using this, ensure your embeddings are L2 normalized first.

        Args:
            vec_a: First vector
            vec_b: Second vector

        Returns:
            Dot product value (unbounded)
        """
        if len(vec_a) != len(vec_b):
            raise ValueError("Vectors must have same dimensions")

        return sum(a * b for a, b in zip(vec_a, vec_b))

    @staticmethod
    def euclidean_distance(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculate Euclidean distance between two vectors.
        Note: Lower values = more similar.

        Args:
            vec_a: First vector
            vec_b: Second vector

        Returns:
            Distance value (0 = identical, larger = more different)
        """
        if len(vec_a) != len(vec_b):
            raise ValueError("Vectors must have same dimensions")

        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))

    @staticmethod
    def euclidean_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Convert Euclidean distance to similarity score.

        Args:
            vec_a: First vector
            vec_b: Second vector

        Returns:
            Similarity score between 0 and 1
        """
        distance = SimilarityCalculator.euclidean_distance(vec_a, vec_b)
        return 1 / (1 + distance)

    @staticmethod
    def calculate(
        vec_a: List[float],
        vec_b: List[float],
        metric: SimilarityMetric = SimilarityMetric.COSINE
    ) -> float:
        """
        Calculate similarity using specified metric.

        Args:
            vec_a: First vector
            vec_b: Second vector
            metric: Similarity metric to use

        Returns:
            Similarity score
        """
        if metric == SimilarityMetric.COSINE:
            return SimilarityCalculator.cosine_similarity(vec_a, vec_b)
        elif metric == SimilarityMetric.DOT_PRODUCT:
            return SimilarityCalculator.dot_product(vec_a, vec_b)
        elif metric == SimilarityMetric.EUCLIDEAN:
            return SimilarityCalculator.euclidean_similarity(vec_a, vec_b)
        else:
            return SimilarityCalculator.cosine_similarity(vec_a, vec_b)

    @staticmethod
    def normalize_vector(vector: List[float]) -> List[float]:
        """
        L2 normalize a vector.
        After normalization, dot product equals cosine similarity.

        Args:
            vector: Input vector

        Returns:
            Normalized vector with magnitude 1
        """
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude == 0:
            return vector
        return [v / magnitude for v in vector]

    @staticmethod
    def batch_similarity(
        query_vector: List[float],
        candidate_vectors: List[Tuple[str, List[float]]],
        metric: SimilarityMetric = SimilarityMetric.COSINE,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Calculate similarity between query and multiple candidates.
        Returns top-k most similar.

        Args:
            query_vector: Query embedding
            candidate_vectors: List of (id, vector) tuples
            metric: Similarity metric
            top_k: Number of top results to return

        Returns:
            Sorted list of (id, score) tuples
        """
        scores = []

        for candidate_id, candidate_vec in candidate_vectors:
            score = SimilarityCalculator.calculate(
                query_vector, candidate_vec, metric
            )
            scores.append((candidate_id, score))

        # Sort by score descending (higher = more similar)
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_k]

    @staticmethod
    def recommend_metric(embedding_model: str) -> SimilarityMetric:
        """
        Recommend similarity metric based on embedding model.

        Args:
            embedding_model: Name of the embedding model

        Returns:
            Recommended similarity metric
        """
        normalized_models = [
            'text-embedding-ada-002',
            'text-embedding-3-small',
            'text-embedding-3-large',
            'all-MiniLM-L6-v2',
            'all-mpnet-base-v2'
        ]

        model_lower = embedding_model.lower()

        for model in normalized_models:
            if model in model_lower:
                return SimilarityMetric.COSINE

        return SimilarityMetric.COSINE
