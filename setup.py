from setuptools import setup, find_packages
import codecs

# Read the README file with proper encoding
with codecs.open("README.md", "r", "utf-8") as fh:
    long_description = fh.read()

setup(
    name="devtracker-cli",
    version="0.1.0",
    packages=["devtracker_cli"],
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devtracker=devtracker_cli.cli:cli",
        ],
    },
    author="Aswin M S",
    author_email="deto2026@gmail.com",
    description="A command-line tool to track development time and breaks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aswinms926/devtracker-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 