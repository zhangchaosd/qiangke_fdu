from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import threading
from PIL import Image
import ddddocr
import io

xwjck_ls = [   # 学位基础课
]

xwzyk_ls = [   # 学位专业课
]

zyxxk_ls = [   # 专业选修课
]

ggxxk_ls = [   # 公共选修课
    '陶艺|陶艺',
]

xuehao = '21210240419'
pwd = 'wwww'

scale_factor = 2
show_yzm = False

xuehao_input_xpath = '/html/body/div/article[1]/section/div[4]/div[1]/input'  # 学号输入框
pwd_input_xpath = '/html/body/div/article[1]/section/div[4]/div[2]/input'  # 密码输入框
yzm_input_xpath = '/html/body/div/article[1]/section/div[4]/div[3]/input'  # 验证码输入框
yzm_xpath = '/html/body/div/article[1]/section/div[4]/div[3]/img'  # 验证码图片
login_xpath = '/html/body/div/article[1]/section/div[4]/button[2]'  # 登录按钮
errmsg_xpath = '/html/body/div/article[1]/section/div[4]/button[1]'  # 错误信息

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

def safe_get_element_by_xpath(driver, xpath, try_times=300):
    res = None
    fail_cnt = 0
    while(res is None):
        if fail_cnt > try_times:
            break
        try:
            res = driver.find_element_by_xpath(xpath)
            return True, res
        except:
            res = None
        fail_cnt = fail_cnt + 1
    exit()
    return False, None

def get_snap(driver):  # 对目标网页进行截屏。这里截的是全屏
    driver.save_screenshot('full_snap.png')
    page_snap_obj=Image.open('full_snap.png')
    return page_snap_obj
 
 
def get_image(driver): # 对验证码所在位置进行定位，然后截取验证码图片
    img = driver.find_element_by_xpath(yzm_xpath)
    time.sleep(2)
    location = img.location
    print(location)
    size = img.size
    left = location['x'] * scale_factor
    top = location['y'] * scale_factor
    right = left + size['width']  * scale_factor
    bottom = top + size['height'] * scale_factor

    page_snap_obj = get_snap(driver)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    if show_yzm:
        image_obj.show()
    imgByteArr = io.BytesIO()
    image_obj.save(imgByteArr, format='PNG') # format: PNG / JPEG
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

click_interval=0.2


def search(driver, first_label_xpath, second_label_xpath=None, table_xpath=None, course_names=None):
    res, first_label = safe_get_element_by_xpath(driver, first_label_xpath)
    if res is False:
        pass  # TODO
    first_label.click()
    # time.sleep(click_interval)
    if second_label_xpath is not None:
        res, second_label=safe_get_element_by_xpath(driver, second_label_xpath)
        if res is False:
            pass  # TODO
        second_label.click()
        # time.sleep(click_interval)
    res, table=safe_get_element_by_xpath(driver, table_xpath)
    if res is False:
        return  # TODO
    height=1
    try_times = 0
    while height==1:
        rows=table.find_elements_by_tag_name("tr")
        height = len(rows)  # TODO
        try_times = try_times + 1
        if try_times > 50:
            exit()
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
                    _, xuanke_botton = safe_get_element_by_xpath(driver, xuanke_botton_xpath)
                    xuanke_botton.click()
                    res, queding=safe_get_element_by_xpath(driver, queding_xpath, 300)
                    if res is False:
                        tprint('可能差一点抢到，或者检查在线情况： ', name)
                        break
                    queding.click()
                    tprint('请检查是否抢到课！！！: ', name)
                    time.sleep(2)
                    return

        if found is False:
            tprint('课程没有找到，请检查是否已经选到或者课程名输入错误：', name)
            break



class myThread (threading.Thread):
    def core(self):
        driver=self.driver
        # options = ChromeOptions(); 
        # options.add_argument("disable-infobars")
        # driver = webdriver.Chrome()
        # driver = webdriver.Edge()
        driver.get('http://yjsxk.fudan.edu.cn/yjsxkapp/sys/xsxkappfudan/*default/index.do')
        time.sleep(2)
        _, xuehao_input = safe_get_element_by_xpath(driver, xuehao_input_xpath, 2000)
        xuehao_input.clear()
        xuehao_input.send_keys(xuehao)
        _, pwd_input = safe_get_element_by_xpath(driver, pwd_input_xpath, 2000)
        pwd_input.clear()
        pwd_input.send_keys(pwd)

        exit_button = None
        image = get_image(driver)
        yzm = self.ocr.classification(image)
        _, yzm_input = safe_get_element_by_xpath(driver, yzm_input_xpath)
        yzm_input.clear()
        yzm_input.send_keys(yzm)
        _, login_button = safe_get_element_by_xpath(driver, login_xpath)

        login_button.click()
        time.sleep(1)
        try:
            exit_button = driver.find_element_by_id('logoutSpan')
        except:
            exit_button = None
        if exit_button is None:
            self.close()


        while True:
            self.check_stop()
            if len(xwjck_ls) > 0:
                search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=xwjck_xpath, table_xpath=xwjck_table_xpath, course_names=xwjck_ls)
            if len(xwzyk_ls) > 0:
                search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=xwzyk_xpath, table_xpath=xwzyk_table_xpath, course_names=xwzyk_ls)
            if len(zyxxk_ls) > 0:
                search(driver=driver, first_label_xpath=xkzyk_xpath, second_label_xpath=zyxxk_xpath, table_xpath=zyxxk_table_xpath, course_names=zyxxk_ls)
            if len(ggxxk_ls) > 0:
                search(driver=driver, first_label_xpath=ggxxk_xpath, table_xpath=ggxxk_table_xpath, course_names=ggxxk_ls)

    def __init__(self):
        threading.Thread.__init__(self)
        self.should_stop=False
        options = ChromeOptions(); 
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('window-size=1920x1080')
        self.driver=webdriver.Chrome(options=options)
        # self.driver.maximize_window()
        self.ocr=ddddocr.DdddOcr()

    def run(self):
        self.core()
    
    def close(self):
        self.should_stop=True
    
    def check_stop(self):
        if not self.should_stop:
            return
        self.driver.close()
        time.sleep(0.1)
        exit()


if __name__ == '__main__':
    while(True):
        t1 = myThread()
        t1.start()
        t1.join(300)  # 300
        print('try kill')
        t1.close()
        print('kill done')
        time.sleep(0.1)
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
'''
pip install flatbuffers
pip3 install -i https://test.pypi.org/simple/ onnxruntime
pip install ddddocr==1.4.2
'''