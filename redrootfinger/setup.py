from setuptools import setup, find_packages

setup(
    name="redrootfinger",
    version="0.2.0",
    author="Agampreet",
    description="Advanced web fingerprinting engine for RedRoot",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "colorama",
        "python-Wappalyzer",
        "lxml"
    ],
    entry_points={
        "console_scripts": [
            "redrootfinger=redrootfinger.cli:main"
        ]
    },
)
