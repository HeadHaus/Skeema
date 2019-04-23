"""
Setup

"""

from setuptools import setup
from os import path

from setup.common import (
    get_long_description
)

current_directory = path.abspath(path.dirname(__file__))

setup(
    name='skeema',
    version='0.0.1',
    description=get_long_description(current_directory),

    packages=[
        'skeema.core',
        'skeema.dependency'
    ],
    include_package_data=True
)
