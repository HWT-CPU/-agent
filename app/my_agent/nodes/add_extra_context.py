from datetime import date

from langgraph.runtime import Runtime

from app.my_agent.context import DataAgentContext
from app.my_agent.state import DataAgentState, DateInfoState, DBInfoState
from app.core.log import logger


async def add_extra_context(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type": "progress", "step": "添加额外信息", "status": "running"})

    try:
        dw_mysql_repository = runtime.context["dw_mysql_repository"]

        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        weekday = today.strftime("%A")
        quarter = f"Q{(today.month - 1) // 3 + 1}"
        date_info = DateInfoState(date=date_str, weekday=weekday, quarter=quarter)

        db = await dw_mysql_repository.get_db()
        db_info = DBInfoState(**db)

        writer({"type": "progress", "step": "添加额外信息", "status": "success"})
        logger.info(f"数据库信息：{db_info}")
        logger.info(f"日期信息：{date_info}")
        return {"date_info": date_info, "db_info": db_info}
    except Exception as e:
        writer({"type": "progress", "step": "添加额外信息", "status": "error"})
        logger.error(f"添加额外信息时出错：{e}")
        raise