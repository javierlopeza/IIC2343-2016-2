class Proceso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.paginas_utilizadas = 0
        self.page_faults = 0

        self.tabla_de_paginas = {}  # {8: {"marco": 2, "disco": 0}, 3: {"marco": 2, "disco": 1}, 7: {"marco": 1, "disco": 0}}
        # Si una entrada de la tabla no es válida no estará en el diccionario.
        # Si una entrada de la tabla es válida -> {"pagina_virtual": {"marco": m, "disco": d}}
        #   Si para una entrada de la tabla: validez=1 y disco=0 -> {"pagina_virtual": {"marco": m, "disco": 0}}
        #   Si para una entrada de la tabla: validez=1 y disco=1 -> {"pagina_virtual": {"marco": m, "disco": 1}}

    def __str__(self):
        ret = "\nPROCESO: {}\n".format(self.nombre)
        ret += "Páginas Utilizadas = {}\n".format(len(self.tabla_de_paginas))
        ret += "Page-Faults = {}".format(self.page_faults)
        return ret


class MemoriaVirtual:
    def __init__(self, size, page_size):
        self.size = size
        self.page_size = page_size

        self.n_bits_offset = bin(page_size)[2:][::-1].index('1')
        self.n_bits_pagina = bin(size)[2:][::-1].index('1') - self.n_bits_offset
        self.n_bits_dir = self.n_bits_offset + self.n_bits_pagina

        ##print("n_bits_offset VIR", self.n_bits_offset)
        ##print("n_bits_pagina VIR", self.n_bits_pagina)
        ##print("n_bits_dir", self.n_bits_dir)


class MemoriaPrincipal:
    def __init__(self, size, page_size):
        self.size = size
        self.marco_size = page_size

        self.n_bits_offset = bin(page_size)[2:][::-1].index('1')
        self.n_bits_marco = bin(size)[2:][::-1].index('1') - self.n_bits_offset
        self.n_bits_dir = self.n_bits_offset + self.n_bits_marco

        ##print("n_bits_offset MEM", self.n_bits_offset)
        ##print("n_bits_marco MEM", self.n_bits_marco)

        self.memoria = {}  # {marco_fisico: ["nombre_proceso", orden], ...}
        n_marcos_fisicos = int(size/page_size)
        for marco in range(n_marcos_fisicos):
            self.memoria[marco] = ["", marco + 1]

    def __str__(self):
        ret = "---------------------------------------\n"
        ret += "           MEMORIA PRINCIPAL         \n"
        ret += "---------------------------------------\n"
        ret += "MARCO" + 8*" " + "PROCESO" + 8*" " + "ORDEN\n"
        for marco in self.memoria.keys():
            marco_bin = bin(marco)[2:].zfill(self.n_bits_marco)
            if self.memoria[marco][0] == "":
                proceso = "--" + 13*" "
            else:
                proceso = str(self.memoria[marco][0]) + 13*" "
            ret += "{}({}{}{}\n".format(marco_bin, str(marco) + ")" + " "*(13 - len(str(marco_bin)) - len(str(marco)) - 2), proceso, self.memoria[marco][1])
        return ret

class Simulacion:
    def __init__(self, filename):
        with open(filename) as file:
            propiedades = [x.split("=")[1].strip() for x in file.readlines()]

        VIR_SIZE = int(propiedades[0])
        MEM_SIZE = int(propiedades[1])
        PAGE_SIZE = int(propiedades[2])
        SEC = [x.upper().strip() for x in propiedades[3].split(",")]

        self.secuencia = SEC
        self.proceso_actual = None
        self.procesos = {}  # {"nombre_proceso": Proceso(), ...}

        self.memoria_virtual = MemoriaVirtual(VIR_SIZE, PAGE_SIZE)
        self.memoria_principal = MemoriaPrincipal(MEM_SIZE, PAGE_SIZE)

    def run(self):

        #print("\nEstado Inicial Memoria Principal")
        #print(self.memoria_principal)

        for dato in self.secuencia:
            # Cambio de contexto.
            if dato.startswith("P"):
                #print("\nΞ Cambio de contexto: {} toma el control de la CPU.\n".format(dato))
                # Proceso se reinicia.
                if dato in self.procesos.keys():
                    self.proceso_actual = self.procesos[dato]

                # Proceso se inicia por primera vez.
                else:
                    self.proceso_actual = Proceso(nombre=dato)  # Nuevo proceso.
                    self.procesos[dato] = self.proceso_actual   # Se agrega el nuevo proceso a diccionario de procesos.

            # TODO: Acceso a memoria.
            else:
                #print("Proceso {} solicita acceso a dirección virtual = {}".format(self.proceso_actual.nombre, dato))
                pagina_bin = str(bin(int(dato))[2:]).zfill(self.memoria_virtual.n_bits_dir)[:self.memoria_virtual.n_bits_pagina]
                pagina = int(pagina_bin, 2)
                ##print(pagina_bin, pagina)

                if pagina in self.proceso_actual.tabla_de_paginas:  # TODO: La página está en la tabla de páginas del proceso actual.
                    #print("-> La página está en la tabla de páginas del proceso actual.")
                    if self.proceso_actual.tabla_de_paginas[pagina]["disco"] == 0:  # El marco asociado a la página está en la memoria principal.
                        #print("-> El marco asociado a la página ya está en la memoria principal.")
                        #print(self.proceso_actual.tabla_de_paginas)
                        pass  # OK
                    else:  # TODO: El marco asociado a la página está en el disco (page-fault).
                        #print("-> page-fault : el marco asociado a la página está en el disco.")
                        self.proceso_actual.page_faults += 1

                        # Todos los marcos físicos están en uso. Buscamos cuál hacer swap-out por FIFO (orden == 1).
                        for marco in self.memoria_principal.memoria.keys():
                            if self.memoria_principal.memoria[marco][1] == 1:
                                marco_elegido = marco

                                # Actualizamos la tabla de páginas del proceso asociado al marco que hace swap-out.
                                nombre_proceso_out = self.memoria_principal.memoria[marco_elegido][0]
                                #print("-> swap-out del marco {} asociado al proceso {}.".format(marco_elegido, nombre_proceso_out))
                                for pag in self.procesos[nombre_proceso_out].tabla_de_paginas:
                                    if self.procesos[nombre_proceso_out].tabla_de_paginas[pag]["marco"] == marco_elegido:
                                        # Ahora el marco está en disco por swap-out.
                                        #print("DISCO = 1", nombre_proceso_out, pag, "<------------------------------------------------------------")
                                        self.procesos[nombre_proceso_out].tabla_de_paginas[pag]["disco"] = 1
                                        self.procesos[nombre_proceso_out].tabla_de_paginas[pag]["marco"] = -1

                                        break

                                # Actualizamos la tabla de páginas del proceso actual.
                                self.proceso_actual.tabla_de_paginas[pagina] = {"marco": marco_elegido, "disco": 0}

                                # Mapeamos la página al marco físico.
                                self.memoria_principal.memoria[marco_elegido] = [self.proceso_actual.nombre, len(self.memoria_principal.memoria)]

                                #print("-> Se mapea la página {} del proceso actual {} al marco {}.".format(pagina, self.proceso_actual.nombre, marco_elegido))
                                #print("Proceso OUT:", self.procesos[nombre_proceso_out].tabla_de_paginas)
                                #print("Proceso Actual:",self.proceso_actual.tabla_de_paginas)

                                # Actualizamos los órdenes de FIFO.
                                for marco in self.memoria_principal.memoria.keys():
                                    if marco != marco_elegido:
                                        self.memoria_principal.memoria[marco][1] -= 1
                                break


                        pass

                else:  # TODO: La página no está en la tabla de páginas del proceso actual.
                    #print("-> page-fault : no existe la entrada en la tabla de páginas.")
                    self.proceso_actual.page_faults += 1

                    # Buscamos un marco físico sin uso.
                    marco_vacio = None
                    for marco in sorted(self.memoria_principal.memoria.keys()):
                        if self.memoria_principal.memoria[marco][0] == "":
                            marco_vacio = marco
                            #print("-> Se mapea la página {} del proceso actual {} al marco {} que está sin uso.".format(pagina, self.proceso_actual.nombre, marco_vacio))
                            break
                    if marco_vacio != None:  # Hay un marco físico sin uso.
                        # Agregamos nueva entrada en la tabla de páginas del proceso actual.
                        self.proceso_actual.tabla_de_paginas[pagina] = {"marco": marco_vacio, "disco": 0}

                        # Mapeamos la página al marco físico.
                        self.memoria_principal.memoria[marco_vacio] = [self.proceso_actual.nombre, len(self.memoria_principal.memoria)]

                        # Actualizamos los órdenes de FIFO.
                        for marco in self.memoria_principal.memoria.keys():
                            if marco != marco_vacio:
                                self.memoria_principal.memoria[marco][1] -= 1

                    else:  # Todos los marcos físicos están en uso. Buscamos cuál hacer swap-out por FIFO (orden == 1).
                        for marco in self.memoria_principal.memoria.keys():
                            if self.memoria_principal.memoria[marco][1] == 1:
                                marco_elegido = marco

                                # Actualizamos la tabla de páginas del proceso asociado al marco que hace swap-out.
                                nombre_proceso_out = self.memoria_principal.memoria[marco_elegido][0]
                                #print("-> swap-out del marco {} asociado al proceso {}.".format(marco_elegido, nombre_proceso_out))
                                for pag in self.procesos[nombre_proceso_out].tabla_de_paginas:
                                    if self.procesos[nombre_proceso_out].tabla_de_paginas[pag]["marco"] == marco_elegido:
                                        # Ahora el marco está en disco por swap-out.
                                        #print("DISCO = 1", nombre_proceso_out, pag, "<------------------------------------------------------------")
                                        self.procesos[nombre_proceso_out].tabla_de_paginas[pag]["disco"] = 1
                                        self.procesos[nombre_proceso_out].tabla_de_paginas[pag]["marco"] = -1

                                        break

                                # Agregamos nueva entrada en la tabla de páginas del proceso actual.
                                self.proceso_actual.tabla_de_paginas[pagina] = {"marco": marco_elegido, "disco": 0}

                                # Mapeamos la página al marco físico.
                                self.memoria_principal.memoria[marco_elegido] = [self.proceso_actual.nombre, len(self.memoria_principal.memoria)]

                                #print("-> Se mapea la página {} del proceso actual {} al marco {}.".format(pagina, self.proceso_actual.nombre, marco_elegido))
                                #print("Proceso OUT:", self.procesos[nombre_proceso_out].tabla_de_paginas)
                                #print("Proceso Actual:", self.proceso_actual.tabla_de_paginas)


                                # Actualizamos los órdenes de FIFO.
                                for marco in self.memoria_principal.memoria.keys():
                                    if marco != marco_elegido:
                                        self.memoria_principal.memoria[marco][1] -= 1
                                break

                #print(self.memoria_principal)

        for proceso in sorted(self.procesos.keys()):
            print(self.procesos[proceso])

"""
simulacion = Simulacion("test4lagos.txt")
simulacion.run()
"""

import sys
filename = str(sys.argv[1])

simulacion = Simulacion(filename)
simulacion.run()
