import os
from setuptools import setup, find_packages

base_path = os.path.dirname(os.path.abspath(__file__))
# Parse README.rst for long_description
with open(os.path.join(base_path, 'README.rst')) as f:
    readme = f.read()

setup(
    name='cmd_utils',
    version='0.1.0', # TODO test, then 1.0?
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    description='Utilities for command line tools.',
    long_description=readme,
    url='https://github.com/connordelacruz/cmd-utils',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development',
        'Development Status :: 4 - Beta',
    ],
    packages=find_packages(),
    install_requires=[
        'blessings>=1.7,<1.8',
    ],
)
