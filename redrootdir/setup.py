from setuptools import setup, find_packages

setup(
    name="redrootdir",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "redrootdir=redrootdir.scanner_core:main"
        ]
    },
)
