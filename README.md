# Sports Tournament Scheduling

This is a homework solution for course NAIL062 at MFF UK.

The goal is to find a solution (or show that there is none) for the [Sports Tournament Scheduling](https://www.csplib.org/Problems/prob026/) problem by encoding it to CNF and solving the formula with a SAT solver.

# Documentation

## Problem description

The problem is to schedule a tournament of $n$ teams over $n-1$ weeks, with each week divided into $n/2$ periods, and each period divided into two slots. The first team in each slot plays at home, whilst the second plays the first team away. A tournament must satisfy the following three constraints:

- every team plays once a week,
- every team plays at most twice in the same period over the tournament,
- every team plays every other team.

An example schedule for 8 teams is:

|              | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 | Week 7 |
|--------------|--------|--------|--------|--------|--------|--------|--------|
| **Period 1** | 0 v 1  | 0 v 2  | 4 v 7  | 3 v 6  | 3 v 7  | 1 v 5  | 2 v 4  |
| **Period 2** | 2 v 3  | 1 v 7  | 0 v 3  | 5 v 7  | 1 v 4  | 0 v 6  | 5 v 6  |
| **Period 3** | 4 v 5  | 3 v 5  | 1 v 6  | 0 v 4  | 2 v 6  | 2 v 7  | 0 v 7  |
| **Period 4** | 6 v 7  | 4 v 6  | 2 v 5  | 1 v 2  | 0 v 5  | 3 v 4  | 1 v 3  |

## Encoding

The problem is encoded using a single set of variables. Variable encoded with parameters $Plays(t, w, p)$ represents that team **t** plays in week **w** and period **p**.

Function encode (and eventually decode the other way around) handles the linear encoding.

We use the following constraints:

- Every team plays exactly once a week

    $\neg Plays(t,w,p_1) \vee \neg Plays(t,w,p_2)$ for each $t$ and $w$ ensures that a team plays at most once a week.

    To make sure it plays at least once, we add one clause containing the literals $Plays(t,w,p)$ for all periods $p$, for each team and week.

- Every team plays at most twice in the same period

    $\neg Plays(t,w_1,p) \vee \neg Plays(t,w_2,p) \vee \neg Plays(t,w_3,p)$ for each $t$ and $p$.

- Exactly two teams play in each match

    $\neg Plays(t_1,w,p) \vee \neg Plays(t_2,w,p) \vee \neg Plays(t_3,w,p)$ for each $w$ and $p$ ensures that at most two teams play in a match.

    To make sure that at least two teams play, we add, for each team $t'$, a clause containing the literals $Plays(t,w,p)$ of all the other teams $t \neq t'$.

- Every two teams meet exactly once

    The number of unique pairs of teams is exactly the same as the number of scheduled matches. Therefore, we do not need to ensure that every two teams meet at least once.

    It is enough to require that every two teams meet at most once, and then every pair will meet exactly once.

## User documentation

Basic usage:

```
scheduler.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The number of teams playing (should be even).
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
* `-v {0,1}`, `--verb {0,1}` : Verbosity of the SAT solver used.

Example:
```
python3 scheduler.py -i 6
```

The program first prints the raw output of the SAT solver. If the formula is satisfiable, it also prints the tournament schedule as a table with one row per period and one column per week - teams are indexed from 0. 

Each cell contains the two teams playing a certain match:

```
0 v 1 | 3 v 2 | ...
2 v 5 | 1 v 4 | ...
...
```

If the formula is not satisfiable, only the solver output is printed.
