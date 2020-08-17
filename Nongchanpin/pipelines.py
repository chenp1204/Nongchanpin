# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt


class WriteExcelPipeline(object):
    def __init__(self):
        self.file_name = "农产品.xls"
        self.book = xlwt.Workbook(encoding="gb18030")
        self.sheets = {}

    def process_item(self, item, spider):
        cate_name = item['cate1_name']
        if cate_name in self.sheets:
            self.current_sheet = self.sheets[cate_name][0]
            self.current_row = self.sheets[cate_name][1]
        else:
            self.current_sheet = self.book.add_sheet(cate_name)
            self.current_row = 1
            self.sheets[cate_name] = [self.current_sheet, self.current_row]
            self.tall_style = xlwt.easyxf('font:height 300')
            first_row = self.current_sheet.row(0)
            first_row.set_style(self.tall_style)
            head = ['分类', '品种', '采购量', '产品规格', '补充说明', '期望货源地', '收货地', '联系人', '联系电话', '发布时间']
            for h in head:
                self.current_sheet.write(0, head.index(h), h)

        if item['cate2_name'] is not None:
            self.current_sheet.write(int(self.current_row), 0, item['cate2_name'])
            self.current_sheet.write(int(self.current_row), 1, item['breed_name'])
            self.current_sheet.write(int(self.current_row), 2, item['purchase_num'])
            self.current_sheet.write(int(self.current_row), 3, item['product_spec'])
            self.current_sheet.write(int(self.current_row), 4, item['remarks'])
            self.current_sheet.write(int(self.current_row), 5, item['expect_addr'])
            self.current_sheet.write(int(self.current_row), 6, item['receive_addr'])
            self.current_sheet.write(int(self.current_row), 7, item['link_name'])
            self.current_sheet.write(int(self.current_row), 8, item['link_phone'])
            self.current_sheet.write(int(self.current_row), 9, item['publish_date'])
            self.current_sheet.row(self.current_row).set_style(self.tall_style)
            self.current_row = self.current_row + 1
            self.sheets[cate_name][1] = self.current_row

    def close_spider(self, spider):
        self.book.save(self.file_name)
