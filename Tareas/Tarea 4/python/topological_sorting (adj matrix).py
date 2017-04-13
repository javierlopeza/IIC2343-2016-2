def printmatrix(matrix):
	print("\tAdj Matrix")
	for row in matrix:
		r = "\t"
		for e in row:
			r+=str(e)+" "
		print(r)
	print("")


def isZeroRow(row):
	for k in row:
		if k == 1:
			return False
	return True


def clearColumn(matrix, j, size):
	for r in range(size):
		matrix[r][j] = 0
	return matrix


def topological_sort(adjmatrix,size,offset=1):
	graph_sorted = []
	cont = 0
	while len(graph_sorted)<size:

		for r in range(size):
			cont += 1
			#print("Checking r={}\t\t Status: graph_sorted{}".format(r+1,graph_sorted))
			if isZeroRow(adjmatrix[r]) and ((r+offset) not in graph_sorted):
				graph_sorted.append(r+offset)
				#print("\tPushed: {}".format(r+1))
				adjmatrix = clearColumn(adjmatrix, r, size)
			#printmatrix(adjmatrix)
		
	print("CONTADOR: {} iteraciones".format(cont))
	graph_sorted.reverse()

	return graph_sorted





# --------------------------

# matrix: https://en.wikipedia.org/wiki/Topological_sorting#Examples
				# 1 2 3 4 5 6 7 8
adjmatrix1 = 	[[0,0,0,0,0,0,0,0],# 1
				 [0,0,0,0,1,0,1,0],# 2
				 [0,0,0,0,0,0,0,1],# 3
				 [0,0,0,0,1,0,0,1],# 4
				 [0,0,0,0,0,1,0,0],# 5
				 [0,0,0,0,0,0,0,0],# 6
				 [0,0,0,0,0,0,0,0],# 7
				 [1,0,0,0,0,1,1,0]]# 8


				# 0 1 2 3 4 5 6 7
adjmatrix2 = 	[[0,0,1,0,1,0,0,0],# 0
				 [0,0,1,0,0,1,1,0],# 1
				 [0,0,0,0,0,1,1,0],# 2
				 [0,0,0,0,0,0,0,1],# 3
				 [0,0,0,0,0,0,0,1],# 4
				 [0,0,0,0,0,0,0,1],# 5
				 [0,0,0,0,0,0,0,1],# 6
				 [0,0,0,0,0,0,0,0]]# 7


				# 0 1 2 3 4 5 6 7
adjmatrix3 = 	[[0,1,0,0,0,0,0,0],# 0
				 [0,0,1,0,0,0,0,0],# 1
				 [0,0,0,1,0,0,0,0],# 2
				 [0,0,0,0,1,0,0,0],# 3
				 [0,0,0,0,0,1,0,0],# 4
				 [0,0,0,0,0,0,1,0],# 5
				 [0,0,0,0,0,0,0,1],# 6
				 [0,0,0,0,0,0,0,0]]# 7


#printmatrix(adjmatrix)

# MAIN
ts = topological_sort(adjmatrix2,8)
print("\nTopolgical Sorting: {}\n".format(ts))
