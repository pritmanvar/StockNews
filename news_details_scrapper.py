import traceback

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

urls = ["https://www.zeebiz.com/personal-finance/news-power-of-compounding-interest-mutual-fund-sip-retirement-corpus-planning-calculator-how-soon-you-can-build-inr-rs-15000000-with-monthly-investments-of-rs-1500-2500-3500-market-linked-return-345207"]

def get_news_details(url, platform, title):
    try:
        loader = AsyncHtmlLoader([url])
        docs = loader.load()

        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)
        
        detailed_news = """
    # Title: {title}
    # Summary: {summary}
    # Description: 
    {description}"""
        
        page_content = docs_transformed[0].page_content
        first_index = page_content.lower().find(title[:30].lower())
        page_content = page_content[first_index:]
        if "the hindu business" in platform.lower():
            last_index = page_content.lower().find("read comments")
            page_content = page_content[:last_index]
        elif "bloomberg quint" in platform.lower():
            last_index = page_content.lower().find("also read")
            page_content = page_content[:last_index]
        elif "moneycontrol" in platform.lower():
            last_index = page_content.lower().find("moneycontrol news")
            page_content = page_content[:last_index]
        elif "economic times" in platform.lower():
            last_index = page_content.lower().find("you can now subscribe to our")
            page_content = page_content[:last_index]
        elif "zee business" in platform.lower() or "zee bussiness" in platform.lower():
            last_index = page_content.lower().find("RECOMMENDED STORIES".lower())
            page_content = page_content[:last_index]
        elif "finshots" in platform.lower():
            last_index = page_content.lower().find("Don’t forget to share this story".lower())
            page_content = page_content[:last_index]
        else:
            print(platform)
            print("##################################################### DETAILS NOT FOUND ####################################################################")

        print(docs_transformed[0].metadata)
        detailed_news = detailed_news.format(
            title=title,
            summary=docs_transformed[0].metadata["description"],
            description=page_content)
        
        if page_content:
            return detailed_news, True
        else:
            return "", False
    except Exception as e:
        traceback.print_exc()
        print(e)
        return "", False