print ("Sistema de empleados")

nombre = "Eduardo"
puesto = "Desarrollador"
salario = 11000

print("Nombre: ", nombre)
print("Puesto: ", puesto)
print("Salario: ",salario)
if salario > 15000:
    print( "Su salalario es mayor a 15000")
elif salario == 15000:
    print ("Su salario es igual a 15000")
else:
    print("su salario es menor a 15000")

empleados  =["carlos", "maria", "juan", "ana"]
print (empleados)
print (empleados [0])
print (empleados [1])
print (empleados [2])
print (empleados [3])

empleados  = ["carlos", "maria", "juan", "ana"]
print ("lista original :" , empleados)

empleados.append("eduardo")
empleados.append("laura")
print("Lisa nueva :", empleados)

def mostrar_empleado():
    for empleado in empleados:
        print("Empleado  :", empleado)

mostrar_empleado()

def registrar_empleado(nombre,puesto,salario):
    print("nombre",nombre)
    print("puesto",puesto)
    print("salario",salario)

registrar_empleado("Eduardo","Desarrollador",11000)
registrar_empleado("Laura","Administradora",16500)
registrar_empleado("Juan","Administrador",12500)

empleado = {
    "nombre": "juan",
    "puesto": "administrador",
    "salario": 12500
}
print ()
print (empleado)
print (empleado["nombre"])
print (empleado["puesto"])
print (empleado["salario"])

print ("-----nuevo tema----------------")

empleados = [{
    "nombre":"juan",
    "puesto":"administrador",
    "salario":12500,
},{
    "nombre":"maria",
    "puesto":"desarrolladora",
    "salario":15000

},
{
    "nombre":"carlos",
    "puesto":"analista",
    "salario":15000
}
]
for empleado in empleados:
    print("Nombre: ", empleado["nombre"])
    print("Puesto: ", empleado["puesto"])
    print("Salario: ", empleado["salario"])
    print("------------")

nuevo_empleado={
    "nombre":"jose",
    "puesto":"desarrollador",
    "salario":16000
}

empleados.append(nuevo_empleado)

print("Lista actualizada")

for empleado in empleados:
    print("Nombre:", empleado["nombre"])
    print("Puesto:", empleado["puesto"])
    print("Salario:", empleado["salario"])
    print("------------")

def buscar_empleado(nombre_buscar):
    encontrado = False

    for empleado in empleados:
        if empleado["nombre"].lower() == nombre_buscar.lower():
            print("Empleado encontrado:")
            print("Nombre:", empleado["nombre"])
            print("Puesto:", empleado["puesto"])
            print("Salario:", empleado["salario"])
            encontrado = True
            break

    if not encontrado:
        print("Empleado no encontrado")


buscar_empleado("maria")

def actualizar_empleado(nombre_buscar, nuevo_puesto, nuevo_salario):
    for empleado in empleados:
        if empleado["nombre"].lower() == nombre_buscar.lower():
            empleado["puesto"]= nuevo_puesto
            empleado["salario"]= nuevo_salario

            print("Empleado actualizado:")
            print("Nombre:", empleado["nombre"])
            print("Puesto:", empleado["puesto"])
            print("Salario:", empleado["salario"])
            return

    print("empleado no encontrado")

actualizar_empleado("juan","Gerente", 18000)

def eliminar_empleado(nombre_buscar):
    for empleado in empleados:
        if empleado["nombre"].lower()== nombre_buscar.lower():
            empleados.remove(empleado)
            print("empleado eliminado correctamente")
            return
        print("empleado no encontrado")
eliminar_empleado("carlos")

print("empleados restantes:")
for empleado in empleados:
    print("nombre:", empleado["nombre"])
    print("puesto:", empleado["puesto"])
    print("salario:", empleado["salario"])
    print("------------")