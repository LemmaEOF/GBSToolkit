import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="GBSToolkit",
    version="0.1.0",
    author="LemmaEOF",
    # author_email= TODO: set up lemmaeof.gay email probs
    description="Various Python tools for messing around with GB Studio projects.",
    long_description=long_description,
    license="Fuck Around and Find Out License, version 0.2",
    url="https://github.com/LemmaEOF/GBSToolkit",
    project_urls={
        "Bug Tracker": "https://github.com/LemmaEOF/GBSToolkit/issues"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Fuck Around and Find Out License (FAFOL)",
        "License :: Other/Proprietary License (FAFOL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Build Tools",
        "Typing :: Typed"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">3.6",
    install_requires=[
        "kdl-py"
    ]
)