# -*- coding: utf-8 -*-
"""Utilities to configure ML pipelines

A collection of helper functions to configure
ML pipelines in GCP.
"""

import os
import sys
import subprocess

class ConfigHelper:

    def install_python_module(self, python_modules: list):
        # install provided list of python modules
        """install_python_module

        python_modules can be of list of two types:  
        1. String representing module name, or
        2. Dictionary of sub type {'name': module-name, 'version': version-number}
        """
        for python_module in python_modules:
            if type(python_module) is not dict:
                self.execute_py_cmd(f"-m pip install --upgrade {python_module}")
            else:
                self.execute_py_cmd(f"-m pip install --upgrade {python_module['name']}=={python_module['version']}")
        return

    def execute_py_cmd(self, command: str):
        """execute_py_cmd

        Execute a command to be interpreted by python
        """
        exec_cmd = [sys.executable]
        for each_arg in command.split(" "):
            exec_cmd.append(each_arg)
        return subprocess.check_call(exec_cmd)
    
    def execute_sys_cmd(self, command: str):
        """execute_sys_cmd

        Execute a system command
        """
        return subprocess.call(command, shell=True)

    def set_default_project(self, project_id: str):
        # set a default project in GCP
        """set_default_project

        Set a default project in GCP
        """
        
        return self.execute_sys_cmd(f"gcloud config set project {project_id}")
    
    def gcp_auth_user(self):
        # auth the user for google platform
        """gcp_auth_user

        Simple utility to authenticate the user.  
        It will launch a browser which will manage the auth flow.
        If browser is not available it will print the URL to stdout.
        """        
        return self.execute_sys_cmd("gcloud auth login --launch-browser")
    
    def load_config_file(self, filename):
        """load_config_file

        Loads the configuration info as variables.  
        filename defaults to '.env'
        """
        self.install_python_module(["python-dotenv"])
        from dotenv import load_dotenv

        return load_dotenv(dotenv_path=filename)
    
    def restart_kernel(self):
        os._exit(00)

        return