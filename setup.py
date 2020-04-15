import sys,setuptools,os
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="xtelnet",
    version="1.2.7",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    description="simple telnet module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/xtelnet",
    packages=["xtelnet"],
    python_requires=">=2.7",
    install_requires=[],
    license="MIT License",
    entry_points={
       'console_scripts': [
           'xtelnet = xtelnet.__main__:run',
       ],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License ",
    ],
)
