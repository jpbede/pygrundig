from setuptools import setup

setup(
    name='pygrundig',
    version='0.0.1',
    packages=['pygrundig'],
    url='https://github.com/jpbede/pygrundig',
    license='MIT',
    author='Jan-Philipp Benecke',
    author_email='jan-philipp.benecke@jpbe.de',
    description='Python library for controlling grundig smart tv\'s',
    install_requires=["requests", "enum34"]
)
