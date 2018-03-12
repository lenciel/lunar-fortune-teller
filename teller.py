#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import datetime
from lxml import etree

import logging
logger = logging.getLogger('teller')
hdlr = logging.FileHandler('teller.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

# ----------------------------------
# 老黄历数据获取
# 在线接口文档：http://www.laohuangli.net/2018/2018-2-26.html
# ----------------------------------

def lunar_cal_fetcher(delta):
    tomorrow = datetime.date.today() + datetime.timedelta(days=delta)
    cal_url = 'http://www.laohuangli.net/%s/%s-%s-%s.html' % \
              (tomorrow.year, tomorrow.year, tomorrow.month, tomorrow.day)
    print(cal_url)
    try:
        cal_resp = requests.get(cal_url)
        cal_resp.encoding = 'gb2312'
        cal_html_text = cal_resp.text
    except Exception:
        pass
    sel = etree.HTML(cal_html_text)
    bazi_year_path = '//*[@id="USkin_bk"]/table[4]/tr/td[3]/div/font[1]'
    bazi_month_path = '//*[@id="USkin_bk"]/table[4]/tr/td[3]/div/font[2]'
    bazi_date_path = '//*[@id="USkin_bk"]/table[4]/tr/td[3]/div/font[3]'
    bazi_year = sel.xpath(bazi_year_path)[0].text
    bazi_month = sel.xpath(bazi_month_path)[0].text
    bazi_date = sel.xpath(bazi_date_path)[0].text

    lunar_cal_path = '//*[@id="USkin_bk"]/table[6]/tr/td[2]/div/table[3]/tr/td'
    lunar_cal = sel.xpath(lunar_cal_path)[0].text
    lunar_cal_list = lunar_cal.split('\r\n')[1].split(' ')
    #print(lunar_cal_list[17])
    #print(lunar_cal_list[18][0:2])

    xiangchong_path = '//*[@id="USkin_bk"]/table[6]/tr/td[2]/div/table[15]/tr/td/span[2]/following-sibling::text()'
    xiangchong_str = sel.xpath(xiangchong_path)[0][1:]
    #print(xiangchong_str)
    suisa_path = '//*[@id="USkin_bk"]/table[6]/tr/td[2]/div/table[15]/tr/td/span[3]/following-sibling::text()'
    suisa_str = sel.xpath(suisa_path)[0]
    #print(suisa_str)

    logger.info(tomorrow)
    print(tomorrow)
    logger.info('%s%s%s日，%s%s，%s，%s' % (bazi_year, bazi_month, bazi_date, lunar_cal_list[17], lunar_cal_list[18][0:2], xiangchong_str, suisa_str))
    print('%s%s%s日，%s%s，%s，%s' % (bazi_year, bazi_month, bazi_date, lunar_cal_list[17], lunar_cal_list[18][0:2], xiangchong_str, suisa_str))
if __name__ == '__main__':
    for i in range(1,20000): 
        lunar_cal_fetcher(i)
