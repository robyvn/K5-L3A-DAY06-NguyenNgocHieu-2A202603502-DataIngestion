"""Vector store implementation using PostgreSQL + pgvector."""
import json
from typing import Any
import psycopg
from .models import Chunk


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        self.database_url = database_url
        self.dimensions = dimensions

    def create_schema(self) -> None:
        """Create vector extension and chunks table with metadata and vector index."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS document_chunks (
                        chunk_id TEXT PRIMARY KEY,
                        strategy TEXT NOT NULL,
                        document_id TEXT NOT NULL,
                        source TEXT NOT NULL,
                        page INTEGER NOT NULL,
                        content TEXT NOT NULL,
                        metadata JSONB NOT NULL,
                        embedding vector({self.dimensions}) NOT NULL
                    );
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_chunks_strategy ON document_chunks(strategy);
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_chunks_meta ON document_chunks USING gin (metadata);
                """)
            conn.commit()

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Upsert chunks with stable IDs to prevent duplication upon re-ingestion."""
        if len(chunks) != len(vectors):
            raise ValueError(f"Mismatch: {len(chunks)} chunks vs {len(vectors)} vectors")
        
        if not chunks:
            return

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                # Prepare batch insert
                query = """
                    INSERT INTO document_chunks (
                        chunk_id, strategy, document_id, source, page, content, metadata, embedding
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::vector)
                    ON CONFLICT (chunk_id) DO UPDATE SET
                        content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding;
                """
                records = [
                    (
                        c.chunk_id,
                        strategy,
                        c.document_id,
                        c.source,
                        c.page,
                        c.text,
                        json.dumps(c.metadata, ensure_ascii=False),
                        v
                    )
                    for c, v in zip(chunks, vectors)
                ]
                cur.executemany(query, records)
            conn.commit()

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Search top-k chunks by cosine distance with optional JSONB metadata filtering."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                where_clauses = ["strategy = %s"]
                params: list[Any] = [strategy]

                # Apply metadata filters if provided (case-insensitive for text)
                if filters:
                    for key, val in filters.items():
                        where_clauses.append(f"LOWER(metadata->>'{key}') = LOWER(%s)")
                        params.append(str(val))

                where_sql = " AND ".join(where_clauses)
                
                # Order by cosine distance (<=>)
                sql = f"""
                    SELECT chunk_id, document_id, source, page, content, metadata,
                           1 - (embedding <=> %s::vector) AS similarity_score
                    FROM document_chunks
                    WHERE {where_sql}
                    ORDER BY embedding <=> %s::vector ASC
                    LIMIT %s;
                """
                # query_vector is used twice (for score projection and order by)
                full_params = [query_vector] + params + [query_vector, top_k]
                cur.execute(sql, full_params)
                rows = cur.fetchall()

                results = []
                for row in rows:
                    results.append({
                        "chunk_id": row[0],
                        "document_id": row[1],
                        "source": row[2],
                        "page": row[3],
                        "text": row[4],
                        "metadata": row[5] if isinstance(row[5], dict) else json.loads(row[5]),
                        "score": float(row[6])
                    })
                return results
