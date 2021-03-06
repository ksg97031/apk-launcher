import sys
import setuptools
import os


if sys.version_info < (3,6):
    print("Unfortunately, your python version is not supported!\n"
          + "Please upgrade at least to Python 3.6!")
    sys.exit(1)

if os.name == 'nt':
    print("Unfortunately, windows platform is not supported!\n")
    sys.exit(1)

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apk-launcher",
    python_requires='>=3',
    version="1.0.0",
    author="ksg97031",
    author_email="ksg97031@gmail.com",
    description="Easy to handle your apk",
    install_requires=['androguard', 'adb', 'click', 'rsa'],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ksg97031/apk-launcher",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'apk-launcher = scripts.main:run'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
