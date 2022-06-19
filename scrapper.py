import requests
from bs4 import BeautifulSoup

def extract_pages(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text, "html.parser")
  pages = []
  nav = soup.find("nav", "pg_wrap")
  pg_current = int(nav.find("strong", "pg_current").text)
  pages.append(pg_current)
  pg_nexts = nav.find_all("a", "pg_page")
  for pg_next in pg_nexts[:-2]:
    pages.append(int(pg_next.text[:-3]))
  max_page = pages[-1]
  return max_page # 10

def extract_page_info(result):
  title = result.find("a", "td_subject").find("span").text
  company = result.select_one("td:nth-child(2)").select_one("span").text
  location = result.select_one("td:nth-child(3)").select_one("span").text.strip()
  id = result.find("a")["href"][3:]
  info = {"title": title, "company": company, "location": location, "link": f"https://www.jangyu.net/board/{id}"}
  return info

def extract_page(max_page, url):
  infos = []
  for page in range(max_page):
    request = requests.get(f"{url}&page={page}")
    soup = BeautifulSoup(request.text, "html.parser")
    results = soup.find("div", "tbl_head01").find_all("tr")
    del results[0:33]
    del results[20]
    for result in results:
      info = extract_page_info(result)
      infos.append(info)
  return infos

def get_jobs(word):
  url = f"https://www.jangyu.net/board/bbs/board.php?bo_table=inc_guin&sca=&sop=and&sfl=wr_subject&stx={word}"
  max_page = extract_pages(url)
  jobs = extract_page(max_page, url)
  return jobs
    
  
  