import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

version = "1.0.1"

setuptools.setup(
    name="gbstoolkit",
    version=version,
    author="LemmaEOF",
    # author_email= TODO: set up lemmaeof.gay email probs
    description="Various Python tools for messing around with GB Studio projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Fuck Around and Find Out License, version 0.2",
    url="https://github.com/LemmaEOF/GBSToolkit",
    project_urls={
        "Bug Tracker": "https://github.com/LemmaEOF/GBSToolkit/issues"
    },
    entry_points={
        "console_scripts": ["gbstoolkit = gbstoolkit:run_cli"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        # "License :: Fuck Around and Find Out License (FAFOL)",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Build Tools",
        "Typing :: Typed"
    ],
    packages=setuptools.find_packages(),
    python_requires=">3.6",
    install_requires=[
        "kdl-py"
    ]
)
