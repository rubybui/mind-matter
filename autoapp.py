# -*- coding: utf-8 -*-
"""Create an application instance."""
import sys
import os
from mind_matter_api.app import create_app


def configure_python_path():
    # Dynamically add the 'generated' directory to sys.path
    grpc_generated_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated")
    if grpc_generated_file_path not in sys.path:
        sys.path.insert(0, grpc_generated_file_path)
        print(f"Added '{grpc_generated_file_path}' to PYTHONPATH")


configure_python_path() 
app = create_app()
