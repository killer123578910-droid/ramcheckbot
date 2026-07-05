import requests
import os
from dotenv import load_dotenv
load_dotenv()
key=os.getenv("api")
baseu=os.getenv("base_url")
header={
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Basic ssaaAS76DAs6faFFghs1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
count=1
while(True):
    ulr=f'{baseu}&page={count}'
    data =requests.get(ulr,headers=header)
    datae = data.json()
    if not datae["total"] or len(datae["list"])==0:
        break
    sp=datae["list"]
    for i in sp:
        print(f'{i["productName"]} {i["price"]}')
    count+=1
