import unittest
from helper import ConfigHelper

class TestConfigHelper(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.helper = ConfigHelper.ConfigHelper()

    # TODO: find an elegant way to run the auth test
    # def test_gcp_auth_user(self):
    #     self.assertEqual(self.helper.gcp_auth_user(), 0)

    def test_install_module(self):
        self.assertEqual(self.helper.install_python_module(["pip"]), None)

    def test_execute_sys_cmd(self):
        self.assertEqual(self.helper.execute_sys_cmd("ls -al > /dev/null"), 0)

    def test_set_default_project(self):
        gcp_project_id = "kunal-scratch 2>/dev/null"
        self.assertEqual(self.helper.set_default_project(gcp_project_id), 0)
    
    def test_load_config_file(self):
        self.assertEqual(self.helper.load_config_file("./config/example.env"), True)
        self.assertEqual(self.helper.load_config_file("./file-not-found/does-not-exist.env"), False)

if __name__ == '__main__':
    unittest.main()