import urllib, urllib.request
import feedparser
from utilities import clean_text
import os
import requests
import PyPDF2

class ArxivAPI():
    def __init__(self):
        self.url = "http://export.arxiv.org/api/query?"
        
    def search(self, query, start, max_results):
        search_query = 'search_query=%s&start=%i&max_results=%i' % (query, 
                                                            start,
                                                            max_results)
        full_url = self.url+search_query
        data = urllib.request.urlopen(full_url)
        response = data.read().decode('utf-8')

        response_dict = {}
        feed = feedparser.parse(response)
        print(feed)
        for entry in feed.entries:
            response_dict[entry.id.split('/abs/')[-1]] = {'title': clean_text(entry.title),
                                                          'authors': clean_text(entry.author),
                                                          'summary': clean_text(entry.summary),
                                                          'published': entry.published,
                                                          'link': entry.link,
                                                          'downloadlink': entry.links[-1]['href'],
                                                          'id': entry.id.split('/abs/')[-1]}    
        
        
        return response_dict

    def downloadPaper(self, response_dict):

        pdf_link = response_dict[list(response_dict.keys())[0]]['downloadlink']

        save_path = 'paper1.pdf'
        print(pdf_link)
        response = requests.get(pdf_link)

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")
        

if __name__ == "__main__":
    querytext = "genomic"
    start=5
    max_results = 1
    searchapi = ArxivAPI()
    response = searchapi.search(querytext, start, max_results)
    searchapi.downloadPaper(response)

