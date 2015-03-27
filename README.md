Enhancement of Matrix Multiplication using Parallelization and Evolutionary Strategies
=======================================================================================

Project Summary
----------------------------------------

The purpose of this project is to study the common serial implementations of
matrix multiplication and to study the performance benefits of parallel and
approximate solutions. Matrix multiplication is a very well defined problem,
the results can be easily confirmed and benchmarked using a set of defined
matrices for all experiments.

The project utilizes the programming language Python and uses Numpy to perform
matrix operations. The software matrix multiplication algorithms developed
consist of parallel implementations of matrix multiplication algorithms
utilizing the CPU and GPU and approximate algorithms for performing matrix
multiplications generated using evolutionary strategies and evaluated within a
tolerance of error.


Getting Started
----------------------------------------

1.  In order to build the reports containing the results of this project please
    execute the Makefile in the **reports/** folder, by default this will
    generate all of the progress reports for this project.

2.  In order to execute the benchmarks and evaluate the various implementations of
    matrix multiplication you will need to execute the test framework in the 
    **codes/** folder. The test framework follows the instructions outlined in the
    **testplan.yml** document which specifies the tests to execute against the
    benchmark codes.

3.  In order to execute the test framework you will need to install the
    depenencies. Navigate to the **codes/** folder and then execute the setup
    script which the following command, this will install all needed dependencies. 

    `sudo python2 setup.py develop`  
  

4.  After installing the dependencies you can execute the test framework using
    the following command, if you want verbosity you can add the argument
    **--verbose**.

    `python2 test_framework.py --benchmarks=benchmarks testplan.yml`  
  

5.  If you would like to view the various matrix multiplication benchmarks
    you can see the implementations in the **benchmarks/** directory.


License
----------------------------------------

All of the source code in this repository, is licensed under the 
[GNU General Public License, Version 3](http://www.gnu.org/licenses/gpl.html)