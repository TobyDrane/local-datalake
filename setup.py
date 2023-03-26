from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="local-datalake",
    packages=find_packages(),
    long_description=open("README.md").read(),
)
