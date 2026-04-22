import asyncio

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

from app.conf.app_config import QdrantConfig, app_config


class QdrantClientManager:
    def __init__(self, config: QdrantConfig):
        self.client: AsyncQdrantClient | None = None
        self.config: QdrantConfig = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        # 使用容器 IP 地址避免 localhost 解析问题
        self.client = AsyncQdrantClient(
            host=self.config.host,
            port=self.config.port,
            timeout=120,
            prefer_grpc=False,
            https=False,
            check_compatibility=False
        )

    async def close(self):
        await self.client.close()

qdrant_client_manager = QdrantClientManager(app_config.qdrant)

if __name__ == '__main__':
    qdrant_client_manager.init()
    client = qdrant_client_manager.client
    async def test():
        # 先删除已存在的集合（如果存在）
        try:
            await client.delete_collection(collection_name="test_collection_async")
            print("已删除旧集合")
        except Exception as e:
            print(f"集合不存在或删除失败: {e}")
        
        #创建集合
        await client.create_collection(
            collection_name="test_collection_async",
            vectors_config=VectorParams(size=4, distance=Distance.COSINE)
        )
        print("集合创建成功")

        #创建集合
        from qdrant_client.models import PointStruct

        operation_info = await client.upsert(
            collection_name="test_collection_async",
            wait=True,
            points=[
                PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
                PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
                PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
                PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
                PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
                PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
            ],
        )

        #查询数据
        search_result = await client.query_points(
            collection_name="test_collection_async",
            query=[0.2, 0.1, 0.9, 0.7],
            with_payload=False,
            limit=3
        )

        print(search_result.points)
        await qdrant_client_manager.close()

    asyncio.run(test())