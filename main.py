from web_scraping import load_data

print("Search File:", end= " ")
search = input()
print("Limit File:", end= " ")
limit = input()

url = 'https://arxiv.org/search/?query='+ search + '&searchtype=all&source=header'

load_data(url, int(limit))



