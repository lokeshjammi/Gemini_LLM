from bs4 import BeautifulSoup
import requests


class Website:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.links = self.soup.find_all('a')

    def get_links_count(self):
        print(len(self.links))

    def get_links_url(self):
        get_links = []
        for link in self.links:
            get_links.append(link.get('href'))
        return get_links

    def get_webpage_details(self):
        get_webpage_title = self.soup.title.string
        get_webpage_details = self.soup.body.get_text(separator="\n", strip=True)
        return get_webpage_title, get_webpage_details


website = Website('https://www.anthropic.com/')
website.get_webpage_details()