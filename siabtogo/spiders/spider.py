import scrapy

from scrapy.loader import ItemLoader

from ..items import SiabtogoItem
from itemloaders.processors import TakeFirst


class SiabtogoSpider(scrapy.Spider):
	name = 'siabtogo'
	start_urls = ['https://siabtogo.com/category/actualites-2/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="inner"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)


	def parse_post(self, response):
		title = response.xpath('//title/text()').get()
		description = response.xpath('//div[@class="stm_mgb_20 stm_single_post__content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//li[@class="post_date"]//text()[normalize-space()]').get()

		item = ItemLoader(item=SiabtogoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
