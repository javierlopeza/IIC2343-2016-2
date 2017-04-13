# DATA
path = 0
size = 5
graph = [[0,1], [0,0]]
#graph = [[0,1,0],[0,0,1],[1,0,0]]
graph = [[0,1,0,0,0],
		 [0,0,1,0,0],
		 [0,0,0,1,0],
		 [0,0,0,0,1],
		 [0,0,0,0,0]]
origin = 1
end = 3

# CODE
c = size
matriz_calc = graph

while c > 0 and path == 0:
	if matriz_calc[origin-1][end-1] == 1:
		path = 1
		break

	matriz_aux = [[0 for e in range(size)] for e in range(size)]

	for i in range(size):
		for j in range(size):
			for k in range(size):
				matriz_aux[i][j] += matriz_calc[i][k] * graph[k][j]

	matriz_calc = matriz_aux

	if matriz_calc[origin-1][end-1] == 1:
		path = 1
		break

	c-=1

print("PATH : {}".format(path))