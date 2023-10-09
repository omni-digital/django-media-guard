#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="django-media-guard",
    version="0.1.1",
    description="""""",
    author="Omni Digital",
    author_email="engineering@omni-digital.co.uk",
    url="https://github.com/omni-digital/django-media-guard",
    packages=find_packages(exclude=["example", "tests"]),
    include_package_data=True,
    install_requires=["Django>=1.11,<3.3"],
    license="MIT",
    zip_safe=False,
    keywords=["django", "media", "guard", "protect"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
