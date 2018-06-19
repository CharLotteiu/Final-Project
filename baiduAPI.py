# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 19:45:58 2018

@author: asushj
"""

import http.client  
import hashlib  
import json   
import random  
import urllib

class Baidu_Translation:
    def __init__(self):  
        self._q = ''  
        self._from = 'auto'  
        self._to = 'en'  
        self._appid = '20151113000005349'  
        self._key = 'osubCEzlGjzvw8qdQc41'
        self._salt = random.randint(32768, 65536)  
        self._sign = ''  
        self._dst = ''  
        self._enable = True
        self._httpClient = None
        self._myurl = ''

    def Baidu_connect(self,content):  
        self._q = content
        m = str(self._appid)+self._q+str(self._salt)+self._key  
        m_MD5 = hashlib.md5(m.encode())  
        self._sign = m_MD5.hexdigest()          
        Url_1 = '/api/trans/vip/translate'  
        Url_2 = '?appid='+str(self._appid)+'&q='+urllib.parse.quote(self._q)+'&from='+self._from+'&to='+self._to+'&salt='+str(self._salt)+'&sign='+self._sign  
        self.myurl = Url_1+Url_2
        try:
            self._httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')  
            self._httpClient.request('GET', self.myurl)   # response是HTTPResponse对象  
            response = self._httpClient.getresponse()  
            jsonResponse = response.read().decode("utf-8")# 获得返回的结果，结果为json格式  
            js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构  
            self._dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果  
            print (self._dst) # 打印结果 
        except Exception as e:  
            print(e)  
        finally:  
            if self._httpClient:  
                self._httpClient.close() 
        
        
        
if __name__ == '__main__':  
    while True:  
        print("请输入要翻译的内容")  
        content = input() 
        if content:
            Baidu_Translation().Baidu_connect(content)
        else:
            break  
          