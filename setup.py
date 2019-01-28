from jeff.utils import loadConfig
from setuptools import setup, find_packages

setup(
        name='jeff',
        version=loadConfig()['version'],
        description='jeff wrapper for dynamic analysis containers',
        author='JeffJerseyCow',
        author_email='jeffjerseycow@gmail.com',
        url='https://github.com/JeffJerseyCow/jeff',
        packages=find_packages(),
        entry_points={'console_scripts':['jeff=jeff.jeffctl:entryPoint']},
        include_package_data=True,
        package_data={'':['config/jeffconfig.json']},
)
