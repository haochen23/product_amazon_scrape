import requests
import re
import csv
url = 'http://www.amazon.com/s?keywords=Manuka+Health'
htmltext = requests.get(url).content.decode('utf-8')
pattern = re.compile(r"(?:[/dp/]|$)([A-Z0-9]{10})")
# print(htmltext)
ASINLIST = list(set(re.findall(pattern, htmltext)))
print(ASINLIST)
with open('ASIN_list.csv', 'w',newline = '') as f:
    writer = csv.writer(f, dialect='excel')
    for Asin in ASINLIST:
        writer.writerow([Asin])
