import time
import unittest
from tests.settings import TestVariables
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
TODO: figure out how to import models from /dndapp/
'''


class RegisterTest(unittest.TestCase):
        @classmethod
        def setUpClass(inst):
            print('testing user registration')
            inst.driver = webdriver.Firefox()
            inst.driver.get("http://localhost:5555")
            inst.driver.maximize_window()



        def test_register(self):

            try:
                '''
                Check if user is logged in
                '''
                elem = self.driver.find_element_by_id('account-dropdown')

            except:
                '''
                Not logged in, register new user
                '''
                self.driver.find_element_by_id('account-register-ddbtn').click()
                username = self.driver.find_element_by_id('username_field')
                username.clear()
                email = self.driver.find_element_by_id('email_field')
                email.clear()
                password = self.driver.find_element_by_id('password_field')
                password.clear()
                confirm = self.driver.find_element_by_id('confirm_password_field')
                confirm.clear()
                username.send_keys(TestVariables.test_username)
                email.send_keys(TestVariables.test_email)
                password.send_keys(TestVariables.test_password)
                confirm.send_keys(TestVariables.test_password)

                self.driver.find_element_by_id("register-btn").click()


        @classmethod
        def tearDownClass(inst):
            inst.driver.quit()


if __name__ == "__main__":
    unittest.main()
