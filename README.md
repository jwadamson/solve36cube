solve36cube
===========

Script which solves the 36 cube 3d puzzle. Based on the work of Daniel Hepper 
http://daniel.hepper.net/blog/2010/01/how-to-solve-the-36-cube-puzzle/

Allows for options like trying to brute-force a solution using the "obvious" restrictions or with the trick.
Can also print all solutions instead of just the first one found.

usage: solve36cube.py [-h] [-a] [-t] [-u]

Solve the 36 cube puzzle

optional arguments:
  -h, --help    show this help message and exit
  -a, --all     print all solutions
  -t, --trick   use trick positioning of 1,2 and 3,2
  -u, --unique  use an arbitrary coloring of first row to only show unique
                solutions
