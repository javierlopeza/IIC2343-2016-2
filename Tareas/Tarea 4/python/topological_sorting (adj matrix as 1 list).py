def isZeroRow(matrix, r, size):
	pointer = size * r
	i = 0
	while i < size:
		if matrix[pointer] == 1:
			return False
		pointer += 1
		i += 1
	return True


def clearColumn(matrix, j, size):
	pointer = j
	i = 0
	while i < size:
		matrix[pointer] = 0
		pointer += size
		i += 1
	return matrix


def topological_sort(adjmatrix,size):
	graph_sorted = []
	while len(graph_sorted)<size:
		r = 0
		while r < size:
			#print("Checking r={}\t\t Status: graph_sorted{}".format(r+1,graph_sorted))
			if isZeroRow(adjmatrix, r, size) and ((r+1) not in graph_sorted):
				graph_sorted.append(r+1)
				#print("\tPushed: {}".format(r+1))
				adjmatrix = clearColumn(adjmatrix, r, size)
			#printmatrix(adjmatrix)
			r+=1
	graph_sorted.reverse()

	return graph_sorted





# --------------------------

# matrix: https://en.wikipedia.org/wiki/Topological_sorting#Examples
				# 1 2 3 4 5 6 7 8
adjmatrix1 = 	[0,0,0,0,0,0,0,0,# 1
				 0,0,0,0,1,0,1,0,# 2
				 0,0,0,0,0,0,0,1,# 3
				 0,0,0,0,1,0,0,1,# 4
				 0,0,0,0,0,1,0,0,# 5
				 0,0,0,0,0,0,0,0,# 6
				 0,0,0,0,0,0,0,0,# 7
				 1,0,0,0,0,1,1,0]# 8


				# 0 1 2 3 4 5 6 7
adjmatrix2 = 	[0,0,1,0,1,0,0,0,# 0
				 0,0,1,0,0,1,1,0,# 1
				 0,0,0,0,0,1,1,0,# 2
				 0,0,0,0,0,0,0,1,# 3
				 0,0,0,0,0,0,0,1,# 4
				 0,0,0,0,0,0,0,1,# 5
				 0,0,0,0,0,0,0,1,# 6
				 0,0,0,0,0,0,0,0]# 7


				# 0 1 2 3 4 5 6 7
adjmatrix3 = 	[0,1,0,0,0,0,0,0,# 0
				 0,0,1,0,0,0,0,0,# 1
				 0,0,0,1,0,0,0,0,# 2
				 0,0,0,0,1,0,0,0,# 3
				 0,0,0,0,0,1,0,0,# 4
				 0,0,0,0,0,0,1,0,# 5
				 0,0,0,0,0,0,0,1,# 6
				 0,0,0,0,0,0,0,0]# 7


#printmatrix(adjmatrix)

# MAIN
ts = topological_sort(adjmatrix1,8)
print("\nTopolgical Sorting: {}\n".format(ts))
