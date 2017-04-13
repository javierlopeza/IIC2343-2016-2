from datetime import datetime
t0 = datetime.now()

# ----- DATA ----- OK

# adjmatrix1: https://en.wikipeDLa.org/wiki/Topological_sorting#Examples
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


adjmatrix1 = [0,1,1,0,
		     0,0,0,1,
		     0,0,0,1,
		     0,0,0,0]

size = 8

ordering_aux = [0 for n in range(size)]

ordering = [0 for n in range(size)]

len_graph_sorted = 0

contador = 0
# ----- CODE -----
# whileDLsize:
while len_graph_sorted<size:
	DI = 0
	# whileDIsize:
	while DI < size:
		# isZeroRow(adjmatrix, DI, size) -> ?
		# isZeroRow = True
		CL = 1

		AL = size
		AL = AL * DI
		AL += 0	# graph
		BX = AL

		DH = 0
		while DH < size:
			contador += 1
			if adjmatrix[BX] == 1:
				# isZeroRow = False
				CL = 0
				DH = size
			BX += 1
			DH += 1

# OK 1! <------------------------

# ---------- PENDIENTE ------------
		# if isZeroRow == True:
		if CL == 1:
			AL = DI + 1
			# alreadyIn = False
			CL = 0

			BX = 0# dir(ordering_aux)  

			CH = 0
			while CH < size:
				contador += 1


				if ordering_aux[BX] == AL:
					# alreadyIn = True
					CL = 1
					CH = size
				elif ordering_aux[BX] == 0:
					CH = size
				BX += 1
				CH += 1

			#if alreadyIn == False:
			if CL == 0:
				# clearColumn(adjmatrix, DI, size)
				BX = 0    # dir(graph)
				BX += DI
				DH = 0
				AL = size
				while DH < size:
					contador += 1
					adjmatrix[BX] = 0
					BX += AL
					DH += 1

			# CHECK!

				BX = 0 # dir(ordering_aux)
				AL = len_graph_sorted
				BX += AL
				CL = DI
				ordering_aux[BX] = CL+1
				len_graph_sorted += 1
				if len_graph_sorted == size:
					DI = size
# --------------------------------

# OK 2! <------------------------

		# isNotZeroRow:
		DI+=1

DL = size - 1
while DL != -1:
	contador += 1
	BX = 0  # dir(ordering_aux)
	BX += DL
	AL = ordering_aux[BX]

	BX = 0 # dir(ordering)
	CL = size - 1
	CL -= DL
	BX += CL

	ordering[BX] = AL

	DL -= 1


print(contador)
#ordering_aux.reverse()

print("\nTopolgical Sorting (no reversed): {}".format(ordering_aux))
print("\nTopolgical Sorting: {}\n".format(ordering))
print(datetime.now() - t0)
