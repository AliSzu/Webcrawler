from bs4 import BeautifulSoup
import requests
   
urls=[]
   
def scrape(site):
    html = requests.get(site).text 
    soup = BeautifulSoup(html, 'lxml')

    if (site in urls):
        return
    else:
        urls.append(site)
  
    body = soup.find('div', class_ = 'mw-parser-output')
    div = body.find(id="See_also")
    if (div):
        hrefs = div.findNext(['ul'])
        while True:
            if hrefs.name == 'ul':
                for link in hrefs.find_all('a'):
                    if ":" not in link.get('href') and "." not in link.get('href'):
                        new_link = "https://en.wikipedia.org"+link.get('href')
                        if (new_link not in urls): # - czasami podstrony odwolują się do stron, przez które już przeslismy, to ma temu zapobiec zanim funkcja zostanie wywołana z powtarzającym sie linkiem
                            print(new_link)
                            scrape(new_link)
                hrefs = hrefs.findNext(['span'])
            try:
                if (hrefs.get('id') == "External_links" or hrefs.get('id') == "References" or hrefs.get('id') == "Notes" or hrefs.get('id') == "Footnotes" ):
                    break
                else:
                    hrefs = hrefs.findNext(['span'])
                    if ("Navigation" in hrefs): # -- Czasami gdy po sekcji see also nie ma nic to program wychodzi z body, to ma temu zapobiec
                        break
                    hrefs = hrefs.findNext(['ul'])
            except:
                break
       
    
if __name__ =="__main__":
    site = input("Prosze podac link do strony: ")
    scrape(site)
    


