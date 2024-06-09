from tkinter import *
from tkinter import messagebox
import sqlite3
import os


def main_window():
    root = Tk()
    root.title("Aplicación")

    # Funciones para abrir formularios de usuarios, productos y ventas
    def open_user_form():
        form_users()

    def open_product_form():
        form_product()

    def open_sales_form():
        form_ventas()

    # Barra de menú
    barraMenu = Menu(root)
    root.config(menu=barraMenu, width=300, height=300)

    BBDDMenu = Menu(barraMenu, tearoff=0)
    BBDDMenu.add_command(label="Crear Base De Datos", command=elegir_bd)
    BBDDMenu.add_command(label="Salir", command=SalirApp)

    Deletemenu = Menu(barraMenu, tearoff=0)
    Deletemenu.add_command(label="Borrar Campos", command=LimpiarCamposUsuarios)

    CRUDMenu = Menu(barraMenu, tearoff=0)
    CRUDMenu.add_command(label="Crear Registro", command=CrearRegistroUsuarios)
    CRUDMenu.add_command(label="Leer Registro", command=leerRegistros)
    CRUDMenu.add_command(label="Actualizar Registro", command=actualizarRegistro)
    CRUDMenu.add_command(label="Borrar Registro", command=EliminarRegistro)

    HelpMenu = Menu(barraMenu, tearoff=0)
    HelpMenu.add_command(label="Acerca de:")

    barraMenu.add_cascade(label="Base De Datos", menu=BBDDMenu)
    barraMenu.add_cascade(label="Borrar", menu=Deletemenu)
    barraMenu.add_cascade(label="CRUD", menu=CRUDMenu)
    barraMenu.add_cascade(label="Ayuda", menu=HelpMenu)

    # Botones en la ventana principal
    btn_frame = Frame(root)
    btn_frame.pack()

    btn_users = Button(btn_frame, text="Usuarios", command=open_user_form)
    btn_users.grid(row=0, column=0, padx=5, pady=5)

    btn_products = Button(btn_frame, text="Productos", command=open_product_form)
    btn_products.grid(row=0, column=1, padx=5, pady=5)

    btn_sales = Button(btn_frame, text="Ventas", command=open_sales_form)
    btn_sales.grid(row=0, column=2, padx=5, pady=5)

    root.mainloop()



#--------------------------FUNCIONES--------------------------------
#ELEGIR BBDD


def elegir_bd():
    def seleccionar_cliente():
        ConectionBDUsuarios()
        raiz.destroy()

    def seleccionar_producto():
        ConectionBDProductos()
        raiz.destroy()

    def seleccionar_ventas():
        ConectionBDVentas()
        raiz.destroy()

    def cancelar():
        print("Operación cancelada.")
        raiz.destroy()

    raiz = Tk()
    raiz.title("Elige tu Base de Datos")

    miFrame3 = Frame(raiz)
    miFrame3.pack()

    Label(miFrame3, text="Elige la base de Datos:", width=50).pack()

    # Botones
    boton_clientes = Button(miFrame3, text="Clientes", width=10, command=seleccionar_cliente)
    boton_clientes.pack(side="left", padx=5, pady=5)

    boton_productos = Button(miFrame3, text="Productos", width=10, command=seleccionar_producto)
    boton_productos.pack(side="left", padx=5, pady=5)

    boton_ventas = Button(miFrame3, text="Ventas", width=10, command=seleccionar_ventas)
    boton_ventas.pack(side="left", padx=5, pady=5)

    boton_cancelar = Button(miFrame3, text="Cancelar", width=10, command=cancelar)
    boton_cancelar.pack(side="right", padx=5, pady=5)

    raiz.mainloop()
#CREAR BBDD
def ConectionBDUsuarios():
    miBase = sqlite3.connect("Usuarios")
    miCursor = miBase.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS DATOSUSUARIOS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_USUARIO VARCHAR(100),
                APELLIDO_USUARIO VARCHAR(100),
                PASSWORD VARCHAR(50),
                DIRECCION VARCHAR(100),
                COMENTARIO VARCHAR(200)
            )
        ''')
        messagebox.showinfo("BBDD", "Base de Datos de Usuarios creada con exito")
    except Exception as e:
        messagebox.showwarning("ERROR", f"Error creando la Base de Datos: {e}")
    finally:
        miBase.close()

def ConectionBDProductos():
    miBase1 = sqlite3.connect("Productos")
    miCursor = miBase1.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS PRODUCTOS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_PRODUCTO VARCHAR(100),
                PRECIO_PRODUCTO INTEGER,
                CODIGO_REFERENCIA VARCHAR(50)
            )
        ''')
        messagebox.showinfo("BBDD", "Base de Datos de Productos creada con exito")
    except Exception as e:
        messagebox.showwarning("ERROR", f"Error creando la Base de Datos: {e}")
    finally:
        miBase1.close()

def ConectionBDVentas():
    miBase2 = sqlite3.connect("Ventas")
    miCursor = miBase2.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS VENTAS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_PRODUCTO VARCHAR(100),
                DESTINO VARCHAR(100),
                REFERENCIA_PRODUCTO VARCHAR(100)
            )
        ''')
        messagebox.showinfo("BBDD", "Base de Datos de Ventas creada con exito")
    except Exception as e:
        messagebox.showwarning("ERROR", f"Error creando la Base de Datos: {e}")
    finally:
        miBase2.close()


#SALIR APP
def SalirApp():
    valor = messagebox.askquestion("Salir", "¿Deseas salir?")
    if valor == "yes":
        root.destroy()

#CREAR REGISTRO
def CrearRegistroUsuarios():
    global cuadroNombre, cuadroApellido, cuadroPass, cuadroDireccion, textoComentario
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    try:
        miCursor.execute(
            "INSERT INTO DATOSUSUARIOS (NOMBRE_USUARIO, APELLIDO_USUARIO, PASSWORD, DIRECCION, COMENTARIO) VALUES (?, ?, ?, ?, ?)",
            (cuadroNombre.get(), cuadroApellido.get(), cuadroPass.get(), cuadroDireccion.get(), textoComentario.get("1.0", "end-1c"))
        )
        miConexion.commit()
        messagebox.showinfo("BBDD", "Registro añadido correctamente")
    except Exception as e:
        miConexion.rollback()
        messagebox.showerror("BBDD", f"Error al añadir registro: {e}")
    finally:
        miConexion.close()

def CrearRegistroProductos():
    global cuadroNombre, cuadroPrecio, cuadroRef
    miConexion = sqlite3.connect("Productos")
    miCursor = miConexion.cursor()
    try:
        miCursor.execute(
            "INSERT INTO PRODUCTOS (NOMBRE_PRODUCTO, PRECIO_PRODUCTO, CODIGO_REFERENCIA) VALUES (?, ?, ?)",
            (cuadroNombre.get(), cuadroPrecio.get(), cuadroRef.get())
        )
        miConexion.commit()
        messagebox.showinfo("BBDD", "Registro añadido correctamente")
    except Exception as e:
        miConexion.rollback()
        messagebox.showerror("BBDD", f"Error al añadir registro: {e}")
    finally:
        miConexion.close()

def CrearRegistroVentas():
    global cuadroNombreProducto, cuadroDestino, cuadroRefe
    miConexion = sqlite3.connect("Ventas")
    miCursor = miConexion.cursor()
    try:
        miCursor.execute(
            "INSERT INTO VENTAS (NOMBRE_PRODUCTO, DESTINO, REFERENCIA_PRODUCTO) VALUES (?, ?, ?)",
            (cuadroNombreProducto.get(), cuadroDestino.get(), cuadroRefe.get())
        )
        miConexion.commit()
        messagebox.showinfo("BBDD", "Registro añadido correctamente")
    except Exception as e:
        miConexion.rollback()
        messagebox.showerror("BBDD", f"Error al añadir registro: {e}")
    finally:
        miConexion.close()
#LIMPIAR CAMPOS
def LimpiarCamposUsuarios():
    global miId, Nombre, Apellido, Passw, Adrees
    miId.set("")
    Nombre.set("")
    Apellido.set("")
    Passw.set("")
    Adrees.set("")
    textoComentario.delete(1.0, END)
    
def LimpiarCamposArticulos():
    global IdProductos, Nombre_Articulo, Precio_Articulo, CodRef
    IdProductos.set("")
    Nombre_Articulo.set("")
    Precio_Articulo.set("")
    
def LimpiarCamposVentas():
    global IdVentas, Nombre_ArticuloV, Destino, CodRefV
    IdVentas.set("")
    Nombre_ArticuloV.set("")
    Destino.set("")
    CodRefV.set("")

#LEER REGISTROS
def leerRegistros():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID = ?", (miId.get(),))
    elUsuario = miCursor.fetchall()
    for usuario in elUsuario:
        miId.set(usuario[0])
        Nombre.set(usuario[1])
        Apellido.set(usuario[2])
        Passw.set(usuario[3])
        Adrees.set(usuario[4])
        textoComentario.insert(1.0, usuario[5])
    miConexion.commit()
    miConexion.close()

#ACTUALIZAR REGISTRO
def actualizarRegistro():
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO = ?, APELLIDO_USUARIO = ?, PASSWORD = ?, DIRECCION = ?, COMENTARIO = ? WHERE ID = ?", 
                    (Nombre.get(), Apellido.get(), Passw.get(), Adrees.get(), textoComentario.get(1.0, "end-1c"), miId.get()))
    miConexion.commit()
    miConexion.close()
    messagebox.showinfo("Actualizado", "Registro actualizado con éxito")

def EliminarRegistro():
    eliminar = messagebox.askyesno("Eliminar Registro", "¿Desea eliminar el registro?")
    
    if eliminar:
        miConexion = sqlite3.connect("Usuarios")
        miCursor = miConexion.cursor()
        try:
            miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID = ?", (miId.get(),))
            miConexion.commit()
            messagebox.showinfo("Eliminar registro", "El registro ha sido eliminado correctamente")
        except Exception as e:
            miConexion.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
        finally:
            miConexion.close()
    else:
        messagebox.showinfo("Operación Cancelada", "No se ha eliminado el registro.")

#ELIMINAR BBDD
def BorrarBDDUsuarios():
    eliminar = messagebox.askyesno("Eliminar Base de Datos", "¿Desea eliminar la Base de Datos de Usuarios?")
    if eliminar:
        try:
            os.remove("Usuarios")
            messagebox.showinfo("Base de Datos Eliminada", "La base de datos de Usuarios ha sido eliminada exitosamente.")
        except FileNotFoundError:
            messagebox.showerror("Error", "La base de datos de Usuarios no existe.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la base de datos de Usuarios: {e}")
    else:
        messagebox.showinfo("Operación Cancelada", "No se ha eliminado la base de datos de Usuarios.")

def BorrarBDDProductos():
    eliminar = messagebox.askyesno("Eliminar Base de Datos", "¿Desea eliminar la Base de Datos de Productos?")
    if eliminar:
        try:
            os.remove("Productos")
            messagebox.showinfo("Base de Datos Eliminada", "La base de datos de Productos ha sido eliminada exitosamente.")
        except FileNotFoundError:
            messagebox.showerror("Error", "La base de datos de Productos no existe.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la base de datos de Productos: {e}")
    else:
        messagebox.showinfo("Operación Cancelada", "No se ha eliminado la base de datos de Productos.")

def BorrarBDDVentas():
    eliminar = messagebox.askyesno("Eliminar Base de Datos", "¿Desea eliminar la Base de Datos de Ventas?")
    if eliminar:
        try:
            os.remove("Ventas")
            messagebox.showinfo("Base de Datos Eliminada", "La base de datos de Ventas ha sido eliminada exitosamente.")
        except FileNotFoundError:
            messagebox.showerror("Error", "La base de datos de Ventas no existe.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la base de datos de Ventas: {e}")
    else:
        messagebox.showinfo("Operación Cancelada", "No se ha eliminado la base de datos de Ventas.")

def Ventana_BorrarBDD():
    raiz1 = Tk()
    raiz1.title("Elegir Base de Datos a Eliminar")
    
    BotonClientes = Button(raiz1, text="Clientes", width=10, command=BorrarBDDUsuarios)
    BotonClientes.grid(row=1, column=0, sticky="e", padx=10, pady=10)
    
    BotonProductos = Button(raiz1, text="Productos", width=10, command=BorrarBDDProductos)
    BotonProductos.grid(row=1, column=1, sticky="e", padx=10, pady=10)
    
    BotonVentas = Button(raiz1, text="Ventas", width=10, command=BorrarBDDVentas)
    BotonVentas.grid(row=1, column=2, sticky="e", padx=10, pady=10)
    
    raiz1.mainloop()

root = Tk()
root.title("Aplicación")
#-----------------------CREACION DE MENUS-----------------------------
barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)

BBDDMenu = Menu(barraMenu, tearoff=0)
BBDDMenu.add_command(label="Crear Base De Datos", command=elegir_bd)
BBDDMenu.add_command(label="Salir", command=SalirApp)

Deletemenu = Menu(barraMenu, tearoff=0)
Deletemenu.add_command(label="Borrar Campos", command=LimpiarCamposUsuarios)

CRUDMenu = Menu(barraMenu, tearoff=0)
CRUDMenu.add_command(label="Crear Registro", command=CrearRegistroUsuarios)
CRUDMenu.add_command(label="Leer Registro", command=leerRegistros) # Añadir la función de lectura
CRUDMenu.add_command(label="Actualizar Registro", command=actualizarRegistro)
CRUDMenu.add_command(label="Borrar Registro", command=EliminarRegistro)

HelpMenu = Menu(barraMenu, tearoff=0)
HelpMenu.add_command(label="Acerca de:")

barraMenu.add_cascade(label="Base De Datos", menu=BBDDMenu)
barraMenu.add_cascade(label="Borrar", menu=Deletemenu)
barraMenu.add_cascade(label="CRUD", menu=CRUDMenu)
barraMenu.add_cascade(label="Ayuda", menu=HelpMenu)

#---------------------FORMULARIO USUARIOS-------------------------
def form_users():
    miFrame = Frame(root)
    miFrame.pack()

    miId = StringVar()
    Nombre = StringVar()
    Apellido = StringVar()
    Passw = StringVar()
    Adrees = StringVar()

    cuadroID = Entry(miFrame, textvariable=miId)
    cuadroID.grid(row=0, column=1, padx=10, pady=10)

    cuadroNombre = Entry(miFrame, textvariable=Nombre)
    cuadroNombre.grid(row=1, column=1, padx=10, pady=10)

    cuadroApellido = Entry(miFrame, textvariable=Apellido)
    cuadroApellido.grid(row=2, column=1, padx=10, pady=10)

    cuadroPass = Entry(miFrame, textvariable=Passw)
    cuadroPass.grid(row=3, column=1, padx=10, pady=10)
    cuadroPass.config(show="*")

    cuadroDireccion = Entry(miFrame, textvariable=Adrees)
    cuadroDireccion.grid(row=4, column=1, padx=10, pady=10)

    textoComentario = Text(miFrame, width=16, height=5)
    textoComentario.grid(row=5, column=1, padx=10, pady=10)

    #-----------------------BARRA DESPLAZAMIENTO-----------------
    scrollVert = Scrollbar(miFrame, command=textoComentario.yview)
    scrollVert.grid(row=5, column=2, sticky="nsew")
    textoComentario.config(yscrollcommand=scrollVert.set)

    #------------------- AGREGAMOS LABEL-------------------
    ID = Label(miFrame, text="ID")
    ID.grid(row=0, column=0, sticky="e", padx=10, pady=10)

    Name = Label(miFrame, text="Nombre")
    Name.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    Surname = Label(miFrame, text="Apellido")
    Surname.grid(row=2, column=0, sticky="e", padx=10, pady=10)

    Pass = Label(miFrame, text="Contraseña")
    Pass.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    Adress = Label(miFrame, text="Dirección")
    Adress.grid(row=4, column=0, sticky="e", padx=10, pady=10)

    Comments = Label(miFrame, text="Comentario")
    Comments.grid(row=5, column=0, sticky="e", padx=10, pady=10)

    #-------------------BOTONES----------------------
    miFrame2 = Frame(root)
    miFrame2.pack()
    BotonCrear = Button(miFrame2, text="Crear", width=10, command=CrearRegistroUsuarios)
    BotonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)
    BotonRead = Button(miFrame2, text="Leer", width=10, command=leerRegistros)
    BotonRead.grid(row=1, column=1, sticky="e", padx=10, pady=10)
    BotonUpdate = Button(miFrame2, text="Actualizar", width=10, command=actualizarRegistro)
    BotonUpdate.grid(row=1, column=2, sticky="e", padx=10, pady=10)
    BotonDelete = Button(miFrame2, text="Borrar BBDD", width=10, command=Ventana_BorrarBDD)
    BotonDelete.grid(row=1, column=3, sticky="e", padx=10, pady=10)

    #---------------------FORMULARIO PRODUCTOS---------------
def form_product():
        miFrame = Frame(root)
        miFrame.pack()

        IdProductos = StringVar()
        Nombre_Articulo = StringVar()
        Precio_Articulo = IntVar()
        CodRef = StringVar()


        cuadroIDProduct = Entry(miFrame, textvariable=IdProductos)
        cuadroIDProduct.grid(row=0, column=1, padx=10, pady=10)

        cuadroNombreArt = Entry(miFrame, textvariable=Nombre_Articulo)
        cuadroNombreArt.grid(row=1, column=1, padx=10, pady=10)

        cuadroPrecio = Entry(miFrame, textvariable=Precio_Articulo)
        cuadroPrecio.grid(row=2, column=1, padx=10, pady=10)

        cuadroRef = Entry(miFrame, textvariable=CodRef)
        cuadroRef.grid(row=3, column=1, padx=10, pady=10)




        #------------------- AGREGAMOS LABEL-------------------
        ID = Label(miFrame, text="ID")
        ID.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        NameProducto = Label(miFrame, text="Producto")
        NameProducto.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        PrecioProducto = Label(miFrame, text="Precio")
        PrecioProducto.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        CodReferencia = Label(miFrame, text="Referencia")
        CodReferencia.grid(row=3, column=0, sticky="e", padx=10, pady=10)



        #-------------------BOTONES----------------------
        miFrame2 = Frame(root)
        miFrame2.pack()
        BotonCrear = Button(miFrame2, text="Crear", width=10, command=CrearRegistroUsuarios)
        BotonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        BotonRead = Button(miFrame2, text="Leer", width=10, command=leerRegistros)
        BotonRead.grid(row=1, column=1, sticky="e", padx=10, pady=10)
        BotonUpdate = Button(miFrame2, text="Actualizar", width=10, command=actualizarRegistro)
        BotonUpdate.grid(row=1, column=2, sticky="e", padx=10, pady=10)
        BotonDelete = Button(miFrame2, text="Borrar BBDD", width=10, command=Ventana_BorrarBDD)
        BotonDelete.grid(row=1, column=3, sticky="e", padx=10, pady=10)

    #----------------------FORMULARIO VENTAS ------------------------ 
def form_ventas():
    miFrame = Frame(root)
    miFrame.pack()

    IdVentas = StringVar()
    Nombre_ArticuloV = StringVar()
    Destino = StringVar()
    CodRefv = StringVar()


    cuadroIDVentas = Entry(miFrame, textvariable=IdVentas)
    cuadroIDVentas.grid(row=0, column=1, padx=10, pady=10)

    cuadroNombreProducto = Entry(miFrame, textvariable=Nombre_ArticuloV)
    cuadroNombreProducto.grid(row=1, column=1, padx=10, pady=10)

    cuadroDestino = Entry(miFrame, textvariable=Destino)
    cuadroDestino.grid(row=2, column=1, padx=10, pady=10)

    cuadroRefe = Entry(miFrame, textvariable=CodRefv)
    cuadroRefe.grid(row=3, column=1, padx=10, pady=10)





    #------------------- AGREGAMOS LABEL-------------------
    ID = Label(miFrame, text="ID")
    ID.grid(row=0, column=0, sticky="e", padx=10, pady=10)

    Name_Venta = Label(miFrame, text="Nombre")
    Name_Venta.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    Destino_Venta = Label(miFrame, text="Apellido")
    Destino_Venta.grid(row=2, column=0, sticky="e", padx=10, pady=10)

    RefernciaVenta = Label(miFrame, text="Contraseña")
    RefernciaVenta.grid(row=3, column=0, sticky="e", padx=10, pady=10)



    #-------------------BOTONES----------------------
miFrame2 = Frame(root)
miFrame2.pack()
BotonCrear = Button(miFrame2, text="Crear", width=10, command=CrearRegistroUsuarios)
BotonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)
BotonRead = Button(miFrame2, text="Leer", width=10, command=leerRegistros)
BotonRead.grid(row=1, column=1, sticky="e", padx=10, pady=10)
BotonUpdate = Button(miFrame2, text="Actualizar", width=10, command=actualizarRegistro)
BotonUpdate.grid(row=1, column=2, sticky="e", padx=10, pady=10)
BotonDelete = Button(miFrame2, text="Borrar BBDD", width=10, command=Ventana_BorrarBDD)
BotonDelete.grid(row=1, column=3, sticky="e", padx=10, pady=10)
    
    
 
 
root.mainloop()   




