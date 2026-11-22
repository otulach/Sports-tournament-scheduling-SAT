import subprocess

def getInput():
    try:
        print("Write the amount of teams playing (single integer > 1).")
        n = int(input()) 
        return n
    except:
        print("Invalid input format.")

def encode(team, week, period, n):
    return team * (n -1) * (n//2) + week * (n//2) + period + 1

def decode(code, n):
    return code // ((n-1) * (n//2)), (code // (n//2)) % (n-1), code % (n//2)

def excactlyOne(literals):
    clauses = [literals]

    for a in range(len(literals)):
        for b in range(a + 1, len(literals)):
            clauses.append([-literals[a], -literals[b]])

    return clauses

def atMostTwo(literals):
    clauses = []
    
    for a in range(len(literals)):
        for b in range(a + 1, len(literals)):
            for c in range(b + 1, len(literals)):
                clauses.append([-literals[a], -literals[b], -literals[c]])

    return clauses

def excacltyTwo(literals):
    clauses = atMostTwo(literals)

    for a in range(len(literals)):
        clauses.append([literals[:a] + literals[a+1:]])

    return clauses

def createCNF(n):
    teams = range(n)
    weeks = range(n-1)
    periods = range(n//2)
    cnf = []

    # Every team plays once a week
    for t in teams:
        for w in weeks:
            teamPlayingThisWeek =[]
            for p in periods:
                teamPlayingThisWeek.append(encode(t, w, p, n))
            cnf += excactlyOne(teamPlayingThisWeek)

    # Every team plays at most twice a period
    for t in teams:
        for p in periods:
            playedThisPeriod =[]
            for w in weeks:
                playedThisPeriod.append(encode(t, w, p, n))
            cnf += atMostTwo(playedThisPeriod)

    # Exactly two teams in each match
    for w in weeks:
        for p in periods:
            teamsInMatch = []
            for t in teams:
                teamsInMatch.append(encode(t, w, p, n))
            cnf += excacltyTwo(teamsInMatch)

    # Every team plays every other team
    # The teams should meet atleast once, since the amount of matches is n * (n-1) /2. Therefore adding "at most twice" should be sufficient.
    for a in range(len(teams)):
        for b in range(a + 1, len(teams)):
            for i in range(len(weeks)):
                for j in range(i + 1, len(weeks)):
                    for k in range(len(periods)):
                        for l in range(len(periods)):
                            meetAtMostTwice = [-encode(teams[a], weeks[i], periods[k], n), -encode(teams[b], weeks[i], periods[k], n), 
                                               -encode(teams[a], weeks[j], periods[l], n), -encode(teams[b], weeks[j], periods[l], n)]
                            cnf.append(meetAtMostTwice)

    return cnf

def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    # print CNF into formula.cnf in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    # call the solver and return the output
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity) , output_name], stdout=subprocess.PIPE)

def print_result(result):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

