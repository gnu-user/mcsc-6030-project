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


Repository Layout
----------------------------------------

The following is a summary of the various source codes in the repository.

codes/
  - This contains the main code for the project, the soure files 
    setup.py and test_framework.py contain the code for installing the
    dependencies and executing the test framework to evaluate the benchmark
    impementations against the tests.
  - The testplans are YAML documents that end in .yml and contain the 
    descriptions of the test plans to execute, which describes how the
    benchmark codes are evaluated.

benchmarks/
  - This contains each of the matrix multiplication benchmark implementations
    these include the naive, baseline, parallel, and approximate implementations.
  - The helpers.py source file contains many useful helper functions which are
    common to each of the benchmark implemetations.

analysis/
  - This contains the R code that was used to analyze all of the test results
    and generate the tables and plots used for the final report.

reports/
  - Each of the reports for the project including the final report, use the provided
    Makefile to generate the PDF reports from the LaTeX source files.


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
    **--verbose**. As well, if you would like to save the results to a CSV file
    the argument **--save=<file>** can be used. Lastly, it is recommended that 
    you execute the simple test plan which requires much less time to complete
    than the complete test plan.

    `python2 test_framework.py --benchmarks=benchmarks simpleplan.yml`  
  

5.  If you would like to view the various matrix multiplication benchmarks
    you can see the implementations in the **benchmarks/** directory.


License
----------------------------------------

All of the source code in this repository, is licensed under the 
[GNU General Public License, Version 3](http://www.gnu.org/licenses/gpl.html)