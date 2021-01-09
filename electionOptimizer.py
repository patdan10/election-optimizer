from gurobipy import *
import sys
import csv

def modelMaker(states):
    election = Model("lbp")
    #lineup.setParam('OutputFlag', 0)
    
    # 49 - MAINE, 50 - MAINE 1, 51 - MAINE 2, 52 - NEBRASKA, 53 - NEBRASKA 1, 54 - NEBRASKA 2, 55 - NEBRASKA 3
    
    stateVars = []
    maineNebraskaVars = []
    
    maineNebraska = states[49:]
    states = states[:49]
    
    for state in states:
        stateVars.append(election.addVar(vtype=GRB.BINARY, name=state[0]))
    
    for state in maineNebraska:
        maineNebraskaVars.append(election.addVar(vtype=GRB.BINARY, name=state[0]))
    
    
    election.update()
    
    election.addConstr(sum(stateVars[i]*states[i][2] for i in range(len(stateVars))) + sum(maineNebraskaVars[i]*maineNebraska[i][2] for i in range(len(maineNebraska))), GRB.GREATER_EQUAL, 270, name="ElectoralCon")

    """
    lineup.addConstr(sum(sum(sum((teamVars[i][j][k] * teams[i][j][k][3]) for k in range(len(teamVars[i][j]))) for j in range(len(teamVars[i]))) for i in range(len(teamVars))), GRB.LESS_EQUAL, 50000.0, name="moneycon")
       
    lineup.addConstr(sum(sum(teamVars[i][5][k] for k in range(len(teamVars[i][5]))) for i in range(len(teamVars))), GRB.EQUAL, 1, name="GKcon")

    lineup.addConstr(sum(sum(teamVars[i][0][k] for k in range(len(teamVars[i][0]))) for i in range(len(teamVars))) + sum(sum(teamVars[i][1][k] for k in range(len(teamVars[i][1]))) for i in range(len(teamVars))), GRB.GREATER_EQUAL, 2, name="AllFconG")

    lineup.addConstr(sum(sum(sum(teamVars[i][j][k] for k in range(len(teamVars[i][j]))) for j in range(len(teamVars[i]))) for i in range(len(teamVars))), GRB.EQUAL, 8, name="totalCon")
    """
    
    
    # Objective function
    election.setObjective(sum(stateVars[i]*states[i][1] for i in range(len(stateVars))) + (maineNebraskaVars[0]*maineNebraska[0][1]) + (maineNebraskaVars[3]*maineNebraska[3][1]), GRB.MINIMIZE)
    
    election.update()
    election.optimize()
    
    election.printAttr('x')
    
    total = election.getObjective().getValue()
    
    print("TOTAL", total)





#JUST FOR SINGLE CSV TESTING, NO CHROMEDRIVER

def csvScrape2(iteration):
    loc = 'votes.csv'
    states = []
    
    with open(loc, encoding='mac_roman') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        counter = 0
        
        for row in reader:
            if counter <= 0:
                counter += 1
                continue
            if len(row[0]) > 0:
                states.append([row[0], row[iteration], row[iteration+1]])
    
    return states

if __name__ == "__main__":
    iteration = 1
    while iteration < 6:
        states = csvScrape2(iteration)
        modelMaker(states)
        iteration += 2
        break