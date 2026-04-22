from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from app.conf.app_config import app_config
from app.entities.metric_info import MetricInfo


class MetricQdrantRepository:
    collection_name = "metric_info_collection"

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def ensure_collection(self):
        import asyncio
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not await self.client.collection_exists(self.collection_name):
                    await self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(size=app_config.qdrant.embedding_size, distance=Distance.COSINE),
                    )
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Qdrant 连接失败，重试 {attempt + 1}/{max_retries}...")
                    await asyncio.sleep(2)
                else:
                    raise

    async def upsert(self, ids: list[str], embeddings: list[list[float]], payloads: list[dict], batch_size=20):
        points: list[PointStruct] = [PointStruct(id=id, vector=embedding, payload=payload) for id, embedding, payload in
                                     zip(ids, embeddings, payloads)]
        for i in range(0, len(points), batch_size):
            await self.client.upsert(collection_name=self.collection_name, points=points[i:i + batch_size])

    async def search(self, embedding: list[float], score_threshold: float = 0.6, limit: int = 20) -> list[MetricInfo]:
        # 查询数据
        result = await self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=3,
            score_threshold=score_threshold,
        )
        return [MetricInfo(**point.payload) for point in result.points]