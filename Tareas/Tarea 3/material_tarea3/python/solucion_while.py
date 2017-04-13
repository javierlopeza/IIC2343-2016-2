# DATA
path = 0
size = 5
#graph = [[0,1], [0,0]]
#graph = [[0,1,0],[0,0,1],[1,0,0]]
graph = [[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,0,0]]
origin = 1
end = 2

# CODE
ind_origin = origin - 1
ind_end = end -1 
c = size
matriz_calc = graph

if matriz_calc[ind_origin][ind_end] == 1:
	path = 1

while c > 0 and path == 0:
	matriz_aux = [[0 for e in range(size)] for e in range(size)]

	i=size-1
	while i >= 0:
		j=size-1
		while j >= 0:
			k=size-1
			while k >= 0:
				matriz_aux[i][j] += matriz_calc[i][k] * graph[k][j]
				k -= 1
			j -= 1
		i -= 1

	matriz_calc = matriz_aux

	if matriz_calc[ind_origin][ind_end] == 1:
		path = 1
		break

	c-=1

print("PATH : {}".format(path))



