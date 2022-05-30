from setuptools import setup, find_packages

setup(
    name="gradebook",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "gradebook = gradebook.gradebook_bootstrap:main",
        ],
    },
    install_requires=[
        "docopt",
    ],
)
