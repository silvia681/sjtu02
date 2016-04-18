# encoding: utf-8
import traceback
import datetime
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request 
from page import items
import time
import re


#定义要抓取页面的爬虫类
class PageSpider(BaseSpider):
    name = "page"
    start_urls = []
    carno_urlpatten = "http://jiage.autohome.com.cn/price/carlist/p-"
    d_pc = {}  
    f=open('../china.txt')
    chn=f.readlines()
    f.close()
    key=[it[0:6] for it in chn]
    val=[it[6:-1] for it in chn]
    d_pc=dict(zip(key,val))
    
    def __init__(self):
        self.start_urls = self.set_url()
    
    #从carNOList.txt文件中读出要抓取的所有编号，格式化后放入数组中
    def set_url(self):
        url_list = []
        f=open('../carNOList.txt')
        l=f.read()
        f.close()
        ll=l.split('\n')
        for i in range(0,len(ll)):
            url_list.append(self.carno_urlpatten + ll[i])
        return url_list

    #该方法完成爬虫解析文件内容的工作,各位不要修改方法名,只需要完善方法体
    def parse(self, response):
        try:
            
            length=len(response.xpath('//li[@class="price-item"]'))
            #解头 日产 阳光 2014款 1.5XV CVT尊贵版——车主发布价格            
            tl=response.xpath('//div[@class="price-spec-hd fn-clear"]/h2/text()').extract()[0]
            ttl=tl.split(u"——")[0].split(u' ')    
            #发布时间
            ptds=response.xpath('//div[@class="user-name"]/span/text()').extract()
            postdates=[item.split(u' ')[0].replace('-','')[0:8].encode('utf-8') for item in ptds]
            #用户名filter(None,string)
            usernt=response.xpath('//div[@class="user-name"]/a[@class="uname"]/text()').extract()
            usernmt=filter(None,map(lambda it : it.strip("\r\n "),usernt))
            #用户评论
#            cmt=response.xpath('//div[@class="txcon"]/p[@class="txt-cont"]/text()').extract()
            tmp=""
            lit=response.xpath('//ul[@class="price-list"]/li[@class="price-item"]')
            # for each user post generate a item object
            for i in range(0,length):
                data = self.getDefaultDataItem()
                if(len(lit[i].xpath('./div[2]/ul/li')) == 14):
                    data = items.PageItem()
                    if (len(ttl) == 5):      
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[3].encode('utf-8')
                        data['carStyle']= ttl[4].encode('utf-8')
                    elif(len(ttl) == 6):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[4].encode('utf-8')
                        data['carStyle']= ttl[5].encode('utf-8')
                    elif(len(ttl) == 7):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[3]+ttl[4]).encode('utf-8')
                        data['carStyle']= ttl[6].encode('utf-8')
                    elif(len(ttl) == 8):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[5]+ttl[6]).encode('utf-8')
                        data['carStyle']= ttl[7].encode('utf-8')
                    else:
                        print u"不按常理出牌的title"
                    data['post_date'] = postdates[i]
                    data['username'] = usernmt[i].encode('utf-8') 
                    tmp=lit[i].xpath('./div[2]/ul/li[1]/div[2]/i').extract()
                    if (len(tmp) == 1):
                        data['invoce_flg'] = str(1)
                    else:
                        data['invoce_flg'] = str(0)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[2]/div[2]/span/text()').extract()[0])[0]
                    data['bare_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[3]/div[2]/text()').extract()[0])[0]
                    data['guide_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[4]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['buy_tax'] = "未填写"
                    else:
                        data['buy_tax'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[5]/div[2]/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['comm_ins'] = "未填写"
                    else:
                        data['comm_ins'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[6]/div[2]/span/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['total_price'] = "未填写"
                    else:                        
                        data['total_price'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[7]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['license_fee'] = "未填写"
                    else:
                         data['license_fee'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[8]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['use_tax'] = "未填写"
                    else:
                         data['use_tax'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[9]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['trff_tax'] = "未填写"
                    else:
                         data['trff_tax'] = tmp[0].encode('utf-8')                    
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[10]/div[2]/p/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['promotion'] = "未填写"
                    else:
                         data['promotion'] = tmp[0].encode('utf-8')  
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[11]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['deal_date'] = "未填写"
                    else:
                         data['deal_date'] = self.padding(tmp).encode('utf-8')                           
                    tmp=lit[i].xpath('./div[2]/ul/li[12]/div[2]/@pid').extract()[0]
                    if(tmp in self.d_pc):
                        data['prov'] = self.d_pc[tmp]
                    else:
                        print 'unkonwn pro '+tmp
                    tmp=lit[i].xpath('./div[2]/ul/li[12]/div[2]/@cid').extract()[0]
                    if(tmp in self.d_pc):
                        data['city'] = self.d_pc[tmp]
                    else:
                        print 'unkonwn city '+tmp
                    tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p')
                    if(len(tmp) == 1):
                        data['sales_name'] = "无"
                        data['sales_telno'] = "无"
                        data['sales_addr'] = "无"
                    else:
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[1]/a/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_name'] = "未填写"
                        else:
                            data['sales_name'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[1]/span/em[2]/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_telno'] = "未填写"
                        else:
                            data['sales_telno'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[2]/span/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_addr'] = "未填写"
                        else:
                            data['sales_addr'] = tmp[0].encode('utf-8')
                    tmp=lit[i].xpath('./div[2]/ul/li[14]/div[2]/p/text()').extract()         
                    data['comment'] = tmp[0].encode('utf-8')
                    
                    data['curl_timestamp'] = self.getCurrentTimestamp()
                    data['url'] = response.url[0:50]
                    data['data_id'] = response.url[0:50].split('-')[-1] + '-' + postdates[i]
                    data['deal_price'] = ""
                    yield data 
                    #print response.url + " done..."
                elif(len(lit[i].xpath('./div[2]/ul/li')) == 18):
                    
                    data = items.PageItem()
                    if (len(ttl) == 5):      
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[3].encode('utf-8')
                        data['carStyle']= ttl[4].encode('utf-8')
                    elif(len(ttl) == 6):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[4].encode('utf-8')
                        data['carStyle']= ttl[5].encode('utf-8')
                    elif(len(ttl) == 7):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[3]+ttl[4]).encode('utf-8')
                        data['carStyle']= ttl[6].encode('utf-8')
                    elif(len(ttl) == 8):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[5]+ttl[6]).encode('utf-8')
                        data['carStyle']= ttl[7].encode('utf-8')
                    else:
                        print u"不按常理出牌的title"
                    data['post_date'] = postdates[i]
                    data['username'] = usernmt[i].encode('utf-8') 
                    tmp=lit[i].xpath('./div[2]/ul/li[1]/div[2]/i').extract()
                    if (len(tmp) == 1):
                        data['invoce_flg'] = str(1)
                    else:
                        data['invoce_flg'] = str(0)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[2]/div[2]/span/text()').extract()[0])[0]
                    data['bare_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[3]/div[2]/text()').extract()[0])[0]
                    data['guide_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[4]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['buy_tax'] = "未填写"
                    else:
                        data['buy_tax'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[5]/div[2]/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['comm_ins'] = "未填写"
                    else:
                        data['comm_ins'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[6]/div[2]/span/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['total_price'] = "未填写"
                    else:                        
                        data['total_price'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[7]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['license_fee'] = "未填写"
                    else:
                         data['license_fee'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[8]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['use_tax'] = "未填写"
                    else:
                         data['use_tax'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[9]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['trff_tax'] = "未填写"
                    else:
                         data['trff_tax'] = tmp[0].encode('utf-8')                    
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[14]/div[2]/p/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['promotion'] = "未填写"
                    else:
                         data['promotion'] = tmp[0].encode('utf-8')  
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[15]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['deal_date'] = "未填写"
                    else:
                         data['deal_date'] = self.padding(tmp).encode('utf-8')                           
                    tmp=lit[i].xpath('./div[2]/ul/li[16]/div[2]/@pid').extract()[0]
                    if(tmp in self.d_pc):
                        data['prov'] = self.d_pc[tmp] 
                    else:
                        print 'unkown pro '+tmp
                    tmp=lit[i].xpath('./div[2]/ul/li[16]/div[2]/@cid').extract()[0]
                    if(tmp in self.d_pc):
                        data['city'] = self.d_pc[tmp]
                    else:
                        print 'unkonwn city '+tmp
                    tmp=lit[i].xpath('./div[2]/ul/li[17]/div[2]/div/div/p')
                    if(len(tmp) == 1):
                        data['sales_name'] = "无"
                        data['sales_telno'] = "无"
                        data['sales_addr'] = "无"
                    else:
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[1]/a/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_name'] = "未填写"
                        else:
                            data['sales_name'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[1]/span/em[2]/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_telno'] = "未填写"
                        else:
                            data['sales_telno'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[2]/span/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_addr'] = "未填写"
                        else:
                            data['sales_addr'] = tmp[0].encode('utf-8')
                    tmp=lit[i].xpath('./div[2]/ul/li[18]/div[2]/p/text()').extract()         
                    data['comment'] = tmp[0].encode('utf-8')
                    
                    data['curl_timestamp'] = self.getCurrentTimestamp()
                    data['url'] = response.url[0:50]
                    data['data_id'] = response.url[0:50].split('-')[-1] + '-' + postdates[i]
                    data['deal_price'] = ""
                    yield data  
                    #print response.url + " done..."
                elif(len(lit[i].xpath('./div[2]/ul/li')) == 22):
                    data = items.PageItem()
                    if (len(ttl) == 5):      
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[3].encode('utf-8')
                        data['carStyle']= ttl[4].encode('utf-8')
                    elif(len(ttl) == 6):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[4].encode('utf-8')
                        data['carStyle']= ttl[5].encode('utf-8')
                    elif(len(ttl) == 7):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[3]+ttl[4]).encode('utf-8')
                        data['carStyle']= ttl[6].encode('utf-8')
                    elif(len(ttl) == 8):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[5]+ttl[6]).encode('utf-8')
                        data['carStyle']= ttl[7].encode('utf-8')
                    else:
                        print u"不按常理出牌的title"
                    data['post_date'] = postdates[i]
                    data['username'] = usernmt[i].encode('utf-8') 
                    tmp=lit[i].xpath('./div[2]/ul/li[1]/div[2]/i').extract()
                    if (len(tmp) == 1):
                        data['invoce_flg'] = str(1)
                    else:
                        data['invoce_flg'] = str(0)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[2]/div[2]/span/text()').extract()[0])[0]
                    data['bare_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[3]/div[2]/text()').extract()[0])[0]
                    data['guide_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[4]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['buy_tax'] = "未填写"
                    else:
                        data['buy_tax'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[5]/div[2]/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['comm_ins'] = "未填写"
                    else:
                        data['comm_ins'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[6]/div[2]/span/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['total_price'] = "未填写"
                    else:                        
                        data['total_price'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[7]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['license_fee'] = "未填写"
                    else:
                         data['license_fee'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[8]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['use_tax'] = "未填写"
                    else:
                         data['use_tax'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[9]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['trff_tax'] = "未填写"
                    else:
                         data['trff_tax'] = tmp[0].encode('utf-8')                    
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[18]/div[2]/p/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['promotion'] = "未填写"
                    else:
                         data['promotion'] = tmp[0].encode('utf-8')  
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[19]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['deal_date'] = "未填写"
                    else:
                         data['deal_date'] = self.padding(tmp).encode('utf-8')                           
                    tmp=lit[i].xpath('./div[2]/ul/li[20]/div[2]/@pid').extract()[0]
                    if(tmp in self.d_pc):
                        data['prov'] = self.d_pc[tmp] 
                    else:
                        print 'unkonwn pro '+tmp
                    tmp=lit[i].xpath('./div[2]/ul/li[20]/div[2]/@cid').extract()[0]
                    if(tmp in self.d_pc):
                        data['city'] = self.d_pc[tmp]
                    else:
                        print 'unkonwn city '+tmp
                    
                    tmp=lit[i].xpath('./div[2]/ul/li[21]/div[2]/div/div/p')
                    if(len(tmp) == 1):
                        data['sales_name'] = "无"
                        data['sales_telno'] = "无"
                        data['sales_addr'] = "无"
                    else:
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[1]/a/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_name'] = "未填写"
                        else:
                            data['sales_name'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[1]/span/em[2]/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_telno'] = "未填写"
                        else:
                            data['sales_telno'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[13]/div[2]/div/div/p[2]/span/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_addr'] = "未填写"
                        else:
                            data['sales_addr'] = tmp[0].encode('utf-8')
                    tmp=lit[i].xpath('./div[2]/ul/li[22]/div[2]/p/text()').extract()         
                    data['comment'] = tmp[0].encode('utf-8')
                    
                    data['curl_timestamp'] = self.getCurrentTimestamp()
                    data['url'] = response.url[0:50]
                    data['data_id'] = response.url[0:50].split('-')[-1] + '-' + postdates[i]
                    data['deal_price'] = ""
                    yield data    
                    #print response.url + " done..."               
                elif(len(lit[i].xpath('./div[2]/ul/li')) == 26):
                    data = items.PageItem()
                    if (len(ttl) == 5):      
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[3].encode('utf-8')
                        data['carStyle']= ttl[4].encode('utf-8')
                    elif(len(ttl) == 6):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = ttl[4].encode('utf-8')
                        data['carStyle']= ttl[5].encode('utf-8')
                    elif(len(ttl) == 7):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[3]+ttl[4]).encode('utf-8')
                        data['carStyle']= ttl[6].encode('utf-8')
                    elif(len(ttl) == 8):
                        data['brand'] = ttl[0].encode('utf-8')
                        data['factory'] = "未知"
                        data['serial'] = ttl[1].encode('utf-8')
                        data['yearType'] = ttl[2].encode('utf-8')
                        data['volumn'] = (ttl[5]+ttl[6]).encode('utf-8')
                        data['carStyle']= ttl[7].encode('utf-8')
                    else:
                        print u"不按常理出牌的title"
                    data['post_date'] = postdates[i]
                    data['username'] = usernmt[i].encode('utf-8') 
                    tmp=lit[i].xpath('./div[2]/ul/li[1]/div[2]/i').extract()
                    if (len(tmp) == 1):
                        data['invoce_flg'] = str(1)
                    else:
                        data['invoce_flg'] = str(0)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[2]/div[2]/span/text()').extract()[0])[0]
                    data['bare_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[3]/div[2]/text()').extract()[0])[0]
                    data['guide_price'] = str(float(tmp)*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[4]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['buy_tax'] = "未填写"
                    else:
                        data['buy_tax'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[5]/div[2]/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['comm_ins'] = "未填写"
                    else:
                        data['comm_ins'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[6]/div[2]/span/text()').extract()[0])  
                    if(len(tmp) == 0):
                        data['total_price'] = "未填写"
                    else:                        
                        data['total_price'] = str(float(self.padding(tmp))*10000)
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[7]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['license_fee'] = "未填写"
                    else:
                         data['license_fee'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[8]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['use_tax'] = "未填写"
                    else:
                         data['use_tax'] = tmp[0].encode('utf-8')
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[9]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['trff_tax'] = "未填写"
                    else:
                         data['trff_tax'] = tmp[0].encode('utf-8')                    
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[22]/div[2]/p/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['promotion'] = "未填写"
                    else:
                         data['promotion'] = tmp[0].encode('utf-8')  
                    tmp=re.findall(r'[\d|.]+',lit[i].xpath('./div[2]/ul/li[23]/div[2]/text()').extract()[0])
                    if(len(tmp) == 0):
                        data['deal_date'] = "未填写"
                    else:
                         data['deal_date'] = self.padding(tmp).encode('utf-8')                           
                    tmp=lit[i].xpath('./div[2]/ul/li[24]/div[2]/@pid').extract()[0]
                    if(tmp in self.d_pc):
                        data['prov'] = self.d_pc[tmp] 
                    else:
                        print 'unkonwn pro '+tmp
                    tmp=lit[i].xpath('./div[2]/ul/li[24]/div[2]/@cid').extract()[0]
                    if(tmp in self.d_pc):
                        data['city'] = self.d_pc[tmp]
                    else:
                        print 'unkonwn city '+tmp
                    
                    tmp=lit[i].xpath('./div[2]/ul/li[25]/div[2]/div/div/p')
                    if(len(tmp) == 1):
                        data['sales_name'] = "无"
                        data['sales_telno'] = "无"
                        data['sales_addr'] = "无"
                    else:
                        tmp=lit[i].xpath('./div[2]/ul/li[25]/div[2]/div/div/p[1]/a/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_name'] = "未填写"
                        else:
                            data['sales_name'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[25]/div[2]/div/div/p[1]/span/em[2]/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_telno'] = "未填写"
                        else:
                            data['sales_telno'] = tmp[0].encode('utf-8')
                        tmp=lit[i].xpath('./div[2]/ul/li[25]/div[2]/div/div/p[2]/span/text()').extract()
                        if(len(tmp) == 0):
                            data['sales_addr'] = "未填写"
                        else:
                            data['sales_addr'] = tmp[0].encode('utf-8')
                    tmp=lit[i].xpath('./div[2]/ul/li[26]/div[2]/p/text()').extract()         
                    data['comment'] = tmp[0].encode('utf-8')
                    
                    data['curl_timestamp'] = self.getCurrentTimestamp()
                    data['url'] = response.url[0:50]
                    data['data_id'] = response.url[0:50].split('-')[-1] + '-' + postdates[i]
                    data['deal_price'] = ""
                    yield data    
                    #print response.url + " done..."               

                else:
                    print u"其他长度的li"
                    print response.url
                    
            # 判断是否存在下一页
            ll = response.xpath('//div[@class="price-box-bd"]/div[@class="page"]')
            ay=ll.xpath('./a/text()').extract() 
            if(u'下一页' in ay):
                '''
                存在则添加request进行parse
                '''
                i = ay.index(u'下一页')
                ss = './a[' + str(i+1) + ']/@href'
                nexturl = 'http://jiage.autohome.com.cn' + ll.xpath(ss).extract()[0].encode('utf-8')
                #print 'find sub_page...'
                #print nexturl 
                yield Request(nexturl, callback=self.parse)
                    
        except Exception as e:
            print "ERROR PARSE"
            print response.url
            print traceback.format_exc()


    def getDefaultDataItem(self):
        item = items.PageItem()
        item['brand'] = ""
        item['factory'] = ""
        item['serial'] = ""
        item['yearType'] = ""
        item['volumn'] = ""
        item['guide_price'] = ""
        item['carStyle']=""
        item['bare_price'] = ""
        item['buy_tax'] = ""
        item['deal_price'] = ""
        item['comm_ins'] = ""
        item['use_tax'] = ""
        item['trff_tax'] = ""
        item['license_fee'] = ""
        item['total_price'] = ""
        item['invoce_flg'] = ""
        item['promotion'] = ""
        item['deal_date'] = ""
        item['post_date'] = ""
        item['username'] = ""
        item['prov'] = ""
        item['city'] = ""
        item['sales_name'] = ""
        item['sales_telno'] = ""
        item['sales_addr'] = ""
        item['sales_telno'] = ""
        item['comment'] = ""
        item['curl_timestamp'] = ""
        item['url'] = ""
        item['data_id'] = ""
        return item

    def getCurrentTimestamp(self):
        # 得到时间戳
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             
    def padding(self,lstr):
        lls=''
        for i in range(0,len(lstr)):
            lls+=lstr[i]
        return lls
        
        
  