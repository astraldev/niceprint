from setuptools import setup
import pathlib
import os

here = pathlib.Path(__file__).parent
os.chdir(here)
setup(
  name="niceprint",
  version="3.3.0",
  license="MIT",
  url="https://niceprint.readthedocs.io/en/latest/",
  description="A minute package for formating output",
  long_description=str(open('README.md').read()),
  long_description_content_type="text/markdown",
  author="AstralDev",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3.7",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License"
  ],
  author_email="ekureedem480@gmail.com",
  python_requires='>=3',
  py_modules=["niceprint"]
)
