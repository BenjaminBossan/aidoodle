import os

from setuptools import setup, find_packages


with open('VERSION', 'r') as f:
    version = f.read().rstrip()

install_requires = []

tests_require = [
    'pytest',
    'pytest-cov',
]

docs_require = []


README = ''
CHANGES = ''

setup(
    name='aidoodle',
    version=version,
    description='',
    long_description=README,
    license='new BSD 3-Clause',
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/BenjaminBossan/aidoodle",
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
        'docs': docs_require,
    },
)