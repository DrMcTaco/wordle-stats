#!/usr/bin/env python

from setuptools import setup

required = ["tweepy", "loguru"]
extras = {
    "dev": ["black", "pre-commit", "ipdb"],
    "tests": ["pytest>=5.0", "pytest-mock"],
}

setup(
    name="wordle-stats",
    description="__DESCRIPTION__",
    author="Dan Rubin",
    author_email="dmrubin3@gmail.com",
    python_requires=">=3.6",
    install_requires=required,
    extras_require=extras,
    include_package_data=True,
)
