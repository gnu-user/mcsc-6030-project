from setuptools import setup


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='Enhancement of Matrix Multiplication',
    version="0.0.1",
    description='''
    Research project to evaluate strategies for the enhancement of matrix
    multiplcation using parallelization and evolutionary strategies.
    ''',
    long_description=read('README.md'),
    author='Jonathan Gillett',
    author_email='jonathan.gillett@uoit.ca',
    url='https://bitbucket.org/gnu-user/mcsc-6030-projecct',
    install_requires=[
        'docopt',
        'schema',
        'pyyaml',
        'clint',
        'tabulate',
        'numpy',
        'scipy',
        'mpi4py'
    ],
    license=read('LICENSE'),
    keywords='matrix multiplication, evolutionary strategies, parallelization'
)
