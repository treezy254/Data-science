import autogen

# proxy config
config_list_mistral = [
    {
        'base_url': "https://ko-yearly-getting-bulletin.trycloudflare.com/openai",
        'api_key': "NULL"
    }
]


# --------------------

# gpt-4 config
gpt4_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list_mistral,
    "timeout": 120,
}

#-------------------

# Agents configs

import autogen

# config_list_mistral = [
#     {
#         'base_url': "http://0.0.0.0:8000",
#         'api_key': "NULL"
#     }
# ]

# config_list_codellama = [
#     {
#         'base_url': "http://0.0.0.0:25257",
#         'api_key': "NULL"
#     }
# ]

llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_mistral,
}

Root = autogen.UserProxyAgent(
    name="Root",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "proposal"},
    llm_config=llm_config_mistral,
    system_message="A human admin. I recieve task from the user. I write a proposal for how the task could be achieved with some objectives. I present the proposal to the user and await approval. If approved, I save my work and pass on the proposal to the Paper_writer for docuemntation. I monitor the whole project development life cyle. Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
)

Writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config_mistral,
    code_execution_config={"work_dir": "docs"},
    system_message="As a expert technical writer, I am profecient in writing software documentation for projects. When I recieve proposals from Root, I write an overall introduction for it, a literature review, SRS and SDS followed by a an implementation methodology. I use my language skills to describe various UML diagrams which help visualize the system functionality much better. After completing writing the documentation, I save my work and pass it on to the project manager."
    )

Manager = autogen.AssistantAgent(
    name = "Project_manager",
    llm_config=llm_config_mistral,
    system_message="I am an experienced project manager. When I recieve documentations, I identify the task at hand and breakdown the task into steps which can be easily solved.If I feel my work is satisfactory I respond with 'Documentation written' and the proceed to use my linux skills to create a txt file and write my documentation in it and the proceed to handover the proposal to the System_architect. "
    )

Architect = autogen.AssistantAgent(
    name="System_architect",
    llm_config=llm_config_mistral,
    system_message="I am expert system architect. I am well versed in system design patterns and architecture. I read through the documentation of a project and come up with the best system architecture for the system and a design pattern to make the system efficient. I communicate with the Fullstack engineer on how he should implementation the system based on my guidelines and proposal. If i feel my work is satisfactory, I respond with 'System Designed' and ask the Fullstack_engineer to implement my work."
    )

Engineer = autogen.UserProxyAgent(
    name="Fullstack_engineer",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "project"},
    llm_config=llm_config_mistral,
    system_message="I am a professional fullstack engineer. I know how sytems should be structured. Once I recieve guidelines from the System_architect, I proceed to create directories in my working diretory using my linux skills. I prefill the directories with files that have comments on the codes to be implemented. I know of various professional tools and libraries for software development and I use in accomplishing my task. Once I feel I have completed my work to satisfactory levels, I repond with 'System Initialized' and ask the coder to execute his tasks."
    )

coder = autogen.AssistantAgent(
    name="Coder",
    # max_consecutive_auto_reply=10,
    # is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    # code_execution_config={"work_dir": "project"},
    llm_config=llm_config_codellama,
    system_message="I am an experienced software developer. I am profecient at writing well sructure code. I write code based on the instructions provided by the Fullstack_engineer. My code is professionally written with comments wherever possible. My code is dynamic and passes most use cases. I like programming alone so I endure that my work is sufficient. I dont provide shallow code which might be referred to as a tutorial. Since I have much pride in my work, I put in the effort and write as much code as possible while still maintaing professionalism as a software developer. "
)

tester = autogen.UserProxyAgent(
    name="Tester",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "project"},
    llm_config=llm_config_mistral,
    system_message="I am an experienced tester. I execute all the code in my code base. I run the code against several test cases and suggest improvements. When I encounter errors, I inform the coder so thathe can make the necessary changes. Other than that, I write a log file indicating what I have done. When I feel I have completed my tasks completely to satisafction, I repond with 'Test Done' and then I save my work."
    )

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task="""
Implement a document management system in flask which support document create, read, update, delete and search and then the user_proxy agent should run the script to try and perform those operations so provide him with the relevant scripts to execute.
"""

groupchat = autogen.GroupChat(agents=[Root, Writer, Manager, Architect, Engineer, coder, tester], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    coder,
    message=task
)
