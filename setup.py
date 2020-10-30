import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blessedui",
    license="LGPLv3",
    version="0.0.1",
    author="Giacomo Furlan",
    author_email="opensource@giacomofurlan.name",
    description="Graphic library based on blessed to create CLI interfaces at ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elegos/python-blessedui",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=[
        'blessed>=1.17.11'
    ],
    python_requires='>=3.6',
)
