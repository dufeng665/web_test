import time
import logging

import allure
from packaging.tags import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Testltemal:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get("http://litemall.hogwarts.ceshiren.com/#/login")
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys("manage")
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys("manage123")
        self.driver.find_element(By.XPATH, '//*[text()="登录"]').click()
    def teardown_class(self):
        self.driver.quit()

    #截图,在需要截图的地方调用
    def get_screen(self):
        timestamp =int(time.time())
        image_path = f"./images/image_{timestamp}.png"
        self.driver.save_screenshot(image_path)
        #截图放到报告中
        allure.attach.file(image_path,name="picture",attachment_type=allure.attachment_type.PNG)

    # 商场管理-新增
    def test_add_type(self):
        logging.info("进入商场管理")
        self.driver.find_element(By.XPATH, '//span[text()="商场管理"]').click()
        self.driver.find_element(By.XPATH, '//span[text()="商品类目"]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[text()="添加"]').click()
        self.driver.find_element(By.XPATH, '//*[@class="el-input__inner"]').send_keys("新增商品")
        # self.driver.find_element(By.CSS_SELECTOR, '.el-dialog__footer .el-button--primary').click()
        # ele =WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.el-dialog__footer .el-button--primary')))
        # ele.click()
        """
        自定义显示等待条件
        """
        def click_exception(by, element, max_attempts=5):
            def _inner(driver):
                #多次点击
                actul_attempts =0
                while actul_attempts<max_attempts:
                    #点击操作
                    actul_attempts +=1
                    try:
                        driver.find_element(by, element).click()
                        return True
                    except Exception:
                        print("在点击时报错")
                raise Exception("超出最大点击次数")
            return _inner
            #错误写法：return _inner()
        WebDriverWait(self.driver,10).until(click_exception(By.CSS_SELECTOR, '.el-dialog__footer .el-button--primary'))

        #elements没找到会返回空，element没找到会报错
        logging.info("新增商品")
        res = self.driver.find_elements(By.XPATH, '//*[text()="新增商品"]')
        #获取截图
        self.get_screen()
        #删除新增的数据，放在断言之后，会影响断言执行结果
        self.driver.find_element(By.XPATH, '//*[text()="新增商品"]/../..//*[text()="删除"]').click()
        time.sleep(2)
        res = self.driver.find_elements(By.XPATH, '//*[text()="新增商品"]')
        logger.info("断言结果：")
        assert res == []

    # def test_delet_type(self):
    #     self.driver.find_element(By.XPATH, '//span[text()="商场管理"]').click()
    #     self.driver.find_element(By.XPATH, '//span[text()="商品类目"]').click()
    #     time.sleep(2)
    #     self.driver.find_element(By.XPATH, '//*[text()="添加"]').click()
    #     self.driver.find_element(By.XPATH, '//*[@class="el-input__inner"]').send_keys("新增商品")
    #     ele = WebDriverWait(self.driver, 10).until(
    #         expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.el-dialog__footer .el-button--primary')))
    #     ele.click()
    #     # elements没找到会返回空，element没找到会报错
    #     res = self.driver.find_elements(By.XPATH, '//*[text()="新增商品"]')
    #     self.driver.find_element(By.XPATH, '//*[text()="新增商品"]/../..//*[text()="删除"]').click()
    #     WebDriverWait(self.driver, 10).until_not(
    #         expected_conditions.visibility_of_any_elements_located((By.XPATH, '//*[text()="新增商品"]')))
    #     res = self.driver.find_elements(By.XPATH, '//*[text()="新增商品"]')
    #     assert res == []
