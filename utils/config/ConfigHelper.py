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
        print(exec_cmd)
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

        return load_dotenv(dotenv_path=filename, verbose=True, override=False)
          
    def restart_kernel(self):
        """restart_kernel

        Restart the Jupyter (Python) kernel
        """
        os._exit(00)

        return
    
    def install_dependencies(self):
        """install_dependencies

        Install all the python dependencies configured using PYTHON_MODULES
        """
        import json
        # load the dependencies as JSON object
        PYTHON_MODULES = json.loads(os.getenv("PYTHON_MODULES"))

        self.install_python_module(PYTHON_MODULES)
        return 
    
    def create_pipeline_root(self):
        """create_pipeline_root

        Create a GCS bucket to store artefacts created by the pipeline.
        env variable PIPELINE_ROOT is used to specify this bucket
        """
        from google.cloud import storage
        from google.cloud import exceptions as gcp_exceptions
        PIPELINE_ROOT = os.getenv("PIPELINE_ROOT")
        PROJECT_ID = os.getenv("PROJECT_ID")
        storage_client = storage.Client(project=PROJECT_ID) # Create a storage client

        bucket_name = PIPELINE_ROOT.strip("gs://").split("/")[0] # Get the bucket name only if folders exists
        bucket = storage.Bucket(client=storage_client, name=bucket_name, user_project=PROJECT_ID)
        if bucket.exists():
            print(f"Bucket [{bucket_name}] exists")
        else:
            storage_client.create_bucket(bucket_or_name=bucket_name, project=PROJECT_ID)
            print(f"Bucket [{bucket_name}] doesn't exist. Created it")
        # creating required folders
        _bucket_name = "gs://" + bucket_name + "/"
        required_folders = PIPELINE_ROOT[len(_bucket_name):]
        if not required_folders.endswith("/"):
            required_folders = required_folders + "/"
        if bucket.get_blob(required_folders) is not None:
            # folder exists
            print(f"Folder [{required_folders}] exists")
        else:
            # create folder
            bucket.blob(blob_name=required_folders).upload_from_string("")
            print(f"Folder [{required_folders}] created")
        return