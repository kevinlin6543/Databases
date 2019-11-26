import scrapy
import re
from datetime import datetime
from movie_scraper.items import MovieItem
import re

class RottentomatoesSpider(scrapy.Spider):
    name = "rottentomatoes"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ['https://www.rottentomatoes.com/']

    def parse(self, response):
        current_year = datetime.now().year
        year_url = 'https://www.rottentomatoes.com/top/bestofrt/?year={0}'
        years = self.settings.getint('YEARS_TO_SCRAPE')

        for year in range(current_year - years, current_year + 1):
            yield scrapy.Request(year_url.format(year), callback=self.parse_list)

    def parse_list(self, response):
        sel = scrapy.Selector(response=response)
        reviews = response.xpath('//table[@class="table"]//tr//a')
        for review in reviews[1:]:
            href = review.xpath('@href').extract_first()
            yield response.follow(href, callback=self.parse_review)

    def parse_review(self, response):
        sel = scrapy.Selector(response=response)
        review = response.xpath('//h1[@class="mop-ratings-wrap__title mop-ratings-wrap__title--top"]')
        movie = MovieItem()

        date_re = re.compile('([A-z]{3}) (\d+), (\d+)')


        movie["title"] = response.xpath('//h1[@class="mop-ratings-wrap__title mop-ratings-wrap__title--top"]/text()').extract_first()
        movie["consensus"] = response.xpath('normalize-space(//p[@class="mop-ratings-wrap__text '
                                            'mop-ratings-wrap__text--concensus"]/text())').extract_first()
        ratings = response.xpath('normalize-space(//span[@class="mop-ratings-wrap__percentage"]/text())').extract()
        if len(ratings) == 1:
            movie["critic_rating"] = ratings[0]
        else:
            movie["critic_rating"], movie["user_rating"] = ratings
        movie["critic_count"] = int(response.xpath('normalize-space(//small[@class="mop-ratings-wrap__text--small"]/text())').extract_first())

        try:
            movie["audience_count"] = int(''.join(filter(str.isdigit, response.xpath('//strong[@class="mop-ratings-wrap__text--small"]/text()')[1].extract())))
        except:
            movie["audience_count"] = 0

        movie["description"] = response.xpath('normalize-space(//div[@id="movieSynopsis"]/text())').extract_first()
        meta_info = response.xpath('//div[@class="meta-value"]')
        meta_tag = response.xpath('//div[@class="meta-label subtle"]/text()')
        for i in range(len(meta_info)):
            tag = meta_tag[i].extract().rstrip(': ').lower()
            if tag == 'directed by':
                tag = 'director'
            if tag == 'written by':
                tag = 'writer'
            if tag == 'in theaters':
                tag = 'air_date'
                movie[tag] = date_re.match(meta_info[i].xpath('normalize-space(.)').extract_first()).group()
                continue
            try:
                if len(meta_info[i].xpath('.//text()').extract()) > 1 and tag != 'runtime':
                    movie[tag] = meta_info[i].xpath('normalize-space(.)').extract_first().split(', ')
                else:
                    movie[tag] = meta_info[i].xpath('normalize-space(.)').extract_first()
            except:
                continue


        yield movie
