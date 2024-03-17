import sys,setuptools,os
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="xtelnet",
    version="2.2.6",
    author="AlaBouali",
    author_email="ala.bouali.1997@gmail.com",
    description="the best alternative to telnetlib as a telnet client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/xtelnet",
    packages=["xtelnet"],
    python_requires=">=2.7",
    install_requires=['PySocks'],
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
