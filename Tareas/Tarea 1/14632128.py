def to_decimal(digits, base): 
	# digits: [int]
	# base: int
	res = 0 
	potencia = len(digits) - 1
	for d in range(len(digits)):
		res += digits[d]*(base**(potencia-d))
	return res


def positivos(digits, base):  
		# Considera el 0 como positivo 
		#(porque no es necesario invertirlo para observar su modulo)
	# digits: [int]
	# base: int
	lista_positivos = []
	n_posiciones = len(digits)
	# CASO BASE PAR:
	if base % 2 == 0:
		n_positivos = int((base ** (n_posiciones))/2 - 1)
	# CASO BASE IMPAR
	else:
		n_positivos = int(((base ** (n_posiciones)) - 1)/2)

	lista_positivos.append([0 for d in digits])
	n = [0 for d in digits]
	for i in range(n_positivos):
		nuevo_n = sumar1(n, base)
		lista_positivos.append(nuevo_n)
	return lista_positivos


def sumar1(digits, base):
	# digits: [int]
	# base: int
	carry = 0
	for d in range(len(digits)):
		posicion_actual = len(digits)-1-d
		if posicion_actual == len(digits)-1:
			digits[posicion_actual] += 1 + carry
		else:
			digits[posicion_actual] += carry
		carry = 0
		if digits[posicion_actual] == base:
			digits[posicion_actual] = 0
			carry += 1
		else:
			break
	return(digits[:])


def inverso(digits, base):
	digits = [0] + digits  # Agrego 0 a la izquierda
	complemento = [base - 1 - d for d in digits]  # Cambio cada digito por su complemento
	inverso = sumar1(complemento, base)
	return inverso[1:]


def read_numbers(filename):
	with open(filename) as f:
		readlines = f.read().splitlines() 
	lineas = [linea.replace(" ", "").split(",") for linea in readlines]
	pares = [(int(linea[0]), [int(d) for d in linea[1:]]) for linea in lineas]
	return pares


def get_inverso(base, digits):
	digits_str = ",".join([str(d) for d in digits])

	lista_positivos = positivos(digits, base)
	if digits in lista_positivos:  # El numero ingresado es positivo o cero.
		modulo = to_decimal(digits, base)
		inverso_aditivo = inverso(digits, base)
		inverso_aditivo_str = ",".join([str(d) for d in inverso_aditivo])
		display = "{} ({}) ==> {}".format(digits_str, modulo, inverso_aditivo_str)

	else:  # El numero ingresado es negativo.
		inverso_aditivo = inverso(digits, base)
		inverso_aditivo_str = ",".join([str(d) for d in inverso_aditivo])
		modulo = to_decimal(inverso_aditivo, base)
		display = "{} (-{}) ==> {}".format(digits_str, modulo, inverso_aditivo_str)

	return display


# --- main ---

import sys
filename = str(sys.argv[1])
numbers = read_numbers(filename)

for base, digits in numbers:
	nuevo_inverso = get_inverso(base, digits)
	print(nuevo_inverso)










