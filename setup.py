from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mgen1/__init__.py
from mgen1 import __version__ as version

setup(
    name="mgen1",
    version=version,
    description="نظام إدارة الأعضاء والبطائق",
    author="Your Organization",
    author_email="your.email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
