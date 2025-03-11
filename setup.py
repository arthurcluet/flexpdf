from setuptools import setup, find_packages

setup(
    name="flexpdf",
    version="0.1.0",
    description="A component-based library for building structured PDFs with ReportLab",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "reportlab",
    ],
)
