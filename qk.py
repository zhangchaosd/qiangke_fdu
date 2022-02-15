from xmlrpc.client import boolean
from selenium import webdriver
import time

xwjck_ls = [   # 学位基础课
]

xwzyk_ls = [   # 学位专业课
]

zyxxk_ls = [   # 专业选修课
]

ggxxk_ls = [   # 公共选修课
    '陶艺|陶艺',
]

xwggk_xpath = '/html/body/div/header/div/ul/li[1]/a'

xkzyk_xpath = '/html/body/div/header/div/ul/li[2]/a'         # 学科专业课  一级目录
xwjck_xpath = '/html/body/div/article[8]/div/div/ul/li[1]'   # 学位基础课  二级目录
xwjck_table_xpath = '/html/body/div/article[8]/div/div/div[2]/div[1]/div[2]/table'
xwzyk_xpath = '/html/body/div/article[8]/div/div/ul/li[2]'   # 学位专业课  二级目录
xwzyk_table_xpath = '/html/body/div/article[8]/div/div/div[2]/div[2]/div[2]/table'
zyxxk_xpath = '/html/body/div/article[8]/div/div/ul/li[3]'   # 专业选修课  二级目录
zyxxk_table_xpath = '/html/body/div/article[8]/div/div/div[2]/div[3]/div[2]/table'

ggxxk_xpath = '/html/body/div/header/div/ul/li[3]/a'         # 公共选修课  一级目录
ggxxk_table_xpath = '/html/body/div/article[10]/div/div[2]/table'

queding_xpath = '/html/body/div[3]/div[6]/div/button[1]'
quxiao_xpath = '/html/body/div[3]/div[6]/div/button[2]'

def search(driver, first_label_xpath, second_label_xpath=None, table_xpath=None, course_names=None):
    first_label = driver.find_element_by_xpath(first_label_xpath)
    first_label.click()
    if second_label_xpath is not None:
        second_label=None
        while(second_label==None):
            try:
                second_label = driver.find_element_by_xpath(second_label_xpath) # 公共选修课
            except:
                # print('try fail 1')
                second_label=None
        second_label.click()
    table=None
    while(table==None):
        try:
            table = driver.find_element_by_xpath(table_xpath)
        except:
            # print('try fail 2')
            table=None
    height=1
    while height==1:
        rows=table.find_elements_by_tag_name("tr")
        height = len(rows)
    if second_label_xpath is None:  # 公共选修课课程名在第二列
        flag = 0
    else:
        flag = 1
    for name in course_names:
        found = False
        for r in range(1, height):
            if name in rows[r].find_elements_by_tag_name('td')[1 + flag].text:
                found = True
                if '已满' == rows[r].find_elements_by_tag_name('td')[10 - flag].text:
                    print('课程已满: ', name)
                    pass
                else:
                    print('尝试抢课!!!:', name)
                    c = int(12-flag)
                    xuanke_botton_xpath = table_xpath + '/tbody/tr[' + str(r) + ']/td[' + str(c) + ']'
                    if flag == 0:
                        xuanke_botton_xpath = xuanke_botton_xpath + '/div'
                    xuanke_botton_xpath = xuanke_botton_xpath + '/a'
                    xuanke_botton = driver.find_element_by_xpath(xuanke_botton_xpath)
                    xuanke_botton.click()
                    queding=None
                    cnt=0
                    while(queding==None):
                        try:
                            queding = driver.find_element_by_xpath(queding_xpath)
                        except:
                            print('try fail 3')
                            queding=None
                            cnt=cnt+1
                        if cnt>300:
                            print('可能差一点抢到，或者检查在线情况： ', name)
                            break
                    queding.click()
                    print('请检查是否抢到课！！！: ', name)
                    time.sleep(2)
                    return

        if found is False:
            print('课程没有找到，请检查是否已经选到或者课程名输入错误：', name)
            break


# driver = webdriver.Chrome()
driver = webdriver.Edge()

driver.get('http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/*default/index.do')
driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[1]/input").clear() # 清楚文本
driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[1]/input").send_keys("21210240419") # 模拟按键输入
driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[2]/input").clear() # 清楚文本
driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[2]/input").send_keys("zc960218fd") # 模拟按键输入

input()

turn = 0
while True:
    if (turn % 100) == 0:
        print(turn)
    if len(xwjck_ls) > 0:
        search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=xwjck_xpath, table_xpath=xwjck_table_xpath, course_names=xwjck_ls)
    if len(xwzyk_ls) > 0:
        search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=xwzyk_xpath, table_xpath=xwzyk_table_xpath, course_names=xwzyk_ls)
    if len(zyxxk_ls) > 0:
        search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=zyxxk_xpath, table_xpath=zyxxk_table_xpath, course_names=zyxxk_ls)
    if len(ggxxk_ls) > 0:
        search(driver=driver, first_label_xpath=ggxxk_xpath, table_xpath=ggxxk_table_xpath, course_names=ggxxk_ls)
    turn = turn + 1


exit()

'''
安装 selenium
下载对应chrome版本的driver
复制到/usr/local/bin目录（由于Mac该目录是隐藏的，所以可通过快捷键command+shift+g打开）
查看ChromeDriver版本：chromedriver –version
更改安全设置

/html/body/div/article[8]/div/div/div[2]/div[3]/div[2]/table/tbody/tr[3]
/html/body/div/article[8]/div/div/div[2]/div[3]/div[2]/table/tbody/tr[3]/td[11]/a
/html/body/div/article[8]/div/div/div[2]/div[3]/div[2]/table/tbody/tr[3]/td[10]/a

/html/body/div/article[10]/div/div[2]/table/tbody/tr[3]/td[12]/div/a
/html/body/div/article[10]/div/div[2]/table/tbody/tr[6]/td[12]/a


/html/body/div/article[8]/div/div/div[2]/div[1]/div[2]/table/tbody/tr/td[11]/a
'''