from selenium import webdriver
import time

ls = [
    {
        '课程名称|班级': '陶艺|陶艺'
    },



]

print(ls[0]['课程名称|班级'])

# driver = webdriver.Chrome()
driver = webdriver.Edge()

# driver.get('http://www.baidu.com/')
# time.sleep(10)
# driver.find_element_by_id("kw").clear() # 清楚文本
# driver.find_element_by_id("kw").send_keys("selenium") # 模拟按键输入
# exit()
input()
xwggk = driver.find_element("xkkctab_7") # 学位公共课
xkggk = driver.find_element("xkkctab_8") # 学科专业课
ggxxk = driver.find_element("xkkctab_9") # 公共选修课
xkggk.click()
queren = driver.find_element_by_xpath("/html/body/div[3]/div[6]/div/button[1]")
# k = driver.find_element_by_xpath("/html/body/div/article[8]/div/div/div[2]/div[1]/div[2]/table/tbody/tr/td[11]/a")
# k.click()
#  /html/body/div[3]/div[6]/div/button[1]
# while(len(ls) > 0):
#     for ke in ls:
#         driver.find
#         pass
#     pass

exit()

'''
安装 selenium
下载对应chrome版本的driver
复制到/usr/local/bin目录（由于Mac该目录是隐藏的，所以可通过快捷键command+shift+g打开）
查看ChromeDriver版本：chromedriver –version
更改安全设置

https://zhuanlan.zhihu.com/p/111859925
//*[@id="ggkc_tab_container"]/ul/li[1]
/html/body/div/article[7]/div/div/ul/li[2]
//*[@id="xkkctab_9"]/text()


//*[@id="tbody_7e163ded22ff4eb191a65532b76057da"]/tr[2]/td[12]


/html/body/div/article[10]/div/div[2]/table/tbody/tr[2]/td[2]

/html/body/div/article[10]/div/div[2]/table/tbody/tr[24]/td[12]/div/a
/html/body/div/article[10]/div/div[2]/table/tbody/tr[3]/td[12]/div/a
/html/body/div/article[8]/div/div/div[2]/div[1]/div[2]/table/tbody/tr/td[11]/a   学科专业课

'''