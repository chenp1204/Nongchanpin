# -*- coding: utf-8 -*-
import scrapy

import json
import time
import xmltodict

from Nongchanpin.items import PurchaseProduct


class HuinongSpider(scrapy.Spider):
    name = 'HuinongSpider'
    allowed_domains = ['cnhnb.com']

    def start_requests(self):
        yield scrapy.Request(
            'https://truffle.cnhnb.com/monk/operation-support/v500/category/menu/query',
            method='POST',
            headers={'Content-Type': 'application/json'},
            callback=self.parse)

    def parse(self, response):
        # 类别列表
        cate_list = ['水果', '蔬菜', '禽畜肉蛋', '中药材', '苗木花草', '种子种苗']
        res = json.loads(response.text)
        if res['message'] == 'success' and len(res['data']) > 0:
            for cate in res['data']:
                if cate['name'] in cate_list:
                    form_data = {
                        'cateId1': cate['value'],
                        'id': 'category',
                        'num': '0',
                        'pageNumber': 1,
                        'pageSize': 2000,
                        'searchId': '09869987ac2f4b371d0148940e94e268a1c678',
                        'sfrom': '3'
                    }
                    yield scrapy.Request(
                        'https://truffle.cnhnb.com/banana/purchase/search/list',
                        method='POST',
                        body=json.dumps(form_data),
                        headers={'Content-Type': 'application/json'},
                        callback=self.parse_list,
                        meta={'cate': cate}
                    )

    def parse_list(self, response):
        res = self.xmldata2json(response.text)
        if res['msg'] == 'success':
            cate = response.meta['cate']
            res_data = res['data']
            res_list = res_data['datas']['datas']
            page_num = res_data['pageNum']
            total_page = res_data['totalPages']

            if len(res_list) > 0:
                for item in res_list:
                    product = PurchaseProduct()
                    # 大类
                    product['cate1_name'] = cate['name']
                    # 二级分类
                    product['cate2_name'] = item['cateName'] if 'cateName' in item else ''
                    # 品种
                    product['breed_name'] = item['breedName'] if 'breedName' in item else ''
                    # 采购量
                    product['purchase_num'] = ''.join([item['frequent'], item['qty'], item['unit']])
                    # 期望货源地
                    product['expect_addr'] = item['scopeFullName'] if 'scopeFullName' in item else ''
                    # 收货地
                    product['receive_addr'] = item['placeFullName'] if 'placeFullName' in item else ''
                    # 产品规格
                    product['product_spec'] = item['specifications'] if 'specifications' in item else ''
                    # 补充说明
                    product['remarks'] = item['explanation'] if 'explanation' in item else ''
                    # 发布时间
                    if item['operateTime'] is not None:
                        timestamp = int(item['operateTime'])
                        localtime = time.localtime(timestamp/1000)
                        datetime = time.strftime('%Y-%m-%d', localtime)
                        product['publish_date'] = datetime

                    yield scrapy.Request(
                        'https://truffle.cnhnb.com/banana/purchase/search/detailinfo?purchaseId=' + item['purchaseId'],
                        headers={'Content-Type': 'application/json'},
                        callback=self.parse_detail,
                        meta={'product': product}
                    )

            if page_num < total_page:
                form_data = {
                    'cateId1': cate['value'],
                    'id': 'category',
                    'num': '0',
                    'pageNumber': page_num + 1,
                    'pageSize': 2000,
                    'searchId': '09869987ac2f4b371d0148940e94e268a1c678',
                    'sfrom': '3'
                }
                yield scrapy.Request(
                    'https://truffle.cnhnb.com/banana/purchase/search/list',
                    method='POST',
                    body=json.dumps(form_data),
                    headers={'Content-Type': 'application/json'},
                    callback=self.parse_list)

    def parse_detail(self, response):
        res = self.xmldata2json(response.text)
        if res['msg'] == 'success':
            product = response.meta['product']
            res_data = res['data']
            purchase_dto = res_data['purchaseDto']
            if res_data is not None and purchase_dto is not None:
                # 联系人
                product['link_name'] = '{0}（{1}）'.format(purchase_dto['linkName'] if 'linkName' in purchase_dto else '', res_data['tradeTypeStr'] if 'tradeTypeStr' in res_data else '')
                # 联系电话
                product['link_phone'] = purchase_dto['telPhone'] if 'telPhone' in purchase_dto else ''

                yield product

    def xmldata2json(self, xmltext):
        jsonstr = xmltodict.parse(xmltext)
        res = json.dumps(jsonstr)
        res = json.loads(res)
        if 'BaseResult' in res:
            return res['BaseResult']
        else:
            return res
