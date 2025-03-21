#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Setup
Package setup script
"""

from setuptools import setup, find_packages

# Import version from package
from src.graphreporter import __version__

# Package description
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

# Package requirements
requirements = [
    "msal>=1.20.0,<2.0.0",
    "requests>=2.28.0,<3.0.0",
    "pandas>=1.5.0,<2.0.0",
    "typer>=0.7.0,<0.8.0",
    "pydantic>=1.10.0,<2.0.0",
    "python-dotenv>=0.21.0,<0.22.0",
    "openpyxl>=3.0.10,<3.1.0",
    "rich>=12.6.0,<13.0.0",
]

# Development requirements
dev_requirements = [
    "pytest>=7.0.0,<8.0.0",
    "pytest-cov>=4.0.0,<5.0.0",
    "black>=23.0.0,<24.0.0",
    "isort>=5.10.0,<6.0.0",
    "flake8>=5.0.0,<6.0.0",
]

setup(
    name="graphreporter",
    version=__version__,
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python CLI tool for retrieving and reporting Microsoft Entra ID data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/graphreporter",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "graphreporter=graphreporter.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
) 