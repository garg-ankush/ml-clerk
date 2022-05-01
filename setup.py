from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ml-clerk",
    version="v1.0.0",
    author="Ankush Garg",
    author_email="unkushgarg@gmail.com",
    description="Module to record/document your model changes",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/unkush-garg/ml-clerk",
    packages=find_packages(),
    install_requires=[
        'numpy == 1.22.3',
        'pandas == 1.4.2',
        'pygsheets == 2.0.5',
        'python-dotenv == 0.20.0',
        'openpyxl == 3.0.9'
    ]
)
