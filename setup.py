from setuptools import setup, find_packages

setup(
    name="erasmus",
    version="0.0.1",
    description="Audio recording era estimation",
    author="David Su",
    packages=find_packages(),
    install_requires=[
        "librosa==0.5.0",
        "matplotlib==2.0.0"
    ]
)
