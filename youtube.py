import os
os.system("clear")
def getVideoData(videoId,other=False):
  from requests import get
  get = get("https://www.youtube.com/oembed?format=json&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D" + videoId)
  json = eval(str(get.json()))
  link = "https://www.youtube.com/watch?v="+videoId
  if other == False:
    del json["html"],json["thumbnail_width"],json["thumbnail_height"],json["height"],json["width"],json["version"],json["thumbnail_url"], json["provider_name"],json["type"],json["provider_url"]
    
  #update json
  json["title"] = str(json['title'])
  json['author_name'] = str(json['author_name'])
  json['author_url'] = str(json['author_url'])
  json["data_type"] = "video"
  return json,link

def getChannelData(channelId):
  imp_meta = ["title","description","og:url"]
  from bs4 import BeautifulSoup
  from requests import get
  e = get("https://www.youtube.com/channel/"+channelId).text
  bs = BeautifulSoup(e,"html.parser")
  c = bs.findAll("meta")
  c = list(c)
  json = {}
  for elem in c:
    elem = str(elem)
    for meta in imp_meta:
      elem = elem.replace('<meta content="','')
      if "name=\""+meta+"\"/>" in elem:
        elem = elem.replace('" name="'+meta+'"/>','')  
        if meta == "title":
          json["name"] = elem
        elif meta == "description":
          json["des"] = elem
      elif "property=\""+meta+"\"/>" in elem:
        elem = elem.replace('" property="'+meta+'"/>','')
        if meta == "title":
          json["name"] = elem
        elif meta == "description":
          json["des"] = elem
        elif meta == "og:url":
          json["url"] = elem
  json["data_type"] = "channel"
  return json   

def getUserData(userId):
  from bs4 import BeautifulSoup
  from requests import get
  get = get("https://www.youtube.com/user/"+userId).text
  bs = BeautifulSoup(get,"html.parser")
  e = bs.findAll("link")
  e = list(e)
  theOne = ""
  for x in e:
    x = str(x)
    if 'rel="canonical"/>' in x:
      x = x.replace('<link href="','')
      x = x.replace('" rel="canonical"/>','')
      theOne = x 
  theOne = theOne.replace("https://www.youtube.com/channel/","")    
  e = getChannelData(theOne)
  e["from"] = "function getUserData"
  return e
