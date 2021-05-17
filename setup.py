import os
from setuptools import setup, find_packages

base_path = os.path.dirname(os.path.abspath(__file__))
# Parse README.rst for long_description
with open(os.path.join(base_path, 'README.rst')) as f:
    readme = f.read()

setup(
    name='cmd_utils',
    version='0.1.0',
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    description='Utilities for command line tools.',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        'blessings>=1.7,<1.8',
    ],
    # TODO: license, url, classifiers
)
