from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="markdown_translator",
    version="0.1.0",
    author="Your Name / Project Team",
    author_email="your.email@example.com",
    description="Tool to translate Markdown files using LLM APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="URL to project repo subsection if applicable",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Choose appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mdtranslate=src.cli:main",
        ],
    },
) 