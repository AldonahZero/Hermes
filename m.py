import base64
from selenium import webdriver
import random
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time



class Amsshopping():

    def __init__(self, url, username, password):
        self.url = url
        options = webdriver.ChromeOptions()
        # 设置为开发者模式，避免被识别
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 创建浏览器对象
        self.driver = webdriver.Chrome(executable_path='./mylib/chromedriver',options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """})
        self.username = username
        self.password = password
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(20)
        print(self.driver.page_source)
        self.driver.page_source
        self.driver.find_element_by_css_selector('#header-navigation > ul > li:nth-child(3) > button').click()
        username_input = self.driver.find_element_by_css_selector('#edit-loginphone--7')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_css_selector(
            '#login-password')
        password_input.send_keys(self.password)
        # self.get_image()
        login_button = self.driver.find_element_by_css_selector(
            '#hermes-account-login-form > div > div:nth-child(2) > button')
        login_button.click()
        # self.driver.implicitly_wait(10)
        # search = self.driver.find_element_by_css_selector('#block-hermes-commerce-nav-search')
        # search.clear()
        # # 搜索按钮
        # search.send_keys('H078607CKAA')
        # # 再次购物按钮
        # reshopping_button = self.driver.find_element_by_css_selector('#tray-account > div > button')
        # reshopping_button.click()
        # # 点击搜索按钮
        # search_button = self.driver.find_element_by_css_selector('.btn.search.icon.icon-search')
        # search_button.click()
        # input()

    def shopping(self):
        time.sleep(3)
        #加入购物袋
        self.driver.find_element_by_css_selector('#add-to-cart-button-in-stock').click()
        # self.driver.implicitly_wait(5)
        #查看购物袋
        time.sleep(3)
        self.driver.find_element_by_css_selector('body > h-modal > div.modal-container.ng-trigger.ng-trigger-easeAnimation > div.modal-footer > div > h-button > button').click()
        # self.driver.implicitly_wait(5)
        time.sleep(3)
        #结算
        self.driver.find_element_by_css_selector("#open-checkout").click()
        self.driver.implicitly_wait(5)
        self.login()
        self.driver.implicitly_wait(5)
        #继续购物
        self.driver.find_element_by_css_selector('#tray-account > div > button').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_css_selector('#open-cart').click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector("#open-checkout").click()
        #下一步
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector('#hermes-checkout-delivery-form > div > section:nth-child(4) > p > button').click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector('#edit-terms-conditions-checkbox').click()
        #确认并付款
        self.driver.find_element_by_css_selector('#hermes-checkout-china-payment-form > div > section > p > button').click()
        input()

    def verificate(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(6)
        try:
            frame = self.driver.find_element_by_css_selector('body > iframe')
            self.driver.switch_to.frame(frame)
        except Exception:
            frame = self.driver.find_element_by_css_selector('div>iframe')
            self.driver.switch_to.frame(frame)
        print(1)
        self.driver.find_element_by_css_selector('div.geetest_radar_tip').click()
        print(2)
        time.sleep(2)
        self.driver.execute_script(
            "var y=document.getElementsByClassName('geetest_canvas_slice geetest_absolute')[0];"
            "y.style.display='none';"
            "y.style.opacity=1;"
        )
        image1 = self.get_captcha_pic("image1.png")
        self.driver.execute_script(
            "var x=document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0];"
            "x.style.display='block';"
            "x.style.opacity=1;"
        )
        image2 = self.get_captcha_pic("image2.png")  # 获取无缺口验证码图片
        gap = self.get_gap(image1, image2)
        print(gap)
        gap -= 6
        track = self.slide_path(self.check_gap(gap))
        print(track)
        self.driver.execute_script(
            "var y=document.getElementsByClassName('geetest_canvas_slice geetest_absolute')[0];"
            "y.style.display='block';"
            "y.style.opacity=1;"
        )
        # 拖动滑块
        slide = self.get_slider()
        self.move_to_gap(slide, track)
        time.sleep(1)
        try:
            self.shopping()
        except Exception:
            self.shopping()
        input()
        self.driver.close()
    def pixel_is_equal(self, image1, image2, x, y):
        """
        判断两张图片的像素是否相等,不相等即为缺口位置
        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 55  # 像素色差
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True  # 像素色差小于60，默认为没区别
        else:
            return False
    def check_gap(self, gap):
        """
        校准gap，可以自己调节，越精细，效果越好
        :param gap:
        :return: gap
        """
        aa = round(gap / 12.5)
        bb = {4: 38, 5: 41, 6: 42, 7: 43, 8: 46, 9: 52, 10: 54, 11: 59, 12: 62, 13: 65, 14: 68, 15: 71, 16: 74, 17: 79,
              18: 84, 19: 86, 20: 87, 21: 92, 22: 93, 23: 95, 24: 98, 25: 101}
        return gap - bb.get(int(aa))
    def get_captcha_pic(self, name="captcha.png"):
        """
        获取验证码图片
        :param name:
        :return: captcha图片对象
        """
        time.sleep(5)
        self.driver.save_screenshot(name)  # 截屏幕图
        im = Image.open(name)
        # aa = (572, 193, 980, 452)  # 获取验证码图片在屏幕图当中的位置，测量不知道比例，可以再一边测好了
        aa =(800, 350, 1200, 600)
        captcha = im.crop(aa)  # todo 识别的时候存在问题
        captcha.save(name)  # 保存验证码图片
        return captcha
    def get_gap(self, image1, image2):
        """
        获取缺口位置
        :param image1:完整图片
        :param image2: 带缺口的图片
        :return:
        """
        left = 60  # 设置一个起始量,因为验证码一般不可能在左边，加快识别速度
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.pixel_is_equal(image1, image2, i, j):
                    left = i
                    return left
        return left
    # def slide_path(self, gap):
    #     """
    #     滑动路径
    #     :param gap:
    #     :return: 滑动路径
    #     """
    #     # 移动轨迹
    #     track = []
    #     # 当前位移
    #     current = 0
    #     # 减速阈值
    #     mid = gap * 4 / 5
    #     # 计算间隔
    #     t = 0.2
    #     # 初速度
    #     v = 0
    #     while current < gap:
    #         if current < mid:
    #             # 加速度为正2
    #             a = random.randint(2, 3)
    #         else:
    #             # 加速度为负3
    #             a = -random.randint(3, 4)
    #         # 初速度v0
    #         v0 = v
    #         # 当前速度v = v0 + at
    #         v = v0 + a * t
    #         # 移动距离x = v0t + 1/2 * a * t^2
    #         move = v0 * t + 1 / 2 * a * t * t
    #         # 当前位移
    #         current += move
    #         # 加入轨迹
    #         track.append(round(move))
    #     return track
    def slide_path(self,gap):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ① v=v0+at
        ② s=v0t+(1/2)at²
        ③ v²-v0²=2as
        :param gap: 需要移动的距离
        :return: 存放每0.2秒移动的距离
        """
        print("distance", gap)
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 2
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = [2]
        # 当前的位移
        current = 0
        # 到达 mid 值开始减速(中点)
        mid = gap * 7 / 8
        # 多划出去 10 像素
        gap += 13  # 先滑过一点，最后再反着滑动回来
        # a = random.randint(1,3)
        while current < gap:
            # 设置速度
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(2, 4)  # 加速运动
            else:
                a = -random.randint(3, 5)  # 减速运动

            # 初速度
            v0 = v
            # 0.2 秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t

        print(tracks)
        total = sum(tracks)
        # 对超出的移动的内容进行修正
        while (total - gap) > -13:
            # 反着滑动到大概准确位置
            tracks.append(-random.randint(2, 3))
            total = sum(tracks)

        print('tracks', tracks)
        print('sumtracks', sum(tracks))
        random.shuffle(tracks)
        return tracks

    def get_slider(self):
        """
        获取滑块
        :return:
        """
        slide = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slide
    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()
    def built_url(self):

        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        try:
            self.shopping()
        except Exception:
            self.driver.implicitly_wait(10)
            self.verificate()

if __name__ == '__main__':
    url = "https://www.hermes.cn/cn/zh/product/trim-31-anate-rainbow%E8%82%A9%E8%83%8C%E5%8C%85-H079227CKAB/"
    username = '18279411205'
    password = '199806230024'
    ams_shopping = Amsshopping(url, username, password)
    ams_shopping.built_url()