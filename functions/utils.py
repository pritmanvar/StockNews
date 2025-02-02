import tiktoken
import json

def calculate_tokens(news):
    encoding = tiktoken.get_encoding("cl100k_base")
    news_json = json.dumps(news)
    tokens = encoding.encode(news_json)
    num_tokens = len(tokens)
    return num_tokens

def unicode_to_string(s):
    return s.encode().decode('unicode_escape')