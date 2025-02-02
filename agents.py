import json
import time

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from schemas import NewsList

load_dotenv()

llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0.6,
    max_tokens=130000,
    timeout=None,
    max_retries=2,
    # other params...
)

def basic_analysis(news_list):
    prompt = PromptTemplate.from_file(
                template_file="prompts/news_selector.yml",
                input_variables=["list_of_news_object"]
            )


    for _ in range(5):
        response = llm.invoke(prompt.invoke({"list_of_news_object": news_list}))
        
        print(response.content)
        # Extract the substring between the first '[' and the last ']'
        start_index = response.content.find('[')
        end_index = response.content.rfind(']')
        
        print(start_index, " START INDEX ###################################")
        print(end_index, " LAST INDEX ###################################")
        abstracted_string = ""
        if start_index != -1 and end_index != -1 and start_index < end_index:
            abstracted_string = response.content[start_index : end_index + 1]
            print("ABSTRACTED STRING")
            print(abstracted_string)
            print()
            results = json.loads(abstracted_string)
            print("PARSER RESPONSE")
            print(results)
            print(type(results))
            
            return results

        time.sleep(30)
        
    raise ValueError("LLM response is not in correct format.")
    