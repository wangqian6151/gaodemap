# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ConvenientStoreItem(Item):
    collection = table = 'ConvenientStore'

    keywords = Field()
    id = Field()
    detail_url = Field()
    share_url = Field()
    detail_json_url = Field()
    name = Field()
    type = Field()
    typecode = Field()
    address = Field()
    location = Field()
    tel = Field()
    pcode = Field()
    pname = Field()
    citycode = Field()
    cityname = Field()
    adcode = Field()
    adname = Field()
    gridcode = Field()
    navi_poiid = Field()
    entr_location = Field()
    business_area = Field()
    rating = Field()
    parent_id = Field()
    parent_detail_url = Field()
    parent_share_url = Field()
    parent_detail_json_url = Field()

    business_type = Field()
    info_weburl = Field()
    opentime = Field()


class JewelryStoreItem(Item):
    collection = table = 'JewelryStore'

    keywords = Field()
    name = Field()
    adcode = Field()
    adname = Field()
    address = Field()
    type = Field()
    typecode = Field()
    id = Field()
    detail_url = Field()
    share_url = Field()
    detail_json_url = Field()
    location = Field()
    tel = Field()
    pcode = Field()
    pname = Field()
    citycode = Field()
    cityname = Field()
    gridcode = Field()
    navi_poiid = Field()
    entr_location = Field()
    business_area = Field()
    rating = Field()
    parent_id = Field()
    parent_detail_url = Field()
    parent_share_url = Field()
    parent_detail_json_url = Field()

    # business_type = Field()
    # info_weburl = Field()
    # opentime = Field()


class MifenStoreItem(Item):
    collection = table = 'MifenStore'

    keywords = Field()
    name = Field()
    adcode = Field()
    adname = Field()
    address = Field()
    type = Field()
    typecode = Field()
    tag = Field()
    biz_type = Field()
    rating = Field()
    cost = Field()
    meal_ordering = Field()
    id = Field()
    detail_url = Field()
    share_url = Field()
    detail_json_url = Field()
    location = Field()
    tel = Field()
    pcode = Field()
    pname = Field()
    citycode = Field()
    cityname = Field()
    gridcode = Field()
    navi_poiid = Field()
    entr_location = Field()
    business_area = Field()
    parent_id = Field()
    parent_detail_url = Field()
    parent_share_url = Field()
    parent_detail_json_url = Field()

    # business_type = Field()
    # info_weburl = Field()
    # opentime = Field()

