from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
import Util

from Contacto import Contacto

#Lista de imágenes para los botones
iconos = ["./iconos/agregar.png", \
          "./iconos/editar.png", \
          "./iconos/eliminar.png", \
          "./iconos/guardar.png", \
          "./iconos/ordenar.png", \
          "./iconos/aceptar.png", \
          "./iconos/cancelar.png", \
          ]

#Lista de tooltips para los botones
textosTooltip = [ "agregar Contacto", \
                  "modificar Contacto", \
                  "quitar Contacto", \
                  "guardar los cambios realizados", \
                  "ordenar la lista de contactos", \
                  "aceptar los cambios", \
                  "cancelar la edición"
                  ]

#posiciones de los botones de edición para habilitarlos/deshabilitarlos
indiceBA = 5
indiceBC = 6

#Lista de encabezados de la tabla de datos
encabezados = ["ID", \
               "Nombre", \
               "Correo", \
               "Móvil"
               ]
#lista de paneles: Panel de lista y panel de edición
paneles = []
#Objeto tabla para despliegue de los datos
tContactos = None

#subrutina que cambia el ambiente de LISTAR a EDITAR y viceversa
def habilitar(editando):
    global indiceBA, indiceBC
    #Cambiar el estado de los botones
    for i in range(0, len(botones)):
        if editando:
            if i!=indiceBA and i!=indiceBC:
                botones[i].configure(state=DISABLED)
            else:
                botones[i].configure(state=NORMAL)
        else:
            if i!=indiceBA and i!=indiceBC:
                botones[i].configure(state=NORMAL)
            else:
                botones[i].configure(state=DISABLED)
    #Desplegar el panel respectivo
    if len(nb.tabs())>0:
        nb.forget(0) #limpiar las pestañas
    if editando:
        nb.add(paneles[1], text="Editando Contacto")
    else:
        nb.add(paneles[0], text="Lista de contactos")
    nb.focus() #refrescar las pestañas

#Metodo que muestra los contactos en una tabla
def mostrar():
    global tContactos
    datos = Contacto.pasarMatriz()
    tContactos = Util.mostrarTabla(paneles[0], encabezados, datos, tContactos)

#Método para limpiar los objetos de la edicion de un Contacto
def limpiar():
    #Dejar los controles vacíos
    txtId.delete(0, END)
    txtNombre.delete(0, END)
    txtCorreo.delete(0, END)
    txtMovil.delete(0, END)
    #paneles[1].Text = "Editando datos de un nuevo Contacto"

#Metodo para ir a la edición de un registro
def iniciarEdicion():
    habilitar(True)
    #Se esta editando un Contacto existente?
    if Contacto.indice >= 0:
        c = Contacto.contactos[Contacto.indice]
        if c != None:
            Util.mostrar(txtId, c.id, False)
            Util.mostrar(txtNombre, c.nombre, False)
            Util.mostrar(txtCorreo, c.correo, False)
            Util.mostrar(txtMovil, c.movil, False)
            #paneles[1].Text = "Editando datos del Contacto [" + c.nombre + "]"
    else:
        limpiar()

def agregar():
    Contacto.indice = -1
    iniciarEdicion()
    
def modificar():
    global tContactos
    #verificar si hay un contacto seleccionado
    if tContactos.selection():
        Contacto.indice = tContactos.index(tContactos.selection())
        iniciarEdicion()
    else:
        messagebox.showinfo("", "debe seleccionar un contacto")

def eliminar():
    global tContactos
    #verificar si hay un contacto seleccionado
    if tContactos.selection():
        decision = messagebox.askquestion("Eliminando Contacto", "Está seguro?")
        if decision == "yes":
            #indice del contacto a eliminar
            Contacto.indice = tContactos.index(tContactos.selection())
            Contacto.eliminar()
            mostrar()
            messagebox.showinfo("", "El contacto fue retirado")
    else:
        messagebox.showinfo("", "debe seleccionar un contacto")

def guardar():
    Contacto.guardar("Contactos.json")
    messagebox.showinfo("", "La información fue guardada en disco")

def ordenar():
    Contacto.ordenar()
    mostrar()
    messagebox.showinfo("", "La lista de conatctos fue ordenada")

def aceptar():
    #verificar si se está agregando un contacto
    if Contacto.indice == -1:
        Contacto.agregar(txtId.get(), \
                         txtNombre.get(), \
                         txtCorreo.get(), \
                         txtMovil.get() )
        messagebox.showinfo("", "Contacto agregado al final de la lista")
    else:
        #Estoy modificando un contacto
        Contacto.modificar(txtId.get(), \
                         txtNombre.get(), \
                         txtCorreo.get(), \
                         txtMovil.get() )
    #Volver al modo de listado
    habilitar(False)
    mostrar()
    

def cancelar():
    #Volver al modo de listado
    habilitar(False)

#Construir interfaz gráfica
v = Tk()
v.title("Mis contactos")
botones = Util.agregarBarra(v, iconos, textosTooltip) #Agrega una barra de herramientas
nb = Notebook(v)
nb.pack(fill=BOTH, expand=YES)

paneles.append(Frame(v)) #panel de listado
paneles.append(Frame(v)) #panel de edición

#Objetos para editar un Contacto
Util.agregarEtiqueta(paneles[1], "ID:", 0, 0)
Util.agregarEtiqueta(paneles[1], "Nombre:", 1, 0)
Util.agregarEtiqueta(paneles[1], "Correo", 2, 0)
Util.agregarEtiqueta(paneles[1], "Móvil", 3, 0)
txtId=Util.agregarTexto(paneles[1], 15, 0, 1)
txtNombre=Util.agregarTexto(paneles[1], 30, 1, 1)
txtCorreo=Util.agregarTexto(paneles[1], 30, 2, 1)
txtMovil=Util.agregarTexto(paneles[1], 30, 3, 1)

#Comenzar con el despliegue de los datos

habilitar(False)
Contacto.obtener("Contactos.csv")
mostrar()

#Agregar los eventos asociados a los botones
botones[0].configure(command=agregar)
botones[1].configure(command=modificar)
botones[2].configure(command=eliminar)
botones[3].configure(command=guardar)
botones[4].configure(command=ordenar)
botones[5].configure(command=aceptar)
botones[6].configure(command=cancelar)



