from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser


class App:
    def __init__(self, dotakey):
        self.dotakey = dotakey
        # self.phone_num = phone_num
        # self.passwd = passwd

    chromedriver = r"driver/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)

    def run(self):
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
        self.driver.get('https://detail.damai.cn/item.htm?id=593089517773')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-spm="dconfirm"]')))

        dconfirm_button = self.driver.find_element_by_xpath('//button[@data-spm="dconfirm"]')
        while dconfirm_button.get_attribute('class') == 'privilege_sub disabled':
            print(dconfirm_button.get_attribute('class'), '确定按钮无法点击，刷新页面')
            # self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-spm="dconfirm"]')))
            try:
                dconfirm_button = self.driver.find_element_by_xpath('//button[@data-spm="dconfirm"]')
            except Exception as e:
                print('寻找按钮失败', e)

        self.driver.find_element_by_css_selector("#privilege_val").send_keys(self.dotakey)
        dconfirm_button.click()
        try:
            self.driver.find_element_by_xpath(
                '//a[@class="cafe-c-input-number-handler cafe-c-input-number-handler-up"]').click()
        except Exception as e:
            print("未成功点击+号", e)
        self.driver.find_element_by_xpath('//div[@class="select_right_list"]/div[3]/span[2]').click()
        dbuy_button = self.driver.find_element_by_xpath('//div[@data-spm="dbuy"]')
        print('寻找按钮:', dbuy_button.text)
        dbuy_button.click()


def get_config(section, key):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get(section, key)


if __name__ == '__main__':
    dotakey = get_config('info', 'privilege_val')
    myapp = App(dotakey)
    myapp.run()
