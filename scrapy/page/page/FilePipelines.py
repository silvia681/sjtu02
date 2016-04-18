# encoding: utf-8
import sys
import os
import traceback
import datetime

class PagePipeline(object):

    #把解析后的内容放入文件中
    def process_item(self, item, spider):
        folder = '../output/page_output/'+ self.getExcTime()
        if not os.path.exists(folder):
            os.makedirs(folder)        
        fname =  '../output/page_output/'+ self.getExcTime()+'/'+ item['data_id'] + '.txt'
        try:
            outfile = open(fname, 'wb')
            outfile.write(item['brand']+self.getJobFieldSpt()+item['factory']+self.getJobFieldSpt()+item['serial']+self.getJobFieldSpt()+item['yearType']+self.getJobFieldSpt()+item['volumn']+self.getJobFieldSpt()+item['carStyle']+self.getJobFieldSpt()+item['guide_price']+self.getJobFieldSpt()+item['bare_price']+self.getJobFieldSpt()+item['buy_tax']+self.getJobFieldSpt()+item['deal_price']+self.getJobFieldSpt()+item['comm_ins']+self.getJobFieldSpt()+item['use_tax']+self.getJobFieldSpt()+item['trff_tax']+self.getJobFieldSpt()+item['license_fee']+self.getJobFieldSpt()+item['total_price']+self.getJobFieldSpt()+item['invoce_flg']+self.getJobFieldSpt()+item['promotion']+self.getJobFieldSpt()+item['deal_date']+self.getJobFieldSpt()+item['post_date']+self.getJobFieldSpt()+item['username']+self.getJobFieldSpt()+item['prov']+self.getJobFieldSpt()+item['city']+self.getJobFieldSpt()+item['sales_name']+self.getJobFieldSpt()+item['sales_telno']+self.getJobFieldSpt()+item['sales_addr']+self.getJobFieldSpt()+item['comment']+self.getJobFieldSpt()+item['curl_timestamp']+self.getJobFieldSpt()+item['url']+self.getJobFieldSpt()+item['data_id'])
            outfile.close()
            
        except Exception as e:
            print "ERROR GEN FILE!! >>> " + fname
            print item['url']
            #print traceback.format_exc()

    def getJobFieldSpt(self):
	#得到生成的职位文件字段间的分隔符。使用ascii码1，和hive中默认的分隔符相同
	    return chr(1)

    def getExcTime(self):
        # get time
        return datetime.datetime.now().strftime('%Y%m%d')   