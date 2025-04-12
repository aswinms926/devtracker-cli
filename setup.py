from setuptools import setup, find_packages

setup(
    name="devtracker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devtracker=devtracker.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line tool for tracking development time",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/devtracker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 