from setuptools import setup, find_packages

setup(
        name='jeff',
        version='v0.0.1',
        description='jeff wrapper for dynamic analysis containers',
        author='JeffJerseyCow',
        author_email='jeffjerseycow@gmail.com',
        url='https://github.com/JeffJerseyCow/jeff',
        packages=find_packages(),
        entry_points={'console_scripts':['jeff=jeff.jeffctl:main']},
)
