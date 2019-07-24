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
    def __init__(self, provider='nos'):
        super().__init__()
        self.provider = provider
        self.prov_data = None
    
    def get_news(self):
        self._retrieve()
        
        articles = []

        for art in self.data:

            title = art[self.prov_data['title']]
            date = art[self.prov_data['date']]
            raw_text = art[self.prov_data['text']]
            url = art[self.prov_data['url']]

            h2t = HTML2Text()
            h2t.ignore_links = True
            h2t.ignore_images = True

            text = h2t.handle(raw_text)[0:200].strip()

            if not text[-1] in ('.', '?', '!'):
                text += '...'

            tmp_article = {
                'title': title,
                'date':  '{}:{}'.format(date.tm_hour, date.tm_min),
                'text': text,
                'url': url
            }

            articles.append(tmp_article)
        
        return articles
    
    def _retrieve(self):
        with open('providers.json', 'r') as prov_file:
            prov = json.load(prov_file)
        
        self.prov_data = prov[self.provider]
        
        raw_data = fp.parse(self.prov_data['website']).entries
        self.data = raw_data