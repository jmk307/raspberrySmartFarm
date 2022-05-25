import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

# html을 통째로 읽는다
ids = {}
data = {"id": [], "name": [], "temp": [], "humi": []}

for i in range(1, 35, 1):
    page = requests.get(
        "https://www.nongsaro.go.kr/portal/ps/psz/psza/contentMain.ps?menuId=PS00376&pageIndex="+str(i), verify=False)
    soup = bs(page.text, "html.parser")
    # span tag를 가지고 있고, class가 contArea인 태그를 모두 추출
    all = soup.find_all('span', 'contArea')
    # strong tag, a tag를 가지고 있으면 추출
    elements = soup.select('strong:not(.en) a')

    for s in all:
        link = s.find("a")
        num = link.get("onclick")
        items = re.findall('\(([^)]+)', num)  # 괄호 안에 있는 문자들만 추출
        for ids in items:
            ids = ids.strip("'")  # 링크에 해당하는 숫자를 추출하기 위해서
            data["id"].append(ids)
    for index, element in enumerate(elements, 1):
        data["name"].append(element.text)

print("html parsing......")
for i in data["id"]:
    # 추출한 식물별 아이디값을 통해 식물정보 검색
    page = requests.get(
        "https://www.nongsaro.go.kr/portal/ps/psz/psza/contentSub.ps?menuId=PS00376&cntntsNo=" + str(i), verify=False)
    soup = bs(page.text, "html.parser")

    elements = soup.select('tbody>tr')  # 생육적온과 습도가 들어있는 태그 추적
    temp_flag = 0
    humi_flag = 0

    for element in elements:
        # 태그 안쪽에 "생육적온"이라는 말이 있으면 해당 태그에서 앞뒤로 한 칸정도 가져옴
        if "생육적온" in element.text and "기능성정보" not in element.text and "특별관리" not in element.text:
            soup = bs(str(element), "html.parser")
            # td tag안쪽에 있는 문자만을 가져옴. 즉, "16~20℃"의 형태로 추출함
            temp = soup.select_one('td').text
            temp = temp.split('~')[0]  # 16~20℃ 의 형태로 나오면, 앞글자만 가져옴
            # "0℃ 미만"처럼, 형식을 벗어나는 문자열의 경우 0℃가 적정온도로 간주
            temp = re.sub('[^a-zA-Z0-9]', ' ', temp).strip()
            print("temp:"+str(temp))
            data["temp"].append(temp)
            temp_flag = 1
            break

    for element in elements:
        # 태그 안쪽에 "습도"라는 말이 있으면 해당 태그에서 앞뒤로 한 칸정도 가져옴
        if "습도" in element.text and "%" in element.text:
            soup = bs(str(element), "html.parser")
            # td tag안쪽에 있는 문자만을 가져옴. 즉, "40~70%"의 형태로 추출함
            humi = soup.select_one('td').text
            humi = humi.split('~')[0]  # 40~70% 의 형태로 나오면, 앞글자만 가져옴
            # "70% 이상"처럼, 형식을 벗어나는 문자열의 경우 70%가 적정습도로 간주
            humi = re.sub('[^a-zA-Z0-9]', ' ', humi).strip()
            print("humi:" + str(humi))
            data["humi"].append(humi)
            humi_flag = 1
            break

# 가끔, 온, 습도 정보중에 온도만 나와있거나, 습도만 나와있는경우, 빈 칸을 -1로 채운다.
    if temp_flag == 0:
        print("temp not detected...")
        data["temp"].append(-1)
    if humi_flag == 0:
        print("humi not detected...")
        data["humi"].append(-1)

print(len(data["temp"]), " and ", len(data["humi"]))


df = pd.DataFrame(data)
df.to_csv('nongsaro.csv', index=False, encoding='cp949')
