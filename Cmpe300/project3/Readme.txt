# Knight's Tour Project

## Overview
This project implements algorithms to solve the Knight's Tour problem on an 8x8 chessboard. It includes two approaches: a purely random approach and a combination of random moves followed by a backtracking algorithm.

## Part 1: Random Approach
The knight moves randomly from a starting position, aiming to cover more than a specified percentage of the board.

## Part 2: Random + Backtracking
The knight starts with k random moves, then uses backtracking to complete the tour, targeting more than p percent of the board.

### Requirements
Python 3.x

### Running the Program
Execute the script with the following command:
```
python main.py [partName]
```
where partName is either "part1" or "part2".

### Output
The program outputs the success rate and success probability of the algorithms.