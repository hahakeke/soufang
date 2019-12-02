# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisSpider
import scrapy
import logging
from soufang.items import NewHouseItem
from soufang.items import EsfHouseItem

logger = logging.getLogger(__name__)

class FangtxSpider(RedisSpider):
    name = 'fangtx'
    # allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang_start"

    def parse(self, response):
        tr_list = response.xpath('//div[@class="outCont"]//tr[contains(@id,"sffamily")]')[0:-2]
        province = None
        for tr in tr_list:
            pro_text = tr.xpath(".//td[2]//text()").get()
            province_text = re.sub(r"\s", "", pro_text)
            if province_text:
                province = province_text
            city_alist = tr.xpath(".//td[3]/a")
            for alist in city_alist:
                city = alist.xpath(".//text()").get()
                city_href = alist.xpath(".//@href").get()
                href_list = city_href.split('.')
                new_house_link = href_list[0] + ".newhouse." + href_list[1] + "." +href_list[2]
                esf_house_link = href_list[0] + ".esf." + href_list[1] + "." +href_list[2]
                if city == "北京":
                    new_house_link = "https://newhouse.fang.com/house/"
                    esf_house_link = "https://esf.fang.com/"
                yield scrapy.Request(new_house_link,callback=self.parse_newhouse_list,meta={"info":{province,city}})
                yield scrapy.Request(esf_house_link,callback=self.parse_esf_list,meta={"info":{province, city}})

    # 新房信息获取
    def parse_newhouse_list(self,response):
        province,city = response.meta.get("info")
        lis = response.xpath('//*[@id="newhouse_loupai_list"]/ul/li[not(@style)]')
        for li in lis:
            name_cg = li.xpath('.//div[@class="nlc_details"]//div[@class="nlcd_name"]/a/text()').get()
            if name_cg:
                name = re.sub(r"\s", "", name_cg)
            price_cg = "".join(li.xpath('.//div[@class="nhouse_price"]//text()').getall())
            price = re.sub(r'\s|广告', "", price_cg)
            rooms = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            areas_cg = "".join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())
            areas = re.sub(r"\s|/|－", "", areas_cg)
            address = "".join(li.xpath('.//div[@class="address"]/a/@title').getall())
            district_cg = li.xpath('.//div[@class="address"]/a/span/text()').get()
            if district_cg:
                district = re.sub(r"\s|\[|\]", "", district_cg)
            else:
                district_cg = re.sub(r"\s", "", li.xpath('.//div[@class="address"]/a/text()').get())
                try:
                    district = re.findall(r"\[(.*?)\]",district_cg)[0]
                except Exception as f:
                    logger.warning(f)
            sales = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            href = li.xpath('.//div[@class="nlc_details"]//div[@class="nlcd_name"]/a/@href').get()
            oringin_url = "https:" + href
            item = NewHouseItem(province=province, city=city, name=name, price=price, rooms=rooms, areas=areas, address=address, district=district, sales=sales, oringin_url=oringin_url)
            yield item
        # 下一页
        next_href = response.xpath('//div[@class="page"]//a[contains(text(),"下一页")]/@href').get()
        url_list = response.url.split('/')
        if next_href:
            new_next_url = "https://" +url_list[2] +  next_href
            yield scrapy.Request(url=new_next_url, callback=self.parse_newhouse_list, meta={"info": {province, city}})

    # 二手房列表页数据获取
    def parse_esf_list(self,response):
        item = EsfHouseItem()
        province,city = response.meta.get("info")
        item["province"] = province
        item["city"] = city
        dl_list = response.xpath('//div[contains(@class,"shop_list")]//dl[@dataflag="bg"]')
        url_list = response.url.split('/')
        for dl in dl_list:
            item["name"] = dl.xpath('.//dd/p[@class="add_shop"]/a/@title').get()
            tel_info = dl.xpath('.//dd/p[@class="tel_shop"]/text()').getall()
            item["rooms"] = re.sub(r"\s", "", tel_info[0])
            item["area"] = re.sub(r"\s", "", tel_info[1])
            item["floor"] = re.sub(r"\s", "", tel_info[2])
            try:
                item["direction"] = re.sub(r"\s", "", tel_info[3])
            except Exception as f:
                item["direction"] = None
                logger.warning(f)
            if len(tel_info) >= 5:
                item["age"] = re.sub(r"\s", "", tel_info[4])
            else:
                item["age"] = None
            item["address"] = dl.xpath('.//dd/p[@class="add_shop"]/span/text()').get()
            pri = dl.xpath('.//dd[@class="price_right"]/span[1]/b/text()').get()
            ce = dl.xpath('.//dd[@class="price_right"]/span[1]/text()').get()
            item["price"] = pri + ce
            item["unit_price"] = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').get()
            href = dl.xpath('.//dd/h4/a/@href').get()
            if href:
                item["link"] = "https://" + url_list[2] + href
            yield item
        # 下一页
        next_href = response.xpath('//div[@class="page_al"]/p/a[contains(text(),"下一页")]/@href').get()
        if next_href:
            next_url ="https://" + url_list[2] + next_href
            yield scrapy.Request(url=next_url, callback=self.parse_esf_list,meta={"info": {province, city}})






