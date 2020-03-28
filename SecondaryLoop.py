import time
import requests

while True:
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Updates", 'r') as f:
        text = f.readline()
        if text != "":
            r = requests.get(url=text).text
        f.close()
    time.sleep(6)
