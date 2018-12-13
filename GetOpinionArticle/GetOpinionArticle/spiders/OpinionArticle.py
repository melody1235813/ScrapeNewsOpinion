import scrapy
import json
from GetOpinionArticle.items import OpinionArticleItem

class opinionArticleSpider(scrapy.Spider):
    name = "opnews"
#    base_url = "https://www.bing.com/news/search?q={0}&qs=n&form=NWRFSH&sp=-1&pq={0}&sc=0-29&sk=&cvid=CCAEF3DCCD9C41ACB9A1220F2C1591FD&p1=%5bNewsVertical+UserAugmentation%3d%22%5bqlf%242102%3a15%5d%22%5d&setflight=filteropinion"
#    query_set = ["donald trump", "medical marijuana", "# disruptj20", "olympics boxing"]
#    start_urls = ["https://www.bing.com/news/search?q={0}&setflight=filteropinion&mkt=en-US&p1=%5bNewsVertical+UserAugmentation%3d%22%5bqlf%242102%3a15%5d%22%5d&filter=NewsVerticalV2&format=pbxml".format(q.replace(' ', '%20')) for q in query_set]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # python3
        self.query_set = []
        if self.query_set_file is not None:
            self.query_set = [q.strip('\n') for q in open(self.query_set_file, 'r', encoding='utf8').readlines()] 
        self.start_urls = ["https://www.bing.com/news/search?q={0}&setflight=filteropinion&mkt=en-US&p1=%5bNewsVertical+UserAugmentation%3d%22%5bqlf%242102%3a15%5d%22%5d&filter=NewsVerticalV2&format=pbxml".format(q.replace(' ', '%20')) for q in self.query_set]   
        self.url_q_dict = {}
        for q in self.query_set:
            self.url_q_dict["https://www.bing.com/news/search?q={0}&setflight=filteropinion&mkt=en-US&p1=%5bNewsVertical+UserAugmentation%3d%22%5bqlf%242102%3a15%5d%22%5d&filter=NewsVerticalV2&format=pbxml".format(q.replace(' ', '%20'))] = q

            
    def parse(self, response):      
        item = OpinionArticleItem()
        op_news = response.xpath("//k_AnswerDataKifResponse/text()").extract()[0].replace("\n", "")
        data = json.loads(op_news)
        info = []
        query = self.url_q_dict[response.url]
        for per_arti in data['results'][0]['response'][0]['resultSet']:
            cur_info = {}    
            cur_info['title'] = data['results'][0]['response'][0]['resultSet'][0]['article']['title'],
            cur_info['url'] = data['results'][0]['response'][0]['resultSet'][0]['article']['url'],
            cur_info['source'] = data['results'][0]['response'][0]['resultSet'][0]['article']['source'],
            cur_info['snippet'] = data['results'][0]['response'][0]['resultSet'][0]['article']['snippet'],
            cur_info['image'] = data['results'][0]['response'][0]['resultSet'][0]['article']['image']
            info.append(cur_info)
            
        item['query'] = query,
        item['info'] = info
#        j_op_news = json.loads({selfimpo.url_q_dict[response.url]:op_news})
#        j_articles = j_op_news[0]['results'][0]['response'][0]['resultSet']
        yield item