from agents import post_content_llm, get_text_post_content

details = """UBS Global Research started coverage on India's second-largest stock exchange, BSE Ltd., with a 'buy' rating, noting improvement in volumes. Volumes moving from National Stock Exchange Ltd. to BSE are not fully priced in, according to the brokerage.

UBS Global Research gave a target price of Rs 5,350 apiece, which implied a 36.26% upside from Friday's closing price. BSE's valuation is at 33 times one-year forward premium.

BSE's market share increased because of better broker management and the offering of an alternate expiry day to NSE. UBS Global expects BSE to gain further market share.

NSE being the default exchange puts BSE at a disadvantage. This disadvantage kept BSE's cash market share lower. NSE dominates 93–94% market share. Hence, implementing a common contract note can help generate a combined order book and neutrality among brokers, UBS Global Research said.
ADVERTISEMENT

UBS Global Research expects BSE's Star MF platform to register a 37% CAGR over financial years 2024 and 2027, on the back of sticky mutual fund distribution. Fees from listing and book-building activities to register a 21% revenue CAGR in the same period. Ignoring some reduction in cash turnover market share for BSE in recent months, UBS Global Research projects 14% CAGR for the segment.

A cyclical slowdown will cause a 20% decline in average daily premium turnover by financial year 2026. A change in open interest calculation methodology, as proposed in the Securities Exchange Board of India's recent draft consultation, adds to the recent risks to the BSE's growth.

"""

reference = "https://www.ndtvprofit.com/markets/bse-gets-ubs-buy-initiation-as-volumes-moving-from-nse-not-priced-in"

content = get_text_post_content(details, "https://www.ndtvprofit.com/markets/bse-gets-ubs-buy-initiation-as-volumes-moving-from-nse-not-priced-in")

content = content[0].replace('"', '')

if "</think>" in content:
    content = content.split("</think>")[1]

start_indx = content.find("#")
content = f"""{content[:start_indx]}
{reference}

{content[start_indx:]}
"""
print(content)