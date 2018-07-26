import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="foodlog",
    version="0.1.0",
    author="Hal Peterson",
    author_email="vobine@gmail.com",
    description="Food/diet/lifestyle logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vobine/foodlog",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=(
        "Flask",
    ),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: ",
        "Operating System :: OS Independent",
    ),
)
