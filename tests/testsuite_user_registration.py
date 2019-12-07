import unittest
from tests.test_register_user import RegisterTest
from tests.test_login_logout import LoginLogoutTest
from tests.test_delete_user import DeleteUserTest

register_test = unittest.TestLoader().loadTestsFromTestCase(RegisterTest)
login_logout_test = unittest.TestLoader().loadTestsFromTestCase(LoginLogoutTest)
delete_user_test = unittest.TestLoader().loadTestsFromTestCase(DeleteUserTest)

test_suite = unittest.TestSuite([register_test, login_logout_test, delete_user_test])

unittest.TextTestRunner(verbosity=2).run(test_suite)
