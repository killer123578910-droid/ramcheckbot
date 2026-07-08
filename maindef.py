from datetime import datetime
import requests
import os
from dotenv import load_dotenv


matra={
    283:"Ram",
    284:"SSD",
    279:"VGA",
    278:"MAIN"}

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
def crawling():
    crawldatetime=datetime.now().isoformat()
    kq1={"Ram":[],
         "SSD":[],
         "VGA":[],
         "MAIN":[],
         "crawl_time":crawldatetime}
    for key,value in matra.items():
        kq=[]
        count=1
        while(True):
            ulr=f'{baseu}&page={count}&category={key}'
            data =requests.get(ulr,headers=header)
            datae = data.json()
            sp=datae["list"]
            if not sp:
                break
            kq.extend(sp)
            count+=1
        kq1[value]=kq
    return kq1