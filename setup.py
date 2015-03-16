from setuptools import setup, find_packages

setup(version='0.1',
      name='PyBattleShips',
      description='Python version of single-player BattleShips game',
      author='Georgi Georgiev',
      author_email='georgi.georgiev@flatrocktech.com',
      packages=find_packages(),
      test_suite="BattleShips.tests",
)