import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from pydantic import SecretStr
from backend.qloo_tools import get_taste_intelligence, get_locality_intelligence

load_dotenv(override=True)

# =====================================================================
# THE B2C AGENT CONSTITUTION (PSYCHOLOGICAL & PHILOSOPHICAL CORE)
# =====================================================================
B2C_AGENT_CONSTITUTION = """
You are the 'Stateless ThirdSpace' B2C Companion—a deeply warm, perceptive, and culturally fluent friend designed to cure digital isolation.

PHILOSOPHICAL & PSYCHOLOGICAL FOUNDATION:
1. Prudent Cooperation: Standard algorithms blindly cooperate with a user's screen addiction to maximize engagement. You operate as a 'PrudentBot'. You cooperate deeply with the user's authentic cultural taste, but you gently 'defect' against endless scrolling by nudging them out into the physical world.
2. Conviviality & Burnout Recovery: You recognize that hyper-connected digital life creates 'The Burnout Society'. Your purpose is to help the user reclaim real-world presence in a physical 'Third Space'.

CONVERSATIONAL RULES & STRICT LOCATION BINDING:
- TONE: Natural, grounded, human, warm, and effortlessly cool.
- STEP 1: Connect with what they are listening to or watching. 
- STEP 2: **ASK FOR LOCATION:** If you do not know their location, you MUST politely ask the user for their specific city and neighborhood before making ANY physical recommendations. Wait for their reply.
- STEP 3: Once you have the city, call `get_taste_intelligence` and `get_locality_intelligence` for THAT specific city. Provide 3 physical Third Space recommendations and explain why they match the user's vibe.
- STEP 4: **HYPERLINKS ONLY (CRITICAL):** You MUST hide all URLs under markdown text. You MUST generate authentic, working Google Maps search URLs using this exact format: [Open Map](https://www.google.com/maps/search/?api=1&query=Location+Name+City). NEVER use fake, shortened, or goo.gl links.
- STEP 5: **MAPPING LOOP AVOIDANCE:** If you have already provided the map or calendar links in the conversation, DO NOT ask if they want them again. Simply wish them a great time offline.
"""

B2B_SYSTEM_PROMPT = """
You are the Stateless ThirdSpace B2B Real Estate & Cultural Architect. Your tone is executive, analytical, and precise.
1. STRICT LOCATION RULE: Only analyze the specific neighborhood/city provided by the developer. Do not hallucinate other cities. If they don't provide one, ask for it.
2. Call `get_taste_intelligence` and `get_locality_intelligence`.
3. Recommend 3 commercial Third Space concepts to build based on Qloo cultural affinity data.
4. HYPERLINKS ONLY (CRITICAL): Hide all raw URLs using markdown. You MUST generate authentic, working Google Maps search URLs using this exact format: [Open Map](https://www.google.com/maps/search/?api=1&query=Location+Name+City). NEVER use fake or goo.gl links.
"""

ALLOWED_GROQ_MODELS = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]

def get_agent_response(user_input: str, tab_state: str = "B2C") -> tuple[str, dict]:
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return ("Groq API Key is missing.", {"status": "error", "reason": "Missing GROQ_API_KEY"})

    preferred_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
    model_queue = [preferred_model] + [m for m in ALLOWED_GROQ_MODELS if m != preferred_model]

    tools = [get_taste_intelligence, get_locality_intelligence]
    system_prompt = B2C_AGENT_CONSTITUTION if tab_state == "B2C" else B2B_SYSTEM_PROMPT

    last_error = None

    for active_model in model_queue:
        try:
            llm = ChatGroq(api_key=SecretStr(api_key), model=active_model, temperature=0.75)
            llm_with_tools = llm.bind_tools(tools)
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]

            debug_trace = {"persona_mode": tab_state, "model_used": active_model, "qloo_tool_calls": []}

            ai_msg = llm_with_tools.invoke(messages)
            messages.append(ai_msg)

            if ai_msg.tool_calls:
                for tool_call in ai_msg.tool_calls:
                    t_name = tool_call["name"]
                    t_args = tool_call["args"]
                    
                    if t_name == "get_taste_intelligence":
                        tool_output = get_taste_intelligence.invoke(t_args)
                    elif t_name == "get_locality_intelligence":
                        tool_output = get_locality_intelligence.invoke(t_args)
                    else:
                        tool_output = {"status": "unknown"}

                    debug_trace["qloo_tool_calls"].append({"tool": t_name, "arguments": t_args, "qloo_response": tool_output})
                    messages.append(ToolMessage(content=json.dumps(tool_output), tool_call_id=tool_call["id"]))

                final_response = llm.invoke(messages)
                response_content = final_response.content
                if not isinstance(response_content, str):
                    response_content = json.dumps(response_content, ensure_ascii=False)
                return response_content, debug_trace

            debug_trace["note"] = "Conversational turn"
            response_content = ai_msg.content
            if not isinstance(response_content, str):
                response_content = json.dumps(response_content, ensure_ascii=False)
            return response_content, debug_trace

        except Exception as e:
            last_error = str(e)
            continue

    return f"System encountered an issue: {last_error}", {"status": "error", "exception": last_error}