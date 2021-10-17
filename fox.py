from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import json
from threading import Thread
import random
import time

# 无头模式
# opt = webdriver.FirefoxOptions()
# opt.add_argument("--headless")
# opt.add_argument('--disable-gpu')
# dr = webdriver.Firefox(options=opt)
# 有界面
dr = webdriver.Firefox()

# 随机点击
def randClick():
  # 顶部输入框
  # e = dr.find_element_by_xpath('//*[@id="searchboxheader"]/div[1]/div/div/div[1]/input')
  # ActionChains(dr).click(e).perform()

  # {'x': 350, 'y': 236}
  # {'height': 40.0, 'width': 234.9166717529297}
  try:
    # 价格表
    e = dr.find_element_by_xpath('/html/body/main/div[2]/div[1]/div[2]/div[2]/section/div[1]/div[2]/h1/span')
  except:
    # 商品标题
    e = dr.find_element_by_xpath('/html/body/main/div[2]/div[1]/div[2]/div[2]/section/div[1]/div[2]/h1/span')

  location = e.location
  size = e.size

  x = random.uniform(location['x'], size['height'])
  y = random.uniform(location['y'], size['width'])
  print("tips:点击坐标x=%s,y=%s",x,y)
  ActionChains(dr).move_by_offset(x, y).click().perform()
  ActionChains(dr).move_by_offset(-x, -y).perform()

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

def expand_shadow_element(element):
  retryCount = 0
  while 1:
    retryCount += 1
    if retryCount > 20:
      return None
    shadow_root = dr.execute_script('return arguments[0].shadowRoot.children', element)
    if len(shadow_root) > 0:
      return shadow_root
    else:
      time.sleep(1)

def findStockInputElement():
    e = dr.find_elements_by_class_name('add_to_cart_form')
    e = e[1]
    e = e.find_elements_by_tag_name('ti-add-to-cart')
    e = e[0]
    e = expand_shadow_element(e)
    e = e[1]
    e = e.find_elements_by_tag_name('ti-input')
    e = e[0]
    e = expand_shadow_element(e)
    e = e[1]
    return e


def findAddCartButton():
  e = dr.find_elements_by_class_name('add_to_cart_form')
  e = e[1]
  e = e.find_elements_by_tag_name('ti-add-to-cart')
  e = e[0]
  e = expand_shadow_element(e)
  e = e[2]
  e = expand_shadow_element(e)
  e = e[1]
  return e

url = 'https://www.ti.com/store/ti/zh/p/product/?p=THS6212IRHFT'
foxCreate(url)
# 库存输入框
# document.getElementsByClassName("add_to_cart_form")[1].getElementsByTagName('ti-add-to-cart')[0].shadowRoot.children[0].getElementsByTagName('ti-input')[0].shadowRoot.children[0].value=999
# 加入购物车按钮
# document.getElementsByClassName("add_to_cart_form")[1].getElementsByTagName('ti-add-to-cart')[0].shadowRoot.children[1].shadowRoot.children[0]
#输入框
inputElement = findStockInputElement()
print(inputElement)
# inputElement.clear()
# inputElement.send_keys(3)

#加入购物车
addCartButton = findAddCartButton()

# refershCookie(dr)
# getCookies(dr)
# threedClick()

# 关闭窗体
# dr.close()
# dr.quit()

