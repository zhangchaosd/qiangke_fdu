from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import multiprocessing as mp
import threading as td
# from PIL import Image

xwjck_ls = [   # 学位基础课
]

xwzyk_ls = [   # 学位专业课
]

zyxxk_ls = [   # 专业选修课
]

ggxxk_ls = [   # 公共选修课
    '陶艺|陶艺',
]

yzm_input_xpath = '/html/body/div/article[1]/section/div[4]/div[3]/input'  # 验证码输入框
yzm_xpath = '/html/body/div/article[1]/section/div[4]/div[3]/img'   # 验证码图片
'/html/body/div/article[1]/section/div[4]/button[2]'
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

yxkc_xpath = '/html/body/div/header/div/ul/li[3]/a'         # 已选课程  一级目录

queding_xpath = '/html/body/div[3]/div[6]/div/button[1]'
quxiao_xpath = '/html/body/div[3]/div[6]/div/button[2]'

def tprint(*t):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(cur_time)
    print(*t)

def safe_get_element_by_xpath(driver, xpath):
    res = None
    fail_cnt = 0
    while(res is None):
        if fail_cnt > 30:
            break
        try:
            res = driver.find_element_by_xpath(xpath)
            return True, res
        except:
            res = None
        fail_cnt = fail_cnt + 1
    return False, None

# def get_snap(driver):  # 对目标网页进行截屏。这里截的是全屏
#     driver.save_screenshot('full_snap.png')
#     page_snap_obj=Image.open('full_snap.png')
#     return page_snap_obj
 
 
# def get_image(driver): # 对验证码所在位置进行定位，然后截取验证码图片
#     img = driver.find_element_by_xpath(yzm_xpath)
#     time.sleep(2)
#     location = img.location
#     print(location)
#     size = img.size
#     left = location['x']
#     top = location['y']
#     right = left + size['width']
#     bottom = top + size['height']
 
#     page_snap_obj = get_snap(driver)
#     image_obj = page_snap_obj.crop((left, top, right, bottom))
#     image_obj.show()
#     return image_obj  # 得到的就是验证

click_interval=0.2


def search(driver, first_label_xpath, second_label_xpath=None, table_xpath=None, course_names=None):
    first_label = driver.find_element_by_xpath(first_label_xpath)
    first_label.click()
    time.sleep(click_interval)
    if second_label_xpath is not None:
        second_label=None
        faile_times=0
        while(second_label==None):
            try:
                second_label = driver.find_element_by_xpath(second_label_xpath) # 公共选修课
            except:
                tprint('try fail 1')
                second_label=None
                faile_times=faile_times+1
                if faile_times > 20:
                    driver.find_element_by_xpath(yxkc_xpath).click()
                    time.sleep(1)
                    faile_times=0
                    first_label.click()
                    time.sleep(click_interval)
        second_label.click()
        time.sleep(click_interval)
    table=None
    faile_times=0
    while(table==None):
        try:
            table = driver.find_element_by_xpath(table_xpath)
        except:
            tprint('try fail 2')
            faile_times=faile_times+1
            if faile_times > 20:
                return
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
                    tprint('课程已满: ', name)
                    pass
                else:
                    tprint('尝试抢课!!!:', name)
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
                            tprint('try fail 3')
                            queding=None
                            cnt=cnt+1
                        if cnt>300:
                            tprint('可能差一点抢到，或者检查在线情况： ', name)
                            break
                    queding.click()
                    tprint('请检查是否抢到课！！！: ', name)
                    time.sleep(2)
                    return

        if found is False:
            tprint('课程没有找到，请检查是否已经选到或者课程名输入错误：', name)
            break

def core():
    # options = ChromeOptions(); 
    # options.add_argument("disable-infobars")
    driver = webdriver.Chrome()
    # driver = webdriver.Edge()



    driver.get('http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/*default/index.do')
    driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[1]/input").clear() # 清楚文本
    driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[1]/input").send_keys("21210240419") # 模拟按键输入
    driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[2]/input").clear() # 清楚文本
    driver.find_element_by_xpath("/html/body/div/article[1]/section/div[4]/div[2]/input").send_keys("zc960218fd") # 模拟按键输入
    # get_image(driver)
    time.sleep(1000)
    input()

    turn = 0
    while True:
        try:
            if (turn % 100) == 0:
                tprint(str(turn))
            if len(xwjck_ls) > 0:
                search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=xwjck_xpath, table_xpath=xwjck_table_xpath, course_names=xwjck_ls)
            if len(xwzyk_ls) > 0:
                search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=xwzyk_xpath, table_xpath=xwzyk_table_xpath, course_names=xwzyk_ls)
            if len(zyxxk_ls) > 0:
                search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=zyxxk_xpath, table_xpath=zyxxk_table_xpath, course_names=zyxxk_ls)
            if len(ggxxk_ls) > 0:
                search(driver=driver, first_label_xpath=ggxxk_xpath, table_xpath=ggxxk_table_xpath, course_names=ggxxk_ls)
        except:
            pass
        else:
            turn = turn + 1



if __name__ == '__main__':
    p1 = mp.Process(target=core, args=())
    p2 = mp.Process(target=core, args=())
    p1.start()
    p2.start()
    input()
    exit()

'''
pip3 install selenium
把 chromedriver 放到 /usr/local/bin
打开终端，输入 chromedriver -version ，以能看到版本号为准
（由于Mac该目录是隐藏的，所以可通过快捷键command+shift+g打开）
查看ChromeDriver版本：chromedriver –version
可能要更改安全设置
chmod u+x ./chromedriver
'''