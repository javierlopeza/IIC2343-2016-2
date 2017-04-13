# graph * matriz_aux = matriz_calc


# DATA
path = 0
size = 5
graph = [0,1,0,0,0, 
		 0,0,1,0,0, 
		 0,0,0,1,0, 
		 0,0,0,0,1, 
		 0,0,0,0,0]
origin = 1
end = 5

ind_origin = None
ind_end = None
contador_general = None

# CODE
ind_origin = origin - 1
ind_end = end -1 
contador_general = size
matriz_calc = graph

def multiplicar(factor1, factor2):
	return factor1*factor2

def potencia(base, exponente):
	return base**exponente


var3 = ind_origin*size
var3 += ind_end
if matriz_calc[var3] == 1:
	path = 1
	#jump end


while contador_general > 0 and path == 0:
	# matriz_aux -> matriz nula
	size_squared = potencia(size,2)
	matriz_aux = []
	while size_squared > 0:
		matriz_aux += [0]
		size_squared -= 1

	i=size-1
	while i >= 0:
		j=size-1
		while j >= 0:
			k=size-1
			while k >= 0:
				var3 = i*size
				var3 += k
				factor1 = matriz_calc[var3]
				var3 = k*size
				var3 += j
				factor2 = graph[var3]
				producto = multiplicar(factor1, factor2)

				var3 = i*size
				var3 += j
				matriz_aux[var3] +=  producto

				k -= 1
			j -= 1
		i -= 1

	matriz_calc = matriz_aux

	var3 = ind_origin*size
	var3 += ind_end
	if matriz_calc[var3] == 1:
		path = 1
		break #jump end

	contador_general -= 1 

print("PATH : {}".format(path))
#end:

