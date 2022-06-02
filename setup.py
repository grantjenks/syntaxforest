import pathlib
import re
import setuptools

init = (pathlib.Path('syntaxforest') / '__init__.py').read_text()
match = re.search(r"^__version__ = '(.+)'$", init, re.MULTILINE)
version = match.group(1)

with open('README.rst') as reader:
    readme = reader.read()

setuptools.setup(
    name='syntaxforest',
    version=version,
    description='Syntax Forest',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='https://github.com/grantjenks/syntaxforest',
    license='Apache 2.0',
    packages=['syntaxforest'],
    install_requires=[
        'Django==3.2.*',
        'lxml',
        'modelqueue',
        'pygments',
        'tree-sitter-languages',
    ],
    project_urls={
        'Documentation': 'https://syntaxforest.com',
        'Source': 'https://github.com/grantjenks/syntaxforest',
        'Tracker': 'https://github.com/grantjenks/syntaxforest/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
