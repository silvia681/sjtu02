# encoding: utf-8

from scrapy.item import Item, Field

#定义存放page内容的类
class PageItem(Item):
    brand = Field() #品牌
    factory = Field() #厂商
    serial = Field()  # 车系
    yearType = Field()  # 年款
    volumn = Field()   # 排量
    carStyle = Field()   # 车型
    guide_price = Field()  # 厂商指导价（元）
    bare_price = Field()   #裸车价（元）
    buy_tax = Field()   # 购置税（元）
    deal_price = Field()  # 新车实际成交价（含税）（元）
    comm_ins = Field()   # 商业保险（元）
    use_tax = Field()  # 车船使用税
    trff_tax = Field()  # 交强险
    license_fee = Field()   # 上牌费用
    total_price = Field()  # 合计价格
    invoce_flg = Field()  # 是否包含发票
    promotion = Field()   # 促销套餐
    deal_date = Field()   # 购车时间
    post_date = Field()  # 发表时间
    username = Field()  # 发布昵称
    prov = Field()   # 购车地点（省）
    city = Field()   # 购车地点（市）
    sales_name = Field()   # 购买商家名称
    sales_telno = Field()   # 商家电话
    sales_addr = Field()   # 商家地址
    comment = Field()   # 购买感受
    curl_timestamp = Field()   # 数据抓取时间
    url = Field()   # 来源网址
    data_id = Field()   # txt文件的文件名,比如“00062-20151020”
