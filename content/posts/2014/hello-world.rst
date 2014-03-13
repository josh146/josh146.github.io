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

    .. image:: {filename}/images/thesis.png
        :scale: 10 %

