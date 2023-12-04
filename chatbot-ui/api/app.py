import os
import openai
import pinecone  
import langchain
from flask_cors import CORS
from dotenv import load_dotenv 
from flask import Flask, request, make_response, jsonify
from langchain.vectorstores import Pinecone 
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, Tool
from langchain.chains import RetrievalQA, LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory

load_dotenv()
verbosity = False

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), 
                 temperature=0.0, 
                 model_name='gpt-4-1106-preview')

embed = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    openai_api_key=openai.api_key
)

pinecone.init(      
	api_key=os.getenv("PINECONE_API_KEY"),      
	environment=os.getenv("PINECONE_ENV")     
)   

index_name = 'kegg-medicus-database-index'
index = pinecone.Index(index_name)

vectorstore = Pinecone(
    index=index, 
    embedding=embed, #.embed_query(), 
    text_key= "text"
)

# vectore database
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# websearch powered by DuckDuckGo
wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
search = DuckDuckGoSearchRun(api_wrapper=wrapper, backend='text')
def duck_wrapper(input_text):
    try:
        search_results = search.run(f'''{input_text}''') 
    except Exception as er:
        print(er)
        return "There was an error fetching results for that query. Please try again"
    # print(search_results)
    else:
        return search_results

# conversation summary tool
mem_template = """This is a conversation between a human and a bot:
{chat_history}
Write a summary of the conversation for {input}:
"""

mem_prompt = PromptTemplate(input_variables=["input", "chat_history"], template=mem_template)
memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=memory)
summary_chain = LLMChain(
    llm=llm,
    prompt=mem_prompt,
    verbose=verbosity,
    memory=readonlymemory,  # use the read-only memory to prevent the tool from modifying the memory
)

# tool objects list for agent
tools = [
    Tool(
        name='Medicus Text Base',
        func=qa.run,
        description=('''use this tool to respond to queries about drugs (medicine) 
                     and drugs interactions for (contraindications (CI) and precautions (P)),
                    disease and the human genome'''
        )
    ), 
    Tool(
        name ='Web Search',
        func=duck_wrapper,
        description=('''use this tool to answer more general questions 
            about health and wellness
            '''
        )
    ),
    Tool(
        name='Summary',
        func=summary_chain.run,
        description='''useful for when you summarize a conversation. 
        The input to this tool should be a string, 
        representing who will read this summary.''',
    )
]

tool_names = [tool.name for tool in tools]

# initialization of zero shot agent prompt template
from langchain.agents import ZeroShotAgent

prefix = """Act as an expert medical advisor. 
Answering question as best as YOU can. 
You have access to the following tools:"""

suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

#  initializing zeroshot agent chain
llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=verbosity)

agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, 
    tools=tools, verbose=True, 
    memory=memory, 
)

def get_response(input):
    return agent_chain(input)
langchain.debug = verbosity

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": os.getenv("CORS_ORIGIN")}})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    return jsonify(get_response(user_input))

if __name__ == '__main__':
    app.run(debug=True, port=5000)