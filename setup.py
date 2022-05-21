import pathlib
import re
import setuptools

init = (pathlib.Path('tree_sitter_server') / '__init__.py').read_text()
match = re.search(r"^__version__ = '(.+)'$", init, re.MULTILINE)
version = match.group(1)

with open('README.rst') as reader:
    readme = reader.read()

setuptools.setup(
    name='tree_sitter_server',
    version=version,
    description='Tree sitter query server.',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='https://github.com/grantjenks/tree-sitter-server',
    license='Apache 2.0',
    packages=['tree_sitter_server'],
    install_requires=[
        'Django==3.2.*',
        'tree-sitter-languages',
    ],
    project_urls={
        'Documentation': 'https://github.com/grantjenks/tree-sitter-server',
        'Source': 'https://github.com/grantjenks/tree-sitter-server',
        'Tracker': 'https://github.com/grantjenks/tree-sitter-server/issues',
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
