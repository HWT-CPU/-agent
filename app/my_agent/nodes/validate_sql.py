from langgraph.runtime import Runtime

from app.my_agent.context import DataAgentContext
from app.my_agent.state import DataAgentState
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.core.log import logger

async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type": "progress", "step": "验证SQL", "status": "running"})

    try:
        sql = state['sql']

        dw_mysql_repository: DWMySQLRepository = runtime.context["dw_mysql_repository"]

        try:
            await dw_mysql_repository.validate_sql(sql)
            logger.info("SQL语法正确")
            writer({"type": "progress", "step": "验证SQL", "status": "success"})
            return {'error': None}
        except Exception as e:
            logger.error(f"SQL语法错误: {e}")
            writer({"type": "progress", "step": "验证SQL", "status": "success"})
            return {'error': str(e)}
    except Exception as e:
        logger.error(f"验证SQL失败: {e}")
        writer({"type": "progress", "step": "验证SQL", "status": "error"})
        raise