#encoding:utf-8
import requests
import re
from bs4 import BeautifulSoup
import os


url='https://www.zhihu.com/question/24590883'                  #把你的爬的网址输入
kv={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0'}                               #模拟登陆，
r=requests.get(url,headers=kv)                                 #获取网页
print(r.status_code)

#print(len(r.text))
print(r.text)
q=r.text
bs=BeautifulSoup(q,"html.parser")                              #把获取的网页q熬成汤bs,便于后面解析
print(bs)

title=bs.title                         # 获取标题
filename_old=title.string.strip()
filename=re.sub('[\/:*?"<>|]', '-', filename_old)      # 用来保存内容的文件名，因为文件名不能有一些特殊符号，所以使用正则表达式过滤掉
print(filename)

answernum=bs.find("h4", class_="List-headerText")              #总回答数
answernum2=answernum.find('span').get_text()                      #获取标签外的内容的中文方法
print(answernum2)

subtitle=bs.find("div", class_="ContentItem-meta")             #回答人的名字
c=subtitle.find_all('meta')
d=c[0].attrs['content']
print(d)                            #< meta itemprop="name"  content="春雨医生">这种标签内形式的查找与筛选出中文

goodcount=bs.find("div", class_="List-item")             #<meta content="31213" itemprop="upvoteCount"/>点赞数
goodcount2=goodcount.find_all('meta')
for each_goodcount2 in goodcount2:
    itemprop=each_goodcount2.attrs['itemprop']
    if itemprop=="upvoteCount":
        goodcount3=each_goodcount2.attrs['content']
        print(goodcount3)

answer=bs.find("div",class_="RichContent-inner")          #找到这段附近的内容
print(answer)
sub_folder=os.path.join(os.getcwd(), "the_key_to_question")   #专门用于存放下载的电子书的目录,名字命名为问题名
if not os.path.exists(sub_folder):
    os.mkdir(sub_folder)
os.chdir(sub_folder)
k = 0
index = 0

name=filename + ".txt"                                          #文件名命名为小题目
with open(name, 'a+')as f:                                      #增加a+从而增加文本内容，而不是重写
#    f.write(answernum2.encode('utf-8')+'\n')
    f.write(answernum2 + '\n')
    for each_answer in answer:
#        f.write('['+d.encode('utf-8')+']'+'\n')
#        f.write(goodcount3.encode('utf-8')+'点赞'+'\n')
        f.write('['+d+']'+'\n')
        f.write(goodcount3+'点赞'+'\n')

        for a in each_answer.strings:                            # 循环获取每一个答案的内容，然后保存到文件中
            f.write(a+'\n')                      #选出中文大段写入
        k=k+1
    index=index+1
f.close()