import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tests.settings import TestVariables

class DeleteUserTest(unittest.TestCase):

    @classmethod
    def setUpClass(inst):
        print('testing user deletion')
        inst.driver = webdriver.Firefox()
        inst.driver.get("http://localhost:5555")
        inst.driver.maximize_window()
        inst.login_url = 'http://localhost:5555/login'


    def test_delete_user(self):

        try:
            '''
            Check if user is logged in
            '''
            elem = self.driver.find_element_by_id("account-dropdown")

        except:
            '''
            If user is not logged in, then log in
            '''
            self.driver.get(self.login_url)
            email = self.driver.find_element_by_id("email_field")
            email.clear()
            email.send_keys(TestVariables.test_email)
            password = self.driver.find_element_by_id("password_field")
            password.clear()
            password.send_keys(TestVariables.test_password)
            self.driver.find_element_by_id("login-btn").click()

            '''
            Delete user
            '''
            self.driver.find_element_by_id('account-dropdown').click()
            self.driver.find_element_by_id('account-ddbtn').click()
            self.driver.find_element_by_id('delete-btn').click()
            self.driver.find_element_by_id('confirm-delete').click()


    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()

if __name__ == "__main__":
    unittest.main()
