"""Package Setup for syntaxforest
"""

import pathlib
import re
import setuptools

from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox

        errno = tox.cmdline(self.test_args)
        exit(errno)


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
    tests_require=['tox'],
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
    cmdclass={'test': Tox},
)
