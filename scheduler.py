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
        for b in range(a, len(literals)):
            clauses.append([-literals[a], -literals[b]])

    return clauses

def atMostTwo(literals):
    clauses = []
    
    for a in range(len(literals)):
        for b in range(a, len(literals)):
            for c in range(b, len(literals)):
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