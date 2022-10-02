from setuptools import find_packages, setup

setup(
  name='remote_donation',
  version='1.0.0',
  packages=find_packages(
    exclude=['tests', 'tests.*', '*.tests', '*.tests.*', 'pipenv', 'env']
  )
)
