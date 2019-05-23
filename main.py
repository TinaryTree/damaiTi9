from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')


def get_config(section, key):
    return config.get(section, key)


class App:
    dotakey = get_config('info', 'privilege_val')
    name = get_config('info', 'name')
    phone = get_config('info', 'phone')
    round = get_config('model', 'round')
    quantity = get_config('model', 'quantity')
    express = get_config('model', 'express')

    chromedriver = r"driver/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)

    def login(self):
        """登陆模块"""

        self.driver.get('https://passport.damai.cn/login')
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, 'alibaba-login-box')))
        # self.driver.switch_to.frame('alibaba-login-box')
        # self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(self.phone_num)
        # self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(self.passwd)

        WebDriverWait(self.driver, 3000).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-spm="duserinfo"]/div')))
        print('登陆成功')
        user_name = self.driver.find_element_by_xpath('//a[@data-spm="duserinfo"]/div').text
        print('账号：', user_name)

    def detail_page_auto(self):
        """详情页自动"""

        self.driver.get('https://detail.damai.cn/item.htm?id=593089517773')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-spm="dconfirm"]')))

        dconfirm_button = self.driver.find_element_by_xpath('//button[@data-spm="dconfirm"]')
        while dconfirm_button.get_attribute('class') == 'privilege_sub disabled':
            print(dconfirm_button.get_attribute('class'), '确定按钮无法点击，刷新页面')
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-spm="dconfirm"]')))
            try:
                dconfirm_button = self.driver.find_element_by_xpath('//button[@data-spm="dconfirm"]')
            except Exception as e:
                print('寻找按钮失败', e)

        self.driver.find_element_by_css_selector("#privilege_val").send_keys(self.dotakey)
        dconfirm_button.click()
        if self.quantity != 1:
            try:
                self.driver.find_element_by_xpath(
                    '//a[@class="cafe-c-input-number-handler cafe-c-input-number-handler-up"]').click()
            except Exception as e:
                print("未成功点击+号", e)
        self.driver.find_element_by_xpath(f'//div[@class="select_right_list"]/div[{self.round}]/span[2]').click()
        dbuy_button = self.driver.find_element_by_xpath('//div[@data-spm="dbuy"]')
        print('寻找按钮:', dbuy_button.text)
        dbuy_button.click()

    def confirm_auto(self):
        """自动确认订单"""

        title = self.driver.title
        while title != '确认订单':
            title = self.driver.title
        if self.express == 'True':
            try:
                self.driver.find_element_by_xpath('//*[@id="confirmOrder_1"]/div[1]/div[2]/div[2]').click()
                time.sleep(2)
            except Exception as e:
                print('未能成功选择快递', e)

        else:
            try:
                self.driver.find_element_by_xpath(
                    '//div[@id="confirmOrder_1"]/div[1]/div[4]/div[1]/div[2]/span/input').send_keys(self.name)
                self.driver.find_element_by_xpath(
                    '//div[@id="confirmOrder_1"]/div[1]/div[4]/div[2]/div[2]/span[2]/input').send_keys(self.phone)
            except Exception as e:
                print('联系人输入出错', e)

        try:
            self.driver.find_element_by_xpath(
                '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div[1]/label/span[1]/input').click()
            self.driver.find_element_by_xpath(
                '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div[2]/label/span[1]/input').click()
        except Exception as e:
            print('购票人选择出错', e)

        self.driver.find_element_by_xpath('//div[@class="submit-wrapper"]/button').click()


if __name__ == '__main__':
    print('版本1.2')

    myapp = App()
    myapp.login()
    myapp.detail_page_auto()
    myapp.confirm_auto()
