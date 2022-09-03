from setuptools import setup, find_packages
from sys import platform

# read the contents of the README file
import os
from os import path

# function to recursively get files for resourcee
def package_files(directory):
    paths = []
    for (p, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", p, filename))
    return paths


# get all files recursively from /resources
data_files = package_files("./data")


setup(
    name="melbourne_comp90089_nlp",
    version="0.0.0.1",
    packages=find_packages(),
    install_requires=[
        # NOTE: spacy imports numpy to bootstrap its own setup.py in 2.3.2
        "medspacy==0.2.0.1"
    ],
    package_data={"melbourne_comp90089_nlp": data_files},
)