import os
import json
import time
import traceback

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.cache import BaseCache
from dotenv import load_dotenv

load_dotenv()

ChatGroq.model_rebuild()

analysis_llm_indx = 0
analysis_llm = [
    ChatGroq(
        model="llama-3.2-3b-preview",
        temperature=0.8,
        max_tokens=800,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("GROQ_ANALYSIS_API_KEY"),
    ),
    ChatGroq(
        model="llama-3.2-3b-preview",
        temperature=0.8,
        max_tokens=800,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("GROQ_ANALYSIS_API_KEY2"),
    ),
]
post_content_llm = ChatGroq(
    model="qwen-qwq-32b",
    temperature=0.8,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("THREADS_POST_GENERATION_API_KEY"),
)

class NewsObject(BaseModel):
    title: str = Field(description="Title of the news")
    url: str = Field(description="URL of the news")
    description: str = Field(description="Description of the news")
    time: str = Field(description="Time of the news")
    source: str = Field(description="Source of the news")
    will_it_directly_impact_any_stock: str = Field(description="Will it directly impact any Indian stock -> true/false")
    directly_mentioned_companies_in_news: list = Field(description="List of companies mentioned in the news")
    how_will_it_impact: str = Field(description="How will it impact")
    reason: str = Field(description="Reason for the impact")
    
def basic_analysis(news):
    global analysis_llm_indx
    prompt = PromptTemplate.from_file(
        template_file="prompts/news_selector.yml",
        input_variables=["news_object"],
    )
    # parser = JsonOutputParser(pydantic_object=NewsObject)


    for _ in range(5):
        try:
            response = analysis_llm[analysis_llm_indx].invoke(
                prompt.invoke({"news_object": news})
            )
            analysis_llm_indx = (analysis_llm_indx + 1) % len(analysis_llm)
            print("################ BASIC ANALYSIS AGENT RESPONSE ################")
            print(response.content)
            print("################ BASIC ANALYSIS END AGENT RESPONSE ################")

            start_index = response.content.find("{")
            end_index = response.content.rfind("}")

            print("start index:", start_index)
            print("end index:", end_index)

            abstracted_string = ""
            if start_index != -1 and end_index != -1 and start_index < end_index:
                abstracted_string = response.content[start_index : end_index + 1]

                try:
                    results = json.loads(abstracted_string)
                    print(results)
                    return results
                except Exception as e:
                    print(e)
                    traceback.print_exc()
        except Exception as e:
            print(e)
            traceback.print_exc()
            time.sleep(30)

    raise ValueError("LLM response is not in correct format.")


def get_text_post_content(details, reference):
    try:
        prompt = PromptTemplate.from_file(
            template_file="prompts/post_generator_without_source.yml",
            input_variables=["NEWS_CONTENT", "CHAR_LENGTH"],
        )

        user_query = prompt.invoke(
            {"NEWS_CONTENT": details, "CHAR_LENGTH": 490- len(reference)}
        )
        response = post_content_llm.invoke(user_query)

        print("POST CONTENT RESPONSE:", response)
        
        content = response.content.replace('"', '')

        if "</think>" in content:
            content = content.split("</think>")[1]

        start_indx = content.find("#")
        content = f"""{content[:start_indx]}
        {reference}

        {content[start_indx:]}
        """
        
        return content, True
    except Exception as e:
        print(e)
        traceback.print_exc()
        return "", False
