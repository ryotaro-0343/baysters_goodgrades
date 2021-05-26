import requests
from bs4 import BeautifulSoup

url = 'https://www.baystars.co.jp/game/result'
r = requests.get(url)
soup = BeautifulSoup(r.text)

found = soup.select('.information--date')
a = found[0]
print('{0}'.format(a.text[:6]))
