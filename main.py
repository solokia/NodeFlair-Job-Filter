import requests
import time
import random
import csv
import argparse

endpoint = "https://www.nodeflair.com/api/v2/jobs?"
# joblisting = []
seniorities = ["intern","junior","mid","senior","lead","manager","director","principal"]
positions = []#can"t be bothered too many use query instead...
tech_stacks= ["AWS","Google+Cloud","Python","Vue.js","JavaScript","Typescript","Docker","Kubernetes","Go","Node.js"]

class NodeFlairService:
    def __init__(self,**kwargs):        
        # self.page = 1
        self.job_listing=[]
        self.finalPage=1
        self.salary=kwargs["salary"]
        self.params = {"query":kwargs["query"],
                    "page":1,
                    "sort_by":kwargs["sortby"],
                    "seniorities%5B%5D":"&seniorities%5B%5D=".join(kwargs["seniorities"]),
                    "tech_stacks%5B%5D":"&tech_stacks%5B%5D=".join(kwargs["techstacks"]),
                    "salary_mind":self.salary}
        self.paramsStr = "".join([k+"="+str(v)+"&" for k,v in self.params.items()]) #why didn't i just join the loops... 
        
        self.sleep_min=kwargs["sleepmin"]
        self.sleep_max=kwargs["sleepmax"]
    def setup_crawl(self):
        uri = endpoint+self.paramsStr[:-1]
        print(uri)
        res = requests.get(uri).json()
        print(res)
        print(res.keys())
        self.job_listing += res["job_listings"]
        self.finalPage = res["total_listings_count"]/len(res["job_listings"])
        self.params["page"]+=1
        print("max pages : %s"%(str(self.finalPage)))

    def crawl(self):
        print("start crawling")
        while(self.params["page"]<self.finalPage):
            time.sleep(random.uniform(self.sleep_min,self.sleep_max))
            self.paramsStr = "".join([k+"="+str(v)+"&" for k,v in self.params.items()])
            uri = endpoint+self.paramsStr[:-1]
            print("page: %s"%(str(self.params["page"])))
            res = requests.get(uri).json()
            # print(res.json())
            self.job_listing += res["job_listings"]
            self.params["page"]+=1

    def output(self):
        temp = self.job_listing
        for i in range(len(temp)):
            temp[i]["job_path"]="https://www.nodeflair.com/"+temp[i]["job_path"]
            temp[i]["companyname"] = temp[i]["company"]["companyname"]
        keys = temp[0].keys()
        with open("out.csv", "w", newline="") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(temp)

    def start(self):
        self.setup_crawl()
        self.crawl()
        self.output()

def run():

    parser = argparse.ArgumentParser(description="Command Line Utility for scrapping Nodeflaire")
    # parser.add_argument("-r", "--resolution", default="-1:360", help="output resolution. defaulted -1:360. scales to width based on 360 as height.")
    parser.add_argument("-sr", "--seniorities", default=seniorities, help="sets seniorities seperated by space check Nodeflaire for spelling", nargs="*")
    parser.add_argument("-ts", "--techstacks", default=tech_stacks, help="sets techstacks seperated by space check Nodeflaire for spelling", nargs="*")
    parser.add_argument("-s", "--salary", default=5000, help="Set salary default 5000 INT ONLY NO CHECKS DONE")
    parser.add_argument("-q", "--query", default="", help="Set query default empty")
    parser.add_argument("-sb", "--sortby", default="recent", help="sort by default recent")
    parser.add_argument("-mi", "--sleepmin", default=1, help="minimum sleep secs before next query")
    parser.add_argument("-ma", "--sleepmax", default=2, help="minimum sleep secs before next query")
    
    args = parser.parse_args()
    nf = NodeFlairService(**vars(args))
    nf.start()

if __name__ == "__main__":
    run()