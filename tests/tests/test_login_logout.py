import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tests.settings import TestVariables

class LoginLogoutTest(unittest.TestCase):

    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.get("http://localhost:5555")
        inst.driver.maximize_window()
        inst.login_url = 'http://localhost:5555/login'
        inst.home_url = 'http://localhost:5555/home'
        inst.create_url = 'http://localhost:5555/create'

    def test_login(self):
        print('testing login')
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
        Try to access Create Character page - should pass
        '''
        self.driver.find_element_by_id("nav-to-create").click()
        self.assertTrue(self.driver.current_url == self.create_url)


    def test_logout(self):
        print('testing logout')
        try:
            '''
            Check if user is logged in, then log out
            '''
            elem = self.driver.find_element_by_id("account-dropdown")
            self.driver.find_element_by_id("account-dropdown").click()
            time.sleep(1)
            self.driver.find_element_by_id("account-logout-ddbtn").click()

        except:
            '''
            If user is logged out, then log in and log out
            '''
            self.driver.get(login_url)
            email = self.driver.find_element_by_id("email_field")
            email.send_keys("TestVariables.test_email")
            password_elem = self.driver.find_element_by_id("password_field")
            password_elem.send_keys("TestVariables.test_password")
            self.driver.find_element_by_id("login-btn").click()
            self.assertTrue(self.driver.current_url == self.home_url)
            self.driver.find_element_by_id("account-dropdown").click()
            time.sleep(1)
            self.driver.find_element_by_id("account-logout-ddbtn").click()

        '''
        Try to access Create Character page - should fail
        '''
        self.driver.find_element_by_id("nav-to-create").click()
        self.assertFalse(self.driver.current_url == self.create_url)



    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()

if __name__ == "__main__":
    unittest.main()
