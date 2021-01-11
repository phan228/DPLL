# DPLL

How to run:	`python dpll.py <filename>`

The test files are in "CNF Formulas" folder

The cnf file is parsed into a list of clauses, called cnf, and each clause is a list of literals. An example of the data structure is as below:
		
		cnf = [	['-x1', 'x2', 'x3'],	
			['x2', '-x3', 'x4'],...	]

The DPLL algorithm the starts running using the cnf list and a truth_assignment list (which is initialized to empty). This truth_assignment list contains the literals that are assigned to True, for example: [x1, -x2] -> x1 is True and -x2 is True (which means x2 is False)

The algorithm first finds all unit clauses and set them to True, then processes all pure literals (only x or -x exist within the whole cnf)

The remaining literals that are not pure literals or in a unit clause are then picked based on the number of times they appear in the cnf (the one that appears the most is selected because it's the most constrained)

DPLL then runs recursively until the cnf is found satisfiable, or when there're conflicts -> unsatisfiable

The result is then printed out as "SATISFIABLE" and the truth assignments of all literals, or as "UNSATISFIABLE"

*2020 Intro to Artificial Intelligence*
