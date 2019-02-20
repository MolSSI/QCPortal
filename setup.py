"""
QCPortal
A client interface to the QC Archive Project
"""
from setuptools import setup, find_packages
import versioneer

DOCLINES = __doc__.split("\n")

setup(
    # Self-descriptive entries which should always be present
    name='qcportal',
    author='MolSSI',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='BSD-3-Clause',
    # Which Python importable modules should be included when your package is installed
    packages=find_packages(),

    install_requires=[
        'numpy>=1.7',
        'pandas',
        'requests',
        'pydantic>=0.19',
        'qcelemental>=0.2.6'
    ],

    tests_require=[
        'pytest',
        'pytest-cov',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ],

    # Manual control if final package is compressible or not, set False to prevent the .egg from being made
    zip_safe=True,
)
