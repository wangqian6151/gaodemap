# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from urllib.request import quote, unquote

from gaodemap.items import ConvenientStoreItem, JewelryStoreItem, MifenStoreItem


class GaodePoiSpider(scrapy.Spider):
    name = 'gaode_poi'
    allowed_domains = ['amap.com']
    base_url = 'https://restapi.amap.com/v3/place/polygon?polygon={polygon}&offset=20&page={page}&keywords={keywords}&output=json&key={key}&extensions=all'
    detail_json_url = 'https://ditu.amap.com/detail/get/detail?id={id}'
    detail_url = 'https://www.amap.com/detail/{id}'
    share_url = 'https://www.amap.com/place/{id}'

    def start_requests(self):
        key = "00123244546578898900-"  # 这里填入你的高德API的ak 
        # keywords = '便利店|便民商店|超市|超级市场'
        # keywords = '便利店|便民商店|超市'
        # keywords = '便利店|便民商店'
        # keywords = '便利店'
        # keywords = '珠宝首饰工艺品'
        # keywords = '珠宝首饰'
        # keywords = '珠宝'
        # keywords = '餐饮服务'
        # keywords = '米粉'
        keywords = '长沙米粉'
        lat_lt = 22.856649
        lng_lt = 113.677578
        lat_rb = 22.237799
        lng_rb = 114.651724  # 坐标范围
        # las = 0.003906  # 给las一个值
        # las = 0.007812  # 给las一个值
        # las = 0.015625  # 给las一个值
        # las = 0.03125  # 给las一个值
        # las = 0.03125  # 给las一个值
        las = 0.0625  # 给las一个值
        # las = 0.125  # 给las一个值
        lat_count = int((lat_lt - lat_rb) / las + 1)
        lng_count = int((lng_rb - lng_lt) / las + 1)
        self.logger.debug('lat_count: {} lon_count: {}'.format(lat_count, lng_count))
        print('lat_count: {} lon_count: {}'.format(lat_count, lng_count))
        for lat_c in range(0, lat_count):
            lat_b1 = round(lat_lt - las * lat_c, 6)
            for lng_c in range(0, lng_count):
                lng_b1 = round(lng_lt + las * lng_c, 6)
                polygon = str(lng_b1) + ',' + str(lat_b1) + '|' + str(round(lng_b1 + las, 6)) + ',' + str(
                    round(lat_b1 - las, 6))
                url = self.base_url.format(polygon=polygon, page=0, keywords=keywords, key=key)
                url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
                self.logger.debug('start url: {}'.format(url))
                print('start url: {}'.format(url))
                yield Request(url, callback=self.parse_poi,
                              meta={'polygon': polygon, 'page': 0, 'keywords': keywords, 'key': key})

    def parse_poi(self, response):
        polygon = response.meta.get('polygon')
        page = response.meta.get('page')
        keywords = response.meta.get('keywords')
        key = response.meta.get('key')
        data = json.loads(response.text)
        print('data: {}'.format(data))
        self.logger.debug('data: {}'.format(data))
        if int(data.get('count')) and data.get('pois'):
            print("data.get('count'): {}".format(data.get('count')))
            self.logger.debug("data.get('count'): {}".format(data.get('count')))
            if int(data.get('count')) >= 800:
                print('parse_poi count >= 800 url: {}'.format(response.url))
                self.logger.debug('parse_poi count >= 800 url: {}'.format(response.url))
            for item in data.get('pois'):
                if '便利店' in keywords:
                    convenient_store_item = ConvenientStoreItem()
                    convenient_store_item['keywords'] = keywords
                    convenient_store_item['name'] = item.get('name')
                    convenient_store_item['id'] = item.get('id')
                    convenient_store_item['detail_url'] = self.detail_url.format(id=item.get('id'))
                    convenient_store_item['share_url'] = self.share_url.format(id=item.get('id'))
                    convenient_store_item['detail_json_url'] = self.detail_json_url.format(id=item.get('id'))
                    convenient_store_item['type'] = item.get('type')
                    convenient_store_item['typecode'] = item.get('typecode')
                    convenient_store_item['address'] = item.get('address') if item.get('address') else None
                    convenient_store_item['location'] = item.get('location')
                    convenient_store_item['tel'] = item.get('tel') if item.get('tel') else None
                    convenient_store_item['pcode'] = item.get('pcode')
                    convenient_store_item['pname'] = item.get('pname')
                    convenient_store_item['citycode'] = item.get('citycode')
                    convenient_store_item['cityname'] = item.get('cityname')
                    convenient_store_item['adcode'] = item.get('adcode') if item.get('adcode') else None
                    convenient_store_item['adname'] = item.get('adname') if item.get('adname') else None
                    convenient_store_item['gridcode'] = item.get('gridcode') if item.get('gridcode') else None
                    convenient_store_item['navi_poiid'] = item.get('navi_poiid') if item.get('navi_poiid') else None
                    convenient_store_item['entr_location'] = item.get('entr_location') if item.get(
                        'entr_location') else None
                    convenient_store_item['business_area'] = item.get('business_area') if item.get(
                        'business_area') else None
                    convenient_store_item['rating'] = item.get('biz_ext').get('rating') if item.get('biz_ext').get(
                        'rating') else None
                    convenient_store_item['parent_id'] = item.get('parent') if item.get('parent') else None
                    if item.get('parent'):
                        convenient_store_item['parent_detail_json_url'] = self.detail_json_url.format(
                            id=item.get('parent'))
                        convenient_store_item['parent_share_url'] = self.share_url.format(id=item.get('parent'))
                        convenient_store_item['parent_detail_url'] = self.detail_url.format(id=item.get('parent'))
                    yield convenient_store_item
                elif '珠宝' in keywords:
                    jewelry_store_item = JewelryStoreItem()
                    jewelry_store_item['keywords'] = keywords
                    jewelry_store_item['name'] = item.get('name')
                    jewelry_store_item['id'] = item.get('id')
                    jewelry_store_item['detail_url'] = self.detail_url.format(id=item.get('id'))
                    jewelry_store_item['share_url'] = self.share_url.format(id=item.get('id'))
                    jewelry_store_item['detail_json_url'] = self.detail_json_url.format(id=item.get('id'))
                    jewelry_store_item['type'] = item.get('type')
                    jewelry_store_item['typecode'] = item.get('typecode')
                    jewelry_store_item['address'] = item.get('address') if item.get('address') else None
                    jewelry_store_item['location'] = item.get('location')
                    jewelry_store_item['tel'] = item.get('tel') if item.get('tel') else None
                    jewelry_store_item['pcode'] = item.get('pcode')
                    jewelry_store_item['pname'] = item.get('pname')
                    jewelry_store_item['citycode'] = item.get('citycode')
                    jewelry_store_item['cityname'] = item.get('cityname')
                    jewelry_store_item['adcode'] = item.get('adcode') if item.get('adcode') else None
                    jewelry_store_item['adname'] = item.get('adname') if item.get('adname') else None
                    jewelry_store_item['gridcode'] = item.get('gridcode') if item.get('gridcode') else None
                    jewelry_store_item['navi_poiid'] = item.get('navi_poiid') if item.get('navi_poiid') else None
                    jewelry_store_item['entr_location'] = item.get('entr_location') if item.get(
                        'entr_location') else None
                    jewelry_store_item['business_area'] = item.get('business_area') if item.get(
                        'business_area') else None
                    jewelry_store_item['rating'] = item.get('biz_ext').get('rating') if item.get('biz_ext').get(
                        'rating') else None
                    jewelry_store_item['parent_id'] = item.get('parent') if item.get('parent') else None
                    if item.get('parent'):
                        jewelry_store_item['parent_detail_json_url'] = self.detail_json_url.format(
                            id=item.get('parent'))
                        jewelry_store_item['parent_share_url'] = self.share_url.format(id=item.get('parent'))
                        jewelry_store_item['parent_detail_url'] = self.detail_url.format(id=item.get('parent'))
                    yield jewelry_store_item
                elif '米粉' in keywords:
                    mifen_store_item = MifenStoreItem()
                    mifen_store_item['keywords'] = keywords
                    mifen_store_item['name'] = item.get('name')
                    mifen_store_item['id'] = item.get('id')
                    mifen_store_item['detail_url'] = self.detail_url.format(id=item.get('id'))
                    mifen_store_item['share_url'] = self.share_url.format(id=item.get('id'))
                    mifen_store_item['detail_json_url'] = self.detail_json_url.format(id=item.get('id'))
                    mifen_store_item['tag'] = item.get('tag') if item.get('tag') else None
                    mifen_store_item['biz_type'] = item.get('biz_type') if item.get('biz_type') else None
                    mifen_store_item['type'] = item.get('type')
                    mifen_store_item['typecode'] = item.get('typecode')
                    mifen_store_item['address'] = item.get('address') if item.get('address') else None
                    mifen_store_item['location'] = item.get('location')
                    mifen_store_item['tel'] = item.get('tel') if item.get('tel') else None
                    mifen_store_item['pcode'] = item.get('pcode')
                    mifen_store_item['pname'] = item.get('pname')
                    mifen_store_item['citycode'] = item.get('citycode')
                    mifen_store_item['cityname'] = item.get('cityname')
                    mifen_store_item['adcode'] = item.get('adcode') if item.get('adcode') else None
                    mifen_store_item['adname'] = item.get('adname') if item.get('adname') else None
                    mifen_store_item['gridcode'] = item.get('gridcode') if item.get('gridcode') else None
                    mifen_store_item['navi_poiid'] = item.get('navi_poiid') if item.get('navi_poiid') else None
                    mifen_store_item['entr_location'] = item.get('entr_location') if item.get(
                        'entr_location') else None
                    mifen_store_item['business_area'] = item.get('business_area') if item.get(
                        'business_area') else None
                    mifen_store_item['rating'] = item.get('biz_ext').get('rating') if item.get('biz_ext').get(
                        'rating') else None
                    mifen_store_item['cost'] = item.get('biz_ext').get('cost') if item.get('biz_ext').get(
                        'cost') else None
                    mifen_store_item['meal_ordering'] = item.get('biz_ext').get('meal_ordering') if item.get(
                        'biz_ext').get('meal_ordering') else None
                    mifen_store_item['parent_id'] = item.get('parent') if item.get('parent') else None
                    if item.get('parent'):
                        mifen_store_item['parent_detail_json_url'] = self.detail_json_url.format(
                            id=item.get('parent'))
                        mifen_store_item['parent_share_url'] = self.share_url.format(id=item.get('parent'))
                        mifen_store_item['parent_detail_url'] = self.detail_url.format(id=item.get('parent'))
                    yield mifen_store_item
                    # self.logger.debug('parse_poi detail_json_url:' + convenient_store_item['detail_json_url'])
                    # yield Request(url=convenient_store_item['detail_json_url'],
                    #               meta={'convenient_store_item': convenient_store_item}, callback=self.parse_details)

            page += 1
            self.logger.debug('parse_poi page_num: {}'.format(page))
            print('parse_poi page_num: {}'.format(page))
            url = self.base_url.format(polygon=polygon, page=page, keywords=keywords, key=key)
            url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
            self.logger.debug('parse_poi url: {}'.format(url))
            print('parse_poi url: {}'.format(url))
            yield Request(url, callback=self.parse_poi,
                          meta={'polygon': polygon, 'page': page, 'keywords': keywords, 'key': key})

    def parse_details(self, response):
        self.logger.debug('parse_details response.url: {}'.format(response.url))
        print('parse_details response.url: {}'.format(response.url))
        convenient_store_item = response.meta.get('convenient_store_item')
        result = json.loads(response.text)
        self.logger.debug('parse_details result: {}'.format(result))
        print('parse_details result: {}'.format(result))
        self.logger.debug('parse_details status: {}'.format(result.get('status')))
        print('parse_details status: {}'.format(result.get('status')))
        self.logger.debug('parse_details data: {}'.format(result.get('data')))
        print('parse_details data: {}'.format(result.get('data')))
        if result.get('status') == '1' and type(result.get('data')) == dict:
            data = result.get('data')
            convenient_store_item['business_type'] = data.get('shopping').get('business')
            convenient_store_item['info_weburl'] = data.get('shopping').get('info_weburl')
            convenient_store_item['opentime'] = data.get('shopping').get('opentime2')
            yield convenient_store_item
