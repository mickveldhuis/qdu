import json
import feedparser as fp
from html2text import HTML2Text

class Service:
    """
    The Parent class of services.
    """

    def __init__(self):
        self.data = None
    
    def _retrieve(self):
        pass

class NewsService(Service):
    def __init__(self, provider, controller):
        super().__init__()
        self.provider = provider
        self.controller = controller 
    
    def get_news(self):
        self._retrieve()
        
        articles = []

        for art in self.data:
            title = art['title']
            date = art['published'] # 'published_parsed'
            raw_text = art['summary']
            url = art['link']

            h2t = HTML2Text()
            h2t.ignore_links = True
            h2t.ignore_images = True

            text = h2t.handle(raw_text)[0:200].strip()

            if not text[-1] in ('.', '?', '!'):
                text += '...'

            tmp_article = {
                'title': title,
                'date':  date,
                'text': text,
                'url': url
            }

            articles.append(tmp_article)
        
        return articles
    
    def _retrieve(self):
        prov = self.controller.get_providers()
        
        raw_data = fp.parse(prov[self.provider]['url']).entries
        self.data = raw_data