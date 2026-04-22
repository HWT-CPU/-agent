from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.entities.value_info import ValueInfo
from app.my_agent.context import DataAgentContext
from app.my_agent.llm import llm
from app.my_agent.state import DataAgentState
from app.prompt.prompt_loader import load_prompt
from app.core.log import logger

async def recall_value(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type": "progress", "step": "召回字段取值", "status": "running"})

    try:
        query = state["query"]
        keywords = state["keywords"]
        value_es_repository = runtime.context["value_es_repository"]

        # 借助LLM扩展关键词
        # chain = pormpt | llm | output_parser
        prompt = PromptTemplate(template=load_prompt("extend_keywords_for_value_recall"), input_variables=["query"])
        output_parser = JsonOutputParser()
        chain = prompt | llm | output_parser
        result = await chain.ainvoke({"query": query})
        keywords = set(keywords + result)

        # 根据关键词召回字段取值
        value_infos_map: dict[str, ValueInfo] = {}  # 因为同一关键词或者不同关键词会检索出相同字段，所有用字典类型进行去重
        for keyword in keywords:
            current_value_infos: list[ValueInfo] = await value_es_repository.search(keyword)
            for current_value_info in current_value_infos:
                if current_value_info.id not in value_infos_map:
                    value_infos_map[current_value_info.id] = current_value_info
        retrieved_value_infos: list[ValueInfo] = list(value_infos_map.values())

        writer({"type": "progress", "step": "召回字段取值", "status": "success"})
        logger.info(f"检索到字段取值：{list(value_infos_map.keys())}")
        return {"retrieved_value_infos": retrieved_value_infos}
    except Exception as e:
        logger.error(f"召回字段取值失败：{e}")
        writer({"type": "progress", "step": "召回字段取值", "status": "error"})
        raise



