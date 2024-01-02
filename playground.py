import os

import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent
# from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent  
from autogen.code_utils import extract_code

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
)
if not config_list:
    os.environ["MODEL"] = "gpt-4"
    os.environ["OPENAI_API_KEY"] = "NULL"
    os.environ["OPENAI_BASE_URL"] = "https://ko-yearly-getting-bulletin.trycloudflare.com/openai" # optional

    config_list = autogen.config_list_from_models(
        model_list=[os.environ.get("MODEL", "gpt-4")],
    )

llm_config = {
    "timeout": 60,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

def termination_msg(x):
    _msg = str(x.get("content", "")).upper().strip().strip("\n").strip(".")
    return isinstance(x, dict) and (_msg.endswith("TERMINATE") or _msg.startswith("TERMINATE"))

def _is_termination_msg(message):
    if isinstance(message, dict):
        message = message.get("content")
        if message is None:
            return False
    cb = extract_code(message)
    contain_code = False
    for c in cb:
        # todo: support more languages
        if c[0] == "python":
            contain_code = True
            break
    return not contain_code

agents = []


agent = UserProxyAgent(
    name="Boss",
    is_termination_msg=termination_msg,
    human_input_mode="TERMINATE",
    system_message="""The boss who ask questions and give tasks. Reply `TERMINATE` in the end if the task is done.""",
    default_auto_reply="Good, thank you. Reply `TERMINATE` to finish.",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
)


agents.append(agent)


agent = AssistantAgent(
    name="Senior_Python_Engineer",
    system_message="""You are a senior python engineer. Reply `TERMINATE` in the end if the task is done.""",
    llm_config=llm_config,
    is_termination_msg=termination_msg,
)


agents.append(agent)


agent = UserProxyAgent(
    name="Product_Manager",
    human_input_mode="NEVER",
    system_message="""You are a product manager. Reply `TERMINATE` in the end if the task is done.""",
    llm_config=llm_config,
    is_termination_msg=termination_msg,
)


agents.append(agent)


init_sender = None
for agent in agents:
    if "UserProxy" in str(type(agent)):
        init_sender = agent
        break

if not init_sender:
    init_sender = agents[0]


groupchat = autogen.GroupChat(
    agents=agents, messages=[], max_round=12, speaker_selection_method="round_robin", allow_repeat_speaker=False
)  # todo: auto, sometimes message has no name
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

recipient = manager

# if isinstance(init_sender, (RetrieveUserProxyAgent, MathUserProxyAgent)):
#     init_sender.initiate_chat(recipient, problem="find papers on LLM applications from arxiv in the last week, create a markdown table of different domains.")
# else:
init_sender.initiate_chat(recipient, message="find papers on LLM applications from arxiv in the last week, create a markdown table of different domains and save it in 'llm.md' file in the current dir.")
