
class Cache:
    def __init__(self, size, line_size, corr, subs, write, mem_size):
        self.size = size
        self.line_size = line_size
        self.corr = corr
        self.subs = subs
        self.write = write

        self.n_bits_direccion = str(bin(mem_size))[2:][::-1].index("1")

        self.n_lineas = int(self.size / self.line_size)

        self.validar_associative()

        if self.validar_pot2():
            self.construir_cache()
        else:
            raise ValueError("Error en los parametros ingresados. Los valores deben ser potencias de 2.")

        self.hits = 0
        self.miss = 0

        self.hits_write = 0
        self.total_writes = 0

    def validar_associative(self):
        # Verificamos que si es n-way associative efectivamente se formen al menos 2 conjuntos,
        # si no: corresponde a full-associative.
        if self.corr == "2W" or self.corr == "4W" or self.corr == "8W":
            way_number = int(self.corr[0])
            n_conjuntos = int(self.n_lineas / way_number)
            if n_conjuntos == 1:
                self.corr = "FA"

    def validar_pot2(self):
        # Se verifica que los parametros sean potencia de 2.
        size_bin = str(bin(self.size))[2:]
        line_size_bin = str(bin(self.line_size))[2:]
        if size_bin.count("1") != 1:
            return False
        elif line_size_bin.count("1") != 1:
            return False
        return True


    def construir_cache(self):
        # Linea = [[dir_dato1, dir_dato2, ...], orden, accesos, tiempo, dirty]

        if self.corr == "FA" or self.corr == "DM":
            self.memoria = []
            orden = 1
            for linea in range(self.n_lineas):
                new_linea = [[]]
                for pos in range(self.line_size):
                    new_linea[0].append('')
                new_linea.append(orden)
                orden += 1
                new_linea.append(0)
                new_linea.append(0)
                new_linea.append(0)
                self.memoria.append(new_linea)

        elif self.corr == "2W" or self.corr == "4W" or self.corr == "8W":
            way = int(self.corr[0])

            self.memoria = []
            orden = 1
            for linea in range(self.n_lineas):
                new_linea = [[]]
                for pos in range(self.line_size):
                    new_linea[0].append('')
                new_linea.append(orden)
                orden += 1
                if orden > way:
                    orden = 1
                new_linea.append(0)
                new_linea.append(0)
                new_linea.append(0)
                self.memoria.append(new_linea)



    def traer_dato(self, dir_dato, w=False):  # dado que el dato no se encontro al buscarlo -> guardo el bloque correspondiente al dato

        dir_bin = str(bin(dir_dato))[2:].zfill(self.n_bits_direccion)

        if self.corr == "FA":
            ubicacion = int(dir_bin[-str(bin(self.line_size))[2:][::-1].index("1"):], 2)
            for l in range(len(self.memoria)):
                if self.memoria[l][0][ubicacion] == '':

                    pos = (dir_dato//self.line_size)*self.line_size     # SE GUARDA EL BLOQUE COMPLETO
                    for d in range(self.line_size):
                        self.memoria[l][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                        pos += 1

                    for line in range(len(self.memoria)):           # UPDATE ORDEN
                        self.memoria[line][1] -= 1
                    self.memoria[l][1] = self.n_lineas

                    if self.subs == "FIFO" or self.subs == "LFU":
                        self.memoria[l][2] = 1              # UPDATE ACCESOS (1)

                    elif self.subs == "LRU":
                        self.memoria[l][3] = 0              # UPDATE TIEMPO (0)

                    if w == True:
                        self.memoria[l][4] = 1      # Si es escritura: bit-dirty = 1
                    else:
                        self.memoria[l][4] = 0      # Si no: bit-dirty = 0

                    return

            # POLITICAS DE REEMPLAZO
            if self.subs == "FIFO":
                print("-> FIFO")
                for l in range(len(self.memoria)):
                    if self.memoria[l][1] == 1:

                        # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                        if self.memoria[l][4] == 1:
                            print("WRITE-HIT!")
                            self.hits_write += 1

                        pos = (dir_dato//self.line_size)*self.line_size         # SE GUARDA EL BLOQUE COMPLETO
                        for d in range(self.line_size):
                            self.memoria[l][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                            pos += 1

                        for line in range(len(self.memoria)):       # UPDATE ORDEN
                            self.memoria[line][1] -= 1

                        self.memoria[l][1] = self.n_lineas

                        if w == True:
                            self.memoria[l][4] = 1      # Si es escritura: bit-dirty = 1
                        else:
                            self.memoria[l][4] = 0      # Si no: bit-dirty = 0

                        return

            elif self.subs == "LFU":
                # Buscamos el indice de la linea con menor numero de accesos
                min_accesos = 999999999999999
                indice_min_accesos = None
                cont_min_accesos = 0
                for l in range(len(self.memoria)):
                    if self.memoria[l][2] == min_accesos:
                        cont_min_accesos += 1
                    if self.memoria[l][2] < min_accesos:
                        cont_min_accesos = 1
                        min_accesos = self.memoria[l][2]
                        indice_min_accesos = l

                if cont_min_accesos == 1:  # Hay un bloque unico con el minimo de accesos -> LFU puro
                    print("-> LFU")

                    # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                    if self.memoria[indice_min_accesos][4] == 1:
                        print("WRITE-HIT!")
                        self.hits_write += 1
                    if w == True:
                        self.memoria[indice_min_accesos][4] = 1      # Si es escritura: bit-dirty = 1
                    else:
                        self.memoria[indice_min_accesos][4] = 0      # Si no: bit-dirty = 0

                    pos = (dir_dato//self.line_size)*self.line_size         # SE GUARDA EL BLOQUE COMPLETO
                    for d in range(self.line_size):
                        self.memoria[indice_min_accesos][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                        pos += 1

                    for line in range(len(self.memoria)):       # UPDATE ORDEN (de los que se accedio mas recientemente)
                        if self.memoria[line][1] > self.memoria[indice_min_accesos][1]:
                            self.memoria[line][1] -= 1
                    self.memoria[indice_min_accesos][1] = self.n_lineas

                    # UPDATE ACCESOS (linea actualizada)
                    self.memoria[indice_min_accesos][2] = 1

                    return

                elif cont_min_accesos > 1:  # Hay mas de un bloque con el minimo de accesos igual -> LFU + FIFO
                    print("-> LFU + FIFO")
                    min_orden = 999999999999999
                    indice_min_accesos_y_orden = -1
                    for l in range(len(self.memoria)):
                        if self.memoria[l][1] < min_orden and self.memoria[l][2] == min_accesos:
                            indice_min_accesos_y_orden = l
                            min_orden = self.memoria[l][1]

                    # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                    if self.memoria[indice_min_accesos_y_orden][4] == 1:
                        print("WRITE-HIT!")
                        self.hits_write += 1
                    if w == True:
                        self.memoria[indice_min_accesos_y_orden][4] = 1      # Si es escritura: bit-dirty = 1
                    else:
                        self.memoria[indice_min_accesos_y_orden][4] = 0      # Si no: bit-dirty = 0

                    pos = (dir_dato//self.line_size)*self.line_size         # SE GUARDA EL BLOQUE COMPLETO
                    for d in range(self.line_size):
                        self.memoria[indice_min_accesos_y_orden][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                        pos += 1

                    for line in range(len(self.memoria)):       # UPDATE ORDEN (de los que se accedio mas recientemente)
                        if self.memoria[line][1] > self.memoria[indice_min_accesos_y_orden][1]:
                            self.memoria[line][1] -= 1
                    self.memoria[indice_min_accesos_y_orden][1] = self.n_lineas

                    # UPDATE ACCESOS (linea actualizada)
                    self.memoria[indice_min_accesos_y_orden][2] = 1

                    return

            elif self.subs == "LRU":
                print("-> LRU")
                max_tiempo = -1
                indice_max_tiempo = -1
                for l in range(len(self.memoria)):
                    if self.memoria[l][3] > max_tiempo:
                        max_tiempo = self.memoria[l][3]
                        indice_max_tiempo = l

                # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                if self.memoria[indice_max_tiempo][4] == 1:
                    print("WRITE-HIT!")
                    self.hits_write += 1
                if w == True:
                    self.memoria[indice_max_tiempo][4] = 1      # Si es escritura: bit-dirty = 1
                else:
                    self.memoria[indice_max_tiempo][4] = 0      # Si no: bit-dirty = 0

                pos = (dir_dato // self.line_size) * self.line_size         # SE GUARDA EL BLOQUE COMPLETO
                for d in range(self.line_size):
                    self.memoria[indice_max_tiempo][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                    pos += 1

                # El tiempo se avanza en la simulacion (+1 a todos los tiempos durante la simulacion)
                self.memoria[indice_max_tiempo][3] = 0      # UPDATE TIEMPO (dato guardado)

                return

        elif self.corr == "DM":
            n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
            ubicacion = int(dir_bin[-n_bits_ubicacion:], 2)
            n_bits_indice = str(bin(self.n_lineas))[2:][::-1].index("1")
            indice = int(dir_bin[-n_bits_indice-n_bits_ubicacion:-n_bits_ubicacion], 2)

            # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
            if self.memoria[indice][4] == 1:
                print("WRITE-HIT!")
                self.hits_write += 1
            if w == True:
                self.memoria[indice][4] = 1      # Si es escritura: bit-dirty = 1
            else:
                self.memoria[indice][4] = 0      # Si no: bit-dirty = 0

            pos = (dir_dato//self.line_size)*self.line_size         # SE GUARDA EL BLOQUE COMPLETO
            for d in range(self.line_size):
                self.memoria[indice][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                pos += 1

        elif self.corr == "2W" or self.corr == "4W" or self.corr == "8W":
            # 1. Me posiciono en el inicio del conjunto correspondiente al dato.
            # 2. Reviso si alguno de los bloques del conjunto esta vacio.
                # Si hay alguno vacio lo uso.
                # Si no, aplico politica de reemplazo dentro del conjunto.
            way_number = int(self.corr[0])

            n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
            ubicacion = int(dir_bin[-n_bits_ubicacion:], 2)
            n_conjuntos = int(self.n_lineas / way_number)
            n_bits_conjunto = str(bin(n_conjuntos))[2:][::-1].index("1")
            conjunto = int(dir_bin[-n_bits_conjunto-n_bits_ubicacion:-n_bits_ubicacion], 2)
            print("CONJUNTO: {}".format(dir_bin[-n_bits_conjunto-n_bits_ubicacion:-n_bits_ubicacion]))

            indice = conjunto * way_number
            for i in range(way_number):
                if self.memoria[indice + i][0][ubicacion] == '':

                    if w == True:
                        self.memoria[indice + i][4] = 1      # Si es escritura: bit-dirty = 1
                    else:
                        self.memoria[indice + i][4] = 0      # Si no: bit-dirty = 0

                    pos = (dir_dato//self.line_size)*self.line_size     # SE GUARDA EL BLOQUE COMPLETO
                    for d in range(self.line_size):
                        self.memoria[indice + i][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                        pos += 1

                    for j in range(way_number):               # UPDATE ORDEN
                        self.memoria[indice + j][1] -= 1
                    self.memoria[indice + i][1] = way_number

                    if self.subs == "FIFO" or self.subs == "LFU":
                        self.memoria[indice + i][2] = 1              # UPDATE ACCESOS (1)

                    elif self.subs == "LRU":
                        self.memoria[indice + i][3] = 0              # UPDATE TIEMPO (0)

                    return

            # POLITICAS DE REEMPLAZO
            if self.subs == "FIFO":
                print("-> FIFO")
                for i in range(way_number):
                    if self.memoria[indice + i][1] == 1:

                        # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                        if self.memoria[indice + i][4] == 1:
                            print("WRITE-HIT!")
                            self.hits_write += 1
                        if w == True:
                            self.memoria[indice + i][4] = 1      # Si es escritura: bit-dirty = 1
                        else:
                            self.memoria[indice + i][4] = 0      # Si no: bit-dirty = 0

                        pos = (dir_dato//self.line_size)*self.line_size     # SE GUARDA EL BLOQUE COMPLETO
                        for d in range(self.line_size):
                            self.memoria[indice + i][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                            pos += 1

                        for j in range(way_number):               # UPDATE ORDEN
                            self.memoria[indice + j][1] -= 1
                        self.memoria[indice + i][1] = way_number

                        return

            elif self.subs == "LFU":
                # Me posiciono al comienzo del conjunto.
                # Busco la linea con menos accesos, y veo si es la unica con minimo de accesos o hay mas de una.
                    # Si es la unica con minimo de accesos, la reemplazo.
                    # Si hay mas de una con el minimo de accesos les aplico FIFO solo a esas para decidir cual reemplazo.
                # Reemplazo.
                # Actualizo los ordenes del conjunto (de solo aquellas lineas que entraron mas recientes al reemplazado).
                # Actualizo los accesos de la linea reemplazada (1).

                # Buscamos el indice de la linea con menor numero de accesos
                min_accesos = 999999999999999
                indice_min_accesos = None
                cont_min_accesos = 0
                for i in range(way_number):
                    if self.memoria[indice + i][2] == min_accesos:
                        cont_min_accesos += 1
                    if self.memoria[indice + i][2] < min_accesos:
                        cont_min_accesos = 1
                        min_accesos = self.memoria[indice + i][2]
                        indice_min_accesos = indice + i

                if cont_min_accesos == 1:  # Hay un bloque unico con el minimo de accesos -> LFU puro
                    print("-> LFU")

                    # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                    if self.memoria[indice_min_accesos][4] == 1:
                        print("WRITE-HIT!")
                        self.hits_write += 1
                    if w == True:
                        self.memoria[indice_min_accesos][4] = 1      # Si es escritura: bit-dirty = 1
                    else:
                        self.memoria[indice_min_accesos][4] = 0      # Si no: bit-dirty = 0

                    pos = (dir_dato // self.line_size) * self.line_size         # SE GUARDA EL BLOQUE COMPLETO
                    for d in range(self.line_size):
                        self.memoria[indice_min_accesos][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                        pos += 1

                    for j in range(way_number):       # UPDATE ORDEN (de los que se accedio mas recientemente)
                        if self.memoria[indice + j][1] > self.memoria[indice_min_accesos][1]:
                            self.memoria[indice + j][1] -= 1
                    self.memoria[indice_min_accesos][1] = way_number

                    # UPDATE ACCESOS (linea actualizada)
                    self.memoria[indice_min_accesos][2] = 1

                    return

                elif cont_min_accesos > 1:  # Hay mas de un bloque con el minimo de accesos igual -> LFU + FIFO
                    print("-> LFU + FIFO")
                    min_orden = 999999999999999
                    indice_min_accesos_y_orden = None
                    for i in range(way_number):
                        if self.memoria[indice + i][1] < min_orden and self.memoria[indice + i][2] == min_accesos:
                            indice_min_accesos_y_orden = indice + i
                            min_orden = self.memoria[indice + i][1]

                    # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                    if self.memoria[indice_min_accesos_y_orden][4] == 1:
                        print("WRITE-HIT!")
                        self.hits_write += 1
                    if w == True:
                        self.memoria[indice_min_accesos_y_orden][4] = 1      # Si es escritura: bit-dirty = 1
                    else:
                        self.memoria[indice_min_accesos_y_orden][4] = 0      # Si no: bit-dirty = 0

                    pos = (dir_dato // self.line_size) * self.line_size         # SE GUARDA EL BLOQUE COMPLETO
                    for d in range(self.line_size):
                        self.memoria[indice_min_accesos_y_orden][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                        pos += 1

                    for j in range(way_number):       # UPDATE ORDEN (de los que se accedio mas recientemente)
                        if self.memoria[indice + j][1] > self.memoria[indice_min_accesos_y_orden][1]:
                            self.memoria[indice + j][1] -= 1
                    self.memoria[indice_min_accesos_y_orden][1] = way_number

                    # UPDATE ACCESOS (linea actualizada)
                    self.memoria[indice_min_accesos_y_orden][2] = 1

                    return


            elif self.subs == "LRU":
                print("-> LRU")
                # Me posiciono al comienzo del conjunto.
                # Busco el tiempo maximo dentro del conjunto, y el indice asociado a ese tiempo.
                # Reemplazo.
                # Actualizo el tiempo de la linea reemplazada.
                max_tiempo = -1
                indice_max_tiempo = -1
                for i in range(way_number):
                    if self.memoria[indice + i][3] > max_tiempo:
                        max_tiempo = self.memoria[indice + i][3]
                        indice_max_tiempo = indice + i

                # Vemos si el bit-dirty de la linea que se va a sustituir esta en 1.
                if self.memoria[indice_max_tiempo][4] == 1:
                    print("WRITE-HIT!")
                    self.hits_write += 1
                if w == True:
                    self.memoria[indice_max_tiempo][4] = 1      # Si es escritura: bit-dirty = 1
                else:
                    self.memoria[indice_max_tiempo][4] = 0      # Si no: bit-dirty = 0

                pos = (dir_dato // self.line_size) * self.line_size     # SE GUARDA EL BLOQUE COMPLETO
                for d in range(self.line_size):
                    self.memoria[indice_max_tiempo][0][d] = str(bin(pos))[2:].zfill(self.n_bits_direccion)
                    pos += 1

                # El tiempo se avanza en la simulacion (+1 a todos los tiempos durante la simulacion)
                self.memoria[indice_max_tiempo][3] = 0      # UPDATE TIEMPO (dato guardado)

                return



    def buscar_dato(self, dir_dato, w=False):

        dir_bin = str(bin(dir_dato))[2:].zfill(self.n_bits_direccion)

        if self.corr == "FA":
            ubicacion = int(dir_bin[-str(bin(self.line_size))[2:][::-1].index("1"):], 2)
            for l in range(len(self.memoria)):
                if self.memoria[l][0][ubicacion] == dir_bin:
                    if self.subs == "LRU":
                        # Se actualiza el tiempo de acceso (0)
                        self.memoria[l][3] = 0
                    else:
                        # Se actualiza el contador de accesos (+1)
                        self.memoria[l][2] += 1
                    if w == True:  # Hit al escribir -> se pone dirty
                        self.memoria[l][4] = 1
                    return True
            return False

        elif self.corr == "DM":
            n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
            ubicacion = int(dir_bin[-n_bits_ubicacion:], 2)
            n_bits_indice = str(bin(self.n_lineas))[2:][::-1].index("1")
            indice = int(dir_bin[-n_bits_indice-n_bits_ubicacion:-n_bits_ubicacion], 2)

            if self.memoria[indice][0][ubicacion] == dir_bin:
                if w == True:  # Hit al escribir -> se pone dirty
                    self.memoria[indice][4] = 1
                return True
            return False

        elif self.corr == "2W" or self.corr == "4W" or self.corr == "8W":
            way_number = int(self.corr[0])

            n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
            ubicacion = int(dir_bin[-n_bits_ubicacion:], 2)
            n_conjuntos = int(self.n_lineas / way_number)
            n_bits_conjunto = str(bin(n_conjuntos))[2:][::-1].index("1")
            conjunto = int(dir_bin[-n_bits_conjunto-n_bits_ubicacion:-n_bits_ubicacion], 2)
            #print("N BITS UBICACION: {}".format(n_bits_ubicacion))
            #print("N BITS CONJUNTO: {}".format(n_bits_conjunto))
            indice = conjunto * way_number
            for i in range(way_number):
                if self.memoria[indice + i][0][ubicacion] == dir_bin:
                    if self.subs == "LRU":
                        # Se actualiza el tiempo de acceso (0)
                        self.memoria[indice + i][3] = 0
                    else:
                        # Se actualiza el contador de accesos (+1)
                        self.memoria[indice + i][2] += 1
                    if w == True:  # Hit al escribir -> se pone dirty
                        self.memoria[indice + i][4] = 1
                    return True
            return False


    def avanzar_tiempos(self):
        for l in range(len(self.memoria)):
            self.memoria[l][3] += 1


    def __str__(self):

        if self.corr == "DM":
            ret = "CACHE:\nINDICE LINEA\tUBICACION PALABRA\tDIRECCION DATO\tDIRTY\n"
            for b in range(len(self.memoria)):
                n_bits_indice = str(bin(self.n_lineas))[2:][::-1].index("1")
                indice_bloque = str(bin(b))[2:].zfill(n_bits_indice)
                for p in range(len(self.memoria[b][0])):
                    n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
                    ubicacion_palabra = str(bin(p))[2:].zfill(n_bits_ubicacion)
                    if self.memoria[b][0][p] == '':
                        dir_dato = " "*self.n_bits_direccion
                        dir_dato_int = "( )"
                    else:
                        dir_dato = self.memoria[b][0][p]
                        dir_dato_int = "({})".format(int(self.memoria[b][0][p], 2))
                    bit_dirty = self.memoria[b][4]
                    ret += "{} ({})\t\t\t{} ({})\t\t\t\t{} {}\t\t{}\n".format(indice_bloque, b, ubicacion_palabra, p, dir_dato, dir_dato_int, bit_dirty)


        elif self.subs == "FIFO":
            ret = "CACHE:\nINDICE LINEA\tUBICACION PALABRA\tDIRECCION DATO\tORDEN\tDIRTY\n"
            for b in range(len(self.memoria)):
                n_bits_indice = str(bin(self.n_lineas))[2:][::-1].index("1")
                indice_bloque = str(bin(b))[2:].zfill(n_bits_indice)
                for p in range(len(self.memoria[b][0])):
                    n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
                    ubicacion_palabra = str(bin(p))[2:].zfill(n_bits_ubicacion)
                    if self.memoria[b][0][p] == '':
                        dir_dato = " "*self.n_bits_direccion
                        dir_dato_int = "( )"
                    else:
                        dir_dato = self.memoria[b][0][p]
                        dir_dato_int = "({})".format(int(self.memoria[b][0][p], 2))
                    bit_dirty = self.memoria[b][4]
                    ret += "{} ({})\t\t\t{} ({})\t\t\t\t{} {}\t\t{}\t\t{}\n".format(indice_bloque, b, ubicacion_palabra, p, dir_dato, dir_dato_int, self.memoria[b][1], bit_dirty)

        elif self.subs == "LFU":
            ret = "---------------------------------  CACHE -----------------------------------------\n"
            ret += "INDICE LINEA\tUBICACION PALABRA\tDIRECCION DATO\tORDEN\tACCESOS\tDIRTY\n"
            for b in range(len(self.memoria)):
                n_bits_indice = str(bin(self.n_lineas))[2:][::-1].index("1")
                indice_bloque = str(bin(b))[2:].zfill(n_bits_indice)
                for p in range(len(self.memoria[b][0])):
                    n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
                    ubicacion_palabra = str(bin(p))[2:].zfill(n_bits_ubicacion)
                    if self.memoria[b][0][p] == '':
                        dir_dato = " "*self.n_bits_direccion
                        dir_dato_int = "( )"
                    else:
                        dir_dato = self.memoria[b][0][p]
                        dir_dato_int = "({})".format(int(self.memoria[b][0][p], 2))
                    ret += "{} ({})\t\t\t{} ({})\t\t\t\t{} {}\t\t{}\t\t{}\t\t{}\n".format(indice_bloque, b, ubicacion_palabra, p, dir_dato, dir_dato_int, self.memoria[b][1], self.memoria[b][2], self.memoria[b][4])

        elif self.subs == "LRU":
            ret = "CACHE:\nINDICE LINEA\tUBICACION PALABRA\tDIRECCION DATO\tTIEMPO\tDIRTY\n"
            for b in range(len(self.memoria)):
                n_bits_indice = str(bin(self.n_lineas))[2:][::-1].index("1")
                indice_bloque = str(bin(b))[2:].zfill(n_bits_indice)
                for p in range(len(self.memoria[b][0])):
                    n_bits_ubicacion = str(bin(self.line_size))[2:][::-1].index("1")
                    ubicacion_palabra = str(bin(p))[2:].zfill(n_bits_ubicacion)
                    if self.memoria[b][0][p] == '':
                        dir_dato = " "*self.n_bits_direccion
                        dir_dato_int = "( )"
                    else:
                        dir_dato = self.memoria[b][0][p]
                        dir_dato_int = "({})".format(int(self.memoria[b][0][p], 2))
                    ret += "{} ({})\t\t\t{} ({})\t\t\t\t{} {}\t\t{}\t\t{}\n".format(indice_bloque, b, ubicacion_palabra, p, dir_dato, dir_dato_int, self.memoria[b][3], self.memoria[b][4])

        return ret


class MemoriaPrincipal:
    def __init__(self, size):
        self.size = size
        self.n_bits_direccion = str(bin(size))[2:][::-1].index("1")

class Simulacion:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            propiedades = file.read().splitlines()
            propiedades = [x for x in propiedades if x != ""]

        CACHE_SIZE = int(propiedades[0].split("=")[1])
        LINE_SIZE = int(propiedades[1].split("=")[1])
        MEM_SIZE = int(propiedades[2].split("=")[1])
        CORR = propiedades[3].split("=")[1].upper()
        SUBS = propiedades[4].split("=")[1].upper()
        WRITE = propiedades[5].split("=")[1].upper()

        self.cache = Cache(CACHE_SIZE, LINE_SIZE, CORR, SUBS, WRITE, MEM_SIZE)
        self.memoria_principal = MemoriaPrincipal(MEM_SIZE)

        SEC = propiedades[6].split("=")[1].split(",")
        self.secuencia = SEC

    def run(self):
        print("CACHE_SIZE = {}".format(self.cache.size))
        print("LINE_SIZE = {}".format(self.cache.line_size))
        print("MEM_SIZE = {}".format(self.memoria_principal.size))
        print("CORR = {}".format(self.cache.corr))
        print("SUBS = {}".format(self.cache.subs))
        print("WRITE = {}".format(self.cache.write))
        print("SEC = {}\n".format(self.secuencia))

        hits_list = []

        # Se itera sobre la secuencia de peticiones de lectura y escritura.
        print("- ESTADO INICIAL -")
        print(self.cache)
        for data in self.secuencia:

            # TODO: Caso: Lectura
            if not data.upper().endswith("W"):
                dir_dato = int(data)
                print("Peticion Lectura: dir_dato = {}({})".format(str(bin(dir_dato))[2:].zfill(self.memoria_principal.n_bits_direccion), dir_dato))
                # Buscamos en la cache para ver si ya teniamos el dato, si no lo traemos de la memoria principal.
                if self.cache.buscar_dato(dir_dato) == True:
                    # Es un HIT!
                    print("HIT!")
                    self.cache.hits += 1
                    hits_list.append(data)
                else:
                    # Es un MISS -> traemos el dato desde la memoria principal a la cache
                    print("MISS!")
                    self.cache.miss += 1
                    self.cache.traer_dato(dir_dato)


            # TODO: Caso: Escritura
            elif data.upper().endswith("W"):
                dir_dato = int(data[:-1])
                print("Peticion Escritura: dir_dato = {}({})".format(str(bin(dir_dato))[2:].zfill(self.memoria_principal.n_bits_direccion), dir_dato))
                # Buscamos en la cache para ver si ya teniamos el dato, si no lo traemos de la memoria principal.
                if self.cache.buscar_dato(dir_dato, w=True) == True:
                    # Es un HIT! -> ponemos el bit-dirty en 1 al buscar dato
                    print("HIT! (linea dirty)")
                    self.cache.hits += 1
                    hits_list.append(data)
                else:
                    # Es un MISS -> traemos el dato desde la memoria principal a la cache
                    print("MISS! (linea dirty)")
                    self.cache.miss += 1
                    self.cache.traer_dato(dir_dato, w=True)

                self.cache.total_writes += 1

            # Se avanza en 1 unidad de tiempo los tiempos de acceso de cada linea de la cache.
            #print(self.cache)
            self.cache.avanzar_tiempos()

        if self.cache.write == "WT":
            write_rate = 1
        elif self.cache.write == "WB":
            if self.cache.total_writes != 0:
                write_rate = "{}/{} = {}".format(self.cache.hits_write, self.cache.total_writes, self.cache.hits_write/self.cache.total_writes)
            else:
                write_rate = 1

        print("----------------")
        print("Nº HITS = {}".format(self.cache.hits))
        print("Nº MISS = {}".format(self.cache.miss))
        print("HIT-RATE = {}/{} = {}".format(self.cache.hits, self.cache.hits+self.cache.miss, self.cache.hits/(self.cache.hits + self.cache.miss)))
        #print("----------------")
        print("WRITE-RATE = {}".format(write_rate))
        print("----------------")
        print("HITS: {}".format(hits_list))

"""
import sys
filename = str(sys.argv[1])

simulacion = Simulacion(filename)
simulacion.run()
"""

simulacion = Simulacion("test1.txt")
simulacion.run()

