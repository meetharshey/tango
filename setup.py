# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'tango',
    version = '0.0.1',
    author = 'meetHarsh, e',
    author_email = 'tango@gmail.com',
    license = 'MIT',
    description = 'Description',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/tango',
    py_modules = ['cli', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    entry_points = '''
        [console_scripts]
        tango=cli:cli
    '''
)