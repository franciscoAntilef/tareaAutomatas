from DataStruct.Stack import Stack
from DataStruct.Queue import Queue

transiciones = []
pilaMemoria = Stack()
estadoInicial = ""
palabraEntrada = ""
colaEntrada = Queue()
estadoFinal =        ""

def transicion_esta_correcta(tran):
    ##hay que modificar esto
    return tran[0]!='(' or tran[2]!=',' or tran[4]!=',' or tran[6]!=')' or tran[7]!='=' or tran[8]!='(' or tran[10]!=',' or tran[len(tran)-1]!=')'
        
def pide_transiciones(transiciones):
    tran=input("Ingrese las transiciones (presiones ENTER para terminar,exit para terminar la ejecucion del programa):")
    tran=tran.replace(' ','')
    while tran!="":
        while(transicion_esta_correcta(tran) and tran!="exit"):
            tran=input("Error...Ingrese las transiciones otra vez:")
            tran=tran.replace(' ','')
        if (tran=="exit"):
            while(tran!="S" and tran!="s" and tran!="N" and tran!="n"):
                tran=input("Ha elegido salir de el programa, ¿Esta usted seguro de salir? s(si) - n(no)")
            if(tran=="S" or tran=="s"):
                return True
        transiciones.append(tran)
        tran=input("Ingrese las transiciones (presiones ENTER para terminar):")
        tran=tran.replace(' ','')
    if transiciones==[]:
        return True
    else:
        return False
        
def por_stack_vacio():
    resp=str(input("El automata acepta por stack vacio(1) o estado final(2)?:"))
    resp=resp.replace(' ','')
    while resp not in ("1","2"):
        resp=str(input("Error...El automata acepta por stack vacio(1) o estado final(2)?:"))
        resp=resp.replace(' ','')
    return resp=="1"

def validaEntrada(mensaje):
    estado=str(input(mensaje))
    estado=estado.replace(' ','')
    while estado=="":
        estado=str(input("Error..."+mensaje))
        estado=estado.replace(' ','')
    return estado

def buscar_transicion(transiciones,estadoActual,sim,variableStack):
    pos=0
    while pos<len(transiciones):
        if transiciones[pos][1]==estadoActual and transiciones[pos][3]==sim and transiciones[pos][5]==variableStack :
            return transiciones[pos]
        pos = pos + 1
    return ""

def apilado(pilaMemoria,tran):
    pos=11
    print("Transición detectada: ")
    print(tran)
    if(tran[11]!="E"):
        pilaMemoria.apilar(tran[5])
    while pos<len(tran)-2:
        print("se Agrega símbolo ",tran[pos]," en posición:",pos)
        pilaMemoria.apilar(tran[pos])
        print("Pila de memoria:")
        if(not pilaMemoria.es_vacia()):
            for x in pilaMemoria.items:
                print (x)
        pos = pos + 1
    #Agrego la condición de que si el stack está vacío: entonces "E" (epsilon) es situado en la tapa para representar que está vacío
    #Esto es necesario para cierto tipo de transiciones, en donde se pregunta si el stack está vacío
    if(pilaMemoria.es_vacia()):
        pilaMemoria.apilar("E")
        print("PILA VACÍA")
    print()

def calculaTransiciones(transiciones,estadoInicial,colaEntrada,pilaMemoria,acept):
    iteracion = 1
    estadoActual= estadoInicial 
    while(not colaEntrada.es_vacia()):
        print("****************")
        print("Cola entrada:")
        for x in colaEntrada.items:
            print(x,end=" ")  
        sim = colaEntrada.desencolar()
        #Si la pila esta vacía, quiere decir que no se puede continuar
        print("pila: ")
        for x in pilaMemoria.items :
            print(x)
        variableStack=pilaMemoria.desapilar()
        print(" estadoActual: ",estadoActual," sim: ",sim," variableStack: ",variableStack)
        tran=buscar_transicion(transiciones,estadoActual,sim,variableStack)
        print(tran)
        #Agregada nueva condición: si el símbolo leido es E, quiere decir que llegamos al final de la palabra
        #Por lo tanto, es posible que no hayan más trnasiciones
        #Esto debido a que no todos los automatas tienen transiciones cuando leen un epsilon
        #Si no existe la transición y llegamos al final de la palabra, devolvemos
        #si es que habia el simbolo que quitamos anteriormente
        if (sim=="E" and tran==""):
            pilaMemoria.apilar(variableStack)
            return 1
        #Si existe la transición, pasará a este "elif", en donde se procede normalmente
        elif(tran!=""):
            estadoActual=tran[9]
            apilado(pilaMemoria,tran)
        #En el caso de no estar leyendo "E", y la transición no existe: queire decir que el APD no acepta la palabra:
        else:
            print("no existe la transicion ")
            return -1
        print("termino la iteracion: ",iteracion)
        print("*****************")
        iteracion=iteracion+1
    print("Estado Final: ",estadoActual)
    return estadoActual


def apd_stack_vacio(transiciones,estadoInicial,colaEntrada,pilaMemoria):
    existe=calculaTransiciones(transiciones,estadoInicial,colaEntrada,pilaMemoria,"pilaVacia")
    #Agregada nueva condición: si existe==-1 quiere decir que una transición no existe,
    #Y por lo tanto: la palabra no es aceptada por el APD
    if(pilaMemoria.desapilar()=="E" and existe!=-1):
        return True
    else:
        return False

def apd_estado_final(transiciones,estadoInicial,colaEntrada,estado_final,pilaMemoria):
    final=calculaTransiciones(transiciones,estadoInicial,colaEntrada,pilaMemoria,"estadoFinal")
    #Agregada nueva condición: si final =-1, significa que no existe una transición,
    #Y por lo tanto: que la palabra no es aceptada por el APD
    if(final==estado_final and final!=-1):
        return True
    else:
        return False

def crearPalabra(palabraEntrada,colaEntrada):
    pos=0
    while pos<len(palabraEntrada):
        colaEntrada.encolar(palabraEntrada[pos])
        pos = pos + 1

def main():
    #PRESENTACIÓN:
    print("Bienvenido a nuesta super tarea salvaje(la epsilon=E )")
    print("Al momento de escribir las transiciones, se puede escribir el comando 'exit' (sin comillas) para salir del programa")
    print("Las transiciones deben ingresarse de la forma:")
    print("          (1,a,R)=('2','RA')")
    print("o tambien (q,b,R)=(w,AAR)   ")
    print()
    print("Donde cada elemento es:")
    print("   1(q) :Estado actual (los nodos solo se pueden representar por números)")
    print("   a(b) :El símbolo leido en la palabra (puede que ser cualquier símbolo)")
    print("   R :Símbolo en la tapa del stack al leer la símnolo de la palabra")
    print("   2(w) :estado final al completarse la transición")
    print("   RA(AAR) : 'A' Se apilará en la tapa del stack")
    print("No se puede usar la letra 'E' como simbolo de palabra ni del Stack, ya que está reservada por el programa(si se el programa no funcionará de manera correcta)")
    print("Por último, el símbolo inicial del stack de memoria siempre es :'R'")
    print()
    print()
    #Se inica el código
    salir=False
    salir=pide_transiciones(transiciones)
    while(transiciones==[] and salir==False):
        print("Error, no se han ingresado transiciones, por favor ingrese transiciones o ")
        salir=pide_transiciones(transiciones)
    while(salir==False):
        pilaMemoria.apilar("R")
        estadoInicial = validaEntrada("Ingrese el estado Inicial : ")
        palabraEntrada = validaEntrada("Ingrese la palabra de entrada : ")
        crearPalabra(palabraEntrada,colaEntrada)
        colaEntrada.encolar("E")
        if(por_stack_vacio() ):
            if(apd_stack_vacio(transiciones,estadoInicial,colaEntrada,pilaMemoria)):
                print("La palabra es aceptado por el APD por stack vacio")
            else:
                print("La palabra NO es aceptado por el APD por stack vacio ") 
        
        else:
            for x in pilaMemoria.items:
                print(x)
            estadoFinal=validaEntrada("Ingrese el estado Final : ")
            if(apd_estado_final(transiciones,estadoInicial,colaEntrada,estadoFinal,pilaMemoria)):
                print("La palabra es aceptado por el APD por estado final")
            else:
                print("La palabra NO es aceptada por el APD por estado final ")
        
        pregunta=str(input("Quiere ingresar otra palabra para este autómata? S(si) - N(no:El programa finalizará)"))
        pregunta=pregunta.replace(' ','')
        while pregunta not in ("S","N","n"):
            pregunta=str(input("Error...Debe ingresar 'S' o 'N' : "))
            pregunta=pregunta.replace(' ','')
        if pregunta=="N" or pregunta=="n":
            salir=True
        while (not pilaMemoria.es_vacia()):
            pilaMemoria.desapilar()
        while(not colaEntrada.es_vacia()):
            colaEntrada.desencolar()
    print("Fin de la Ejecucion.....Que tenga buen día! :3")
    input()
            
main()
