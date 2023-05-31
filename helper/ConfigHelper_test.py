import unittest
from helper import ConfigHelper

class TestConfigHelper(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.helper = ConfigHelper.ConfigHelper()

    def test_install_module(self):
        self.assertEqual(self.helper.install_python_module(["pip"]), None)

    def test_execute_sys_cmd(self):
        self.assertEqual(self.helper.execute_sys_cmd("ls -al > /dev/null"), 0)

    def test_set_default_project(self):
        gcp_project_id = "kunal-scratch"
        self.assertEqual(self.helper.set_default_project(gcp_project_id), 0)
        
if __name__ == '__main__':
    unittest.main()