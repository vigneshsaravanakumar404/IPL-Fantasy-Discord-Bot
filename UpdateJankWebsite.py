from requests import get
from time import sleep

urls = [
    "https://ipl-fantasy-api.onrender.com/",
    "https://ipl-fantasy-api.onrender.com/players/all",
    "https://ipl-fantasy-api.onrender.com/api/players/all",
]

while True:
    for url in urls:
        print(get(url).status_code)
    sleep(5 * 60)
