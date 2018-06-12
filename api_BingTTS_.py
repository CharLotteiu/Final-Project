
# coding: utf-8

# In[1]:


import http.client, urllib.parse, json
from xml.etree import ElementTree


# In[2]:


import time


# In[3]:


class BingTTS:
    def __init__(self):
        self.apiKey = "b5020c6a408d473d890c724c236320b4"
        self.AccessTokenHost = "westus.api.cognitive.microsoft.com"
        self.TTSHost = "westus.tts.speech.microsoft.com"
        self.filepath = "D:/pythontest/"
        self.tmp = ""
        
    def getToken(self):
        #通过API连接到服务器后获取Token值
        headers = {"Ocp-Apim-Subscription-Key": self.apiKey}
        path = "/sts/v1.0/issueToken"
        params = ""
        conn = http.client.HTTPSConnection(self.AccessTokenHost)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        accesstoken = data.decode("UTF-8")
        print ("Access Token: " + accesstoken)
        return (accesstoken)
        
    def getHeaders(self, accesstoken):
        #获得Token值后拼装http报文的头部
        headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
			"Authorization": "Bearer " + accesstoken, 
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
			"User-Agent": "TTSForPython"}
        return (headers)
    
    def getBody(self, gender, lang, role, text):
        #获得输入信息后按照格式拼装http报文的body
        body = ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
        voice = ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
        mystr = 'Microsoft Server Speech Text to Speech Voice (' + lang + ', ' + role + ')'
        voice.set('name', mystr)
        voice.text = text
        return (body)
    
    def getWave(self, iheaders, ibody):
        #获得音频数据
        headers = iheaders
        body = ibody
        print ("\nConnect to server to synthesize the wave")
        conn = http.client.HTTPSConnection(self.TTSHost)
        conn.request("POST", "/cognitiveservices/v1", ElementTree.tostring(body), headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
        return (data)
    
    def saveAsRecord(self,idata):
        #将音频数据保存成音频文件
        filename = time.strftime("%Y-%m-%d %H%M%S", time.localtime()) + '.wav'
        filename = self.filepath + filename
        self.tmp = filename
        data = idata
        f = open(filename,'wb+')
        f.write(data)
        f.close()
        return (0)
    
    def Text2Speech(self, text, gender = 'Male', lang = 'en-US', role = 'Guy24KRUS'):
        #对外开放的han
        igender = gender
        ilang = lang
        irole = role
        itext = text
        accesstoken = self.getToken()
        headers = self.getHeaders(accesstoken)
        body = self.getBody(igender, ilang, irole, itext)
        data = self.getWave(headers, body)
        print("The synthesized wave length: %d" %(len(data)))
        self.saveAsRecord(data)
    
    def getFilename(self):
        filename = self.tmp
        self.tmp = ""
        return (filename)


# In[4]:


TTStool = BingTTS()


# In[5]:


TTStool.getToken()


# In[6]:


TTStool.Text2Speech('Today is a beautiful Friday. I am studying with Coco.','Male', 'en-US','Guy24KRUS')


# In[7]:


TTStool.Text2Speech('Coco and I had a quarrel yesterday, but we reconcile today.')

