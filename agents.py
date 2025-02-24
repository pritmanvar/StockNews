import os
import json
import time
import traceback

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

analysis_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.8,
    max_tokens=130000,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_ANALYSIS_API_KEY"),
)
post_content_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.8,
    max_tokens=250,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("THREADS_POST_GENERATION_API_KEY"),
)

def basic_analysis(news_list):
    prompt = PromptTemplate.from_file(
                template_file="prompts/news_selector.yml",
                input_variables=["list_of_news_object"]
            )

    for _ in range(5):
        try:
            response = analysis_llm.invoke(prompt.invoke({"list_of_news_object": news_list}))
            print("################ BASIC ANALYSIS AGENT RESPONSE ################")
            print(response)
            print("################ BASIC ANALYSIS END AGENT RESPONSE ################")

            # Extract the substring between the first '[' and the last ']'
            start_index = response.content.find('[')
            end_index = response.content.rfind(']')
            

            print("start index:",start_index)
            print("end index:",end_index)

            abstracted_string = ""
            if start_index != -1 and end_index != -1 and start_index < end_index:
                abstracted_string = response.content[start_index : end_index + 1]
                
                try:
                    results = json.loads(abstracted_string)
                    return results
                except Exception as e:
                    print(e)
                    traceback.print_exc()

            time.sleep(30)
        except Exception as e:
            print(e)
            traceback.print_exc()

    raise ValueError("LLM response is not in correct format.")

def get_text_post_content(details, reference):
    try:
        prompt = PromptTemplate.from_file(
                    template_file="prompts/post_generator.yml",
                    input_variables=["NEWS_CONTENT", "REFERENCE_URL"]
                )
        
        user_query = prompt.invoke({"NEWS_CONTENT": details, "REFERENCE_URL": reference})
        response = post_content_llm.invoke(user_query)

        print("POST CONTENT RESPONSE:", response)
        return response.content, True
    except Exception as e:
        print(e)
        traceback.print_exc()
        return "", False