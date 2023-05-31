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