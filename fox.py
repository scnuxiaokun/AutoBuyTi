from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import json

# 窗体构建
opt = webdriver.FirefoxOptions()
opt.add_argument("--headless")
opt.add_argument('--disable-gpu')
dr = webdriver.Firefox(options=opt)

# 约束窗体大小
dr.set_window_size(1024, 1366)
dr.maximize_window()
time.sleep(1)

# 随机点击
def randClick():
  # 顶部输入框
  # e = dr.find_element_by_xpath('//*[@id="searchboxheader"]/div[1]/div/div/div[1]/input')
  # ActionChains(dr).click(e).perform()

  # 商品标题
  # e = dr.find_element_by_xpath('/html/body/main/div[2]/div[1]/div[2]/div[2]/section/div[1]/div[2]/h1/span')
  # ActionChains(dr).click(e).perform()

  # 价格表
  # {'x': 350, 'y': 236}
  # {'height': 40.0, 'width': 234.9166717529297}
  e = dr.find_element_by_xpath('/html/body/main/div[2]/div[1]/div[2]/div[2]/section/div[1]/div[2]/h1/span')
  location = e.location
  size = e.size

  x = random.uniform(location['x'], size['height'])
  y = random.uniform(location['y'], size['width'])
  print("tips:点击坐标x=%s,y=%s",x,y)
  ActionChains(dr).move_by_offset(x, y).click().perform()

# 爬url
def foxCreate(url):
  # 隐形加载
  dr.implicitly_wait(5)
  dr.get(url)

  #todo 被墙处理
  html = dr.page_source
  print('tips:current_url=' + dr.current_url)
  if 'Access Denied' in html:
    print('tips:Access Denied')
    exit()

# 获取浏览器cookie
def getCookies(dr):
  dictCookies = dr.get_cookies()
  jsonCookies = json.dumps(dictCookies)

  with open('driver_cookie.txt', 'w') as f:
    f.write(jsonCookies)
  print('tips:driver_cookie保存成功')

# 替换cookie后刷新浏览器
def refershCookie(dr):
  # f1 = open('cookie.txt')
  print('tips:current_url=' + dr.current_url)
  try:
    f1 = open('driver_cookie.txt')
  except:
    f1 = open('cookie.txt')
  cookie = f1.read()
  cookie = json.loads(cookie)
  for c in cookie:
    dr.add_cookie(c)
  # 刷新页面
  print('tips:cookies替换成功')
  dr.refresh()
  print('tips:浏览器刷新成功')

url = 'https://www.ti.com/store/ti/zh/p/product/?p=THS6212IRHFT'
foxCreate(url)
refershCookie(dr)
getCookies(dr)

# 轮询执行点击方法
randClick()

# 关闭窗体
dr.quit()

