from sqlalchemy import text
from sqlalchemy.dialects.mssql import dialect
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch


class DWMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_column_type(self, table_name)->dict[str, str]:
        sql = f"show columns from {table_name}"
        result = await self.session.execute(text(sql))
        result_dict = result.mappings().fetchall()
        return {row['Field']: row['Type'] for row in result_dict}

    async def get_column_values(self, table_name, column_name, limit=10):
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        result = await self.session.execute(text(sql))
        return [row[0] for row in result.fetchall()]

    async def get_db(self):
        sql = "select version()"
        result = await self.session.execute(text(sql))
        version = result.scalar()

        dialect = self.session.bind.dialect.name
        return {"dialect": dialect, "version": version}

    async def validate_sql(self, sql: str):
        sql = f"explain {sql}"
        await self.session.execute(text(sql))

    async def run_sql(self, sql: str):
        result = await self.session.execute(text(sql))
        return [dict(row) for row in result.mappings().fetchall()]