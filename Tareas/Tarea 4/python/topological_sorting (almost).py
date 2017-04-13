from datetime import datetime
t0 = datetime.now()

# ----- DATA ----- OK
size = 8

# adjmatrix1: https://en.wikipedia.org/wiki/Topological_sorting#Examples
				# 1 2 3 4 5 6 7 8
adjmatrix = 	[0,0,0,0,0,0,0,0,# 1
				 0,0,0,0,1,0,1,0,# 2
				 0,0,0,0,0,0,0,1,# 3
				 0,0,0,0,1,0,0,1,# 4
				 0,0,0,0,0,1,0,0,# 5
				 0,0,0,0,0,0,0,0,# 6
				 0,0,0,0,0,0,0,0,# 7
				 1,0,0,0,0,1,1,0]# 8

				# 0 1 2 3 4 5 6 7
adjmatrix1 = 	[0,0,1,0,1,0,0,0,# 0
				 0,0,1,0,0,1,1,0,# 1
				 0,0,0,0,0,1,1,0,# 2
				 0,0,0,0,0,0,0,1,# 3
				 0,0,0,0,0,0,0,1,# 4
				 0,0,0,0,0,0,0,1,# 5
				 0,0,0,0,0,0,0,1,# 6
				 0,0,0,0,0,0,0,0]# 7

				# 0 1 2 3 4 5 6 7
adjmatrix1 = 	[0,1,0,0,0,0,0,0,# 0
				 0,0,1,0,0,0,0,0,# 1
				 0,0,0,1,0,0,0,0,# 2
				 0,0,0,0,1,0,0,0,# 3
				 0,0,0,0,0,1,0,0,# 4
				 0,0,0,0,0,0,1,0,# 5
				 0,0,0,0,0,0,0,1,# 6
				 0,0,0,0,0,0,0,0]# 7

graph_sorted = [0 for n in range(size)]

# ----- CODE -----
DI = 0
while DI<size:
	r = 0
	while r < size:
		# isZeroRow(adjmatrix, r, size) -> ?
		isZeroRow = True
		pointer = size * r
		i = 0
		while i < size:
			if adjmatrix[pointer] == 1:
				isZeroRow = False
				i = size
			pointer += 1
			i += 1


		if isZeroRow:
			if (r+1) not in graph_sorted:
				graph_sorted[DI] = r+1
				DI += 1

				# clearColumn(adjmatrix, r, size)
				pointer = r
				i = 0
				while i < size:
					adjmatrix[pointer] = 0
					pointer += size
					i += 1

		r+=1

graph_sorted.reverse()

print("\nTopolgical Sorting: {}\n".format(graph_sorted))
print(datetime.now() - t0)
