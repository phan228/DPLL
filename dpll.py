import sys
import time

# Get new cnf without the chosen literal
def simplify(cnf, p):
	new_cnf = []
	
	if type(p) is list:
		p = int((''.join(map(str,p))))
		
	for clause in cnf:
		if p in clause:
			continue		# ignore/ dont add the clauses that contain p
		if -p in clause:
			c = [x for x in clause if x != -p]	# delete occurences of -p in clauses
			if len(c) == 0:		# the case where p is true and -p is a unit clause
				return -1		# which means p is True and False -> conflict
			new_cnf.append(c)
		else:
			new_cnf.append(clause)
	
	return new_cnf

# Process unit clauses
def unit_clause(cnf):
	truth_assignments = []
	unit_clauses = [c for c in cnf if len(cnf) == 1]
	
	while len(unit_clauses) > 0:
		p = unit_clauses[0]
		# print('p = '+str(p))
		truth_assignments.append(p)
		cnf = simplify(cnf, p)
		if cnf == -1:
			return -1, []
		if not cnf:		# if cnf is empty (all clauses are unit clauses)
			return cnf, truth_assignments
		# update cnf and go again
		unit_clauses = [c for c in cnf if len(cnf) == 1]
	
	return cnf, truth_assignments

def occurences(cnf):
	occurences = {}		# map of { "x1: # of currences", "x2: # of currences",...}
	
	for clause in cnf:
		for x in clause:
			if x in occurences:
				occurences[x] += 1
			else:
				occurences[x] = 1
	
	return occurences

# Process pure literals
def pure_literal(cnf):
	count = occurences(cnf)
	pure_literals = []
	
	for x, times in count.items():
		if -x not in count:
			pure_literals.append(x)
	
	for x in pure_literals:
		cnf = simplify(cnf, x)

	return cnf, pure_literals

def DPLL(cnf, truth_assignments):
	if cnf == -1:		# not satisfiable because of conflict
		return []
	if not cnf:			# cnf is empty -> done
		return truth_assignments
	
	cnf, unit_clauses = unit_clause(cnf)
	cnf, pure_literals = pure_literal(cnf)
	#cnf, unit_clauses = unit_clause(cnf)
	truth_assignments = truth_assignments + pure_literals + unit_clauses
	
	# Testing the process
	#for i in cnf:
	#	print(str(i))
	#print('Pure literals: ' + str(pure_literals))
	#print('Unit clauses: ' + str(unit_clauses))
	#print('Truth assignments: '+str(truth_assignments))
	#print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
	
	if cnf == -1:		# not satisfiable because of conflict
		return []
	if not cnf:			# cnf is empty -> done
		return truth_assignments

	count = occurences(cnf)
	p = max(count, key=count.get)		# choose the literal that appears the most
	solution = DPLL(simplify(cnf, p), truth_assignments + [p])
	if not solution:
		solution = DPLL(simplify(cnf, -p), truth_assignments + [-p])

	return solution

def Main(argv):
	if len(sys.argv) < 2:
		print("Please use: python dpll.py filename")
		return
	else:
		# read file
		f = open(sys.argv[1], 'r')
		everything = f.readlines()				# data = ['x1 x2 x3', 'x2 x3 x4', ...]
		f.close()

		start = 0
		clauseNum = 0

		find_p = [line.split(' ') for line in everything]
		for i  in range(len(find_p)):
			if find_p[i][0] == "p":
				start = i + 1
				clauseNum = int(find_p[i][4])
				for j in range(3):
					find_p[i+1][j] = find_p[i+1][j+1]
				find_p[i+1].pop()
				break

		cnf = []
		for i in range(start, clauseNum+start):	
			cnf.append(find_p[i])				# cnf = [	['x1', 'x2', 'x3', '0'],
												#			['x2', 'x3', 'x4', '0'], ...]
		for i in range(len(cnf)):
			for j in range(4):
				cnf[i][j] = int(cnf[i][j])

		# removing the last 0's
		for i in cnf:
			i.pop()

	# Run DPLL
	start = time.time()
	solved = DPLL(cnf, [])
	stop = time.time()
	print('Time taken in seconds = '+str(stop - start))
	if solved:
		print("SATISFIABLE")
		print('Truth assignments: ')
		print(solved)
	else:
		print("UNSATISFIABLE")

if __name__ == '__main__':
	Main(sys.argv)
	