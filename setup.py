from setuptools import setup, find_packages
import re
import os


READMEFILE = 'README.rst'
VERSIONFILE = os.path.join('eugene', '__init__.py')
VSRE = r"""^__version__ = ['"]([^'"]*)['"]"""


def get_version():
    verstrline = open(VERSIONFILE, 'rt').read()
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError(
            'Unable to find version string in {0}.'.format(VERSIONFILE))


setup(
    name='eugene',
    version=get_version(),
    author='Will Kahn-Greene',
    author_email='willg@bluesock.org',
    description='HTML web app for simulating a ship-to-ship comms system',
    long_description=open(READMEFILE).read(),
    license='MIT',
    url='https://github.com/willkg/eugene/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # TODO
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License'
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        ]
)
