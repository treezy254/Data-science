Prompt flow

Prompt flow is a suite of development tools designed to streamline the end-to-end development cycle of LLM-based AI applications, from ideation, prototyping, testing, evaluation to production deployment and monitoring. It makes prompt engineering much easier and enables you to build LLM apps with production quality.

With prompt flow, you will be able to:

    Create flows that link LLMs, prompts, Python code and other tools together in a executable workflow.
    Debug and iterate your flows, especially the interaction with LLMs with ease.
    Evaluate your flows, calculate quality and performance metrics with larger datasets.
    Integrate the testing and evaluation into your CI/CD system to ensure quality of your flow.
    Deploy your flows to the serving platform you choose or integrate into your app's code base easily.
    (Optional but highly recommended) Collaborate with your team by leveraging the cloud version of Prompt flow in Azure AI.

    Welcome to join us to make prompt flow better by participating discussions, opening issues, submitting PRs.

This documentation site contains guides for prompt flow sdk, cli and vscode extension users.

Quick Start

This guide will walk you through the fist step using of prompt flow code-first experience.

Prerequisite - To make the most of this tutorial, you'll need:

    Know how to program with Python :)
    A basic understanding of Machine Learning can be beneficial, but it's not mandatory.

Learning Objectives - Upon completing this tutorial, you should learn how to:

    Setup your python environment to run prompt flow
    Clone a sample flow & understand what's a flow
    Understand how to edit the flow using visual editor or yaml
    Test the flow using your favorite experience: CLI, SDK or VS Code Extension.

Set up your dev environment

    A python environment with version python=3.9 or higher version like 3.10. It's recommended to use python environment manager miniconda. After you have installed miniconda, run below commands to create a python environment:

conda create --name pf python=3.9
conda activate pf

    Install promptflow and promptflow-tools.

pip install promptflow promptflow-tools

    Check the installation.

# should print promptflow version, e.g. "0.1.0b3"
pf -v

Understand what's a flow

A flow, represented as a YAML file, is a DAG of functions, which is connected via input/output dependencies, and executed based on the topology by prompt flow executor. See Flows for more details.
Get the flow sample

Clone the sample repo and check flows in folder examples/flows.

git clone https://github.com/microsoft/promptflow.git

Understand flow directory

The sample used in this tutorial is the web-classification flow, which categorizes URLs into several predefined classes. Classification is a traditional machine learning task, and this sample illustrates how to perform classification using GPT and prompts.

cd promptflow/examples/flows/standard/web-classification

A flow directory is a directory that contains all contents of a flow. Structure of flow folder:

    flow.dag.yaml: The flow definition with inputs/outputs, nodes, tools and variants for authoring purpose.
    .promptflow/flow.tools.json: It contains tools meta referenced in flow.dag.yaml.
    Source code files (.py, .jinja2): User managed, the code scripts referenced by tools.
    requirements.txt: Python package dependencies for this flow.

flow_dir

In order to run this specific flow, you need to install its requirements first.

pip install -r requirements.txt

Understand the flow yaml

The entry file of a flow directory is flow.dag.yaml which describes the DAG(Directed Acyclic Graph) of a flow. Below is a sample of flow DAG:

flow_dag

This graph is rendered by VS Code extension which will be introduced in the next section.
Using VS Code Extension to visualize the flow

Note: Prompt flow VS Code Extension is highly recommended for flow development and debugging.

    Prerequisites for VS Code extension.
        Install latest stable version of VS Code
        Install VS Code Python extension

    Install Prompt flow for VS Code extension

    Select python interpreter

    vscode vscode

    Open dag in vscode. You can open the flow.dag.yaml as yaml file, or you can also open it in visual editor. vscode

Develop and test your flow
How to edit the flow

To test your flow with varying input data, you have the option to modify the default input. If you are well-versed with the structure, you may also add or remove nodes to alter the flow's arrangement.

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Flow.schema.json
inputs:
  url:
    type: string
    # change the default value of input url here
    default: https://play.google.com/store/apps/details?id=com.twitter.android
...

See more details of this topic in Develop a flow.
Create necessary connections

:::{note} If you are using WSL or other OS without default keyring storage backend, you may encounter StoreConnectionEncryptionKeyError, please refer to FAQ for the solutions. :::

The connection helps securely store and manage secret keys or other sensitive credentials required for interacting with LLM and other external tools for example Azure Content Safety.

The sample flow web-classification uses connection open_ai_connection inside, e.g. classify_with_llm node needs to talk to llm using the connection.

We need to set up the connection if we haven't added it before. Once created, the connection will be stored in local db and can be used in any flow.

::::{tab-set}

:::{tab-item} CLI :sync: CLI

Firstly we need a connection yaml file connection.yaml:

If you are using Azure Open AI, prepare your resource follow with this instruction and get your api_key if you don't have one.

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
name: open_ai_connection
type: azure_open_ai
api_key: <test_key>
api_base: <test_base>
api_type: azure
api_version: <test_version>

If you are using OpenAI, sign up account via OpenAI website, login and find personal API key, then use this yaml:

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/OpenAIConnection.schema.json
name: open_ai_connection
type: open_ai
api_key: "<user-input>"
organization: "" # optional

Then we can use CLI command to create the connection.

pf connection create -f connection.yaml

More command details can be found in CLI reference.

:::

:::{tab-item} SDK :sync: SDK

In SDK, connections can be created and managed with PFClient.

from promptflow import PFClient
from promptflow.entities import AzureOpenAIConnection

# PFClient can help manage your runs and connections.
pf = PFClient()

try:
    conn_name = "open_ai_connection"
    conn = pf.connections.get(name=conn_name)
    print("using existing connection")
except:
    connection = AzureOpenAIConnection(
        name=conn_name,
        api_key="<test_key>",
        api_base="<test_base>",
        api_type="azure",
        api_version="<test_version>",
    )

    # use this if you have an existing OpenAI account
    # from promptflow.entities import OpenAIConnection
    # connection = OpenAIConnection(
    #     name=conn_name,
    #     api_key="<user-input>",
    # )

    conn = pf.connections.create_or_update(connection)
    print("successfully created connection")

print(conn)

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

    Click the promptflow icon to enter promptflow control panel

    vsc_add_connection

    Create your connection.

    vsc_add_connection

    vsc_add_connection

    vsc_add_connection

:::

::::

Learn more on more actions like delete connection in: Manage connections.
Test the flow

:::{admonition} Note Testing flow will NOT create a batch run record, therefore it's unable to use commands like pf run show-details to get the run information. If you want to persist the run record, see Run and evaluate a flow :::

Assuming you are in working directory promptflow/examples/flows/standard/

::::{tab-set}

:::{tab-item} CLI :sync: CLI

Change the default input to the value you want to test.

q_0

pf flow test --flow web-classification  # "web-classification" is the directory name

flow-test-output-cli

:::

:::{tab-item} SDK :sync: SDK

The return value of test function is the flow/node outputs.

from promptflow import PFClient

pf = PFClient()

flow_path = "web-classification"  # "web-classification" is the directory name

# Test flow
flow_inputs = {"url": "https://www.youtube.com/watch?v=o5ZQyXaAv1g", "answer": "Channel", "evidence": "Url"}  # The inputs of the flow.
flow_result = pf.test(flow=flow_path, inputs=flow_inputs)
print(f"Flow outputs: {flow_result}")

# Test node in the flow
node_name = "fetch_text_content_from_url"  # The node name in the flow.
node_inputs = {"url": "https://www.youtube.com/watch?v=o5ZQyXaAv1g"}  # The inputs of the node.
node_result = pf.test(flow=flow_path, inputs=node_inputs, node=node_name)
print(f"Node outputs: {node_result}")

Flow test outputs :::

:::{tab-item} VS Code Extension :sync: VS Code Extension

Use the code lens action on the top of the yaml editor to trigger flow test dag_yaml_flow_test

Click the run flow button on the top of the visual editor to trigger flow test. visual_editor_flow_test :::

::::

Concepts

While how LLMs work may be elusive to many developers, how LLM apps work is not - they essentially involve a series of calls to external services such as LLMs/databases/search engines, or intermediate data processing, all glued together. Thus LLM apps are merely Directed Acyclic Graphs (DAGs) of function calls. These DAGs are flows in prompt flow.
Flows

A flow in prompt flow is a DAG of functions (we call them tools). These functions/tools connected via input/output dependencies and executed based on the topology by prompt flow executor.

A flow is represented as a YAML file and can be visualized with our Prompt flow for VS Code extension. Here is an example:

flow_dag
Flow types

Prompt flow has three flow types:

    Standard flow and Chat flow: these two are for you to develop your LLM application. The primary difference between the two lies in the additional support provided by the "Chat Flow" for chat applications. For instance, you can define chat_history, chat_input, and chat_output for your flow. The prompt flow, in turn, will offer a chat-like experience (including conversation history) during the development of the flow. Moreover, it also provides a sample chat application for deployment purposes.
    Evaluation flow is for you to test/evaluate the quality of your LLM application (standard/chat flow). It usually run on the outputs of standard/chat flow, and compute some metrics that can be used to determine whether the standard/chat flow performs well. E.g. is the answer accurate? is the answer fact-based?

When to use standard flow vs. chat flow?

As a general guideline, if you are building a chatbot that needs to maintain conversation history, try chat flow. In most other cases, standard flow should serve your needs.


Tools

Tools are the fundamental building blocks of a flow.

Each tool is an executable unit, basically a function to performs various tasks including but not limited to:

    Accessing LLMs for various purposes
    Querying databases
    Getting information from search engines
    Pre/post processing of data

Prompt flow provides 3 basic tools:

    LLM: The LLM tool allows you to write custom prompts and leverage large language models to achieve specific goals, such as summarizing articles, generating customer support responses, and more.
    Python: The Python tool enables you to write custom Python functions to perform various tasks, such as fetching web pages, processing intermediate data, calling third-party APIs, and more.
    Prompt: The Prompt tool allows you to prepare a prompt as a string for more complex use cases or for use in conjunction with other prompt tools or python tools.

More tools

Our partners also contributes other useful tools for advanced scenarios, here are some links:

    Vector DB Lookup: vector search tool that allows users to search top k similar vectors from vector database.
    Faiss Index Lookup: querying within a user-provided Faiss-based vector store.

Custom tools

You can create your own tools that can be shared with your team or anyone in the world. Learn more on Create and Use Tool Package


With prompt flow, you can use variants to tune your prompt. In this article, you'll learn the prompt flow variants concept.
Variants

A variant refers to a specific version of a tool node that has distinct settings. Currently, variants are supported only in the LLM tool. For example, in the LLM tool, a new variant can represent either a different prompt content or different connection settings.

Suppose you want to generate a summary of a news article. You can set different variants of prompts and settings like this:
Variants 	Prompt 	Connection settings
Variant 0 	Summary: {{input sentences}} 	Temperature = 1
Variant 1 	Summary: {{input sentences}} 	Temperature = 0.7
Variant 2 	What is the main point of this article? {{input sentences}} 	Temperature = 1
Variant 3 	What is the main point of this article? {{input sentences}} 	Temperature = 0.7

By utilizing different variants of prompts and settings, you can explore how the model responds to various inputs and outputs, enabling you to discover the most suitable combination for your requirements.
Benefits of using variants

    Enhance the quality of your LLM generation: By creating multiple variants of the same LLM node with diverse prompts and configurations, you can identify the optimal combination that produces high-quality content aligned with your needs.
    Save time and effort: Even slight modifications to a prompt can yield significantly different results. It's crucial to track and compare the performance of each prompt version. With variants, you can easily manage the historical versions of your LLM nodes, facilitating updates based on any variant without the risk of forgetting previous iterations. This saves you time and effort in managing prompt tuning history.
    Boost productivity: Variants streamline the optimization process for LLM nodes, making it simpler to create and manage multiple variations. You can achieve improved results in less time, thereby increasing your overall productivity.
    Facilitate easy comparison: You can effortlessly compare the results obtained from different variants side by side, enabling you to make data-driven decisions regarding the variant that generates the best outcomes.


Design principles

When we started this project, LangChain already became popular esp. after the ChatGPT launch. One of the questions we’ve been asked is what’s the difference between prompt flow and LangChain. This article is to elucidate the reasons for building prompt flow and the deliberate design choices we have made. To put it succinctly, prompt flow is a suite of development tools for you to build LLM apps with a strong emphasis of quality through experimentations, not a framework - which LangChain is.

While LLM apps are mostly in exploration stage, Microsoft started in this area a bit earlier and we’ve had the opportunity to observe how developers are integrating LLMs into existing systems or build new applications. These invaluable insights have shaped the fundamental design principles of prompt flow.
1. Expose the prompts vs. hiding them

The core essence of LLM applications lies in the prompts themselves, at least for today. When developing a reasonably complex LLM application, the majority of development work should be “tuning” the prompts (note the intentional use of the term "tuning," which we will delve into further later on). Any framework or tool trying to help in this space should focus on making prompt tuning easier and more straightforward. On the other hand, prompts are very volatile, it's unlikely to write a single prompt that can work across different models or even different version of same models. Building a successful LLM-based application, you have to understand every prompt introduced, so that you can tune it when necessary. LLM is simply not powerful or deterministic enough that you can use a prompt written by others like you use libraries in traditional programming languages.

In this context, any design that tries to provide a smart function or agent by encapsulating a few prompts in a library is unlikely to yield favorable results in real-world scenarios. And hiding prompts inside a library’s code base only makes it’s hard for people to improve or tailor the prompts to suit their specific needs.

Prompt flow, being positioned as a tool, refrains from wrapping any prompts within its core codebase. The only place you will see prompts are our sample flows, which are, of course, available for adoption and utilization. Every prompt should be authored and controlled by the developers themselves, rather than relying on us.
2. A new way of work

LLMs possess remarkable capabilities that enable developers to enhance their applications without delving deep into the intricacies of machine learning. In the meantime, LLMs make these apps more stochastic, which pose new challenges to application development. Merely asserting "no exception" or "result == x" in gated tests is no longer sufficient. Adopting a new methodology and employing new tools becomes imperative to ensure the quality of LLM applications — an entirely novel way of working is required.

At the center of this paradigm shift is evaluation, a term frequently used in machine learning space, refers to the process of assessing the performance and quality of a trained model. It involves measuring how well the model performs on a given task or dataset, which plays a pivotal role in understanding the model's strengths, weaknesses, and overall effectiveness. Evaluation metrics and techniques vary depending on the specific task and problem domain. Some common metrics include accuracy, precision and recall, you probably already familiar with. Now the LLM apps share similarities with machine learning models, they requires an evaluation-centric approach integrated into the development workflow, with a robust set of metrics and evaluation forming the foundation for ensuring the quality of LLM applications.

Prompt flow offers a range of tools to streamline the new way of work:

    Develop your evaluation program as Evaluation flow to calculate metrics for your app/flow, learn from our sample evaluation flows.
    Iterate on your application flow and run evaluation flows via the SDK/CLI, allowing you to compare metrics and choose the optimal candidate for release. These iterations include trying different prompts, different LLM parameters like temperature etc. - this is referred as “tuning” process earlier, or sometime referred as experimentation.
    Integrate the evaluation into your CI/CD pipeline, aligning the assertions in your gated tests with the selected metrics.

Prompt flow introduces two conceptual components to facilitate this workflow:

    Evaluation flow: a flow type that indicates this flow is not for deploy or integrate into your app, it’s for evaluating an app/flow performance.
    Run: every time you run your flow with data, or run an evaluation on the output of a flow, a Run object is created to manage the history and allow for comparison and additional analysis.

While new concepts introduce additional cognitive load, we firmly believe they hold greater importance compared to abstracting different LLM APIs or vector database APIs.
3. Optimize for “visibility”

There are quite some interesting application patterns emerging because of LLMs, like Retrieval Augmented Generation (RAG), ReAct and more. Though how LLMs work may remain enigmatic to many developers, how LLM apps work is not - they essentially involve a series of calls to external services such as LLMs, databases, and search engines, all glued together. Architecturally there isn’t much new, patterns like RAG and ReAct are both straightforward to implement once a developer understands what they are - plain Python programs with API calls to external services can totally serve the purpose effectively.

By observing many internal use cases, we learned that deeper insight into the detail of the execution is critical. Establishing a systematic method for tracking interactions with external systems is one of design priority. Consequently, We adopted an unconventional approach - prompt flow has a YAML file describing how function calls (we call them Tools) are executed and connected into a Directed Acyclic Graph (DAG).

This approach offers several key benefits, primarily centered around enhanced visibility:

    During development, your flow can be visualized in an intelligible manner, enabling clear identification of any faulty components. As a byproduct, you obtain an architecturally descriptive diagram that can be shared with others.
    Each node in the flow has it’s internal detail visualized in a consistent way.
    Single nodes can be individually run or debugged without the need to rerun previous nodes.

promptflow-dag

The emphasis on visibility in prompt flow's design helps developers to gain a comprehensive understanding of the intricate details of their applications. This, in turn, empowers developers to engage in effective troubleshooting and optimization.

Despite there're some control flow features like "activate-when" to serve the needs of branches/switch-case, we do not intend to make Flow itself Turing-complete. If you want to develop an agent which is fully dynamic and guided by LLM, leveraging Semantic Kernel together with prompt flow would be a favorable option.


In prompt flow, you can utilize connections to securely manage credentials or secrets for external services.
Connections

Connections are for storing information about how to access external services like LLMs: endpoint, api keys etc.

    In your local development environment, the connections are persisted in your local machine with keys encrypted.
    In Azure AI, connections can be configured to be shared across the entire workspace. Secrets associated with connections are securely persisted in the corresponding Azure Key Vault, adhering to robust security and compliance standards.

Prompt flow provides a variety of pre-built connections, including Azure Open AI, Open AI, etc. These pre-built connections enable seamless integration with these resources within the built-in tools. Additionally, you have the flexibility to create custom connection types using key-value pairs, empowering them to tailor the connections to their specific requirements, particularly in Python tools.
Connection type 	Built-in tools
Azure Open AI 	LLM or Python
Open AI 	LLM or Python
Cognitive Search 	Vector DB Lookup or Python
Serp 	Serp API or Python
Custom 	Python

By leveraging connections in prompt flow, you can easily establish and manage connections to external APIs and data sources, facilitating efficient data exchange and interaction within their AI applications.



HOW TO GUIDES

How to Develop a Flow
We provide guides on how to develop a flow by writing a flow yaml from scratch in this section.

Develop chat flow

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

From this document, you can learn how to develop a chat flow by writing a flow yaml from scratch. You can find additional information about flow yaml schema in Flow YAML Schema.
Flow input data

The most important elements that differentiate a chat flow from a standard flow are chat input and chat history. A chat flow can have multiple inputs, but chat history and chat input are required inputs in chat flow.

    Chat Input: Chat input refers to the messages or queries submitted by users to the chatbot. Effectively handling chat input is crucial for a successful conversation, as it involves understanding user intentions, extracting relevant information, and triggering appropriate responses.

    Chat History: Chat history is the record of all interactions between the user and the chatbot, including both user inputs and AI-generated outputs. Maintaining chat history is essential for keeping track of the conversation context and ensuring the AI can generate contextually relevant responses. Chat history is a special type of chat flow input, that stores chat messages in a structured format.

    An example of chat history:

    [
      {"inputs": {"question": "What types of container software there are?"}, "outputs": {"answer": "There are several types of container software available, including: Docker, Kubernetes"}},
      {"inputs": {"question": "What's the different between them?"}, "outputs": {"answer": "The main difference between the various container software systems is their functionality and purpose. Here are some key differences between them..."}},
    ] 

You can set is_chat_input/is_chat_history to true to add chat_input/chat_history to the chat flow.

inputs:
  chat_history:
    type: list
    is_chat_history: true
    default: []
  question:
    type: string
    is_chat_input: true
    default: What is ChatGPT?

For more information see develop the flow using different tools.
Develop the flow using different tools

In one flow, you can consume different kinds of tools. We now support built-in tool like LLM, Python and Prompt and third-party tool like Serp API, Vector Search, etc.

For more information see develop the flow using different tools.
Chain your flow - link nodes together

Before linking nodes together, you need to define and expose an interface.

For more information see chain your flow.
Set flow output

Chat output is required output in the chat flow. It refers to the AI-generated messages that are sent to the user in response to their inputs. Generating contextually appropriate and engaging chat outputs is vital for a positive user experience.

You can set is_chat_output to true to add chat_output to the chat flow.

outputs:
  answer:
    type: string
    reference: ${chat.output}
    is_chat_output: true



Develop standard flow

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

From this document, you can learn how to develop a standard flow by writing a flow yaml from scratch. You can find additional information about flow yaml schema in Flow YAML Schema.
Flow input data

The flow input data is the data that you want to process in your flow. ::::{tab-set} :::{tab-item} CLI :sync: CLI You can add a flow input in inputs section of flow yaml.

inputs:
  url:
    type: string
    default: https://www.microsoft.com/en-us/d/xbox-wireless-controller-stellar-shift-special-edition/94fbjc7h0h6h

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension When unfolding Inputs section in the authoring page, you can set and view your flow inputs, including input schema (name and type), and the input value.

flow_input :::

:::: For Web Classification sample as shown the screenshot above, the flow input is an url of string type. For more input types in a python tool, please refer to Input types.
Develop the flow using different tools

In one flow, you can consume different kinds of tools. We now support built-in tool like LLM, Python and Prompt and third-party tool like Serp API, Vector Search, etc.
Add tool as your need

::::{tab-set} :::{tab-item} CLI :sync: CLI You can add a tool node in nodes section of flow yaml. For example, yaml below shows how to add a Python tool node in the flow.

nodes:
- name: fetch_text_content_from_url
  type: python
  source:
    type: code
    path: fetch_text_content_from_url.py
  inputs:
    url: ${inputs.url}

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension By selecting the tool card on the very top, you'll add a new tool node to flow.

add_tool :::

::::
Edit tool

::::{tab-set} :::{tab-item} CLI :sync: CLI You can edit the tool by simply opening the source file and making edits. For example, we provide a simple Python tool code below.

from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
  return 'hello ' + input1

We also provide an LLM tool prompt below.

Please summarize the following text in one paragraph. 100 words.
Do not add any information that is not in the text.
Text: {{text}}
Summary:

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension When a new tool node is added to flow, it will be appended at the bottom of flatten view with a random name by default. At the top of each tool node card, there's a toolbar for adjusting the tool node. You can move it up or down, you can delete or rename it too. For a python tool node, you can edit the tool code by clicking the code file. For a LLM tool node, you can edit the tool prompt by clicking the prompt file and adjust input parameters like connection, api and etc. edit_tool :::

::::
Create connection

Please refer to the Create necessary connections for details.
Chain your flow - link nodes together

Before linking nodes together, you need to define and expose an interface.
Define LLM node interface

LLM node has only one output, the completion given by LLM provider.

As for inputs, we offer a templating strategy that can help you create parametric prompts that accept different input values. Instead of fixed text, enclose your input name in {{}}, so it can be replaced on the fly. We use Jinja as our templating language. For example:

Your task is to classify a given url into one of the following types:
Movie, App, Academic, Channel, Profile, PDF or None based on the text content information.
The classification will be based on the url, the webpage text content summary, or both.

Here are a few examples:
{% for ex in examples %}
URL: {{ex.url}}
Text content: {{ex.text_content}}
OUTPUT:
{"category": "{{ex.category}}", "evidence": "{{ex.evidence}}"}

{% endfor %}

For a given URL : {{url}}, and text content: {{text_content}}.
Classify above url to complete the category and indicate evidence.
OUTPUT:

Define Python node interface

Python node might have multiple inputs and outputs. Define inputs and outputs as shown below. If you have multiple outputs, remember to make it a dictionary so that the downstream node can call each key separately. For example:

import json
from promptflow import tool

@tool
def convert_to_dict(input_str: str, input_str2: str) -> dict:
    try:
        print(input_str2)
        return json.loads(input_str)
    except Exception as e:
        print("input is not valid, error: {}".format(e))
        return {"category": "None", "evidence": "None"}

Link nodes together

After the interface is defined, you can use:

    ${inputs.key} to link with flow input.
    ${upstream_node_name.output} to link with single-output upstream node.
    ${upstream_node_name.output.key} to link with multi-output upstream node.

Below are common scenarios for linking nodes together.
Scenario 1 - Link LLM node with flow input and single-output upstream node

After you add a new LLM node and edit the prompt file like Define LLM node interface, three inputs called url, examples and text_content are created in inputs section.

::::{tab-set} :::{tab-item} CLI :sync: CLI You can link the LLM node input with flow input by ${inputs.url}. And you can link examples to the upstream prepare_examples node and text_content to the summarize_text_content node by ${prepare_examples.output} and ${summarize_text_content.output}.

- name: classify_with_llm
  type: llm
  source:
    type: code
    path: classify_with_llm.jinja2
  inputs:
    deployment_name: text-davinci-003
    suffix: ""
    max_tokens: 128
    temperature: 0.2
    top_p: 1
    echo: false
    presence_penalty: 0
    frequency_penalty: 0
    best_of: 1
    url: ${inputs.url}    # Link with flow input
    examples: ${prepare_examples.output} # Link LLM node with single-output upstream node
    text_content: ${summarize_text_content.output} # Link LLM node with single-output upstream node

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension In the value drop-down, select ${inputs.url}, ${prepare_examples.output} and ${summarize_text_content.output}, then you'll see in the graph view that the newly created LLM node is linked to the flow input, upstream prepare_examples and summarize_text_content node.

link_llm_with_flow_input_single_output_node :::

:::: When running the flow, the url input of the node will be replaced by flow input on the fly, and the examples and text_content input of the node will be replaced by prepare_examples and summarize_text_content node output on the fly.
Scenario 2 - Link LLM node with multi-output upstream node

Suppose we want to link the newly created LLM node with covert_to_dict Python node whose output is a dictionary with two keys: category and evidence. ::::{tab-set} :::{tab-item} CLI :sync: CLI You can link examples to the evidence output of upstream covert_to_dict node by ${convert_to_dict.output.evidence} like below:

- name: classify_with_llm
  type: llm
  source:
    type: code
    path: classify_with_llm.jinja2
  inputs:
    deployment_name: text-davinci-003
    suffix: ""
    max_tokens: 128
    temperature: 0.2
    top_p: 1
    echo: false
    presence_penalty: 0
    frequency_penalty: 0
    best_of: 1
    text_content: ${convert_to_dict.output.evidence} # Link LLM node with multi-output upstream node

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension In the value drop-down, select ${convert_to_dict.output}, then manually append evidence, then you'll see in the graph view that the newly created LLM node is linked to the upstream convert_to_dict node.

link_llm_with_multi_output_node ::: :::: When running the flow, the text_content input of the node will be replaced by evidence value from convert_to_dict node output dictionary on the fly.
Scenario 3 - Link Python node with upstream node/flow input

After you add a new Python node and edit the code file like Define Python node interface], two inputs called input_str and input_str2 are created in inputs section. The linkage is the same as LLM node, using ${flow.input_name} to link with flow input or ${upstream_node_name.output} to link with upstream node.

::::{tab-set} :::{tab-item} CLI :sync: CLI

- name: prepare_examples
  type: python
  source:
    type: code
    path: prepare_examples.py
  inputs:
    input_str: ${inputs.url}  # Link Python node with flow input
    input_str2: ${fetch_text_content_from_url.output} # Link Python node with single-output upstream node

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

link_python_with_flow_node_input :::

:::: When running the flow, the input_str input of the node will be replaced by flow input on the fly and the input_str2 input of the node will be replaced by fetch_text_content_from_url node output dictionary on the fly.
Set flow output

When the flow is complicated, instead of checking outputs on each node, you can set flow output and check outputs of multiple nodes in one place. Moreover, flow output helps:

    Check bulk test results in one single table.
    Define evaluation interface mapping.
    Set deployment response schema.

::::{tab-set} :::{tab-item} CLI :sync: CLI You can add flow outputs in outputs section of flow yaml . The linkage is the same as LLM node, using ${convert_to_dict.output.category} to link category flow output with with category value of upstream node convert_to_dict.

outputs:
  category:
    type: string
    reference: ${convert_to_dict.output.category}
  evidence:
    type: string
    reference: ${convert_to_dict.output.evidence}

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension First define flow output schema, then select in drop-down the node whose output you want to set as flow output. Since convert_to_dict has a dictionary output with two keys: category and evidence, you need to manually append category and evidence to each. Then run flow, after a while, you can check flow output in a table.

flow_output :::

::::



Develop evaluation flow

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

The evaluation flow is a flow to test/evaluate the quality of your LLM application (standard/chat flow). It usually runs on the outputs of standard/chat flow, and compute key metrics that can be used to determine whether the standard/chat flow performs well. See Flows for more information.

Before proceeding with this document, it is important to have a good understanding of the standard flow. Please make sure you have read Develop standard flow, since they share many common features and these features won't be repeated in this doc, such as:

    Inputs/Outputs definition
    Nodes
    Chain nodes in a flow

While the evaluation flow shares similarities with the standard flow, there are some important differences that set it apart. The main distinctions are as follows:

    Inputs from an existing run: The evaluation flow contains inputs that are derived from the outputs of the standard/chat flow. These inputs are used for evaluation purposes.
    Aggregation node: The evaluation flow contains one or more aggregation nodes, where the actual evaluation takes place. These nodes are responsible for computing metrics and determining the performance of the standard/chat flow.

Evaluation flow example

In this guide, we use eval-classification-accuracy flow as an example of the evaluation flow. This is a flow illustrating how to evaluate the performance of a classification flow. It involves comparing each prediction to the groundtruth and assigns a Correct or Incorrect grade, and aggregating the results to produce metrics such as accuracy, which reflects how good the system is at classifying the data.
Flow inputs

The flow eval-classification-accuracy contains two inputs:

inputs:
  groundtruth:
    type: string
    description: Groundtruth of the original question, it's the correct label that you hope your standard flow could predict.
    default: APP
  prediction:
    type: string
    description: The actual predicted outputs that your flow produces.
    default: APP

As evident from the inputs description, the evaluation flow requires two specific inputs:

    groundtruth: This input represents the actual or expected values against which the performance of the standard/chat flow will be evaluated.
    prediction: The prediction input is derived from the outputs of another standard/chat flow. It contains the predicted values generated by the standard/chat flow, which will be compared to the groundtruth values during the evaluation process.

From the definition perspective, there is no difference compared with adding an input/output in a standard/chat flow. However when running an evaluation flow, you may need to specify the data source from both data file and flow run outputs. For more details please refer to Run and evaluate a flow.
Aggregation node

Before introducing the aggregation node, let's see what a regular node looks like, we use node grade in the example flow for instance:

- name: grade
  type: python
  source:
    type: code
    path: grade.py
  inputs:
    groundtruth: ${inputs.groundtruth}
    prediction: ${inputs.prediction}

It takes both groundtruth and prediction from the flow inputs, compare them in the source code to see if they match:

from promptflow import tool

@tool
def grade(groundtruth: str, prediction: str):
    return "Correct" if groundtruth.lower() == prediction.lower() else "Incorrect"

When it comes to an aggregation node, there are two key distinctions that set it apart from a regular node:

    It has an attribute aggregation set to be true.

- name: calculate_accuracy
  type: python
  source:
    type: code
    path: calculate_accuracy.py
  inputs:
    grades: ${grade.output}
  aggregation: true  # Add this attribute to make it an aggregation node

    Its source code accepts a List type parameter which is a collection of the previous regular node's outputs.

from typing import List
from promptflow import log_metric, tool

@tool
def calculate_accuracy(grades: List[str]):
    result = []
    for index in range(len(grades)):
        grade = grades[index]
        result.append(grade)

    # calculate accuracy for each variant
    accuracy = round((result.count("Correct") / len(result)), 2)
    log_metric("accuracy", accuracy)

    return result

The parameter grades in above function, contains all results that are produced by the regular node grade. Assuming the referred standard flow run has 3 outputs:

{"prediction": "App"}
{"prediction": "Channel"}
{"prediction": "Academic"}

And we provides a data file like this:

{"groundtruth": "App"}
{"groundtruth": "Channel"}
{"groundtruth": "Wiki"}

Then the grades value would be ["Correct", "Correct", "Incorrect"], and the final accuracy is 0.67.

This example provides a straightforward demonstration of how to evaluate the classification flow. Once you have a solid understanding of the evaluation mechanism, you can customize and design your own evaluation method to suit your specific needs.
More about the list parameter

What if the number of referred standard flow run outputs does not match the provided data file? We know that a standard flow can be executed against multiple line data and some of them could fail while others succeed. Consider the same standard flow run mentioned in above example but the 2nd line run has failed, thus we have below run outputs:

{"prediction": "App"}
{"prediction": "Academic"}

The promptflow flow executor has the capability to recognize the index of the referred run's outputs and extract the corresponding data from the provided data file. This means that during the execution process, even if the same data file is provided(3 lines), only the specific data mentioned below will be processed:

{"groundtruth": "App"}
{"groundtruth": "Wiki"}

In this case, the grades value would be ["Correct", "Incorrect"] and the accuracy is 0.5.
How to set aggregation node in VS Code Extention

img
How to log metrics

:::{admonition} Limitation You can only log metrics in an aggregation node, otherwise the metric will be ignored. ::: Promptflow supports logging and tracking experiments using log_metric function. A metric is a key-value pair that records a single float measure. In a python node, you can log a metric with below code:

from typing import List
from promptflow import log_metric, tool

@tool
def example_log_metrics(grades: List[str]):
    # this node is an aggregation node so it accepts a list of grades
    metric_key = "accuracy"
    metric_value = round((grades.count("Correct") / len(result)), 2)
    log_metric(metric_key, metric_value)

After the run is completed, you can run pf run show-metrics -n <run_name> to see the metrics.


Referencing external files/folders in a flow

Sometimes, pre-existing code assets are essential for the flow reference. In most cases, you can accomplish this by importing a Python package into your flow. However, if a Python package is not available or it is heavy to create a package, you can still reference external files or folders located outside of the current flow folder by using our additional includes feature in your flow configuration.

This feature provides an efficient mechanism to list relative file or folder paths that are outside of the flow folder, integrating them seamlessly into your flow.dag.yaml. For example:

additional_includes:
- ../web-classification/classify_with_llm.jinja2
- ../web-classification/convert_to_dict.py
- ../web-classification/fetch_text_content_from_url.py
- ../web-classification/prepare_examples.py
- ../web-classification/summarize_text_content.jinja2
- ../web-classification/summarize_text_content__variant_1.jinja2

You can add this field additional_includes into the flow.dag.yaml. The value of this field is a list of the relative file/folder path to the flow folder.

Just as with the common definition of the tool node entry, you can define the tool node entry in the flow.dag.yaml using only the file name, eliminating the need to specify the relative path again. For example:

nodes:
- name: fetch_text_content_from_url
  type: python
  source:
    type: code
    path: fetch_text_content_from_url.py
  inputs:
    url: ${inputs.url}
- name: summarize_text_content
  use_variants: true
- name: prepare_examples
  type: python
  source:
    type: code
    path: prepare_examples.py
  inputs: {}

The entry file "fetch_text_content_from_url.py" of the tool node "fetch_text_content_from_url" is located in "../web-classification/fetch_text_content_from_url.py", as specified in the additional_includes field. The same applies to the "summarize_text_content" tool nodes.

    Note:

        If you have two files with the same name located in different folders specified in the additional_includes field, and the file name is also specified as the entry of a tool node, the system will reference the last one it encounters in the additional_includes field.

            If you have a file in the flow folder with the same name as a file specified in the additional_includes field, the system will prioritize the file listed in the additional_includes field. Take the following YAML structure as an example:

additional_includes:
- ../web-classification/prepare_examples.py
- ../tmp/prepare_examples.py
...
nodes:
- name: summarize_text_content
  use_variants: true
- name: prepare_examples
  type: python
  source:
    type: code
    path: prepare_examples.py
  inputs: {}

In this case, the system will use "../tmp/prepare_examples.py" as the entry file for the tool node "prepare_examples". Even if there is a file named "prepare_examples.py" in the flow folder, the system will still use the file "../tmp/prepare_examples.py" specified in the additional_includes field.

    Tips: The additional includes feature can significantly streamline your workflow by eliminating the need to manually handle these references.

        To get a hands-on experience with this feature, practice with our sample flow-with-additional-includes.
        You can learn more about How the 'additional includes' flow operates during the transition to the cloud.



Develop a tool

We provide guides on how to develop a tool and use it.

Adding a Tool Icon

A tool icon serves as a graphical representation of your tool in the user interface (UI). Follow this guidance to add a custom tool icon when developing your own tool package.

Adding a custom tool icon is optional. If you do not provide one, the system uses a default icon.
Prerequisites

    Please ensure that your Prompt flow for VS Code is updated to version 1.4.2 or later.

    Create a tool package as described in Create and Use Tool Package.

    Prepare custom icon image that meets these requirements:
        Use PNG, JPG or BMP format.
        16x16 pixels to prevent distortion when resizing.
        Avoid complex images with lots of detail or contrast, as they may not resize well.

    See this example as a reference.

    Install dependencies to generate icon data URI:

    pip install pillow

Add tool icon with icon parameter

Run the command below in your tool project directory to automatically generate your tool YAML, use -i or --icon parameter to add a custom tool icon:

python <promptflow github repo>\scripts\tool\generate_package_tool_meta.py -m <tool_module> -o <tool_yaml_path> -i <tool-icon-path>

Here we use an existing tool project as an example.

cd D:\proj\github\promptflow\examples\tools\tool-package-quickstart

python D:\proj\github\promptflow\scripts\tool\generate_package_tool_meta.py -m my_tool_package.tools.my_tool_1 -o my_tool_package\yamls\my_tool_1.yaml -i my_tool_package\icons\custom-tool-icon.png

In the auto-generated tool YAML file, the custom tool icon data URI is added in the icon field:

my_tool_package.tools.my_tool_1.my_tool:
  function: my_tool
  icon: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACR0lEQVR4nKWS3UuTcRTHP79nm9ujM+fccqFGI5viRRpjJgkJ3hiCENVN/QMWdBHUVRdBNwX9ARHd2FVEWFLRjaS9XPmSC/EFTNOWc3Pi48y9PHNzz68L7UXTCvreHM65+PA953uElFLyHzLvHMwsJrnzfJqFeAan3cKV9mr8XseeAOXX5vqjSS53jdF+tIz1nIFAMDCzwpvJ5b87+LSYYHw+gcWkEAwluXnOR2Q1R+9YjJ7BKJG4zoXmqr0ddL3+QnV5EeUOK821LsJammcjEeZiafJScrd3bm8H6zkDd4mVztZKAK49/Mj8is4Z/35GPq9R5VJ5GYztDtB1HT1vovGQSiqVAqDugI3I6jpP3i9x9VQVfu8+1N/OvbWCqqqoBSa6h1fQNA1N0xiYTWJSBCZF8HgwSjQapbRQ2RUg5NYj3O6ZochmYkFL03S4mImIzjFvCf2xS5gtCRYXWvBUvKXjyEVeTN/DXuDgxsnuzSMK4HTAw1Q0hZba4NXEKp0tbpq9VkxCwTAETrsVwxBIBIYhMPI7YqyrtONQzSznJXrO4H5/GJ9LUGg0YFYydJxoYnwpj1s9SEN5KzZz4fYYAW6dr+VsowdFgamlPE/Hs8SzQZYzg0S+zjIc6iOWDDEc6uND+N12B9/VVu+mrd79o38wFCCdTeBSK6hxBii1eahxBlAtRbsDdmoiHGRNj1NZ7GM0NISvzM9oaIhiqwOO/wMgl4FsRpLf2KxGXpLNSLLInzH+CWBIA6RECIGUEiEUpDRACBSh8A3pXfGWdXfMgAAAAABJRU5ErkJggg==
  inputs:
    connection:
      type:
      - CustomConnection
    input_text:
      type:
      - string
  module: my_tool_package.tools.my_tool_1
  name: my_tool
  type: python

Verify the tool icon in VS Code extension

Follow steps to use your tool from VS Code extension. Your tool displays with the custom icon:
custom-tool-with-icon-in-extension
FAQ
Can I preview the tool icon image before adding it to a tool?

Yes, you could run below command under the root folder to generate a data URI for your custom tool icon. Make sure the output file has an .html extension.

python <path-to-scripts>\tool\convert_image_to_data_url.py --image-path <image_input_path> -o <html_output_path>

For example:

python D:\proj\github\promptflow\scripts\tool\convert_image_to_data_url.py --image-path D:\proj\github\promptflow\examples\tools\tool-package-quickstart\my_tool_package\icons\custom-tool-icon.png -o output.html

The content of output.html looks like the following, open it in a web browser to preview the icon.

<html>
<body>
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACR0lEQVR4nKWS3UuTcRTHP79nm9ujM+fccqFGI5viRRpjJgkJ3hiCENVN/QMWdBHUVRdBNwX9ARHd2FVEWFLRjaS9XPmSC/EFTNOWc3Pi48y9PHNzz68L7UXTCvreHM65+PA953uElFLyHzLvHMwsJrnzfJqFeAan3cKV9mr8XseeAOXX5vqjSS53jdF+tIz1nIFAMDCzwpvJ5b87+LSYYHw+gcWkEAwluXnOR2Q1R+9YjJ7BKJG4zoXmqr0ddL3+QnV5EeUOK821LsJammcjEeZiafJScrd3bm8H6zkDd4mVztZKAK49/Mj8is4Z/35GPq9R5VJ5GYztDtB1HT1vovGQSiqVAqDugI3I6jpP3i9x9VQVfu8+1N/OvbWCqqqoBSa6h1fQNA1N0xiYTWJSBCZF8HgwSjQapbRQ2RUg5NYj3O6ZochmYkFL03S4mImIzjFvCf2xS5gtCRYXWvBUvKXjyEVeTN/DXuDgxsnuzSMK4HTAw1Q0hZba4NXEKp0tbpq9VkxCwTAETrsVwxBIBIYhMPI7YqyrtONQzSznJXrO4H5/GJ9LUGg0YFYydJxoYnwpj1s9SEN5KzZz4fYYAW6dr+VsowdFgamlPE/Hs8SzQZYzg0S+zjIc6iOWDDEc6uND+N12B9/VVu+mrd79o38wFCCdTeBSK6hxBii1eahxBlAtRbsDdmoiHGRNj1NZ7GM0NISvzM9oaIhiqwOO/wMgl4FsRpLf2KxGXpLNSLLInzH+CWBIA6RECIGUEiEUpDRACBSh8A3pXfGWdXfMgAAAAABJRU5ErkJggg==" alt="My Image">
</body>
</html>

Can I add a tool icon to an existing tool package?

Yes, you can refer to the preview icon section to generate the data URI and manually add the data URI to the tool's YAML file.
Can I add tool icons for dark and light mode separately?

Yes, you can add the tool icon data URIs manually or run the command below in your tool project directory to automatically generate your tool YAML, use --icon-light to add a custom tool icon for the light mode and use --icon-dark to add a custom tool icon for the dark mode:

python <promptflow github repo>\scripts\tool\generate_package_tool_meta.py -m <tool_module> -o <tool_yaml_path> --icon-light <light-tool-icon-path> --icon-dark <dark-tool-icon-path>

Here we use an existing tool project as an example.

cd D:\proj\github\promptflow\examples\tools\tool-package-quickstart

python D:\proj\github\promptflow\scripts\tool\generate_package_tool_meta.py -m my_tool_package.tools.my_tool_1 -o my_tool_package\yamls\my_tool_1.yaml --icon-light my_tool_package\icons\custom-tool-icon-light.png --icon-dark my_tool_package\icons\custom-tool-icon-dark.png

In the auto-generated tool YAML file, the light and dark tool icon data URIs are added in the icon field:

my_tool_package.tools.my_tool_1.my_tool:
  function: my_tool
  icon:
    dark: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAB00lEQVR4nI1SO2iTURT+7iNNb16a+Cg6iJWqRKwVRIrWV6GVUkrFdqiVShBaxIIi4iY4iouDoy4ODkKn4uQkDs5FfEzFYjEtJYQo5P/z35j/3uNw7Z80iHqHC/ec8z3OuQeMMcYYAHenU8n84YMAABw7mo93dEQpAIyBAyAiF1Kq8/Wrl5fHR1x6tjC9uPBcSrlZD4BxIgIgBCei+bnC6cGxSuWHEEIIUa58H7l0dWZqwlqSUjhq7oDWEoAL584Y6ymljDHGmM543BhvaPAsAKLfEjIyB6BeryPw796+EWidUInr16b5z6rWAYCmKXeEEADGRy+SLgXlFfLWbbWoyytULZ4f6Hee2yDgnAG4OVsoff20try08eX92vLSzJVJAJw3q7dISSnDMFx48UypeCa97cPHz7fu3Y/FYo1Go8nbCiAiIUStVus/eaKvN691IAQnsltI24wZY9Kp1Ju373K5bDKZNMa6gf5ZIWrG9/0g0K3W/wYIw3Dvnq6dO7KNMPwvgOf5x3uPHOrp9n3/HwBrLYCu3bv6Tg0PjU0d2L8PAEWfDKCtac6YIVrfKN2Zn8tkUqvfigBaR88Ya66uezMgl93+9Mmjxw8fJBIqWv7NAvwCHeuq7gEPU/QAAAAASUVORK5CYII=
    light: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAB2UlEQVR4nH1SO2hUQRQ9c18K33u72cXs7jOL8UeQCCJoJaIgKAiCWKilaGNlYREFDRGNjayVWKiFFmITECFKJKIokQRRsDFENoooUchHU5qdWZ2512KymxcNOcUwc5nDuefeA2FhZpGFU0S0Mf5S0zpdF2FhISgopUREKfXj59yhoycmPn4GAKDncuXa9VtKKWYGACgowHOdc9a6g0eOA7mx8apzzlp76vRZoGXw6XMRsdb6nwSAmYnoQ3Xi5fBIdk2SiSMiCoKgNZslteruvX4ASikvSwAEAGDqdYhAXO+VypevkwODQ4+HnlGcq2mDNLwtZq5pvWP3AYRJ0Lq2uG5rWNgYFjaBVt+8c19E/jRaWvQgImPj1e279ufaN8elzly5K1/u6r7QZ51zrjmoBqHJ+TU/39ax5cy5i53bdnb39KXtLpr28OMLgiCfz78YHpmemi0W2piZWdIWaMmDCIDWet/ePUlS0toQUWM8yxG8jrVuw/qOTBw19rUiQUQoCGZm50z9txf8By3/K0Rh+PDRk8lv3+MoWklBBACmpmdKxcKn96O3b1SqC6FSyxOUgohk4pjZ9T8YeDX6ptye+PoSpNIrfkGv3747fOzk+UtXjTE+BM14M8tfl7BQR9VzUXEAAAAASUVORK5CYII=
  inputs:
    connection:
      type:
      - CustomConnection
    input_text:
      type:
      - string
  module: my_tool_package.tools.my_tool_1
  name: my_tool
  type: python

Note: Both light and dark icons are optional. If you set either a light or dark icon, it will be used in its respective mode, and the system default icon will be used in the other mode.

Adding Category and Tags for Tool

This document is dedicated to guiding you through the process of categorizing and tagging your tools for optimal organization and efficiency. Categories help you organize your tools into specific folders, making it much easier to find what you need. Tags, on the other hand, work like labels that offer more detailed descriptions. They enable you to quickly search and filter tools based on specific characteristics or functions. By using categories and tags, you'll not only tailor your tool library to your preferences but also save time by effortlessly finding the right tool for any task.
Attribute 	Type 	Required 	Description
category 	str 	No 	Organizes tools into folders by common features.
tags 	dict 	No 	Offers detailed, searchable descriptions of tools through key-value pairs.

Important Notes:

    Tools without an assigned category will be listed in the root folder.
    Tools lacking tags will display an empty tags field.

Prerequisites

    Please ensure that your Prompt flow for VS Code is updated to version 1.1.0 or later.

How to add category and tags for a tool

Run the command below in your tool project directory to automatically generate your tool YAML, use -c or --category to add category, and use --tags to add tags for your tool:

python <promptflow github repo>\scripts\tool\generate_package_tool_meta.py -m <tool_module> -o <tool_yaml_path> --category <tool_category> --tags <tool_tags>

Here, we use an existing tool as an example. If you wish to create your own tool, please refer to the create and use tool package guide.

cd D:\proj\github\promptflow\examples\tools\tool-package-quickstart

python D:\proj\github\promptflow\scripts\tool\generate_package_tool_meta.py -m my_tool_package.tools.my_tool_1 -o my_tool_package\yamls\my_tool_1.yaml --category "test_tool" --tags "{'tag1':'value1','tag2':'value2'}"

In the auto-generated tool YAML file, the category and tags are shown as below:

my_tool_package.tools.my_tool_1.my_tool:
  function: my_tool
  inputs:
    connection:
      type:
      - CustomConnection
    input_text:
      type:
      - string
  module: my_tool_package.tools.my_tool_1
  name: My First Tool
  description: This is my first tool
  type: python
  # Category and tags are shown as below.
  category: test_tool
  tags:
    tag1: value1
    tag2: value2

Tool with category and tags experience in VS Code extension

Follow the steps to use your tool via the VS Code extension.

    Experience in the tool tree
    category_and_tags_in_tool_tree

    Experience in the tool list
    By clicking More in the visual editor, you can view your tools along with their category and tags:
    category_and_tags_in_tool_list
    Furthermore, you have the option to search or filter tools based on tags:
    filter_tools_by_tag

Create and Use Tool Package

In this document, we will guide you through the process of developing your own tool package, offering detailed steps and advice on how to utilize your creation.

The custom tool is the prompt flow tool developed by yourself. If you find it useful, you can follow this guidance to make it a tool package. This will enable you to conveniently reuse it, share it with your team, or distribute it to anyone in the world.

After successful installation of the package, your custom "tool" will show up in VSCode extension as below: custom-tool-list
Create your own tool package

Your tool package should be a python package. To try it quickly, just use my-tools-package 0.0.1 and skip this section.
Prerequisites

Create a new conda environment using python 3.9 or 3.10. Run below command to install PromptFlow dependencies:

pip install promptflow

Install Pytest packages for running tests:

pip install pytest pytest-mock

Clone the PromptFlow repository from GitHub using the following command:

git clone https://github.com/microsoft/promptflow.git

Create custom tool package

Run below command under the root folder to create your tool project quickly:

python <promptflow github repo>\scripts\tool\generate_tool_package_template.py --destination <your-tool-project> --package-name <your-package-name> --tool-name <your-tool-name> --function-name <your-tool-function-name>

For example:

python D:\proj\github\promptflow\scripts\tool\generate_tool_package_template.py --destination hello-world-proj --package-name hello-world --tool-name hello_world_tool --function-name get_greeting_message

This auto-generated script will create one tool for you. The parameters destination and package-name are mandatory. The parameters tool-name and function-name are optional. If left unfilled, the tool-name will default to hello_world_tool, and the function-name will default to tool-name.

The command will generate the tool project as follows with one tool hello_world_tool.py in it:

hello-world-proj/    
│    
├── hello_world/    
│   ├── tools/    
│   │   ├── __init__.py    
│   │   ├── hello_world_tool.py    
│   │   └── utils.py    
│   ├── yamls/    
│   │   └── hello_world_tool.yaml    
│   └── __init__.py    
│    
├── tests/     
│   ├── __init__.py    
│   └── test_hello_world_tool.py    
│    
├── MANIFEST.in    
│    
└── setup.py  

The points outlined below explain the purpose of each folder/file in the package. If your aim is to develop multiple tools within your package, please make sure to closely examine point 2 and 5.

    hello-world-proj: This is the source directory. All of your project's source code should be placed in this directory.

    hello-world/tools: This directory contains the individual tools for your project. Your tool package can contain either one tool or many tools. When adding a new tool, you should create another *_tool.py under the tools folder.

    hello-world/tools/hello_world_tool.py: Develop your tool within the def function. Use the @tool decorator to identify the function as a tool.

        [!Note] There are two ways to write a tool. The default and recommended way is the function implemented way. You can also use the class implementation way, referring to my_tool_2.py as an example.

    hello-world/tools/utils.py: This file implements the tool list method, which collects all the tools defined. It is required to have this tool list method, as it allows the User Interface (UI) to retrieve your tools and display them within the UI.

        [!Note] There's no need to create your own list method if you maintain the existing folder structure. You can simply use the auto-generated list method provided in the utils.py file.

    hello_world/yamls/hello_world_tool.yaml: Tool YAMLs defines the metadata of the tool. The tool list method, as outlined in the utils.py, fetches these tool YAMLs.

        [!Note] If you create a new tool, don't forget to also create the corresponding tool YAML. You can run below command under your tool project to auto generate your tool YAML. You may want to specify -n for name and -d for description, which would be displayed as the tool name and tooltip in prompt flow UI.

    python <promptflow github repo>\scripts\tool\generate_package_tool_meta.py -m <tool_module> -o <tool_yaml_path> -n <tool_name> -d <tool_description>

For example:

python D:\proj\github\promptflow\scripts\tool\generate_package_tool_meta.py -m hello_world.tools.hello_world_tool -o hello_world\yamls\hello_world_tool.yaml -n "Hello World Tool" -d "This is my hello world tool."

To populate your tool module, adhere to the pattern <package_name>.tools.<tool_name>, which represents the folder path to your tool within the package.

tests: This directory contains all your tests, though they are not required for creating your custom tool package. When adding a new tool, you can also create corresponding tests and place them in this directory. Run below command under your tool project:

pytest tests

MANIFEST.in: This file is used to determine which files to include in the distribution of the project. Tool YAML files should be included in MANIFEST.in so that your tool YAMLs would be packaged and your tools can show in the UI.

    [!Note] There's no need to update this file if you maintain the existing folder structure.

setup.py: This file contains metadata about your project like the name, version, author, and more. Additionally, the entry point is automatically configured for you in the generate_tool_package_template.py script. In Python, configuring the entry point in setup.py helps establish the primary execution point for a package, streamlining its integration with other software.

The package_tools entry point together with the tool list method are used to retrieve all the tools and display them in the UI.

entry_points={
      "package_tools": ["<your_tool_name> = <list_module>:<list_method>"],
},

        [!Note] There's no need to update this file if you maintain the existing folder structure.

Build and share the tool package

Execute the following command in the tool package root directory to build your tool package:

python setup.py sdist bdist_wheel

This will generate a tool package <your-package>-0.0.1.tar.gz and corresponding whl file inside the dist folder.

Create an account on PyPI if you don't already have one, and install twine package by running pip install twine.

Upload your package to PyPI by running twine upload dist/*, this will prompt you for your Pypi username and password, and then upload your package on PyPI. Once your package is uploaded to PyPI, others can install it using pip by running pip install your-package-name. Make sure to replace your-package-name with the name of your package as it appears on PyPI.

If you only want to put it on Test PyPI, upload your package by running twine upload --repository-url https://test.pypi.org/legacy/ dist/*. Once your package is uploaded to Test PyPI, others can install it using pip by running pip install --index-url https://test.pypi.org/simple/ your-package-name.
Use your tool from VSCode Extension

    Step1: Install Prompt flow for VS Code extension.

    Step2: Go to terminal and install your tool package in conda environment of the extension. Assume your conda env name is prompt-flow.

    (local_test) PS D:\projects\promptflow\tool-package-quickstart> conda activate prompt-flow
    (prompt-flow) PS D:\projects\promptflow\tool-package-quickstart> pip install .\dist\my_tools_package-0.0.1-py3-none-any.whl

    Step3: Go to the extension and open one flow folder. Click 'flow.dag.yaml' and preview the flow. Next, click + button and you will see your tools. You may need to reload the windows to clean previous cache if you don't see your tool in the list. auto-list-tool-in-extension

FAQs
Why is my custom tool not showing up in the UI?

Confirm that the tool YAML files are included in your custom tool package. You can add the YAML files to MANIFEST.in and include the package data in setup.py. Alternatively, you can test your tool package using the script below to ensure that you've packaged your tool YAML files and configured the package tool entry point correctly.

    Make sure to install the tool package in your conda environment before executing this script.
    Create a python file anywhere and copy the content below into it.

    import importlib
    import importlib.metadata

    def test():
        """List all package tools information using the `package-tools` entry point.

        This function iterates through all entry points registered under the group "package_tools."
        For each tool, it imports the associated module to ensure its validity and then prints
        information about the tool.

        Note:
        - Make sure your package is correctly packed to appear in the list.
        - The module is imported to validate its presence and correctness.

        Example of tool information printed:
        ----identifier
        {'module': 'module_name', 'package': 'package_name', 'package_version': 'package_version', ...}
        """
        entry_points = importlib.metadata.entry_points()
        if isinstance(entry_points, list):
            entry_points = entry_points.select(group=PACKAGE_TOOLS_ENTRY)
        else:
            entry_points = entry_points.get(PACKAGE_TOOLS_ENTRY, [])
        for entry_point in entry_points:
            list_tool_func = entry_point.load()
            package_tools = list_tool_func()

            for identifier, tool in package_tools.items():
                importlib.import_module(tool["module"])  # Import the module to ensure its validity
                print(f"----{identifier}\n{tool}")

    if __name__ == "__main__":
        test()

    Run this script in your conda environment. This will return the metadata of all tools installed in your local environment, and you should verify that your tools are listed.

Why am I unable to upload package to PyPI?

    Make sure that the entered username and password of your PyPI account are accurate.
    If you encounter a 403 Forbidden Error, it's likely due to a naming conflict with an existing package. You will need to choose a different name. Package names must be unique on PyPI to avoid confusion and conflicts among users. Before creating a new package, it's recommended to search PyPI (https://pypi.org/) to verify that your chosen name is not already taken. If the name you want is unavailable, consider selecting an alternative name or a variation that clearly differentiates your package from the existing one.

Advanced features

    Add a Tool Icon
    Add Category and Tags for Tool
    Create and Use Your Own Custom Strong Type Connection
    Customize an LLM Tool
    Use File Path as Tool Input
    Create a Dynamic List Tool Input
    Create Cascading Tool Inputs


Creating Cascading Tool Inputs

Cascading input settings are useful when the value of one input field determines which subsequent inputs are shown. This makes the input process more streamlined, user-friendly, and error-free. This guide will walk through how to create cascading inputs for your tools.
Prerequisites

Please make sure you have the latest version of Prompt flow for VS Code installed (v1.2.0+).
Create a tool with cascading inputs

We'll build out an example tool to show how cascading inputs work. The student_id and teacher_id inputs will be controlled by the value selected for the user_type input. Here's how to configure this in the tool code and YAML.

    Develop the tool function, following the cascading inputs example. Key points:
        Use the @tool decorator to mark the function as a tool.
        Define UserType as an Enum class, as it accepts only a specific set of fixed values in this example.
        Conditionally use inputs in the tool logic based on user_type.

from enum import Enum

from promptflow import tool


class UserType(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"


@tool
def my_tool(user_type: Enum, student_id: str = "", teacher_id: str = "") -> str:
    """This is a dummy function to support cascading inputs.

    :param user_type: user type, student or teacher.
    :param student_id: student id.
    :param teacher_id: teacher id.
    :return: id of the user.
    If user_type is student, return student_id.
    If user_type is teacher, return teacher_id.
    """
    if user_type == UserType.STUDENT:
        return student_id
    elif user_type == UserType.TEACHER:
        return teacher_id
    else:
        raise Exception("Invalid user.")

    Generate a starting YAML for your tool per the tool package guide, then update it to enable cascading:

    Add enabled_by and enabled_by_value to control visibility of dependent inputs. See the example YAML for reference.

        The enabled_by attribute specifies the input field, which must be an enum type, that controls the visibility of the dependent input field.

        The enabled_by_value attribute defines the accepted enum values from the enabled_by field that will make this dependent input field visible.

        Note: enabled_by_value takes a list, allowing multiple values to enable an input.

my_tool_package.tools.tool_with_cascading_inputs.my_tool:
  function: my_tool
  inputs:
    user_type:
      type:
      - string
      enum:
        - student
        - teacher
    student_id:
      type:
      - string
      # This input is enabled by the input "user_type".
      enabled_by: user_type
      # This input is enabled when "user_type" is "student".
      enabled_by_value: [student]
    teacher_id:
      type:
        - string
      enabled_by: user_type
      enabled_by_value: [teacher]
  module: my_tool_package.tools.tool_with_cascading_inputs
  name: My Tool with Cascading Inputs
  description: This is my tool with cascading inputs
  type: python

Use the tool in VS Code

Once you package and share your tool, you can use it in VS Code per the tool package guide. We have a demo flow you can try.

Before selecting a user_type, the student_id and teacher_id inputs are hidden. Once you pick the user_type, the corresponding input appears. before_user_type_selected.png after_user_type_selected_with_student.png after_user_type_selected_with_teacher.png
FAQs
How do I create multi-layer cascading inputs?

If you are dealing with multiple levels of cascading inputs, you can effectively manage the dependencies between them by using the enabled_by and enabled_by_value attributes. For example:

my_tool_package.tools.tool_with_multi_layer_cascading_inputs.my_tool:
  function: my_tool
  inputs:
    event_type:
      type:
      - string
      enum:
        - corporate
        - private
    corporate_theme:
      type:
      - string
      # This input is enabled by the input "event_type".
      enabled_by: event_type
      # This input is enabled when "event_type" is "corporate".
      enabled_by_value: [corporate]
      enum:
        - seminar
        - team_building
    seminar_location:
      type:
      - string
      # This input is enabled by the input "corporate_theme".
      enabled_by: corporate_theme
      # This input is enabled when "corporate_theme" is "seminar".
      enabled_by_value: [seminar]
    private_theme:
      type:
        - string
      # This input is enabled by the input "event_type".
      enabled_by: event_type
      # This input is enabled when "event_type" is "private".
      enabled_by_value: [private]
  module: my_tool_package.tools.tool_with_multi_layer_cascading_inputs
  name: My Tool with Multi-Layer Cascading Inputs
  description: This is my tool with multi-layer cascading inputs
  type: python

Inputs will be enabled in a cascading way based on selections.


Creating a Dynamic List Tool Input

Tool input options can be generated on the fly using a dynamic list. Instead of having predefined static options, the tool author defines a request function that queries backends like APIs to retrieve real-time options. This enables flexible integration with various data sources to populate dynamic options. For instance, the function could call a storage API to list current files. Rather than a hardcoded list, the user sees up-to-date options when running the tool.
Prerequisites

    Please make sure you have the latest version of Prompt flow for VS Code installed (v1.3.1+).
    Please install promptflow package and ensure that its version is 1.0.0 or later.

    pip install promptflow>=1.0.0

Create a tool input with dynamic listing
Create a list function

To enable dynamic listing, the tool author defines a request function with the following structure:

    Type: Regular Python function, can be in tool file or separate file
    Input: Accepts parameters needed to fetch options
    Output: Returns a list of option objects as List[Dict[str, Union[str, int, float, list, Dict]]]:
        Required key:
            value: Internal option value passed to tool function
        Optional keys:
            display_value: Display text shown in dropdown (defaults to value)
            hyperlink: URL to open when option clicked
            description: Tooltip text on hover

This function can make backend calls to retrieve the latest options, returning them in a standardized dictionary structure for the dynamic list. The required and optional keys enable configuring how each option appears and behaves in the tool input dropdown. See my_list_func as an example.

def my_list_func(prefix: str = "", size: int = 10, **kwargs) -> List[Dict[str, Union[str, int, float, list, Dict]]]:
    """This is a dummy function to generate a list of items.

    :param prefix: prefix to add to each item.
    :param size: number of items to generate.
    :param kwargs: other parameters.
    :return: a list of items. Each item is a dict with the following keys:
        - value: for backend use. Required.
        - display_value: for UI display. Optional.
        - hyperlink: external link. Optional.
        - description: information icon tip. Optional.
    """
    import random

    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]
    result = []
    for i in range(size):
        random_word = f"{random.choice(words)}{i}"
        cur_item = {
            "value": random_word,
            "display_value": f"{prefix}_{random_word}",
            "hyperlink": f'https://www.bing.com/search?q={random_word}',
            "description": f"this is {i} item",
        }
        result.append(cur_item)

    return result

Configure a tool input with the list function

In inputs section of tool YAML, add following properties to the input that you want to make dynamic:

    dynamic_list:
        func_path: Path to the list function (module_name.function_name).
        func_kwargs: Parameters to pass to the function, can reference other input values.
    allow_manual_entry: Allow user to enter input value manually. Default to false.
    is_multi_select: Allow user to select multiple values. Default to false.

See tool_with_dynamic_list_input.yaml as an example.

my_tool_package.tools.tool_with_dynamic_list_input.my_tool:
  function: my_tool
  inputs:
    input_text:
      type:
      - list
      dynamic_list:
        func_path: my_tool_package.tools.tool_with_dynamic_list_input.my_list_func
        func_kwargs: 
        - name: prefix  # argument name to be passed to the function
          type: 
          - string
          # if optional is not specified, default to false.
          # this is for UX pre-validaton. If optional is false, but no input. UX can throw error in advanced.
          optional: true
          reference: ${inputs.input_prefix}  # dynamic reference to another input parameter
        - name: size  # another argument name to be passed to the function
          type: 
          - int
          optional: true
          default: 10
      # enum and dynamic list may need below setting.
      # allow user to enter input value manually, default false.
      allow_manual_entry: true
      # allow user to select multiple values, default false.
      is_multi_select: true
    # used to filter 
    input_prefix:
      type:
      - string
  module: my_tool_package.tools.tool_with_dynamic_list_input
  name: My Tool with Dynamic List Input
  description: This is my tool with dynamic list input
  type: python

Use the tool in VS Code

Once you package and share your tool, you can use it in VS Code per the tool package guide. You could try my-tools-package for a quick test.

pip install my-tools-package>=0.0.8

dynamic list tool input options dynamic list tool input selected

    Note: If your dynamic list function call Azure APIs, you need to login to Azure and set default workspace. Otherwise, the tool input will be empty and you can't select anything. See FAQs for more details.

FAQs
I'm a tool author, and want to dynamically list Azure resources in my tool input. What should I pay attention to?

    Clarify azure workspace triple "subscription_id", "resource_group_name", "workspace_name" in the list function signature. System helps append workspace triple to function input parameters if they are in function signature. See list_endpoint_names as an example.

def list_endpoint_names(subscription_id, resource_group_name, workspace_name, prefix: str = "") -> List[Dict[str, str]]:
    """This is an example to show how to get Azure ML resource in tool input list function.

    :param subscription_id: Azure subscription id.
    :param resource_group_name: Azure resource group name.
    :param workspace_name: Azure ML workspace name.
    :param prefix: prefix to add to each item.
    """
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential()
    credential.get_token("https://management.azure.com/.default")

    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name)
    result = []
    for ep in ml_client.online_endpoints.list():
        hyperlink = (
            f"https://ml.azure.com/endpoints/realtime/{ep.name}/detail?wsid=/subscriptions/"
            f"{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft."
            f"MachineLearningServices/workspaces/{workspace_name}"
        )
        cur_item = {
            "value": ep.name,
            "display_value": f"{prefix}_{ep.name}",
            # external link to jump to the endpoint page.
            "hyperlink": hyperlink,
            "description": f"this is endpoint: {ep.name}",
        }
        result.append(cur_item)
    return result

    Note in your tool doc that if your tool user want to use the tool at local, they should login to azure and set ws triple as default. Or the tool input will be empty and user can't select anything.

az login
az account set --subscription <subscription_id>
az configure --defaults group=<resource_group_name> workspace=<workspace_name>

Install azure dependencies.

pip install azure-ai-ml

pip install my-tools-package[azure]>=0.0.8

dynamic list function azure
I'm a tool user, and cannot see any options in dynamic list tool input. What should I do?

If you are unable to see any options in a dynamic list tool input, you may see an error message below the input field stating:

"Unable to display list of items due to XXX. Please contact the tool author/support team for troubleshooting assistance."

If this occurs, follow these troubleshooting steps:

    Note the exact error message shown. This provides details on why the dynamic list failed to populate.
    Contact the tool author/support team and report the issue. Provide the error message so they can investigate the root cause.


Create and Use Your Own Custom Strong Type Connection

Connections provide a secure method for managing credentials for external APIs and data sources in prompt flow. This guide explains how to create and use a custom strong type connection.
What is a Custom Strong Type Connection?

A custom strong type connection in prompt flow allows you to define a custom connection class with strongly typed keys. This provides the following benefits:

    Enhanced user experience - no need to manually enter connection keys.
    Rich intellisense experience - defining key types enables real-time suggestions and auto-completion of available keys as you work in VS Code.
    Central location to view available keys and data types.

For other connections types, please refer to Connections.
Prerequisites

    Please ensure that your Prompt flow for VS Code is updated to at least version 1.2.1.
    Please install promptflow package and ensure that its version is 0.1.0b8 or later.

    pip install promptflow>=0.1.0b8

Create a custom strong type connection

Follow these steps to create a custom strong type connection:

    Define a Python class inheriting from CustomStrongTypeConnection.

    [!Note] Please avoid using the CustomStrongTypeConnection class directly.

    Use the Secret type to indicate secure keys. This enhances security by scrubbing secret keys.

    Document with docstrings explaining each key.

For example:

from promptflow.connections import CustomStrongTypeConnection
from promptflow.contracts.types import Secret


class MyCustomConnection(CustomStrongTypeConnection):
    """My custom strong type connection.

    :param api_key: The api key.
    :type api_key: Secret
    :param api_base: The api base.
    :type api_base: String
    """
    api_key: Secret
    api_base: str = "This is a fake api base."

See this example for a complete implementation.
Use the connection in a flow

Once you create a custom strong type connection, here are two ways to use it in your flows:
With Package Tools:

    Refer to the Create and Use Tool Package to build and install your tool package containing the connection.

    Develop a flow with custom tools. Please take this folder as an example.

    Create a custom strong type connection using one of the following methods:
        If the connection type hasn't been created previously, click the 'Add connection' button to create the connection. create_custom_strong_type_connection_in_node_interface
        Click the 'Create connection' plus sign in the CONNECTIONS section. create_custom_strong_type_connection_add_sign
        Click 'Create connection' plus sign in the Custom category. create_custom_strong_type_connection_in_custom_category

    Fill in the values starting with to-replace-with in the connection template. custom_strong_type_connection_template

    Run the flow with the created custom strong type connection. use_custom_strong_type_connection_in_flow

With Script Tools:

    Develop a flow with python script tools. Please take this folder as an example.

    Create a CustomConnection. Fill in the keys and values in the connection template. custom

    Run the flow with the created custom connection. use_custom_connection_in_flow

Local to cloud

When creating the necessary connections in Azure AI, you will need to create a CustomConnection. In the node interface of your flow, this connection will be displayed as the CustomConnection type.

Please refer to Run prompt flow in Azure AI for more details.

Here is an example command:

pfazure run create --subscription 96aede12-2f73-41cb-b983-6d11a904839b -g promptflow -w my-pf-eus --flow D:\proj\github\ms\promptflow\examples\flows\standard\flow-with-package-tool-using-custom-strong-type-connection --data D:\proj\github\ms\promptflow\examples\flows\standard\flow-with-package-tool-using-custom-strong-type-connection\data.jsonl --runtime test-compute

FAQs
I followed the steps to create a custom strong type connection, but it's not showing up. What could be the issue?

Once the new tool package is installed in your local environment, a window reload is necessary. This action ensures that the new tools and custom strong type connections become visible and accessible.


Customizing an LLM Tool

In this document, we will guide you through the process of customizing an LLM tool, allowing users to seamlessly connect to a large language model with prompt tuning experience using a PromptTemplate.
Prerequisites

    Please ensure that your Prompt flow for VS Code is updated to version 1.2.0 or later.

How to customize an LLM tool

Here we use an existing tool package as an example. If you want to create your own tool, please refer to create and use tool package.

    Develop the tool code as in this example.

    Add a CustomConnection input to the tool, which is used to authenticate and establish a connection to the large language model.

    Add a PromptTemplate input to the tool, which serves as an argument to be passed into the large language model.

    from jinja2 import Template
    from promptflow import tool
    from promptflow.connections import CustomConnection
    from promptflow.contracts.types import PromptTemplate


    @tool
    def my_tool(connection: CustomConnection, prompt: PromptTemplate, **kwargs) -> str:
        # Customize your own code to use the connection and prompt here.
        rendered_prompt = Template(prompt, trim_blocks=True, keep_trailing_newline=True).render(**kwargs)
        return rendered_prompt

Generate the custom LLM tool YAML.
Run the command below in your tool project directory to automatically generate your tool YAML, use -t "custom_llm" or --tool-type "custom_llm" to indicate this is a custom LLM tool:

python <promptflow github repo>\scripts\tool\generate_package_tool_meta.py -m <tool_module> -o <tool_yaml_path> -t "custom_llm"

Here we use an existing tool as an example.

cd D:\proj\github\promptflow\examples\tools\tool-package-quickstart

python D:\proj\github\promptflow\scripts\tool\generate_package_tool_meta.py -m my_tool_package.tools.tool_with_custom_llm_type -o my_tool_package\yamls\tool_with_custom_llm_type.yaml -n "My Custom LLM Tool" -d "This is a tool to demonstrate how to customize an LLM tool with a PromptTemplate." -t "custom_llm"

This command will generate a YAML file as follows:

my_tool_package.tools.tool_with_custom_llm_type.my_tool:
name: My Custom LLM Tool
description: This is a tool to demonstrate how to customize an LLM tool with a PromptTemplate.
# The type is custom_llm.
type: custom_llm
module: my_tool_package.tools.tool_with_custom_llm_type
function: my_tool
inputs:
    connection:
    type:
        - CustomConnection

Use the tool in VS Code

Follow the steps to build and install your tool package and use your tool from VS Code extension.

Here we use an existing flow to demonstrate the experience, open this flow in VS Code extension.

    There is a node named "my_custom_llm_tool" with a prompt template file. You can either use an existing file or create a new one as the prompt template file.
    use_my_custom_llm_tool


Using File Path as Tool Input

Users sometimes need to reference local files within a tool to implement specific logic. To simplify this, we've introduced the FilePath input type. This input type enables users to either select an existing file or create a new one, then pass it to a tool, allowing the tool to access the file's content.

In this guide, we will provide a detailed walkthrough on how to use FilePath as a tool input. We will also demonstrate the user experience when utilizing this type of tool within a flow.
Prerequisites

    Please install promptflow package and ensure that its version is 0.1.0b8 or later.

    pip install promptflow>=0.1.0b8

    Please ensure that your Prompt flow for VS Code is updated to version 1.1.0 or later.

Using File Path as Package Tool Input
How to create a package tool with file path input

Here we use an existing tool package as an example. If you want to create your own tool, please refer to create and use tool package.

    Add a FilePath input for your tool, like in this example.

    import importlib
    from pathlib import Path
    from promptflow import tool
    # 1. import the FilePath type
    from promptflow.contracts.types import FilePath

    # 2. add a FilePath input for your tool method
    @tool
    def my_tool(input_file: FilePath, input_text: str) -> str:
        # 3. customise your own code to handle and use the input_file here
        new_module = importlib.import_module(Path(input_file).stem)

        return new_module.hello(input_text)   

FilePath input format in a tool YAML, like in this example.

 my_tool_package.tools.tool_with_file_path_input.my_tool:
   function: my_tool
     inputs:
       # yaml format for FilePath input
       input_file:
         type:
         - file_path
       input_text:
         type:
         - string
   module: my_tool_package.tools.tool_with_file_path_input
   name: Tool with FilePath Input
   description: This is a tool to demonstrate the usage of FilePath input
   type: python   

        [!Note] tool yaml file can be generated using a python script. For further details, please refer to create custom tool package.

Use tool with a file path input in VS Code extension

Follow steps to build and install your tool package and use your tool from VS Code extension.

Here we use an existing flow to demonstrate the experience, open this flow in VS Code extension:

    There is a node named "Tool_with_FilePath_Input" with a file_path type input called input_file.

    Click the picker icon to open the UI for selecting an existing file or creating a new file to use as input.

    use file path in flow

Using File Path as Script Tool Input

We can also utilize the FilePath input type directly in a script tool, eliminating the need to create a package tool.

    Initiate an empty flow in the VS Code extension and add a python node titled 'python_node_with_filepath' into it in the Visual Editor page.

    Select the link python_node_with_filepath.py in the node to modify the python method to include a FilePath input as shown below, and save the code change.

    import importlib
    from pathlib import Path
    from promptflow import tool
    # 1. import the FilePath type
    from promptflow.contracts.types import FilePath

    # 2. add a FilePath input for your tool method
    @tool
    def my_tool(input_file: FilePath, input_text: str) -> str:
        # 3. customise your own code to handle and use the input_file here
        new_module = importlib.import_module(Path(input_file).stem)

        return new_module.hello(input_text)   

    Return to the flow Visual Editor page, click the picker icon to launch the UI for selecting an existing file or creating a new file to use as input, here we select this file as an example.

    use file path in script tool

FAQ
What are some practical use cases for this feature?

The FilePath input enables several useful workflows:

    Dynamically load modules - As shown in the demo, you can load a Python module from a specific script file selected by the user. This allows flexible custom logic.
    Load arbitrary data files - The tool can load data from files like .csv, .txt, .json, etc. This provides an easy way to inject external data into a tool.

So in summary, FilePath input gives tools flexible access to external files provided by users at runtime. This unlocks many useful scenarios like the ones above.

Run and evaluate a flow

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

After you have developed and tested the flow in init and test a flow, this guide will help you learn how to run a flow with a larger dataset and then evaluate the flow you have created.
Create a batch run

Since you have run your flow successfully with a small set of data, you might want to test if it performs well in large set of data, you can run a batch test and check the outputs.

A bulk test allows you to run your flow with a large dataset and generate outputs for each data row, and the run results will be recorded in local db so you can use pf commands to view the run results at anytime. (e.g. pf run list)

Let's create a run with flow web-classification. It is a flow demonstrating multi-class classification with LLM. Given an url, it will classify the url into one web category with just a few shots, simple summarization and classification prompts.

To begin with the guide, you need:

    Git clone the sample repository(above flow link) and set the working directory to <path-to-the-sample-repo>/examples/flows/.
    Make sure you have already created the necessary connection following Create necessary connections. ::::{tab-set}

:::{tab-item} CLI :sync: CLI

Create the run with flow and data, can add --stream to stream the run.

pf run create --flow standard/web-classification --data standard/web-classification/data.jsonl --column-mapping url='${data.url}' --stream 

Note column-mapping is a mapping from flow input name to specified values, see more details in Use column mapping.

You can also name the run by specifying --name my_first_run in above command, otherwise the run name will be generated in a certain pattern which has timestamp inside.

q_0

With a run name, you can easily view or visualize the run details using below commands:

pf run show-details -n my_first_run

q_0

pf run visualize -n my_first_run

q_0

More details can be found with pf run --help

::: :::{tab-item} SDK :sync: SDK

from promptflow import PFClient

# Please protect the entry point by using `if __name__ == '__main__':`,
# otherwise it would cause unintended side effect when promptflow spawn worker processes.
# Ref: https://docs.python.org/3/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
  # PFClient can help manage your runs and connections.
  pf = PFClient()

  # Set flow path and run input data
  flow = "standard/web-classification" # set the flow directory
  data= "standard/web-classification/data.jsonl" # set the data file

  # create a run, stream it until it's finished
  base_run = pf.run(
      flow=flow,
      data=data,
      stream=True,
      # map the url field from the data to the url input of the flow
      column_mapping={"url": "${data.url}"},
  )

q_0

# get the inputs/outputs details of a finished run.
details = pf.get_details(base_run)
details.head(10)

q_0

# visualize the run in a web browser
pf.visualize(base_run)

q_0

Feel free to check Promptflow Python Library Reference for all SDK public interfaces.

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension Use the code lens action on the top of the yaml editor to trigger batch run dag_yaml_flow_test

Click the bulk test button on the top of the visual editor to trigger flow test. visual_editor_flow_test :::

::::

We also have a more detailed documentation Manage runs demonstrating how to manage your finished runs with CLI, SDK and VS Code Extension.
Evaluate your flow

You can use an evaluation method to evaluate your flow. The evaluation methods are also flows which use Python or LLM etc., to calculate metrics like accuracy, relevance score. Please refer to Develop evaluation flow to learn how to develop an evaluation flow.

In this guide, we use eval-classification-accuracy flow to evaluate. This is a flow illustrating how to evaluate the performance of a classification system. It involves comparing each prediction to the groundtruth and assigns a Correct or Incorrect grade, and aggregating the results to produce metrics such as accuracy, which reflects how good the system is at classifying the data.
Run evaluation flow against run

::::{tab-set}

:::{tab-item} CLI :sync: CLI

Evaluate the finished flow run

After the run is finished, you can evaluate the run with below command, compared with the normal run create command, note there are two extra arguments:

    column-mapping: A mapping from flow input name to specified data values. Reference here for detailed information.
    run: The run name of the flow run to be evaluated.

More details can be found in Use column mapping.

pf run create --flow evaluation/eval-classification-accuracy --data standard/web-classification/data.jsonl --column-mapping groundtruth='${data.answer}' prediction='${run.outputs.category}' --run my_first_run --stream

Same as the previous run, you can specify the evaluation run name with --name my_first_eval_run in above command.

You can also stream or view the run details with:

pf run stream -n my_first_eval_run  # same as "--stream" in command "run create"
pf run show-details -n my_first_eval_run
pf run show-metrics -n my_first_eval_run

Since now you have two different runs my_first_run and my_first_eval_run, you can visualize the two runs at the same time with below command.

pf run visualize -n "my_first_run,my_first_eval_run"

A web browser will be opened to show the visualization result.

q_0

:::

:::{tab-item} SDK :sync: SDK

Evaluate the finished flow run

After the run is finished, you can evaluate the run with below command, compared with the normal run create command, note there are two extra arguments:

    column-mapping: A dictionary represents sources of the input data that are needed for the evaluation method. The sources can be from the flow run output or from your test dataset.
        If the data column is in your test dataset, then it is specified as ${data.<column_name>}.
        If the data column is from your flow output, then it is specified as ${run.outputs.<output_name>}.
    run: The run name or run instance of the flow run to be evaluated.

More details can be found in Use column mapping.

from promptflow import PFClient

# PFClient can help manage your runs and connections.
pf = PFClient()

# set eval flow path
eval_flow = "evaluation/eval-classification-accuracy"
data= "standard/web-classification/data.jsonl"

# run the flow with existing run
eval_run = pf.run(
    flow=eval_flow,
    data=data,
    run=base_run,
    column_mapping={  # map the url field from the data to the url input of the flow
      "groundtruth": "${data.answer}",
      "prediction": "${run.outputs.category}",
    }
)

# stream the run until it's finished
pf.stream(eval_run)

# get the inputs/outputs details of a finished run.
details = pf.get_details(eval_run)
details.head(10)

# view the metrics of the eval run
metrics = pf.get_metrics(eval_run)
print(json.dumps(metrics, indent=4))

# visualize both the base run and the eval run
pf.visualize([base_run, eval_run])

A web browser will be opened to show the visualization result.

q_0

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

There are actions to trigger local batch runs. To perform an evaluation you can use the run against "existing runs" actions.

img img :::

::::

Use column mapping

In this document, we will introduce how to map inputs with column mapping when running a flow.
Column mapping introduction

Column mapping is a mapping from flow input name to specified values. If specified, the flow will be executed with provided value for specified inputs. The following types of values in column mapping are supported:

    ${data.<column_name>} to reference from your test dataset.
    ${run.outputs.<output_name>} to reference from referenced run's output. Note: this only supported when --run is provided for pf run.
    STATIC_VALUE to create static value for all lines for specified column.

Flow inputs override priority

Flow input values are overridden according to the following priority:

"specified in column mapping" > "default value" > "same name column in provided data".

For example, if we have a flow with following inputs:

inputs:
  input1:
    type: string
    default: "default_val1"
  input2:
    type: string
    default: "default_val2"
  input3:
    type: string
  input4:
    type: string
...

And the flow will return each inputs in outputs.

With the following data

{"input3": "val3_in_data", "input4": "val4_in_data"}

And use the following YAML to run

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: path/to/flow
# my_flow has default value val2 for key2
data: path/to/data
# my_data has column key3 with value val3
column_mapping:
    input1: "val1_in_column_mapping"
    input3: ${data.input3}

Since the flow will return each inputs in output, we can get the actual inputs from outputs.output field in run details:

column_mapping_details

    Input "input1" has value "val1_in_column_mapping" since it's specified as constance in column_mapping.
    Input "input2" has value "default_val2" since it used default value in flow dag.
    Input "input3" has value "val3_in_data" since it's specified as data reference in column_mapping.
    Input "input4" has value "val4_in_data" since it has same name column in provided data.



Deploy a flow

A flow can be deployed to multiple platforms, such as a local development service, Docker container, Kubernetes cluster, etc.

Deploy a flow using development server

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

Once you have created and thoroughly tested a flow, you can use it as an HTTP endpoint.

::::{tab-set} :::{tab-item} CLI :sync: CLI We are going to use the web-classification as an example to show how to deploy a flow.

Please ensure you have create the connection required by flow, if not, you could refer to Setup connection for web-classification.

Note: We will use relevant environment variable ({connection_name}_{key_name}) to override connection configurations in serving mode, white space in connection name will be removed directly from environment variable name. For instance, if there is a custom connection named 'custom_connection' with a configuration key called 'chat_deployment_name,' the function will attempt to retrieve 'chat_deployment_name' from the environment variable 'CUSTOM_CONNECTION_CHAT_DEPLOYMENT_NAME' by default. If the environment variable is not set, it will use the original value as a fallback.

The following CLI commands allows you serve a flow folder as an endpoint. By running this command, a flask app will start in the environment where command is executed, please ensure all prerequisites required by flow have been installed.

# Serve the flow at localhost:8080
pf flow serve --source <path-to-your-flow-folder> --port 8080 --host localhost

The expected result is as follows if the flow served successfully, and the process will keep alive until it be killed manually.

img ::: :::{tab-item} VS Code Extension :sync: VSC In visual editor, choose: img then choose format: img then in yaml editor: img ::: ::::
Test endpoint

::::{tab-set} :::{tab-item} Bash You could open another terminal to test the endpoint with the following command:

curl http://localhost:8080/score --data '{"url":"https://play.google.com/store/apps/details?id=com.twitter.android"}' -X POST  -H "Content-Type: application/json"

::: :::{tab-item} PowerShell You could open another terminal to test the endpoint with the following command:

Invoke-WebRequest -URI http://localhost:8080/score -Body '{"url":"https://play.google.com/store/apps/details?id=com.twitter.android"}' -Method POST  -ContentType "application/json"

::: :::{tab-item} Test Page The development server has a built-in web page you can use to test the flow. Open 'http://localhost:8080' in your browser. img ::: ::::

Deploy a flow using Docker

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

There are two steps to deploy a flow using docker:

    Build the flow as docker format.
    Build and run the docker image.

Build a flow as docker format

::::{tab-set} :::{tab-item} CLI :sync: CLI

Use the command below to build a flow as docker format:

pf flow build --source <path-to-your-flow-folder> --output <your-output-dir> --format docker

::: :::{tab-item} VS Code Extension :sync: VSC

In visual editor, choose: img Click the button below to build a flow as docker format: img ::: ::::

Note that all dependent connections must be created before exporting as docker.
Docker format folder structure

Exported Dockerfile & its dependencies are located in the same folder. The structure is as below:

    flow: the folder contains all the flow files
        ...
    connections: the folder contains yaml files to create all related connections
        ...
    Dockerfile: the dockerfile to build the image
    start.sh: the script used in CMD of Dockerfile to start the service
    runit: the folder contains all the runit scripts
        ...
    settings.json: a json file to store the settings of the docker image
    README.md: Simple introduction of the files

Deploy with Docker

We are going to use the web-classification as an example to show how to deploy with docker.

Please ensure you have create the connection required by flow, if not, you could refer to Setup connection for web-classification.
Build a flow as docker format app

Use the command below to build a flow as docker format app:

pf flow build --source ../../flows/standard/web-classification --output dist --format docker

Note that all dependent connections must be created before exporting as docker.
Build Docker image

Like other Dockerfile, you need to build the image first. You can tag the image with any name you want. In this example, we use promptflow-serve.

Run the command below to build image:

docker build dist -t web-classification-serve

Run Docker image

Run the docker image will start a service to serve the flow inside the container.
Connections

If the service involves connections, all related connections will be exported as yaml files and recreated in containers. Secrets in connections won't be exported directly. Instead, we will export them as a reference to environment variables:

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/OpenAIConnection.schema.json
type: open_ai
name: open_ai_connection
module: promptflow.connections
api_key: ${env:OPEN_AI_CONNECTION_API_KEY} # env reference

You'll need to set up the environment variables in the container to make the connections work.
Run with docker run

You can run the docker image directly set via below commands:

# The started service will listen on port 8080.You can map the port to any port on the host machine as you want.
docker run -p 8080:8080 -e OPEN_AI_CONNECTION_API_KEY=<secret-value> web-classification-serve

Test the endpoint

After start the service, you can use curl to test it:

curl http://localhost:8080/score --data '{"url":"https://play.google.com/store/apps/details?id=com.twitter.android"}' -X POST  -H "Content-Type: application/json"



Deploy a flow using Kubernetes

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

There are four steps to deploy a flow using Kubernetes:

    Build the flow as docker format.
    Build the docker image.
    Create Kubernetes deployment yaml.
    Apply the deployment.

Build a flow as docker format

::::{tab-set} :::{tab-item} CLI :sync: CLI

Note that all dependent connections must be created before building as docker.

# create connection if not created before
pf connection create --file ../../../examples/connections/azure_openai.yml --set api_key=<your_api_key> api_base=<your_api_base> --name open_ai_connection

Use the command below to build a flow as docker format:

pf flow build --source <path-to-your-flow-folder> --output <your-output-dir> --format docker

::: :::{tab-item} VS Code Extension :sync: VSC

Click the button below to build a flow as docker format: img ::: ::::

Note that all dependent connections must be created before exporting as docker.
Docker format folder structure

Exported Dockerfile & its dependencies are located in the same folder. The structure is as below:

    flow: the folder contains all the flow files
        ...
    connections: the folder contains yaml files to create all related connections
        ...
    Dockerfile: the dockerfile to build the image
    start.sh: the script used in CMD of Dockerfile to start the service
    runit: the folder contains all the runit scripts
        ...
    settings.json: a json file to store the settings of the docker image
    README.md: Simple introduction of the files

Deploy with Kubernetes

We are going to use the web-classification as an example to show how to deploy with Kubernetes.

Please ensure you have create the connection required by flow, if not, you could refer to Setup connection for web-classification.

Additionally, please ensure that you have installed all the required dependencies. You can refer to the "Prerequisites" section in the README of the web-classification for a comprehensive list of prerequisites and installation instructions.
Build Docker image

Like other Dockerfile, you need to build the image first. You can tag the image with any name you want. In this example, we use web-classification-serve.

Then run the command below:

cd <your-output-dir>
docker build . -t web-classification-serve

Create Kubernetes deployment yaml.

The Kubernetes deployment yaml file acts as a guide for managing your docker container in a Kubernetes pod. It clearly specifies important information like the container image, port configurations, environment variables, and various settings. Below, you'll find a simple deployment template that you can easily customize to meet your needs.

Note: You need encode the secret using base64 firstly and input the <encoded_secret> as 'open-ai-connection-api-key' in the deployment configuration. For example, you can run below commands in linux:

encoded_secret=$(echo -n <your_api_key> | base64)

---
kind: Namespace
apiVersion: v1
metadata:
  name: <your-namespace>
---
apiVersion: v1
kind: Secret
metadata:
  name: open-ai-connection-api-key
  namespace: <your-namespace>
type: Opaque
data:
  open-ai-connection-api-key: <encoded_secret>
---
apiVersion: v1
kind: Service
metadata:
  name: web-classification-service
  namespace: <your-namespace>
spec:
  type: NodePort
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    nodePort: 30123
  selector:
    app: web-classification-serve-app
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-classification-serve-app
  namespace: <your-namespace>
spec:
  selector:
    matchLabels:
      app: web-classification-serve-app
  template:
    metadata:
      labels:
        app: web-classification-serve-app
    spec:
      containers:
      - name: web-classification-serve-container
        image: <your-docker-image>
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
        env:
        - name: OPEN_AI_CONNECTION_API_KEY
          valueFrom:
            secretKeyRef:
              name: open-ai-connection-api-key
              key: open-ai-connection-api-key

Apply the deployment.

Before you can deploy your application, ensure that you have set up a Kubernetes cluster and installed kubectl if it's not already installed. In this documentation, we will use Minikube as an example. To start the cluster, execute the following command:

minikube start

Once your Kubernetes cluster is up and running, you can proceed to deploy your application by using the following command:

kubectl apply -f deployment.yaml

This command will create the necessary pods to run your application within the cluster.

Note: You need replace <pod_name> below with your specific pod_name. You can retrieve it by running kubectl get pods -n web-classification.
Retrieve flow service logs of the container

The kubectl logs command is used to retrieve the logs of a container running within a pod, which can be useful for debugging, monitoring, and troubleshooting applications deployed in a Kubernetes cluster.

kubectl -n <your-namespace> logs <pod-name>

Connections

If the service involves connections, all related connections will be exported as yaml files and recreated in containers. Secrets in connections won't be exported directly. Instead, we will export them as a reference to environment variables:

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/OpenAIConnection.schema.json
type: open_ai
name: open_ai_connection
module: promptflow.connections
api_key: ${env:OPEN_AI_CONNECTION_API_KEY} # env reference

You'll need to set up the environment variables in the container to make the connections work.
Test the endpoint

    Option1:

    Once you've started the service, you can establish a connection between a local port and a port on the pod. This allows you to conveniently test the endpoint from your local terminal. To achieve this, execute the following command:

    kubectl port-forward <pod_name> <local_port>:<container_port> -n <your-namespace>

With the port forwarding in place, you can use the curl command to initiate the endpoint test:

curl http://localhost:<local_port>/score --data '{"url":"https://play.google.com/store/apps/details?id=com.twitter.android"}' -X POST  -H "Content-Type: application/json"

Option2:

minikube service web-classification-service --url -n <your-namespace> runs as a process, creating a tunnel to the cluster. The command exposes the service directly to any program running on the host operating system.

The command above will retrieve the URL of a service running within a Minikube Kubernetes cluster (e.g. http://:<assigned_port>), which you can click to interact with the flow service in your web browser. Alternatively, you can use the following command to test the endpoint:

Note: Minikube will use its own external port instead of nodePort to listen to the service. So please substitute <assigned_port> with the port obtained above.

curl http://localhost:<assigned_port>/score --data '{"url":"https://play.google.com/store/apps/details?id=com.twitter.android"}' -X POST  -H "Content-Type: application/json"


Distribute flow as executable app

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

We are going to use the web-classification as an example to show how to distribute flow as executable app with Pyinstaller.

Please ensure that you have installed all the required dependencies. You can refer to the "Prerequisites" section in the README of the web-classification for a comprehensive list of prerequisites and installation instructions. And we recommend you to add a requirements.txt to indicate all the required dependencies for each flow.

Pyinstaller is a popular tool used for converting Python applications into standalone executables. It allows you to package your Python scripts into a single executable file, which can be run on a target machine without requiring the Python interpreter to be installed. Streamlit is an open-source Python library used for creating web applications quickly and easily. It's designed for data scientists and engineers who want to turn data scripts into shareable web apps with minimal effort. We use Pyinstaller to package the flow and Streamlit to create custom web apps. Prior to distributing the workflow, kindly ensure that you have installed them.
Build a flow as executable format

Note that all dependent connections must be created before building as executable.

# create connection if not created before
pf connection create --file ../../../examples/connections/azure_openai.yml --set api_key=<your_api_key> api_base=<your_api_base> --name open_ai_connection

Use the command below to build a flow as executable format:

pf flow build --source <path-to-your-flow-folder> --output <your-output-dir> --format executable

Executable format folder structure

Exported files & its dependencies are located in the same folder. The structure is as below:

    flow: the folder contains all the flow files.
    connections: the folder contains yaml files to create all related connections.
    app.py: the entry file is included as the entry point for the bundled application.
    app.spec: the spec file tells PyInstaller how to process your script.
    main.py: it will start streamlit service and be called by the entry file.
    settings.json: a json file to store the settings of the executable application.
    build: a folder contains various log and working files.
    dist: a folder contains the executable application.
    README.md: Simple introduction of the files.

A template script of the entry file

PyInstaller reads a spec file or Python script written by you. It analyzes your code to discover every other module and library your script needs in order to execute. Then it collects copies of all those files, including the active Python interpreter, and puts them with your script in a single folder, or optionally in a single executable file.

We provide a Python entry script named app.py as the entry point for the bundled app, which enables you to serve a flow folder as an endpoint.

import os
import sys

from promptflow._cli._pf._connection import create_connection
from streamlit.web import cli as st_cli
from streamlit.runtime import exists

from main import start

def is_yaml_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in ('.yaml', '.yml')

def create_connections(directory_path) -> None:
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_yaml_file(file_path):
                create_connection(file_path)


if __name__ == "__main__":
    create_connections(os.path.join(os.path.dirname(__file__), "connections"))
    if exists():
        start()
    else:
        main_script = os.path.join(os.path.dirname(__file__), "main.py")
        sys.argv = ["streamlit", "run", main_script, "--global.developmentMode=false"]
        st_cli.main(prog_name="streamlit")

A template script of the spec file

The spec file tells PyInstaller how to process your script. It encodes the script names and most of the options you give to the pyinstaller command. The spec file is actually executable Python code. PyInstaller builds the app by executing the contents of the spec file.

To streamline this process, we offer a app.spec spec file that bundles the application into a single file. For additional information on spec files, you can refer to the Using Spec Files. Please replace streamlit_runtime_interpreter_path with the path of streamlit runtime interpreter in your environment.

# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [('connections', 'connections'), ('flow', 'flow'), ('settings.json', '.'), ('main.py', '.'), ('{{streamlit_runtime_interpreter_path}}', './streamlit/runtime')]
datas += collect_data_files('streamlit')
datas += copy_metadata('streamlit')
datas += collect_data_files('keyrings.alt', include_py_files=True)
datas += copy_metadata('keyrings.alt')
datas += collect_data_files('streamlit_quill')

block_cipher = None


a = Analysis(
    ['app.py', 'main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['bs4'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

The bundled application using Pyinstaller

Once you've build a flow as executable format following Build a flow as executable format. It will create two folders named build and dist within your specified output directory, denoted as . The build folder houses various log and working files, while the dist folder contains the app executable application.
Connections

If the service involves connections, all related connections will be exported as yaml files and recreated in the executable package. Secrets in connections won't be exported directly. Instead, we will export them as a reference to environment variables:

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/OpenAIConnection.schema.json
type: open_ai
name: open_ai_connection
module: promptflow.connections
api_key: ${env:OPEN_AI_CONNECTION_API_KEY} # env reference

Test the endpoint

Finally, You can distribute the bundled application app to other people. They can execute your program by double clicking the executable file, e.g. app.exe in Windows system or running the binary file, e.g. app in Linux system.

The development server has a built-in web page they can use to test the flow by opening 'http://localhost:8501' in the browser. The expected result is as follows: if the flow served successfully, the process will keep alive until it is killed manually.

To your users, the app is self-contained. They do not need to install any particular version of Python or any modules. They do not need to have Python installed at all.

Note: The executable generated is not cross-platform. One platform (e.g. Windows) packaged executable can't run on others (Mac, Linux).
Known issues

    Note that Python 3.10.0 contains a bug making it unsupportable by PyInstaller. PyInstaller will also not work with beta releases of Python 3.13.


Add conditional control to a flow

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

In prompt flow, we support control logic by activate config, like if-else, switch. Activate config enables conditional execution of nodes within your flow, ensuring that specific actions are taken only when the specified conditions are met.

This guide will help you learn how to use activate config to add conditional control to your flow.
Prerequisites

Please ensure that your promptflow version is greater than 0.1.0b5.
Usage

Each node in your flow can have an associated activate config, specifying when it should execute and when it should bypass. If a node has activate config, it will only be executed when the activate condition is met. The configuration consists of two essential components:

    activate.when: The condition that triggers the execution of the node. It can be based on the outputs of a previous node, or the inputs of the flow.
    activate.is: The condition's value, which can be a constant value of string, boolean, integer, double.

You can manually change the flow.dag.yaml in the flow folder or use the visual editor in VS Code Extension to add activate config to nodes in the flow.

::::{tab-set} :::{tab-item} YAML :sync: YAML

You can add activate config in the node section of flow yaml.

activate:
  when: ${node.output}
  is: true

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

    Click Visual editor in the flow.dag.yaml to enter the flow interface. visual_editor

    Click on the Activation config section in the node you want to add and fill in the values for "when" and "is". activate_config

:::

::::
Further details and important notes

    If the node using the python tool has an input that references a node that may be bypassed, please provide a default value for this input whenever possible. If there is no default value for input, the output of the bypassed node will be set to None.

    provide_default_value

    It is not recommended to directly connect nodes that might be bypassed to the flow's outputs. If it is connected, the output will be None and a warning will be raised.

    output_bypassed

    In a conditional flow, if a node has activate config, we will always use this config to determine whether the node should be bypassed. If a node is bypassed, its status will be marked as "Bypassed", as shown in the figure below Show. There are three situations in which a node is bypassed.

    bypassed_nodes

    (1) If a node has activate config and the value of activate.when is not equals to activate.is, it will be bypassed. If you want to fore a node to always be executed, you can set the activate config to when dummy is dummy which always meets the activate condition.

    activate_condition_always_met

    (2) If a node has activate config and the node pointed to by activate.when is bypassed, it will be bypassed.

    activate_when_bypassed

    (3) If a node does not have activate config but depends on other nodes that have been bypassed, it will be bypassed.

    dependencies_bypassed

Example flow

Let's illustrate how to use activate config with practical examples.

    If-Else scenario: Learn how to develop a conditional flow for if-else scenarios. View Example
    Switch scenario: Explore conditional flow for switch scenarios. View Example

Use streaming endpoints deployed from prompt flow

In prompt flow, you can deploy flow as REST endpoint for real-time inference.

When consuming the endpoint by sending a request, the default behavior is that the online endpoint will keep waiting until the whole response is ready, and then send it back to the client. This can cause a long delay for the client and a poor user experience.

To avoid this, you can use streaming when you consume the endpoints. Once streaming enabled, you don't have to wait for the whole response ready. Instead, the server will send back the response in chunks as they are generated. The client can then display the response progressively, with less waiting time and more interactivity.

This article will describe the scope of streaming, how streaming works, and how to consume streaming endpoints.
Create a streaming enabled flow

If you want to use the streaming mode, you need to create a flow that has a node that produces a string generator as the flow’s output. A string generator is an object that can return one string at a time when requested. You can use the following types of nodes to create a string generator:

    LLM node: This node uses a large language model to generate natural language responses based on the input.

    {# Sample prompt template for LLM node #}

    system:
    You are a helpful assistant.

    user:
    {{question}}

Python tools node: This node allows you to write custom Python code that can yield string outputs. You can use this node to call external APIs or libraries that support streaming. For example, you can use this code to echo the input word by word:

from promptflow import tool

# Sample code echo input by yield in Python tool node

@tool
def my_python_tool(paragraph: str) -> str:
    yield "Echo: "
    for word in paragraph.split():
        yield word + " "

In this guide, we will use the "Chat with Wikipedia" sample flow as an example. This flow processes the user’s question, searches Wikipedia for relevant articles, and answers the question with information from the articles. It uses streaming mode to show the progress of the answer generation.

chat_wikipedia.png
Deploy the flow as an online endpoint

To use the streaming mode, you need to deploy your flow as an online endpoint. This will allow you to send requests and receive responses from your flow in real time.

Follow this guide to deploy your flow as an online endpoint.

Note

You can follow this document to deploy an online endpoint. Please deploy with runtime environment version later than version 20230816.v10. You can check your runtime version and update runtime in the run time detail page.
Understand the streaming process

When you have an online endpoint, the client and the server need to follow specific principles for content negotiation to utilize the streaming mode:

Content negotiation is like a conversation between the client and the server about the preferred format of the data they want to send and receive. It ensures effective communication and agreement on the format of the exchanged data.

To understand the streaming process, consider the following steps:

    First, the client constructs an HTTP request with the desired media type included in the Accept header. The media type tells the server what kind of data format the client expects. It's like the client saying, "Hey, I'm looking for a specific format for the data you'll send me. It could be JSON, text, or something else." For example, application/json indicates a preference for JSON data, text/event-stream indicates a desire for streaming data, and */* means the client accepts any data format.

        [!NOTE]

        If a request lacks an Accept header or has empty Accept header, it implies that the client will accept any media type in response. The server treats it as */*.

    Next, the server responds based on the media type specified in the Accept header. It's important to note that the client may request multiple media types in the Accept header, and the server must consider its capabilities and format priorities to determine the appropriate response.
        First, the server checks if text/event-stream is explicitly specified in the Accept header:
            For a stream-enabled flow, the server returns a response with a Content-Type of text/event-stream, indicating that the data is being streamed.
            For a non-stream-enabled flow, the server proceeds to check for other media types specified in the header.
        If text/event-stream is not specified, the server then checks if application/json or */* is specified in the Accept header:
            In such cases, the server returns a response with a Content-Type of application/json, providing the data in JSON format.
        If the Accept header specifies other media types, such as text/html:
            The server returns a 424 response with a PromptFlow runtime error code UserError and a runtime HTTP status 406, indicating that the server cannot fulfill the request with the requested data format.

            Note: Please refer handle errors for details.

    Finally, the client checks the Content-Type response header. If it is set to text/event-stream, it indicates that the data is being streamed.

Let’s take a closer look at how the streaming process works. The response data in streaming mode follows the format of server-sent events (SSE).

The overall process works as follows:
0. The client sends a message to the server.

POST https://<your-endpoint>.inference.ml.azure.com/score
Content-Type: application/json
Authorization: Bearer <key or token of your endpoint>
Accept: text/event-stream

{
    "question": "Hello",
    "chat_history": []
}

Note

The Accept header is set to text/event-stream to request a stream response.
1. The server sends back the response in streaming mode.

HTTP/1.1 200 OK
Content-Type: text/event-stream; charset=utf-8
Connection: close
Transfer-Encoding: chunked

data: {"answer": ""}

data: {"answer": "Hello"}

data: {"answer": "!"}

data: {"answer": " How"}

data: {"answer": " can"}

data: {"answer": " I"}

data: {"answer": " assist"}

data: {"answer": " you"}

data: {"answer": " today"}

data: {"answer": " ?"}

data: {"answer": ""}

Note that the Content-Type is set to text/event-stream; charset=utf-8, indicating the response is an event stream.

The client should decode the response data as server-sent events and display them incrementally. The server will close the HTTP connection after all the data is sent.

Each response event is the delta to the previous event. It is recommended for the client to keep track of the merged data in memory and send them back to the server as chat history in the next request.
2. The client sends another chat message, along with the full chat history, to the server.

POST https://<your-endpoint>.inference.ml.azure.com/score
Content-Type: application/json
Authorization: Bearer <key or token of your endpoint>
Accept: text/event-stream

{
    "question": "Glad to know you!",
    "chat_history": [
        {
            "inputs": {
                "question": "Hello"
            },
            "outputs": {
                "answer": "Hello! How can I assist you today?"
            }
        }
    ]
}

3. The server sends back the answer in streaming mode.

HTTP/1.1 200 OK
Content-Type: text/event-stream; charset=utf-8
Connection: close
Transfer-Encoding: chunked

data: {"answer": ""}

data: {"answer": "Nice"}

data: {"answer": " to"}

data: {"answer": " know"}

data: {"answer": " you"}

data: {"answer": " too"}

data: {"answer": "!"}

data: {"answer": " Is"}

data: {"answer": " there"}

data: {"answer": " anything"}

data: {"answer": " I"}

data: {"answer": " can"}

data: {"answer": " help"}

data: {"answer": " you"}

data: {"answer": " with"}

data: {"answer": "?"}

data: {"answer": ""}

4. The chat continues in a similar way.
Handle errors

The client should check the HTTP response code first. See this table for common error codes returned by online endpoints.

If the response code is "424 Model Error", it means that the error is caused by the model’s code. The error response from a PromptFlow model always follows this format:

{
  "error": {
    "code": "UserError",
    "message": "Media type text/event-stream in Accept header is not acceptable. Supported media type(s) - application/json",
  }
}

    It is always a JSON dictionary with only one key "error" defined.
    The value for "error" is a dictionary, containing "code", "message".
    "code" defines the error category. Currently, it may be "UserError" for bad user inputs and "SystemError" for errors inside the service.
    "message" is a description of the error. It can be displayed to the end user.

How to consume the server-sent events
Consume using Python

In this sample usage, we are using the SSEClient class. This class is not a built-in Python class and needs to be installed separately. You can install it via pip:

pip install sseclient-py  

A sample usage would like:

import requests  
from sseclient import SSEClient  
from requests.exceptions import HTTPError  

try:
    response = requests.post(url, json=body, headers=headers, stream=stream)
    response.raise_for_status()

    content_type = response.headers.get('Content-Type')
    if "text/event-stream" in content_type:
        client = SSEClient(response)
        for event in client.events():
            # Handle event, i.e. print to stdout
    else:
        # Handle json response

except HTTPError:
    # Handle exceptions

Consume using JavaScript

There are several libraries to consume server-sent events in JavaScript. Here is one of them as an example.
A sample chat app using Python

Here is a sample chat app written in Python. (Click here to view the source code.)

chat_app
Advance usage - hybrid stream and non-stream flow output

Sometimes, you may want to get both stream and non-stream results from a flow output. For example, in the “Chat with Wikipedia” flow, you may want to get not only LLM’s answer, but also the list of URLs that the flow searched. To do this, you need to modify the flow to output a combination of stream LLM’s answer and non-stream URL list.

In the sample "Chat With Wikipedia" flow, the output is connected to the LLM node augmented_chat. To add the URL list to the output, you need to add an output field with the name url and the value ${get_wiki_url.output}.

chat_wikipedia_dual_output_center.png

The output of the flow will be a non-stream field as the base and a stream field as the delta. Here is an example of request and response.
0. The client sends a message to the server.

POST https://<your-endpoint>.inference.ml.azure.com/score
Content-Type: application/json
Authorization: Bearer <key or token of your endpoint>
Accept: text/event-stream
{
    "question": "When was ChatGPT launched?",
    "chat_history": []
}

1. The server sends back the answer in streaming mode.

HTTP/1.1 200 OK
Content-Type: text/event-stream; charset=utf-8
Connection: close
Transfer-Encoding: chunked

data: {"url": ["https://en.wikipedia.org/w/index.php?search=ChatGPT", "https://en.wikipedia.org/w/index.php?search=GPT-4"]}

data: {"answer": ""}

data: {"answer": "Chat"}

data: {"answer": "G"}

data: {"answer": "PT"}

data: {"answer": " was"}

data: {"answer": " launched"}

data: {"answer": " on"}

data: {"answer": " November"}

data: {"answer": " "}

data: {"answer": "30"}

data: {"answer": ","}

data: {"answer": " "}

data: {"answer": "202"}

data: {"answer": "2"}

data: {"answer": "."}

data: {"answer": " \n\n"}

...

data: {"answer": "PT"}

data: {"answer": ""}

2. The client sends another chat message, along with the full chat history, to the server.

POST https://<your-endpoint>.inference.ml.azure.com/score
Content-Type: application/json
Authorization: Bearer <key or token of your endpoint>
Accept: text/event-stream
{
    "question": "When did OpenAI announce GPT-4? How long is it between these two milestones?",
    "chat_history": [
        {
            "inputs": {
                "question": "When was ChatGPT launched?"
            },
            "outputs": {
                "url": [
                    "https://en.wikipedia.org/w/index.php?search=ChatGPT",
                    "https://en.wikipedia.org/w/index.php?search=GPT-4"
                ],
                "answer": "ChatGPT was launched on November 30, 2022. \n\nSOURCES: https://en.wikipedia.org/w/index.php?search=ChatGPT"
            }
        }
    ]
}

3. The server sends back the answer in streaming mode.

HTTP/1.1 200 OK
Content-Type: text/event-stream; charset=utf-8
Connection: close
Transfer-Encoding: chunked

data: {"url": ["https://en.wikipedia.org/w/index.php?search=Generative pre-trained transformer ", "https://en.wikipedia.org/w/index.php?search=Microsoft "]}

data: {"answer": ""}

data: {"answer": "Open"}

data: {"answer": "AI"}

data: {"answer": " released"}

data: {"answer": " G"}

data: {"answer": "PT"}

data: {"answer": "-"}

data: {"answer": "4"}

data: {"answer": " in"}

data: {"answer": " March"}

data: {"answer": " "}

data: {"answer": "202"}

data: {"answer": "3"}

data: {"answer": "."}

data: {"answer": " Chat"}

data: {"answer": "G"}

data: {"answer": "PT"}

data: {"answer": " was"}

data: {"answer": " launched"}

data: {"answer": " on"}

data: {"answer": " November"}

data: {"answer": " "}

data: {"answer": "30"}

data: {"answer": ","}

data: {"answer": " "}

data: {"answer": "202"}

data: {"answer": "2"}

data: {"answer": "."}

data: {"answer": " The"}

data: {"answer": " time"}

data: {"answer": " between"}

data: {"answer": " these"}

data: {"answer": " two"}

data: {"answer": " milestones"}

data: {"answer": " is"}

data: {"answer": " approximately"}

data: {"answer": " "}

data: {"answer": "3"}

data: {"answer": " months"}

data: {"answer": ".\n\n"}

...

data: {"answer": "Chat"}

data: {"answer": "G"}

data: {"answer": "PT"}

data: {"answer": ""}


Execute flow as a function

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::
Overview

Promptflow allows you to load a flow and use it as a function in your code. This feature is useful when building a service on top of a flow, reference here for a simple example service with flow function consumption.
Load an invoke the flow function

To use the flow-as-function feature, you first need to load a flow using the load_flow function. Then you can consume the flow object like a function by providing key-value arguments for it.

f = load_flow("../../examples/flows/standard/web-classification/")
f(url="sample_url")

Config the flow with context

You can overwrite some flow configs before flow function execution by setting flow.context.
Load flow as a function with in-memory connection override

By providing a connection object to flow context, flow won't need to get connection in execution time, which can save time when for cases where flow function need to be called multiple times.

from promptflow.entities import AzureOpenAIConnection

connection_obj = AzureOpenAIConnection(
    name=conn_name,
    api_key=api_key,
    api_base=api_base,
    api_type="azure",
    api_version=api_version,
)
# no need to create the connection object.  
f.context = FlowContext(
    connections={"classify_with_llm": {"connection": connection_obj}}
)

Local flow as a function with flow inputs override

By providing overrides, the original flow dag will be updated in execution time.

f.context = FlowContext(
    # node "fetch_text_content_from_url" will take inputs from the following command instead of from flow input
    overrides={"nodes.fetch_text_content_from_url.inputs.url": sample_url},
)

Note, the overrides are only doing YAML content replacement on original flow.dag.yaml. If the flow.dag.yaml become invalid after overrides, validation error will be raised when executing.
Load flow as a function with streaming output

After set streaming in flow context, the flow function will return an iterator to stream the output.

f = load_flow(source="../../examples/flows/chat/basic-chat/")
f.context.streaming = True
result = f(
    chat_history=[
        {
            "inputs": {"chat_input": "Hi"},
            "outputs": {"chat_output": "Hello! How can I assist you today?"},
        }
    ],
    question="How are you?",
)


answer = ""
# the result will be a generator, iterate it to get the result
for r in result["answer"]:
    answer += r

Reference our sample for usage.
Next steps

Learn more about:

    Flow as a function sample
    Deploy a flow


Frequency asked questions (FAQ)
General
Stable vs experimental

Prompt flow provides both stable and experimental features in the same SDK.
Feature status 	Description
Stable features 	Production ready

These features are recommended for most use cases and production environments. They are updated less frequently then experimental features.
Experimental features 	Developmental

These features are newly developed capabilities & updates that may not be ready or fully tested for production usage. While the features are typically functional, they can include some breaking changes. Experimental features are used to iron out SDK breaking bugs, and will only receive updates for the duration of the testing period. Experimental features are also referred to as features that are in preview.
As the name indicates, the experimental (preview) features are for experimenting and is not considered bug free or stable. For this reason, we only recommend experimental features to advanced users who wish to try out early versions of capabilities and updates, and intend to participate in the reporting of bugs and glitches.
OpenAI 1.x support

Please use the following command to upgrade promptflow for openai 1.x support:

pip install promptflow>=1.1.0
pip install promptflow-tools>=1.0.0

Note that the command above will upgrade your openai package a version later than 1.0.0, which may introduce breaking changes to custom tool code.

Reach OpenAI migration guide for more details.
Troubleshooting
Connection creation failed with StoreConnectionEncryptionKeyError

Connection creation failed with StoreConnectionEncryptionKeyError: System keyring backend service not found in your operating system. See https://pypi.org/project/keyring/ to install requirement for different operating system, or 'pip install keyrings.alt' to use the third-party backend.

This error raised due to keyring can't find an available backend to store keys. For example macOS Keychain and Windows Credential Locker are valid keyring backends.

To resolve this issue, install the third-party keyring backend or write your own keyring backend, for example: pip install keyrings.alt

For more detail about keyring third-party backend, please refer to 'Third-Party Backends' in keyring.
Pf visualize show error: "tcgetpgrp failed: Not a tty"

If you are using WSL, this is a known issue for webbrowser under WSL; see this issue for more information. Please try to upgrade your WSL to 22.04 or later, this issue should be resolved.

If you are still facing this issue with WSL 22.04 or later, or you are not even using WSL, please open an issue to us.
Installed tool not appearing in VSCode Extension tool list

After installing a tool package via pip install [tool-package-name], the new tool may not immediately appear in the tool list within the VSCode Extension, as shown below:

VSCode Extension tool list

This is often due to outdated cache. To refresh the tool list and make newly installed tools visible:

    Open the VSCode Extension window.

    Bring up the command palette by pressing "Ctrl+Shift+P".

    Type and select the "Developer: Reload Webviews" command.

    Wait a moment for the tool list refreshing.

Reloading clears the previous cache and populates the tool list with any newly installed tools. So that the missing tools are now visible.
Set logging level

Promptflow uses logging module to log messages. You can set logging level via environment variable PF_LOGGING_LEVEL, valid values includes CRITICAL, ERROR, WARNING, INFO, DEBUG, default to INFO. Below is the serving logs after setting PF_LOGGING_LEVEL to DEBUG:

img

Compare to the serving logs with WARNING level:

img
Set environment variables

Currently, promptflow supports the following environment variables:

PF_WORKER_COUNT

Valid for batch run only. The number of workers to use for parallel execution of the Flow.

Default value is 16. If you have large number of batch run date row count, and want more efficiency, you can increase the PF_WORKER_COUNT to improve the batch run concurrency, make it run faster.

When you modify the concurrency, please consider 2 points:

First, the concurrency should be not bigger than your batch run data row count. If not, meaning if the concurrency is bigger, it will run slower due to the time taken for process startup and shutdown.

Second, your batch run risks to fail due to rate limit of your LLM endpoint, in this case you need to set up PF_WORKER_COUNT to a smaller number. Take Azure OpenAI endpoint as example, you can go to Azure OpenAI Studio, navigate to Deployment tab, check out the capacity of your endpoints. Then you can refer to this expression to set up the concurrency.

PF_WORKER_COUNT <= TPM * duration_seconds / token_count / 60

TPM: token per minute, capacity rate limit of your LLM endpoint

duration_seconds: single flow run duration in seconds

token_count: single flow run token count

For example, if your endpoint TPM (token per minute) is 50K, the single flow run takes 10k tokens and runs for 30s, pls do not set up PF_WORKER_COUNT bigger than 2. This is a rough estimation. Please also consider collboaration (teammates use the same endpoint at the same time) and tokens consumed in deployed inference endpoints, playground and other cases which might send request to your LLM endpoints.

PF_BATCH_METHOD

Valid for batch run only. Optional values: 'spawn', 'fork'.

spawn

    The child processes will not inherit resources of the parent process, therefore, each process needs to reinitialize the resources required for the flow, which may use more system memory.

    Starting a process is slow because it will take some time to initialize the necessary resources.

fork

    Use the copy-on-write mechanism, the child processes will inherit all the resources of the parent process, thereby using less system memory.

    The process starts faster as it doesn't need to reinitialize resources.

Note: Windows only supports spawn, Linux and macOS support both spawn and fork.
How to configure environment variables

    Configure environment variables in flow.dag.yaml. Example:

    inputs: []  
    outputs: []  
    nodes: []  
    environment_variables:  
      PF_WORKER_COUNT: 2  
      PF_BATCH_METHOD: "spawn"
      MY_CUSTOM_SETTING: my_custom_value 

    Specify environment variables when submitting runs.

::::{tab-set} :::{tab-item} CLI :sync: CLI

Use this parameter: --environment-variable to specify environment variables. Example: --environment-variable PF_WORKER_COUNT="2" PF_BATCH_METHOD="spawn".

:::

:::{tab-item} SDK :sync: SDK

Specify environment variables when creating run. Example:

    pf = PFClient(
        credential=credential,
        subscription_id="<SUBSCRIPTION_ID>",
        resource_group_name="<RESOURCE_GROUP>",
        workspace_name="<AML_WORKSPACE_NAME>",
    )

    flow = "web-classification"
    data = "web-classification/data.jsonl"
    runtime = "example-runtime-ci"

    environment_variables = {"PF_WORKER_COUNT": "2", "PF_BATCH_METHOD": "spawn"}

    # create run
    base_run = pf.run(
        flow=flow,
        data=data,
        runtime=runtime,
        environment_variables=environment_variables,
    )

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

VSCode Extension supports specifying environment variables only when submitting batch runs. Specify environment variables in batch_run_create.yaml. Example:

    name: flow_name
    display_name: display_name
    flow: flow_folder
    data: data_file
    column_mapping:
        customer_info: <Please select a data input>
        history: <Please select a data input>
    environment_variables:
        PF_WORKER_COUNT: "2"
        PF_BATCH_METHOD: "spawn"

:::

::::
Priority

The environment variables specified when submitting runs always takes precedence over the environment variables in the flow.dag.yaml file.

Initialize and test a flow

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

From this document, customer can initialize a flow and test it.
Initialize flow

Creating a flow folder with code/prompts and yaml definitions of the flow.
Initialize flow from scratch

Promptflow can create three types of flow folder:

    standard: Basic structure of flow folder.
    chat: Chat flow is designed for conversational application development, building upon the capabilities of standard flow and providing enhanced support for chat inputs/outputs and chat history management.
    evaluation: Evaluation flows are special types of flows that assess how well the outputs of a flow align with specific criteria and goals.

::::{tab-set} :::{tab-item} CLI :sync: CLI

# Create a flow
pf flow init --flow <flow-name>

# Create a chat flow
pf flow init --flow <flow-name> --type chat

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

Use VS Code explorer pane > directory icon > right click > the "New flow in this directory" action. Follow the popped out dialog to initialize your flow in the target folder. img

Alternatively, you can use the "Create new flow" action on the prompt flow pane > quick access section to create a new flow img

:::

::::

Structure of flow folder:

    flow.dag.yaml: The flow definition with inputs/outputs, nodes, tools and variants for authoring purpose.
    .promptflow/flow.tools.json: It contains tools meta referenced in flow.dag.yaml.
    Source code files (.py, .jinja2): User managed, the code scripts referenced by tools.
    requirements.txt: Python package dependencies for this flow.

init_flow_folder
Create from existing code

Customer needs to pass the path of tool script to entry, and also needs to pass in the promptflow template dict to prompt-template, which the key is the input name of the tool and the value is the path to the promptflow template. Promptflow CLI can generate the yaml definitions needed for prompt flow from the existing folder, using the tools script and prompt templates.

# Create a flow in existing folder
pf flow init --flow <flow-name> --entry <tool-script-path> --function <tool-function-name> --prompt-template <prompt-param-name>=<prompt-tempate-path>

Take customer-intent-extraction for example, which demonstrating how to convert a langchain code into a prompt flow.

init_output

In this case, promptflow CLI generates flow.dag.yaml, .promptflow/flow.tools.json and extract_intent_tool.py, it is a python tool in the flow.

init_files
Test a flow

:::{admonition} Note Testing flow will NOT create a batch run record, therefore it's unable to use commands like pf run show-details to get the run information. If you want to persist the run record, see Run and evaluate a flow :::

Promptflow also provides ways to test the initialized flow or flow node. It will help you quickly test your flow.
Visual editor on the VS Code for prompt flow.

::::{tab-set} :::{tab-item} VS Code Extension :sync: VS Code Extension

Open the flow.dag.yaml file of your flow. On the top of the yaml editor you can find the "Visual editor" action. Use it to open the Visual editor with GUI support.

img :::

::::
Test flow

Customer can use CLI or VS Code extension to test the flow.

::::{tab-set} :::{tab-item} CLI :sync: CLI

# Test flow
pf flow test --flow <flow-name>

# Test flow with specified variant
pf flow test --flow <flow-name> --variant '${<node-name>.<variant-name>}'

The log and result of flow test will be displayed in the terminal.

flow test

Promptflow CLI will generate test logs and outputs in .promptflow:

    flow.detail.json: Defails info of flow test, include the result of each node.
    flow.log: The log of flow test.
    flow.output.json: The result of flow test.

flow_output_files

:::

:::{tab-item} SDK :sync: SDK

The return value of test function is the flow outputs.

from promptflow import PFClient

pf_client = PFClient()

# Test flow
inputs = {"<flow_input_name>": "<flow_input_value>"}  # The inputs of the flow.
flow_result = pf_client.test(flow="<flow_folder_path>", inputs=inputs)
print(f"Flow outputs: {flow_result}")

The log and result of flow test will be displayed in the terminal.

flow test

Promptflow CLI will generate test logs and outputs in .promptflow:

    flow.detail.json: Defails info of flow test, include the result of each node.
    flow.log: The log of flow test.
    flow.output.json: The result of flow test.

flow_output_files

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

You can use the action either on the default yaml editor or the visual editor to trigger flow test. See the snapshots below: img img

:::

::::
Test a single node in the flow

Customer can test a single python node in the flow. It will use customer provides date or the default value of the node as input. It will only use customer specified node to execute with the input.

::::{tab-set} :::{tab-item} CLI :sync: CLI

Customer can execute this command to test the flow.

# Test flow node
pf flow test --flow <flow-name> --node <node-name>

The log and result of flow node test will be displayed in the terminal. And the details of node test will generated to .promptflow/flow-<node-name>.node.detail.json.

:::

:::{tab-item} SDK :sync: SDK

Customer can execute this command to test the flow. The return value of test function is the node outputs.

from promptflow import PFClient

pf_client = PFClient()

# Test not iun the flow
inputs = {<node_input_name>: <node_input_value>}  # The inputs of the node.
node_result = pf_client.test(flow=<flow_folder_path>, inputs=inputs, node=<node_name>)
print(f"Node outputs: {node_result}")

The log and result of flow node test will be displayed in the terminal. And the details of node test will generated to .promptflow/flow-<node-name>.node.detail.json.

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

The prompt flow extension provides inline actions in both default yaml editor and visual editor to trigger single node runs.

img img

:::

::::
Test with interactive mode

::::{tab-set} :::{tab-item} CLI :sync: CLI

Promptflow CLI provides a way to start an interactive chat session for chat flow. Customer can use below command to start an interactive chat session:

# Chat in the flow
pf flow test --flow <flow-name> --interactive

After executing this command, customer can interact with the chat flow in the terminal. Customer can press Enter to send the message to chat flow. And customer can quit with ctrl+C. Promptflow CLI will distinguish the output of different roles by color, User input, Bot output, Flow script output, Node output.

Using this chat flow to show how to use interactive mode.

chat

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

If a flow contains chat inputs or chat outputs in the flow interface, there will be a selection when triggering flow test. You can select the interactive mode if you want to.

img img

:::

::::

When the LLM node in the chat flow that is connected to the flow output, Promptflow SDK streams the results of the LLM node.

::::{tab-set} :::{tab-item} CLI :sync: CLI The flow result will be streamed in the terminal as shown below.

streaming_output

:::

:::{tab-item} SDK :sync: SDK

The LLM node return value of test function is a generator, you can consume the result by this way:

from promptflow import PFClient

pf_client = PFClient()

# Test flow
inputs = {"<flow_input_name>": "<flow_input_value>"}  # The inputs of the flow.
flow_result = pf_client.test(flow="<flow_folder_path>", inputs=inputs)
for item in flow_result["<LLM_node_output_name>"]:
    print(item)

:::

::::
Debug a single node in the flow

Customer can debug a single python node in VScode by the extension.

::::{tab-set} :::{tab-item} VS Code Extension :sync: VS Code Extension

Break points and debugging functionalities for the Python steps in your flow. Just set the break points and use the debug actions on either default yaml editor or visual editor. img img

:::

::::
Next steps

Manage connections

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

Connection helps securely store and manage secret keys or other sensitive credentials required for interacting with LLM (Large Language Models) and other external tools, for example, Azure Content Safety.

:::{note} To use azureml workspace connection locally, refer to this guide. :::
Connection types

There are multiple types of connections supported in promptflow, which can be simply categorized into strong type connection and custom connection. The strong type connection includes AzureOpenAIConnection, OpenAIConnection, etc. The custom connection is a generic connection type that can be used to store custom defined credentials.

We are going to use AzureOpenAIConnection as an example for strong type connection, and CustomConnection to show how to manage connections.
Create a connection

:::{note} If you are using WSL or other OS without default keyring storage backend, you may encounter StoreConnectionEncryptionKeyError, please refer to FAQ for the solutions. :::

::::{tab-set} :::{tab-item} CLI :sync: CLI Each of the strong type connection has a corresponding yaml schema, the example below shows the AzureOpenAIConnection yaml:

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
name: azure_open_ai_connection
type: azure_open_ai
api_key: "<to-be-replaced>"
api_base: "https://<name>.openai.azure.com/"
api_type: "azure"
api_version: "2023-03-15-preview"

The custom connection yaml will have two dict fields for secrets and configs, the example below shows the CustomConnection yaml:

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/CustomConnection.schema.json
name: custom_connection
type: custom
configs:
  endpoint: "<your-endpoint>"
  other_config: "other_value"
secrets:  # required
  my_key: "<your-api-key>"

After preparing the yaml file, use the CLI command below to create them:

# Override keys with --set to avoid yaml file changes
pf connection create -f <path-to-azure-open-ai-connection> --set api_key=<your-api-key>
# Create the custom connection
pf connection create -f <path-to-custom-connection> --set configs.endpoint=<endpoint> secrets.my_key=<your-api-key>

The expected result is as follows if the connection created successfully.

img :::

:::{tab-item} SDK :sync: SDK Using SDK, each connection type has a corresponding class to create a connection. The following code snippet shows how to import the required class and create the connection:

from promptflow import PFClient
from promptflow.entities import AzureOpenAIConnection, CustomConnection

# Get a pf client to manage connections
pf = PFClient()

# Initialize an AzureOpenAIConnection object
connection = AzureOpenAIConnection(
    name="my_azure_open_ai_connection", 
    api_key="<your-api-key>", 
    api_base="<your-endpoint>"
    api_version="2023-03-15-preview"
)

# Create the connection, note that api_key will be scrubbed in the returned result
result = pf.connections.create_or_update(connection)
print(result)

# Initialize a custom connection object
connection = CustomConnection(
    name="my_custom_connection", 
    # Secrets is a required field for custom connection
    secrets={"my_key": "<your-api-key>"},
    configs={"endpoint": "<your-endpoint>", "other_config": "other_value"}
)

# Create the connection, note that all secret values will be scrubbed in the returned result
result = pf.connections.create_or_update(connection)
print(result)

:::

:::{tab-item} VS Code Extension :sync: VSC

On the VS Code primary sidebar > prompt flow pane. You can find the connections pane to manage your local connections. Click the "+" icon on the top right of it and follow the popped out instructions to create your new connection.

img img ::: ::::
Update a connection

::::{tab-set} :::{tab-item} CLI :sync: CLI The commands below show how to update existing connections with new values:

# Update an azure open ai connection with a new api base
pf connection update -n my_azure_open_ai_connection --set api_base='new_value'
# Update a custom connection
pf connection update -n my_custom_connection --set configs.other_config='new_value'

:::

:::{tab-item} SDK :sync: SDK The code snippet below shows how to update existing connections with new values:

# Update an azure open ai connection with a new api base
connection = pf.connections.get(name="my_azure_open_ai_connection")
connection.api_base = "new_value"
connection.api_key = "<original-key>"  # secrets are required when updating connection using sdk
result = pf.connections.create_or_update(connection)
print(connection)
# Update a custom connection
connection = pf.connections.get(name="my_custom_connection")
connection.configs["other_config"] = "new_value"
connection.secrets = {"key1": "val1"}  # secrets are required when updating connection using sdk
result = pf.connections.create_or_update(connection)
print(connection)

:::

:::{tab-item} VS Code Extension :sync: VSC

On the VS Code primary sidebar > prompt flow pane. You can find the connections pane to manage your local connections. Right click the item of the connection list to update or delete your connections. img ::: ::::
List connections

::::{tab-set} :::{tab-item} CLI :sync: CLI List connection command will return the connections with json list format, note that all secrets and api keys will be scrubbed:

pf connection list

:::

:::{tab-item} SDK :sync: SDK List connection command will return the connections object list, note that all secrets and api keys will be scrubbed:

from promptflow import PFClient
# Get a pf client to manage connections
pf = PFClient()
# List and print connections
connection_list = pf.connections.list()
for connection in connection_list:
    print(connection)

:::

:::{tab-item} VS Code Extension :sync: VSC img ::: ::::
Delete a connection

::::{tab-set} :::{tab-item} CLI :sync: CLI Delete a connection with the following command:

pf connection delete -n <connection_name>

:::

:::{tab-item} SDK :sync: SDK Delete a connection with the following code snippet:

from promptflow import PFClient

# Get a pf client to manage connections
pf = PFClient()
# Delete the connection with specific name
client.connections.delete(name="my_custom_connection")

:::

:::{tab-item} VS Code Extension :sync: VSC

On the VS Code primary sidebar > prompt flow pane. You can find the connections pane to manage your local connections. Right click the item of the connection list to update or delete your connections. img ::: ::::


Manage runs

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

This documentation will walk you through how to manage your runs with CLI, SDK and VS Code Extension.

In general:

    For CLI, you can run pf/pfazure run --help in terminal to see the help messages.
    For SDK, you can refer to Promptflow Python Library Reference and check PFClient.runs for more run operations.

Let's take a look at the following topics:

    Manage runs
        Create a run
        Get a run
        Show run details
        Show run metrics
        Visualize a run
        List runs
        Update a run
        Archive a run
        Restore a run
        Delete a run

Create a run

::::{tab-set} :::{tab-item} CLI :sync: CLI To create a run against bulk inputs, you can write the following YAML file.

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: ../web_classification
data: ../webClassification1.jsonl
column_mapping:
   url: "${data.url}"
variant: ${summarize_text_content.variant_0}

To create a run against existing run, you can write the following YAML file.

$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: ../classification_accuracy_evaluation
data: ../webClassification1.jsonl
column_mapping:
   groundtruth: "${data.answer}"
   prediction: "${run.outputs.category}"
run: <existing-flow-run-name>

Reference here for detailed information for column mapping. You can find additional information about flow yaml schema in Run YAML Schema.

After preparing the yaml file, use the CLI command below to create them:

# create the flow run
pf run create -f <path-to-flow-run>

# create the flow run and stream output
pf run create -f <path-to-flow-run> --stream

The expected result is as follows if the run is created successfully.

img :::

:::{tab-item} SDK :sync: SDK Using SDK, create Run object and submit it with PFClient. The following code snippet shows how to import the required class and create the run:

from promptflow import PFClient
from promptflow.entities import Run

# Get a pf client to manage runs
pf = PFClient()

# Initialize an Run object
run = Run(
    flow="<path-to-local-flow>",
    # run flow against local data or existing run, only one of data & run can be specified.
    data="<path-to-data>",
    run="<existing-run-name>",
    column_mapping={"url": "${data.url}"},
    variant="${summarize_text_content.variant_0}"
)

# Create the run
result = pf.runs.create_or_update(run)
print(result)

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension

You can click on the actions on the top of the default yaml editor or the visual editor for the flow.dag.yaml files to trigger flow batch runs.

img img ::: ::::
Get a run

::::{tab-set} :::{tab-item} CLI :sync: CLI

Get a run in CLI with JSON format.

pf run show --name <run-name>

img

:::

:::{tab-item} SDK :sync: SDK Show run with PFClient

from promptflow import PFClient
# Get a pf client to manage runs
pf = PFClient()
# Get and print the run
run = pf.runs.get(name="<run-name>")
print(run)

:::

:::{tab-item} VS Code Extension :sync: VSC img ::: ::::
Show run details

::::{tab-set} :::{tab-item} CLI :sync: CLI

Get run details with TABLE format.

pf run show --name <run-name>

img

:::

:::{tab-item} SDK :sync: SDK Show run details with PFClient

from promptflow import PFClient
from tabulate import tabulate

# Get a pf client to manage runs
pf = PFClient()
# Get and print the run-details
run_details = pf.runs.get_details(name="<run-name>")
print(tabulate(details.head(max_results), headers="keys", tablefmt="grid"))

:::

:::{tab-item} VS Code Extension :sync: VSC img ::: ::::
Show run metrics

::::{tab-set} :::{tab-item} CLI :sync: CLI

Get run metrics with JSON format.

pf run show-metrics --name <run-name>

img

:::

:::{tab-item} SDK :sync: SDK Show run metrics with PFClient

from promptflow import PFClient
import json

# Get a pf client to manage runs
pf = PFClient()
# Get and print the run-metrics
run_details = pf.runs.get_metrics(name="<run-name>")
print(json.dumps(metrics, indent=4))

:::

::::
Visualize a run

::::{tab-set} :::{tab-item} CLI :sync: CLI

Visualize run in browser.

pf run visualize --names <run-name>

A browser will open and display run outputs.

img

:::

:::{tab-item} SDK :sync: SDK Visualize run with PFClient

from promptflow import PFClient

# Get a pf client to manage runs
pf = PFClient()
# Visualize the run
client.runs.visualize(runs="<run-name>")

:::

:::{tab-item} VS Code Extension :sync: VSC

On the VS Code primary sidebar > the prompt flow pane, there is a run list. It will list all the runs on your machine. Select one or more items and click the "visualize" button on the top-right to visualize the local runs.

img ::: ::::
List runs

::::{tab-set} :::{tab-item} CLI :sync: CLI

List runs with JSON format.

pf run list

img

:::

:::{tab-item} SDK :sync: SDK List with PFClient

from promptflow import PFClient

# Get a pf client to manage runs
pf = PFClient()
# list runs
runs = pf.runs.list()
print(runs)

:::

:::{tab-item} VS Code Extension :sync: VSC

On the VS Code primary sidebar > the prompt flow pane, there is a run list. It will list all the runs on your machine. Hover on it to view more details. img ::: ::::
Update a run

::::{tab-set} :::{tab-item} CLI :sync: CLI

Get run metrics with JSON format.

pf run update --name <run-name> --set display_name=new_display_name

:::

:::{tab-item} SDK :sync: SDK Update run with PFClient

from promptflow import PFClient

# Get a pf client to manage runs
pf = PFClient()
# Get and print the run-metrics
run = pf.runs.update(name="<run-name>", display_name="new_display_name")
print(run)

::: ::::
Archive a run

::::{tab-set} :::{tab-item} CLI :sync: CLI

Archive the run so it won't show in run list results.

pf run archive --name <run-name>

:::

:::{tab-item} SDK :sync: SDK Archive with PFClient

from promptflow import PFClient

# Get a pf client to manage runs
pf = PFClient()
# archive a run
client.runs.archive(name="<run-name>")

:::

:::{tab-item} VS Code Extension :sync: VSC img ::: ::::
Restore a run

::::{tab-set} :::{tab-item} CLI :sync: CLI

Restore an archived run so it can show in run list results.

pf run restore --name <run-name>

:::

:::{tab-item} SDK :sync: SDK Restore with PFClient

from promptflow import PFClient

# Get a pf client to manage runs
pf = PFClient()
# restore a run
client.runs.restore(name="<run-name>")

::: ::::
Delete a run

::::{tab-set} :::{tab-item} CLI :sync: CLI

Caution: pf run delete is irreversible. This operation will delete the run permanently from your local disk. Both run entity and output data will be deleted.

Delete will fail if the run name is not valid.

pf run delete --name <run-name>

:::

:::{tab-item} SDK :sync: SDK Delete with PFClient

from promptflow import PFClient

# Get a pf client to manage runs
pf = PFClient()
# delete a run
client.runs.delete(name="run-name")

::: ::::

Add bug bash sample flows (microsoft#1148)
00494dd
 · 
History
File metadata and controls

58 lines (43 loc) · 3.73 KB
Process image in flow

PromptFlow defines a contract to represent image data.
Data class

promptflow.contracts.multimedia.Image Image class is a subclass of bytes, thus you can access the binary data by directly using the object. It has an extra attribute source_url to store the origin url of the image, which would be useful if you want to pass the url instead of content of image to APIs like GPT-4V model.
Data type in flow input

Set the type of flow input to image and promptflow will treat it as an image.
Reference image in prompt template

In prompt templates that support image (e.g. in OpenAI GPT-4V tool), using markdown syntax to denote that a template input is an image: ![image]({{test_image}}). In this case, test_image will be substituted with base64 or source_url (if set) before sending to LLM model.
Serialization/Deserialization

Promptflow uses a special dict to represent image. {"data:image/<mime-type>;<representation>": "<value>"}

    <mime-type> can be html standard mime image types. Setting it to specific type can help previewing the image correctly, or it can be * for unknown type.

    <representation> is the image serialized representation, there are 3 supported types:

        url

        It can point to a public accessable web url. E.g.

        {"data:image/png;url": "https://developer.microsoft.com/_devcom/images/logo-ms-social.png"}

        base64

        It can be the base64 encoding of the image. E.g.

        {"data:image/png;base64": "iVBORw0KGgoAAAANSUhEUgAAAGQAAABLAQMAAAC81rD0AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABlBMVEUAAP7////DYP5JAAAAAWJLR0QB/wIt3gAAAAlwSFlzAAALEgAACxIB0t1+/AAAAAd0SU1FB+QIGBcKN7/nP/UAAAASSURBVDjLY2AYBaNgFIwCdAAABBoAAaNglfsAAAAZdEVYdGNvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVDnr0DLAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIwLTA4LTI0VDIzOjEwOjU1KzAzOjAwkHdeuQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMC0wOC0yNFQyMzoxMDo1NSswMzowMOEq5gUAAAAASUVORK5CYII="}

        path

        It can reference an image file on local disk. Both absolute path and relative path are supported, but in the cases where the serialized image representation is stored in a file, relative to the containing folder of that file is recommended, as in the case of flow IO data. E.g.

        {"data:image/png;path": "./my-image.png"}

Please note that path representation is not supported in Deployment scenario.
Batch Input data

Batch input data containing image can be of 2 formats:

    The same jsonl format of regular batch input, except that some column may be seriliazed image data or composite data type (dict/list) containing images. The serialized images can only be Url or Base64. E.g.

    {"question": "How many colors are there in the image?", "input_image": {"data:image/png;url": "https://developer.microsoft.com/_devcom/images/logo-ms-social.png"}}
    {"question": "What's this image about?", "input_image": {"data:image/png;url": "https://developer.microsoft.com/_devcom/images/404.png"}}

A folder containing a jsonl file under root path, which contains serialized image in File Reference format. The referenced file are stored in the folder and their relative path to the root path is used as path in the file reference. Here is a sample batch input, note that the name of input.jsonl is arbitrary as long as it's a jsonl file:

BatchInputFolder
|----input.jsonl
|----image1.png
|----image2.png

Content of input.jsonl

{"question": "How many colors are there in the image?", "input_image": {"data:image/png;path": "image1.png"}}
{"question": "What's this image about?", "input_image": {"data:image/png;path": "image2.png"}}


Set global configs

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

Promptflow supports setting global configs to avoid passing the same parameters to each command. The global configs are stored in a yaml file, which is located at ~/.promptflow/pf.yaml by default.

The config file is shared between promptflow extension and sdk/cli. Promptflow extension controls each config through UI, so the following sections will show how to set global configs using promptflow cli.
Set config

pf config set <config_name>=<config_value>

For example:

pf config set connection.provider="azureml://subscriptions/<your-subscription>/resourceGroups/<your-resourcegroup>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>"

Show config

The following command will get all configs and show them as json format:

pf config show

After running the above config set command, show command will return the following result:

{
  "connection": {
    "provider": "azureml://subscriptions/<your-subscription>/resourceGroups/<your-resourcegroup>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>"
  }
}

Supported configs
connection.provider

The connection provider, default to "local". There are 3 possible provider values.
local

Set connection provider to local with connection.provider=local.

Connections will be saved locally. PFClient(or pf connection commands) will manage local connections. Consequently, the flow will be executed using these local connections.
full azure machine learning workspace resource id

Set connection provider to a specific workspace with:

connection.provider=azureml://subscriptions/<your-subscription>/resourceGroups/<your-resourcegroup>/providers/Microsoft.MachineLearningServices/workspaces/<your-workspace>

When get or list connections, PFClient(or pf connection commands) will return workspace connections, and flow will be executed using these workspace connections. Secrets for workspace connection will not be shown by those commands, which means you may see empty dict {} for custom connections.

:::{note} Command create, update and delete are not supported for workspace connections, please manage it in workspace portal, az ml cli or AzureML SDK. :::
azureml

In addition to the full resource id, you can designate the connection provider as "azureml" with connection.provider=azureml. In this case, promptflow will attempt to retrieve the workspace configuration by searching .azureml/config.json from the current directory, then progressively from its parent folders. So it's possible to set the workspace configuration for different flow by placing the config file in the project folder.

The expected format of the config file is as follows:

{
  "workspace_name": "<your-workspace-name>",
  "resource_group": "<your-resource-group>",
  "subscription_id": "<your-subscription-id>"
}

    💡 Tips In addition to the CLI command line setting approach, we also support setting this connection provider through the VS Code extension UI. Click here to learn more.


Tune prompts using variants

:::{admonition} Experimental feature This is an experimental feature, and may change at any time. Learn more. :::

To better understand this part, please read Quick start and Run and evaluate a flow first.
What is variant and why should we care

In order to help users tune the prompts in a more efficient way, we introduce the concept of variants which can help you test the model’s behavior under different conditions, such as different wording, formatting, context, temperature, or top-k, compare and find the best prompt and configuration that maximizes the model’s accuracy, diversity, or coherence.
Create a run with different variant node

In this example, we use the flow web-classification, its node summarize_text_content has two variants: variant_0 and variant_1. The difference between them is the inputs parameters:

...
nodes:
- name: summarize_text_content
  use_variants: true
...
node_variants:
  summarize_text_content:
    default_variant_id: variant_0
    variants:
      variant_0:
        node:
          type: llm
          source:
            type: code
            path: summarize_text_content.jinja2
          inputs:
            deployment_name: text-davinci-003
            max_tokens: '128'
            temperature: '0.2'
            text: ${fetch_text_content_from_url.output}
          provider: AzureOpenAI
          connection: open_ai_connection
          api: completion
          module: promptflow.tools.aoai
      variant_1:
        node:
          type: llm
          source:
            type: code
            path: summarize_text_content__variant_1.jinja2
          inputs:
            deployment_name: text-davinci-003
            max_tokens: '256'
            temperature: '0.3'
            text: ${fetch_text_content_from_url.output}
          provider: AzureOpenAI
          connection: open_ai_connection
          api: completion
          module: promptflow.tools.aoai

You can check the whole flow definition in flow.dag.yaml.

Now we will create a variant run which uses node summarize_text_content's variant variant_1. Assuming you are in working directory <path-to-the-sample-repo>/examples/flows/standard

::::{tab-set}

:::{tab-item} CLI :sync: CLI

Note we pass --variant to specify which variant of the node should be running.

pf run create --flow web-classification --data web-classification/data.jsonl --variant '${summarize_text_content.variant_1}' --column-mapping url='${data.url}' --stream --name my_first_variant_run

:::

:::{tab-item} SDK :sync: SDK

from promptflow import PFClient

pf = PFClient()  # get a promptflow client
flow = "web-classification"
data= "web-classification/data.jsonl"

# use the variant1 of the summarize_text_content node.
variant_run = pf.run(
    flow=flow,
    data=data,
    variant="${summarize_text_content.variant_1}",  # use variant 1.
    column_mapping={"url": "${data.url}"},
)

pf.stream(variant_run)

:::

:::{tab-item} VS Code Extension :sync: VS Code Extension img img :::

::::

After the variant run is created, you can evaluate the variant run with a evaluation flow, just like you evalute a standard flow run.
