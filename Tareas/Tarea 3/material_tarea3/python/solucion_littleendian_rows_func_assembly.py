# graph * matriz2 = matriz3


# --- DATA ---
path = 0
size = 5
graph = [0,1,0,0,0, 
		 0,0,1,0,0, 
		 0,0,0,1,0, 
		 0,0,0,0,1, 
		 0,0,0,0,0]  # 1 -> 2 -> 3 -> 4 -> 5
origin = 5
end = 3

# --- CODE ---


# --- (0) --- -> OK

#ind_origin = origin - 1
A = origin
A -= 1
ind_origin = A
#ind_end = end -1 
A = end
A -= 1
ind_end = A
#contador_general = size
A = size
A -= 2
contador_general = A


# --- (1) ---
# CASO AL NODO DESTINO NO LLEGAN ARCOS
i = 0
parcial = 0
while i < size:
	A = i*size
	A += ind_end
	A += 0 #dir graph
	parcial += graph[A]
	i += 1
if parcial == 0:
	path = -1
	print("caso 1")

# CASO DEL NODO ORIGEN NO SALEN ARCOS
i = 0
parcial = 0
while i < size:
	A = ind_origin*size
	A +=  i
	A += 0 #dir graph
	parcial += graph[A]
	i += 1
print(parcial)
if parcial == 0:
	path = -1
	print("caso 2")



# --- (2) --- -> OK

matriz2 = graph

# --- (funciones) --- -> OK

def multiplicar(factor1, factor2):
	return factor1*factor2

def potencia(base, exponente):
	return base**exponente

# --- (3) --- -> OK

#var3 = ind_origin*size -> OK
A = ind_origin
factor1 = A
A = size
factor2 = A
producto = multiplicar(factor1, factor2)
A = producto
var3 = A

#var3 += ind_end -> OK
B = ind_end
A += B
var3 = A

#var3 += dir graph -> OK
B = A
A = 0  # dir graph
A += B
var3 = A


if graph[var3] == 1:		# |
	path = 1				# | CMP -> OK
	#JMP end  				# |


# --- (4) ---

# whilegeneral:
while contador_general > 0 and path == 0:
	#size_squared = multiplicar(size, size) -> OK
	A = size
	factor1 = A
	factor2 = A
	producto = multiplicar(factor1, factor2)
	A = producto
	size_squared = A

	# crearmatriz3nula -> OK
	matriz3 = []
	while size_squared > 0:
		matriz3 += [0]
		size_squared -= 1


	# I=size-1 -> OK
	A = size
	A -= 1
	I = A

	# whileI:
	while I >= 0:
		# J = size - 1 -> OK
		A = size
		A -= 1
		J = A

		# whileJ:
		while J >= 0:
			# K = size - 1 -> OK
			A = size
			A -= 1
			K = A

			# whileK:
			while K >= 0:
				# var4 = I * size -> OK
				A = I
				factor1 = A
				A = size
				factor2 = A
				producto = multiplicar(factor1, factor2)
				A = producto

				# var4 += K -> OK
				A += K
				A += 0 # dir matriz2
				var4 = A
				
				# var3 = K * size -> OK
				A = K
				factor1 = A
				A = size
				factor2 = A
				producto = multiplicar(factor1, factor2)
				A = producto
				var3 = A
				
				# var3 += J -> OK
				A += J
				A += 0 # dir graph
				var3 = A

				# OK
				factor1 = matriz2[var4]

				# -> OK
				factor2 = graph[var3]

				# CALL multiplicar -> OK
				producto = factor1 and factor2
				A = producto
				var5 = A

				# var3 = I * size -> OK
				A = I
				factor1 = A
				A = size
				factor2 = A
				producto = multiplicar(factor1, factor2)
				A = producto

				# var3 += J -> OK
				A += J
				A += 0 # dir matriz
				A += 0 # sqrsize

				# matriz3[var3] +=  var5 -> OK
				var3 = A
					# --
				A = var5
				A += matriz3[var3]
				matriz3[var3] = A

				#K -= 1 -> OK
				A = K
				A -= 1
				K = A
				# CMP K

			# J -= 1 -> OK
			A = J
			A -= 1
			J = A
			# CMP J

		# I -= 1 -> OK
		A = I
		A -= 1
		I = A
		# CMP I
	
	# Copiar matriz3 en matriz2 -> OK
	matriz2 = matriz3 

	#var3 = ind_origin*size -> OK
	A = ind_origin
	factor1 = A
	A = size
	factor2 = A
	producto = multiplicar(factor1, factor2)
	A = producto
	var3 = A

	#var3 += ind_end -> OK
	B = ind_end
	A += B
	var3 = A

	#var3 += dir matriz2 -> OK
	B = A
	A = 0  # dir matriz2
	A += B
	var3 = A

	if matriz2[var3] == 1:		# |
		path = 1				# | CMP -> OK 
		break #JMP end          # |

	# contador_general -= 1 -> OK
	A = contador_general
	A -= 1
	contador_general = A
	# CMP whilegeneral
	# CMP path
	

print("PATH : {}".format(path))
print(contador_general)
print(matriz2)
#end:

"""
graph	0
		1
		0

		0
		0
		1

		0
		0
		0
"""

"""
graph	0
		1
		0
		0
		0

		0
		0
		1
		0
		0

		0
		0
		0
		1
		0

		0
		0
		0
		0
		1

		0
		0
		0
		0
		0
"""
