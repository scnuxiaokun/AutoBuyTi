from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import json
import threading
import random
import time
import common
import main

# 无头模式
# opt = webdriver.FirefoxOptions()
# opt.add_argument("--headless")
# opt.add_argument('--disable-gpu')
# dr = webdriver.Firefox(options=opt)
# 有界面
# profile = webdriver.FirefoxProfile()
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", "http-pro.moguproxy.com")
# profile.set_preference("network.proxy.http_port", 9003)
# profile.update_preferences()
# dr = webdriver.Firefox(profile)
dr = webdriver.Chrome()

def checkInventory():
  while (1):
    log.info('查库存')
    inventory = 0
    if inventory > 0:
      addCart()
      break
    sleep(10)

def threedClick():
  while(1):
    randNum = random.randint(10, 20)
    randClick(randNum)
    inventory = 0
    if inventory > 0:
      break
    sleep(randNum)

# 随机点击
def randClick(randNum):
  log.info('随机点击')
  try:
    # 高速差分宽带 PLC/HPLC 线路驱动器放大器
    e = dr.find_element_by_xpath('/html/body/main/div[2]/div[1]/div[2]/div[2]/section/div[1]/div[2]/h2')
    ActionChains(dr).move_to_element_with_offset(e,0,10).click().perform()
    log.info('点对了')
  except:
    log.info('点错了')
  # 价格表
  # {'x': 350, 'y': 236}
  # {'height': 40.0, 'width': 234.9166717529297}
  # x = random.uniform(e.location['x'], e.size['height'])
  # y = random.uniform(e.location['y'], e.size['width'])
  # print("tips:点击坐标x=%s,y=%s",x,y)
  # ActionChains(dr).move_by_offset(x, y).click().perform()
  # ActionChains(dr).move_by_offset(-x, -y).perform()

# 爬url
def foxCreate(url):
  # 打开一个新tab
  dr.execute_script("window.open();")
  handles = dr.window_handles
  dr.switch_to.window(handles[1])
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

def waitIfNotLogin(dr):
  retryCount = 0
  while 1:
    retryCount += 1
    if retryCount > 120:
      return False
    if checkLogin(dr):
      log.info("已登录")
      return True
    else:
      log.info("未登录")
      time.sleep(1)

def checkLogin(dr):
  dictCookies = dr.get_cookies()
  for cookie in dictCookies:
    if cookie['name'] == 'login-check' and cookie['value']=='true' :
      return True
  return False

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


def findTiInputElement():
  e = dr.find_elements_by_class_name('add_to_cart_form')
  e = e[1]
  e = e.find_elements_by_tag_name('ti-add-to-cart')
  e = e[0]
  e = expand_shadow_element(e)
  e = e[1]
  e = e.find_elements_by_tag_name('ti-input')
  e = e[0]
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

def setInputElementValue(element, value):
  dr.execute_script('return arguments[0].value=' + str(value), element)

def addCart():
  # 输入框
  inputElement = findStockInputElement()
  tiInputElement = findTiInputElement()
  print(inputElement)
  print(tiInputElement)
  inputElement.clear()
  setInputElementValue(inputElement, 9)
  setInputElementValue(tiInputElement, 9)

  # 加入购物车
  addCartButton = findAddCartButton()
  addCartButton.click()

def checkOut():
  sleep(3)
  # 添加商品成功后点击结算按钮
  dr.find_element_by_id('add_to_cart_modal_checkout').click()
  sleep(2)
  # 批量购物车页面,点击结算按钮
  dr.find_element_by_id('tiCartCalculate_Checkout').click()
  sleep(3)
  # step1:选择企业,点击下一步
  dr.find_element_by_id('paid-shipping-address-select').click()
  sleep(2)
  # step2
  # 勾选项选择
  dr.find_element_by_id('cmpCheckboxflag').click()
  sleep(2)
  # 下一步
  dr.find_element_by_id('tax-invoice-submit').click()
  sleep(2)
  # 确认并继续
  dr.find_elements_by_class_name('vat-modal-button')[1].click()
  sleep(2)
  # step3
  # 点击不是军方
  dr.find_elements_by_class_name('militoryRadio')[1].click()
  sleep(2)
  # 点击下一步
  dr.find_element_by_id('regulations-submit-btn').click()
  sleep(2)
  # step4
  # 滑动条下拉
  e = find_element_by_id('regulations-submit-btn')
  height = dr.execute_script('return arguments[0].offsetHeight', e)
  dr.execute_script('return arguments[0].scrollTo(0,'+height+')', e)
  sleep(2)
  # 接受
  dr.find_elements_by_class_name('js-checkout-toc-radio')[0].click()
  sleep(2)
  # 下一步
  dr.find_element_by_id('shipping-method-submit').click()
  sleep(2)
  # step6
  # 选择企业网银
  dr.find_elements_by_class_name('has-tooltip')[0].click()
  sleep(2)
  # 选择在线支付
  dr.find_elements_by_class_name('js-apm-paymentbtn')[3].click()
  sleep(2)


log = common.initLoger()
# 隐形加载
dr.implicitly_wait(5)
# 打开一个主页面
dr.get("https://www.ti.com.cn/store/ti/zh/p/product/?p=THS6212IRHFT")
# 等待手动登录
waitIfNotLogin(dr)
#打开一个商品页面
url = 'https://www.ti.com.cn/store/ti/zh/p/product/?p=THS6212IRHFT'
foxCreate(url)

# addCart()
checkOut()

# 边点击边查库存
# t1 = threading.Thread(target=threedClick)
# t2 = threading.Thread(target=checkInventory)
# t1.start()
# t2.start()
