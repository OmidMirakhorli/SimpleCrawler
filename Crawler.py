from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import Queue
from bs4 import BeautifulSoup
import threading
import sys
import time
import requests


class AppAnyRun():
    NUMBERTHREAD = 16
    BASE_URL = "https://app.any.run"
    Sub_URL = "https://app.any.run/submissions"
    PRIVACY = 'https://app.any.run/privacy.html'
    tasks = set()
    soup = None
    md5s = set()
    queue = Queue()
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    def define_headers(referer):
        headers={
        'Host': 'app.any.run',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'image/webp,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': referer,
        'Cookie': '__cfduid=dbc6c69329c8452fabae354f2e6b861251595431455; _ga=GA1.2.1464104828.1595431463; _gid=GA1.2.74228395.1595431463; x_mtok=Wy23zxSCzbH9dqZvv; _gat_UA-85156687-1=1',
        'TE': 'Trailers',
        }
        return headers


    def __init__(self):
        driver = webdriver.Firefox(executable_path="C:/Users/omid/Desktop/geckodriver.exe", options=self.options)
        driver.get(self.Sub_URL)
        page = driver.page_source
        time.sleep(5)
        with open("as.html", "w", encoding='utf-8') as dd:
            dd.write(page)
        driver.quit()
        self.soup = BeautifulSoup(page, 'html.parser')
        rows = self.soup.find_all('div', {'class': 'history-table--content__row'})
        self.insert2tasks(rows)



    def gatherLinks(self,tasks):
            urls = set()
            for l in tasks:
                s = BeautifulSoup(l ,'html.parser')
                if s.find('div',{'class':'label label-danger'}):
                    urls.add(str(l))
            return urls



    def fetch_md5(self,url):

        f = BeautifulSoup(url,'html.parser')
        strs = f.select_one(".hash__value")
        self.md5s.add(strs.get_text())
        '''
        for j in strs:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(str(j))
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            hash = BeautifulSoup(str(j),'html.parser')
            hash.find('div',{'class':'hash__value'})
            md5 = hash.get_text()
            print(md5)
            self.md5s.add(md5)
        '''

    def creat_workers(self):
        for _ in range(self.NUMBERTHREAD):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()


    def work(self):
        while True:
            page = self.queue.get()
            self.fetch_md5(str(page))
            self.queue.task_done()


    def create_jobs(self):
        f= self.gatherLinks(self.tasks)
        for link in f:
            self.queue.put(str(link))

        self.queue.join()



    def insert2tasks(self,tasks):
        for task in tasks:
            self.tasks.add(str(task))


    def printmd5(self):
        for md5 in self.md5s:
            print(str(md5))
        sys.stdout.flush()

    '''
    for link in urls:
         try:
            print(link)
            driver.get(link)
            f = WebDriverWait(driver, 10).until(EC.presence_of_element_located("label label-danger"))
    
            danger = driver.find_element_by_class_name(By.CLASS_NAME,"label label-danger")
            if danger !=None or "":
               print(danger.text)
               hash = driver.find_element_by_class_name("descr descr--hash js-copy__md5")
               md5s.add(hash.text)
            else:
                print("Nothing")
         except:
            print("car")
    
    for k in md5s:
        print(k)
    
    
    '''
    '''
        url = urls[0]
        print(BASE_URL + url)
        driver2.get(BASE_URL + url)
        task_page = driver2.page_source
        with open("as.html","w",encoding='utf-8') as dd:
            dd.write(task_page)
        '''

    '''
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', '/tmp')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/zip')
    driver = webdriver.Firefox(executable_path="C:/Users/omid/Desktop/geckodriver.exe",firefox_profile=profile)
    driver.minimize_window()
    driver.get(BASE_URL)
    task_urls = driver.find_elements_by_xpath("//a[@href]")
    for url in task_urls[2:]:
        link = url.get_attribute('href')
        print(link)
        urls.add(link)
        
        
         tasksoup = BeautifulSoup(task_page, 'html.parser')
        f = tasksoup.find('div', {'class': 'label label-danger'})
        if f != None or "":
            hash = tasksoup.find('div', {'class': 'descr descr--hash js-copy__md5'})
            if hash:
                print('md5:{}'.format(hash.get_text()))
                self.md5s.add(hash.get_text())
            else:
                print("md5 doesnt exists")
        else:
            print("Not Malicious")
            
            
            
            
                   urls = set()
        for link in tasks:
            url = link.get('href')
            if url == None or url == '/' or url == self.PRIVACY:
                pass
            else:
                print('link:{}'.format(url))
                urls.add(url)
        
        '''