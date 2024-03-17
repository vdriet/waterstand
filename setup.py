""" setup voor package waterstand """
from setuptools import setup

setup(
    name='waterstand',
    version='0.0.1',
    description='package voor ophalen waterstand',
    packages=['.'],
    licence='GPL-3.0',
    author='Peter van de Riet',
    author_email='vdriet@gmail.com',
    keywords=['waterstand rws rijkswaterstaat'],
    url='https://github.com/vdriet/waterstand',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
)
