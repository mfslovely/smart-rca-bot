from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model="gemma:2b")  # You can change to llama3 or mistral for better formatting

template = """
You are a Root Cause Analysis (RCA) bot. Based on the following system logs, analyze the issue and generate a structured RCA report in this format exactly:

📄 Problem:
<Explain the problem in 2-3 lines based on the logs>

🛠️ Step to Solve:
<List 2-4 actionable and technical steps to investigate or fix the issue>

📝 Summary:
<One-line summary of the most likely root cause>

Logs:
{logs}
"""

prompt = PromptTemplate(input_variables=["logs"], template=template)

def get_root_cause(logs: list[str]) -> str:
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run("\n".join(logs))
