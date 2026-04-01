from core.agents.coordinator_agent import CoordinatorAgent
from core.models import TodoItem


def test_resolves_tool_owner_for_ssl_analyzer_on_web_todo():
    agent = CoordinatorAgent()
    todo = TodoItem(
        id="step_1",
        content="检查 HTTPS 服务的证书与 TLS 配置",
        tool_hint="ssl_analyzer",
        resource="web:https://example.com",
        agent_hint="web_pentest",
    )

    selected, _ = agent._select_sub_agent(todo.agent_hint, todo.resource, todo)
    assert selected is not None
    assert "ssl_analyzer" not in selected.tools_dict

    resolved = agent._resolve_agent_for_tool(selected, todo.tool_hint)
    assert resolved is not None
    assert "ssl_analyzer" in resolved.tools_dict


def test_resolves_tool_owner_for_report_generator():
    agent = CoordinatorAgent()
    todo = TodoItem(
        id="step_1",
        content="汇总巡检结果并生成报告",
        tool_hint="report_generator",
        resource="web:https://example.com",
        agent_hint="web_pentest",
    )

    selected, _ = agent._select_sub_agent(todo.agent_hint, todo.resource, todo)
    assert selected is not None
    assert "report_generator" not in selected.tools_dict

    resolved = agent._resolve_agent_for_tool(selected, todo.tool_hint)
    assert resolved is not None
    assert "report_generator" in resolved.tools_dict


def test_resolve_tool_owner_returns_original_agent_for_unknown_tool():
    agent = CoordinatorAgent()
    todo = TodoItem(
        id="step_1",
        content="执行一个不存在的工具",
        tool_hint="does_not_exist",
        resource="web:https://example.com",
        agent_hint="web_pentest",
    )

    selected, _ = agent._select_sub_agent(todo.agent_hint, todo.resource, todo)
    assert selected is not None

    resolved = agent._resolve_agent_for_tool(selected, todo.tool_hint)
    assert resolved is selected


def test_keeps_original_agent_when_selected_agent_already_has_tool():
    agent = CoordinatorAgent()
    todo = TodoItem(
        id="step_1",
        content="分析站点的 HTTP 安全头",
        tool_hint="header_analyze",
        resource="web:https://example.com",
        agent_hint="web_pentest",
    )

    selected, _ = agent._select_sub_agent(todo.agent_hint, todo.resource, todo)
    assert selected is not None
    assert "header_analyze" in selected.tools_dict

    resolved = agent._resolve_agent_for_tool(selected, todo.tool_hint)
    assert resolved is selected
