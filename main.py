from web_scraping import load_data

print("Search File [String]:", end= " ")
search = input()
search.replace(' ', '+')
print("Limit File [Integer]:", end= " ")
limit = input()
print("Save To [sql/csv]:", end= " ")
save_to = input()

url = 'https://arxiv.org/search/?query='+ search + '&searchtype=all&source=header'

load_data(url, int(limit), 1, save_to)

