# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PurchaseProduct(scrapy.Item):
    # 大类
    cate1_name = scrapy.Field()
    # 二级分类
    cate2_name = scrapy.Field()
    # 品种
    breed_name = scrapy.Field()
    # 采购量
    purchase_num = scrapy.Field()
    # 产品规格
    product_spec = scrapy.Field()
    # 补充说明
    remarks = scrapy.Field()
    # 期望货源地
    expect_addr = scrapy.Field()
    # 收货地
    receive_addr = scrapy.Field()
    # 联系人
    link_name = scrapy.Field()
    # 联系电话
    link_phone = scrapy.Field()
    # 发布时间
    publish_date = scrapy.Field()
