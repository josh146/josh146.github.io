Hello world
##############

:subtitle: a smaller subtitle
:date: 2014-03-05 13:52
:timezone: +0700
:tags: helloworld, blog, first, first
:category: Testing
:author: Josh Izaac

Testing some latex:

* Inline latex: $x^2=\\sin(\\theta)$
* Non-inline latex: $$ \\int_0^1 x^2 dx $$
* An align env:

\\begin{align}
\\int_0^1 x^2 dx
\\end{align}

Pygments
=========

Some inline code to run an mpi based program is ``mpirun -np 2 python --help``. Now for some codeblocks:

.. code-block:: python

    >>> # list unpacking
    >>> l = [[5,2,1],[4,3],[2,3,4],[2]]
    >>> [item for sublist in l for item in sublist]


some fortran code:

.. code-block:: fortran

    program main
        implicit none

        integer :: i,j

        ! a loop
        do i=1, 10
            write(*,*)i**2.d0
        enddo
    end program main


some Bash code:

.. code-block:: bash
    :linenos: inline

    fd = ($(echo *.py))
    for i in {1..10};
    do;
    echo $i;
    done

#. An `internal link <{filename}/pages/about.rst>`_
#. An `external link <http://bbc.com/news>`_


An image:

.. embedly-card:: https://lh5.googleusercontent.com/n7iY8f5n8qJcZraH3bvRJdpdZiYlsT_wU5ZZznpKIxHU=w1351-h901-no
    :card-chrome: 0

.. embedly-card:: https://plus.google.com/photos/107452285898786120113/albums/5964705002702996625

Embedding an article:

.. embedly-card:: http://physics.stackexchange.com/questions/5265/cooling-a-cup-of-coffee-with-help-of-a-spoon
    :card-chrome: 0
