import setuptools
import os

VERSION = '0.1.7'

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="qdata",
    version=VERSION,
    description="Python SDK for getting data quickly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/longxiaofei/spider-BaiduIndex",
    author="longxiaofei",
    author_email="libra.19951002@gmail.com",
    packages=setuptools.find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*", "test.py"]
    ),
    install_requires=[
        "requests>=2.19.1",
        "matplotlib>=3.3.4",
        "pycryptodome>=3.10.1"
    ],
    # entry_points={
    #     'console_scripts': [
    #         'tobe=tobe:main'
    #     ],
    # },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python",
    ],
    keywords='data sdk',
    include_package_data=True
)
