from setuptools import setup, find_packages

setup(
    name='localistico',
    version=0.1,
    packages=find_packages('localistico', exclude=('tests',)),
    include_package_data=True,
)
