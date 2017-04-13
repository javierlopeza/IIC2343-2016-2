# DATA
path = 0
size = 5
#graph = [[0,1], [0,0]]
#graph = [[0,1,0],[0,0,1],[1,0,0]]
graph = [0,1,0,0,0, 
		 0,0,1,0,0, 
		 0,0,0,1,0, 
		 0,0,0,0,1, 
		 0,0,0,0,0]
origin = 1
end = 5

# CODE
ind_origin = origin - 1
ind_end = end -1 
c = size
matriz_calc = graph

if matriz_calc[0 + ind_origin*size + ind_end] == 1:
	path = 1
	#jump end

while c > 0 and path == 0:
	c2 = size ** 2
	matriz_aux = []
	while c2 > 0:
		matriz_aux += [0]
		c2 -= 1

	i=size-1
	while i >= 0:
		j=size-1
		while j >= 0:
			k=size-1
			while k >= 0:
				matriz_aux[0 + i*size + j] += matriz_calc[0 + i*size + k] * graph[0 + k*size + j]
				k -= 1
			j -= 1
		i -= 1

	matriz_calc = matriz_aux

	if matriz_calc[0 + ind_origin*size + ind_end] == 1:
		path = 1
		break #jump end

	c-=1

print("PATH : {}".format(path))
print(matriz_calc)
#end:

