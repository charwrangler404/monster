from setuptools import find_packages, setup

setup(
    name="monster",
    packages=find_packages(include=['monster']),
    version="0.1.0",
    description="Library for tracking tabletop gaming monsters in python",
    author="phrequency-navigator",
    license="MIT",
    requires=['pytest-runner', 'random', 'json'],
)