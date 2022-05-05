import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="planarfibers",
    version="0.0.1",
    author="Julian Karl Bauer",
    author_email="juliankarlbauer@gmx.de",
    description="PlanarFibers "
    "contains selected contributions of "
    "Bauer, Julian Karl, and Thomas Böhlke. "
    "'On the dependence of orientation averaging mean field homogenization on planar fourth-order fiber orientation tensors.'"
    " Mechanics of Materials (2022): 104307.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JulianKarlBauer/orientation_averaging_mean_field",
    packages=["planarfibers"],
    package_dir={"planarfibers": "planarfibers"},
    install_requires=[
        "numpy",
        "scipy",
        "sympy",
        "pandas",
        "matplotlib",  # Required for examples
        "mechmean",
        "mechkit",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)


