#!/usr/bin/python

import argparse
parser = argparse.ArgumentParser(description="Solve the 36 cube puzzle")
parser.add_argument("-a", "--all", dest="PRINT_ALL", action="store_true", help="print all solutions")
parser.add_argument("-t", "--trick", dest="FORCE_TRICK", action="store_true", help="use trick positioning of 1,2 and 3,2")
parser.add_argument("-u", "--unique", dest="UNIQUE", action="store_true", help="use an arbitrary coloring of first row to only show unique solutions")
args = parser.parse_args();

PRINT_ALL = args.PRINT_ALL
FORCE_TRICK = args.FORCE_TRICK
UNIQUE = args.UNIQUE

# lookup of color symbols by bit-mask value
COLORS = dict(zip((1 << i for i in range(6)), ('P','Y','O','B','R','G')))
COLORS[False] = 'X'

if FORCE_TRICK:
 # definition of the base heights with (1,2) and (3,2) switched for special towers
 cube = ((1,3,4,5,2,0),
         (2,5,1,4,1,3),
         (0,1,3,2,5,4),
         (5,4,0,3,0,2),
         (4,2,5,0,3,1),
         (3,0,2,1,4,5))
else:
 cube = ((1,3,4,5,2,0),
         (2,5,0,4,1,3),
         (0,1,3,2,5,4),
         (5,4,1,3,0,2),
         (4,2,5,0,3,1),
         (3,0,2,1,4,5))


def test_color(pos, solution, used_towers, color, size):
 """
 Test if the given color is valid for the given position in the solution 
 Used towers is an array of the towers by tower height, each element is a bitmask of the used colors of that height in solution
 Size should be equivalent to cube[pos/6][pos%6]
 """
 #check if tower of this size and color has already been used
 if color & used_towers[size]:
  return False
 #check if tower has already been used in row or column:
 for i in range(6):
  if color == solution[pos/6][i]: return False
  if color == solution[i][pos%6]: return False
 # special conditions for the two special towers
 if FORCE_TRICK and (pos/6, pos%6) == (1,2) and color != 2: return False
 if FORCE_TRICK and (pos/6, pos%6) == (3,2) and color != 4: return False
 #PYOBRG - force color ordering for first row (colors are interchangable except yellow & orange)
 if UNIQUE:
  if pos == 0 and color != 1 : return False
  if pos == 1 and not (color == 2 or color == 4): return False
  if pos == 2 and color != 8 : return False
  if pos == 3 and not (color == 2 or color == 4): return False
  if pos == 4 and color != 16: return False
  if pos == 5 and color != 32: return False
 return True

def print_solution(solution):
 """
 Print the given solution grid.
 """
 for i in range(6):
  print zip((COLORS[c] for c in solution[i]), (6 - s for s in cube[i]))

def solve(pos, solution, used_towers, best):
 """
 Recursively improve the given solution starting at the given position.
 Prints improved solutions only if they are better than <best> placed towers.
 """
 if pos == 36: return best, solution # completed search of all 36 positions
 size = cube[pos/6][pos%6] # get the size of the base at this position
 # test each color for if the tower of color,size is unused and if it doesn't violate placement rules
 for i in range(6):
  color = 1 << i
  if test_color(pos, solution, used_towers, color, size):
   # mark tower of color+size as used and place it in solution
   used_towers[size] = used_towers[size] | color
   solution[pos/6][pos%6] = color
   # track the best solution to date, printing as we find better solutions
   if pos > best or pos == 35:
    print "#######", pos + 1, "towers placed"
    print_solution(solution)
    best = pos
   # recursively try to improve upon solution
   best, solution = solve(pos+1, solution, used_towers, best)
   # short circuit any more recursion once we hit 36 towers
   if best >= 35 and not PRINT_ALL:
    return best, solution
   # unset the test color from solution and used_towers we un-recurse
   solution[pos/6][pos%6] = False
   used_towers[size] = used_towers[size] ^ color
 return best, solution

#
# MAIN
#

# initial empty solution to start solving procedure
solution = [[False for x in range(6)] for x in range(6)]
# used_towers is size-6 array of int, each value [i] represents used towers of height i as a a bitmask of tower colors
used_towers = [0 for i in range(6)]

solve(0, solution, used_towers, -1)
