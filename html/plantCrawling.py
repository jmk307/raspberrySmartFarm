import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

#html을 통째로 읽는다
ids={}
data={"id":[],"name":[],"temp":[],"humi":[]}

for i in range(1,35,1):
  page = requests.get("https://www.nongsaro.go.kr/portal/ps/psz/psza/contentMain.ps?menuId=PS00376&pageIndex="+str(i),verify=False)
  #page = requests.get("http://www.naver.com")
  #page = requests.get("https://library.gabia.com/")
  soup = bs(page.text, "html.parser")
  #print(soup)
  all=soup.find_all('span','contArea')#span tag를 가지고 있고, class가 contArea인 태그를 모두 추출
  elements = soup.select('strong:not(.en) a')#strong tag, a tag를 가지고 있으면 추출

  for s in all:
    link=s.find("a")
    num=link.get("onclick")
    items = re.findall('\(([^)]+)', num) #괄호 안에 있는 문자들만 추출
    for ids in items:
      ids=ids.strip("'")#링크에 해당하는 숫자를 추출하기 위해서
      #print(ids)
      data["id"].append(ids)
  for index, element in enumerate(elements, 1):
    #print("{} 번째 게시글의 제목: {}".format(i*10+index, element.text))
    data["name"].append(element.text)

for i in data["id"]:
  page = requests.get("https://www.nongsaro.go.kr/portal/ps/psz/psza/contentSub.ps?menuId=PS00376&cntntsNo=" + str(i),verify=False)#추출한 식물별 아이디값을 통해 식물정보 검색
  soup = bs(page.text, "html.parser")
  elements = soup.select('tbody>tr')#생육적온과 습도가 들어있는 태그 추적
  temp_flag=0
  humi_flag=0

  for element in elements:
    if "생육적온" in element.text and "기능성정보" not in element.text and "특별관리" not in element.text:#태그 안쪽에 "생육적온"이라는 말이 있으면 해당 태그에서 앞뒤로 한 칸정도 가져옴
      soup=bs(str(element),"html.parser")
      temp=soup.select_one('td').text #td tag안쪽에 있는 문자만을 가져옴. 즉, "16~20℃"의 형태로 추출함
      temp=temp.split('~')[0]#16~20℃ 의 형태로 나오면, 앞글자만 가져옴
      temp = re.sub('[^a-zA-Z0-9]', ' ', temp).strip()#"0℃ 미만"처럼, 형식을 벗어나는 문자열의 경우 0℃가 적정온도로 간주
      print("temp:"+str(temp))
      data["temp"].append(temp)
      temp_flag=1
      break

  for element in elements:
    if "습도" in element.text and "%" in element.text:#태그 안쪽에 "습도"라는 말이 있으면 해당 태그에서 앞뒤로 한 칸정도 가져옴
      soup=bs(str(element),"html.parser")
      humi=soup.select_one('td').text #td tag안쪽에 있는 문자만을 가져옴. 즉, "40~70%"의 형태로 추출함
      humi=humi.split('~')[0]#40~70% 의 형태로 나오면, 앞글자만 가져옴
      humi = re.sub('[^a-zA-Z0-9]', ' ', humi).strip()#"70% 이상"처럼, 형식을 벗어나는 문자열의 경우 70%가 적정습도로 간주
      print("humi:" + str(humi))
      data["humi"].append(humi)
      humi_flag=1
      break

#가끔, 온, 습도 정보중에 온도만 나와있거나, 습도만 나와있는경우, 다른 한 칸을 -1로 채운다.
  if temp_flag==0:
    print("temp not detected...")
    data["temp"].append(-1)
  if humi_flag==0:
    print("humi not detected...")
    data["humi"].append(-1)

print(len(data["temp"])," and ",len(data["humi"]))




df=pd.DataFrame(data)
df.to_csv('nongsaro.csv',index=False,encoding='cp949')