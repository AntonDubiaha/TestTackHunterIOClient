"""This script is used to install the TestTaskClientandService package."""

from setuptools import find_packages, setup

setup(
    name='TestTaskClientandService',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
