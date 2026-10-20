from datetime import datetime

# SISTEMA DE RESERVAS DEL RESTAURANTE
# Solo Python: listas y diccionarios. No utiliza SQL ni bases de datos externas.
# Los datos se mantienen en memoria y se pierden al cerrar el programa.

ADMIN_DOCUMENTO = "ADMIN"
ADMIN_CONTRASENA = "Admin123"

usuarios = []
mesas = [
    {"id": 1, "numero": 1, "capacidad": 2, "ubicacion": "Ventana"},
    {"id": 2, "numero": 2, "capacidad": 2, "ubicacion": "Ventana"},
    {"id": 3, "numero": 3, "capacidad": 4, "ubicacion": "Salon principal"},
    {"id": 4, "numero": 4, "capacidad": 4, "ubicacion": "Salon principal"},
    {"id": 5, "numero": 5, "capacidad": 4, "ubicacion": "Terraza"},
    {"id": 6, "numero": 6, "capacidad": 6, "ubicacion": "Terraza"},
    {"id": 7, "numero": 7, "capacidad": 8, "ubicacion": "Zona familiar"},
    {"id": 8, "numero": 8, "capacidad": 2, "ubicacion": "Zona romantica"},
]
reservas = []
siguiente_usuario_id = 1
siguiente_reserva_id = 1
siguiente_mesa_id = max((mesa['id'] for mesa in mesas), default=0) + 1
usuario_sesion = None


def separador():
    print("-" * 54)


def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Aviso: este campo no puede quedar vacío.")


def leer_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"Aviso: ingresa un número igual o superior a {minimo}.")
        except ValueError:
            print("Aviso: entrada inválida. Ingresa un número entero.")


def pausar():
    input("\nPresiona ENTER para continuar...")


def buscar_usuario_por_documento(documento):
    return next((u for u in usuarios if u["documento"] == documento), None)


def buscar_usuario_por_id(usuario_id):
    return next((u for u in usuarios if u["id"] == usuario_id), None)


def buscar_mesa_por_id(mesa_id):
    return next((m for m in mesas if m["id"] == mesa_id), None)


def crear_cuenta():
    global siguiente_usuario_id

    print("\n=== CREAR CUENTA ===")
    nombre = leer_texto("Nombre completo: ")
    documento = leer_texto("Documento: ")

    if documento.upper() == ADMIN_DOCUMENTO or buscar_usuario_por_documento(documento):
        print("Aviso: ese documento ya está registrado o está reservado para administración.")
        return

    telefono = leer_texto("Número de teléfono: ")
    contrasena = leer_texto("Crea una contraseña: ")

    usuarios.append({
        "id": siguiente_usuario_id,
        "nombre": nombre,
        "documento": documento,
        "telefono": telefono,
        "contrasena": contrasena,
        "rol": "usuario",
    })
    siguiente_usuario_id += 1
    print("\n¡Cuenta creada correctamente!")
    print("Ahora puedes iniciar sesión con tu documento y contraseña.")


def iniciar_sesion():
    global usuario_sesion

    print("\n=== INICIAR SESIÓN ===")
    documento = leer_texto("Documento o usuario admin: ")
    contrasena = leer_texto("Contraseña: ")

    if documento.upper() == ADMIN_DOCUMENTO and contrasena == ADMIN_CONTRASENA:
        usuario_sesion = {
            "id": 0,
            "nombre": "Administrador",
            "documento": ADMIN_DOCUMENTO,
            "telefono": "",
            "contrasena": ADMIN_CONTRASENA,
            "rol": "admin",
        }
        print("\nAcceso administrativo concedido.")
        return True

    usuario = buscar_usuario_por_documento(documento)
    if usuario and usuario["contrasena"] == contrasena:
        usuario_sesion = usuario
        print(f"\n¡Bienvenido/a, {usuario['nombre']}!")
        return True

    print("Error: documento o contraseña incorrectos.")
    return False


def mostrar_mesas():
    print("\n=== MESAS Y UBICACIONES ===")
    separador()
    for mesa in mesas:
        print(
            f"Mesa {mesa['numero']} | Capacidad: {mesa['capacidad']} comensales "
            f"| Ubicación: {mesa['ubicacion']}"
        )
    separador()


def solicitar_fecha_hora():
    while True:
        print("\n--- FECHA DE LA RESERVA ---")
        fecha = input("Ingresa la fecha (AAAA-MM-DD): ").strip()

        print("\n--- HORA DE LA RESERVA ---")
        hora = input("Ingresa la hora (HH:MM, formato 24 horas): ").strip()

        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if fecha_hora < datetime.now():
                print("Aviso: la fecha y hora deben ser futuras.")
                continue
            return fecha, hora
        except ValueError:
            print("Aviso: formato inválido. Ejemplo: 2026-12-15 y 19:30.")


def mesa_ocupada(mesa_id, fecha, hora, excluir_reserva_id=None):
    return any(
        r["mesa_id"] == mesa_id
        and r["fecha"] == fecha
        and r["hora"] == hora
        and r["estado"] == "Confirmada"
        and r["id"] != excluir_reserva_id
        for r in reservas
    )


def obtener_mesas_disponibles(fecha, hora, comensales, excluir_reserva_id=None):
    return [
        mesa for mesa in mesas
        if mesa["capacidad"] >= comensales
        and not mesa_ocupada(
            mesa["id"], fecha, hora, excluir_reserva_id=excluir_reserva_id
        )
    ]


def elegir_mesa(disponibles):
    if not disponibles:
        print("\nResultado: no hay mesas disponibles para esos datos.")
        return None

    print("\n=== MESAS DISPONIBLES ===")
    separador()
    for mesa in disponibles:
        print(
            f"ID {mesa['id']} | Mesa {mesa['numero']} | "
            f"Capacidad: {mesa['capacidad']} | Ubicación: {mesa['ubicacion']}"
        )
    separador()

    ids_disponibles = [m["id"] for m in disponibles]
    while True:
        mesa_id = leer_entero("Selecciona el ID de la mesa: ")
        if mesa_id in ids_disponibles:
            return buscar_mesa_por_id(mesa_id)
        print("Aviso: selecciona un ID de la lista de mesas disponibles.")


def crear_reserva():
    global siguiente_reserva_id

    print("\n=== CREAR RESERVA ===")
    print("Primero ingresa la fecha, la hora y la cantidad de comensales.")
    fecha, hora = solicitar_fecha_hora()
    comensales = leer_entero("\nCantidad de comensales: ")

    # La disponibilidad se consulta DESPUÉS de capturar fecha, hora y comensales.
    disponibles = obtener_mesas_disponibles(fecha, hora, comensales)
    mesa = elegir_mesa(disponibles)
    if mesa is None:
        return

    print("\n=== RESUMEN DE LA RESERVA ===")
    separador()
    print(f"Cliente: {usuario_sesion['nombre']}")
    print(f"Documento: {usuario_sesion['documento']}")
    print(f"Fecha: {fecha}")
    print(f"Hora: {hora}")
    print(f"Comensales: {comensales}")
    print(f"Mesa: {mesa['numero']} ({mesa['ubicacion']})")
    separador()

    continuar = input("¿Deseas continuar al pago simulado? (s/n): ").strip().lower()
    if continuar != "s":
        print("La reserva no fue creada.")
        return

    print("\n--- PAGO SIMULADO ---")
    print("Este sistema no realiza cobros reales.")
    resultado = input("Escribe 'pagar' para simular un pago exitoso: ").strip().lower()
    if resultado != "pagar":
        print("No se completó el pago. No se guardó la reserva.")
        return

    reservas.append({
        "id": siguiente_reserva_id,
        "fecha": fecha,
        "hora": hora,
        "mesa_id": mesa["id"],
        "usuario_id": usuario_sesion["id"],
        "cantidad_comensales": comensales,
        "estado": "Confirmada",
    })
    print(f"\n¡Reserva exitosa! Tu número de reserva es {siguiente_reserva_id}.")
    siguiente_reserva_id += 1


def imprimir_reserva(reserva):
    mesa = buscar_mesa_por_id(reserva["mesa_id"])
    usuario = buscar_usuario_por_id(reserva["usuario_id"])
    nombre = usuario["nombre"] if usuario else "Usuario desconocido"
    numero_mesa = mesa["numero"] if mesa else "Mesa desconocida"
    ubicacion = mesa["ubicacion"] if mesa else "Ubicación desconocida"
    print(
        f"Reserva #{reserva['id']} | Cliente: {nombre} | Mesa {numero_mesa} "
        f"({ubicacion}) | Fecha: {reserva['fecha']} | Hora: {reserva['hora']} "
        f"| Comensales: {reserva['cantidad_comensales']} "
        f"| Estado: {reserva['estado']}"
    )


def reservas_del_usuario(usuario_id):
    return [r for r in reservas if r["usuario_id"] == usuario_id]


def consultar_mis_reservas():
    print("\n=== MIS RESERVAS ===")
    mis_reservas = reservas_del_usuario(usuario_sesion["id"])
    if not mis_reservas:
        print("No tienes reservas registradas.")
        return
    for reserva in mis_reservas:
        imprimir_reserva(reserva)


def elegir_reserva(reservas_disponibles, mensaje):
    if not reservas_disponibles:
        print("No hay reservas disponibles para esta acción.")
        return None

    for reserva in reservas_disponibles:
        imprimir_reserva(reserva)

    reserva_id = leer_entero(mensaje)
    for reserva in reservas_disponibles:
        if reserva["id"] == reserva_id:
            return reserva
    print("No se encontró una reserva con ese ID en la lista.")
    return None


def editar_reserva(reserva, es_admin=False):
    print(f"\n=== EDITAR RESERVA #{reserva['id']} ===")
    print("Deja los datos nuevos según las indicaciones.")
    print(f"Fecha actual: {reserva['fecha']}")
    print(f"Hora actual: {reserva['hora']}")
    print(f"Comensales actuales: {reserva['cantidad_comensales']}")

    fecha, hora = solicitar_fecha_hora()
    comensales = leer_entero("\nNueva cantidad de comensales: ")
    disponibles = obtener_mesas_disponibles(
        fecha, hora, comensales, excluir_reserva_id=reserva["id"]
    )
    mesa_actual = buscar_mesa_por_id(reserva["mesa_id"])
    if (
        mesa_actual
        and mesa_actual["capacidad"] >= comensales
        and not mesa_ocupada(
            mesa_actual["id"], fecha, hora, excluir_reserva_id=reserva["id"]
        )
    ):
        if all(m["id"] != mesa_actual["id"] for m in disponibles):
            disponibles.append(mesa_actual)

    mesa = elegir_mesa(disponibles)
    if mesa is None:
        print("La reserva no se modificó.")
        return

    reserva["fecha"] = fecha
    reserva["hora"] = hora
    reserva["cantidad_comensales"] = comensales
    reserva["mesa_id"] = mesa["id"]
    print("Reserva actualizada correctamente.")


def editar_mis_reservas():
    print("\n=== EDITAR UNA RESERVA ===")
    editables = [
        r for r in reservas_del_usuario(usuario_sesion["id"])
        if r["estado"] == "Confirmada"
    ]
    reserva = elegir_reserva(editables, "Ingresa el número de reserva a editar: ")
    if reserva:
        editar_reserva(reserva)


def cancelar_mis_reservas():
    print("\n=== CANCELAR RESERVA ===")
    cancelables = [
        r for r in reservas_del_usuario(usuario_sesion["id"])
        if r["estado"] == "Confirmada"
    ]
    reserva = elegir_reserva(cancelables, "Ingresa el número de reserva a cancelar: ")
    if reserva:
        reserva["estado"] = "Cancelada"
        print("Reserva cancelada correctamente.")


# -------------------- GESTIÓN ADMINISTRATIVA DE MESAS --------------------

def admin_crear_mesa():
    global siguiente_mesa_id

    print("\n=== CREAR MESA ===")
    numero = leer_entero("Número de mesa: ")
    if any(m["numero"] == numero for m in mesas):
        print("Error: ya existe una mesa con ese número.")
        return

    capacidad = leer_entero("Capacidad (cantidad de comensales): ")
    ubicacion = leer_texto("Ubicación de la mesa: ")

    mesas.append({
        "id": siguiente_mesa_id,
        "numero": numero,
        "capacidad": capacidad,
        "ubicacion": ubicacion,
    })
    print(f"Mesa {numero} creada correctamente. ID interno: {siguiente_mesa_id}.")
    siguiente_mesa_id += 1


def admin_editar_mesa():
    print("\n=== EDITAR MESA ===")
    mostrar_mesas()
    mesa_id = leer_entero("ID interno de la mesa que deseas editar: ")
    mesa = buscar_mesa_por_id(mesa_id)

    if not mesa:
        print("No existe una mesa con ese ID.")
        return

    print("Presiona ENTER para conservar el dato actual.")
    nuevo_numero = input(f"Número de mesa [{mesa['numero']}]: ").strip()
    nueva_capacidad = input(f"Capacidad [{mesa['capacidad']}]: ").strip()
    nueva_ubicacion = input(f"Ubicación [{mesa['ubicacion']}]: ").strip()

    if nuevo_numero:
        try:
            numero = int(nuevo_numero)
            if numero < 1:
                print("El número de mesa debe ser positivo. Se conserva el actual.")
            elif any(m["numero"] == numero and m["id"] != mesa_id for m in mesas):
                print("Ese número ya está asignado a otra mesa. Se conserva el actual.")
            else:
                mesa["numero"] = numero
        except ValueError:
            print("Número inválido. Se conserva el actual.")

    if nueva_capacidad:
        try:
            capacidad = int(nueva_capacidad)
            if capacidad < 1:
                print("La capacidad debe ser al menos 1. Se conserva la actual.")
            else:
                mesa["capacidad"] = capacidad
        except ValueError:
            print("Capacidad inválida. Se conserva la actual.")

    if nueva_ubicacion:
        mesa["ubicacion"] = nueva_ubicacion

    print("Datos de la mesa actualizados correctamente.")


def admin_eliminar_mesa():
    print("\n=== ELIMINAR MESA ===")
    mostrar_mesas()
    mesa_id = leer_entero("ID interno de la mesa que deseas eliminar: ")
    mesa = buscar_mesa_por_id(mesa_id)

    if not mesa:
        print("No existe una mesa con ese ID.")
        return

    reservas_activas = [
        r for r in reservas
        if r["mesa_id"] == mesa_id and r["estado"] == "Confirmada"
    ]
    if reservas_activas:
        print(
            "No se puede eliminar esta mesa porque tiene reservas confirmadas. "
            "Edita o cancela esas reservas primero."
        )
        return

    confirmar = input(
        f"¿Seguro que deseas eliminar la mesa {mesa['numero']}? (s/n): "
    ).strip().lower()
    if confirmar != "s":
        print("Operación cancelada.")
        return

    mesas.remove(mesa)
    print(f"Mesa {mesa['numero']} eliminada correctamente.")


# -------------------- FUNCIONES DE ADMINISTRACIÓN --------------------

def admin_ver_usuarios():
    print("\n=== PERFILES REGISTRADOS ===")
    if not usuarios:
        print("No hay perfiles de clientes registrados.")
        return
    for usuario in usuarios:
        print(
            f"ID: {usuario['id']} | Nombre: {usuario['nombre']} | "
            f"Documento: {usuario['documento']} | Teléfono: {usuario['telefono']}"
        )


def admin_editar_perfil():
    print("\n=== EDITAR PERFIL DE CLIENTE ===")
    admin_ver_usuarios()
    if not usuarios:
        return

    usuario_id = leer_entero("ID del perfil que deseas modificar: ")
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        print("No existe un perfil con ese ID.")
        return

    print("Presiona ENTER para conservar cada dato actual.")
    nombre = input(f"Nombre [{usuario['nombre']}]: ").strip()
    documento = input(f"Documento [{usuario['documento']}]: ").strip()
    telefono = input(f"Teléfono [{usuario['telefono']}]: ").strip()
    contrasena = input("Nueva contraseña (vacío para conservarla): ").strip()

    if documento and documento != usuario["documento"]:
        otro = buscar_usuario_por_documento(documento)
        if otro:
            print("Ese documento ya está asignado a otro perfil. No se modificó el documento.")
            documento = usuario["documento"]

    if nombre:
        usuario["nombre"] = nombre
    if documento:
        usuario["documento"] = documento
    if telefono:
        usuario["telefono"] = telefono
    if contrasena:
        usuario["contrasena"] = contrasena

    print("Perfil actualizado correctamente.")


def admin_consultar_reservas():
    print("\n=== TODAS LAS RESERVAS ===")
    if not reservas:
        print("No hay reservas registradas en el sistema.")
        return
    for reserva in reservas:
        imprimir_reserva(reserva)


def admin_editar_reserva():
    print("\n=== EDITAR RESERVA GLOBAL ===")
    editables = [r for r in reservas if r["estado"] == "Confirmada"]
    reserva = elegir_reserva(editables, "Ingresa el número de reserva a editar: ")
    if reserva:
        editar_reserva(reserva, es_admin=True)


def admin_cancelar_reserva():
    print("\n=== CANCELAR RESERVA GLOBAL ===")
    cancelables = [r for r in reservas if r["estado"] == "Confirmada"]
    reserva = elegir_reserva(cancelables, "Ingresa el número de reserva a cancelar: ")
    if reserva:
        reserva["estado"] = "Cancelada"
        print("Reserva cancelada por administración.")


def menu_admin():
    global usuario_sesion

    while usuario_sesion and usuario_sesion.get("rol") == "admin":
        print("\n" + "=" * 54)
        print("             PANEL DE ADMINISTRACIÓN")
        print("=" * 54)
        print("1. Ver perfiles de clientes")
        print("2. Editar perfil de cliente")
        print("3. Consultar todas las reservas")
        print("4. Editar reserva")
        print("5. Cancelar reserva")
        print("6. Ver mesas y ubicaciones")
        print("7. Crear mesa")
        print("8. Editar mesa")
        print("9. Eliminar mesa")
        print("10. Cerrar sesión")

        opcion = input("\nSelecciona una opción: ").strip()
        if opcion == "1":
            admin_ver_usuarios()
            pausar()
        elif opcion == "2":
            admin_editar_perfil()
            pausar()
        elif opcion == "3":
            admin_consultar_reservas()
            pausar()
        elif opcion == "4":
            admin_editar_reserva()
            pausar()
        elif opcion == "5":
            admin_cancelar_reserva()
            pausar()
        elif opcion == "6":
            mostrar_mesas()
            pausar()
        elif opcion == "7":
            admin_crear_mesa()
            pausar()
        elif opcion == "8":
            admin_editar_mesa()
            pausar()
        elif opcion == "9":
            admin_eliminar_mesa()
            pausar()
        elif opcion == "10":
            print("Sesión de administrador cerrada.")
            usuario_sesion = None
            return
        else:
            print("Opción inválida.")
            pausar()


def menu_usuario():
    global usuario_sesion

    while usuario_sesion and usuario_sesion.get("rol") == "usuario":
        print("\n" + "=" * 54)
        print(f" BIENVENIDO/A, {usuario_sesion['nombre'].upper()}")
        print("=" * 54)

        mis_reservas = [
            r for r in reservas_del_usuario(usuario_sesion["id"])
            if r["estado"] == "Confirmada"
        ]
        print("1. Ver mesas y ubicaciones")
        print("2. Crear reserva")
        if mis_reservas:
            print("3. Consultar mis reservas")
            print("4. Editar una reserva")
            print("5. Cancelar reserva")
            print("6. Cerrar sesión")
        else:
            print("3. Cerrar sesión")

        opcion = input("\nSelecciona una opción: ").strip()
        if opcion == "1":
            mostrar_mesas()
            pausar()
        elif opcion == "2":
            crear_reserva()
            pausar()
        elif opcion == "3" and mis_reservas:
            consultar_mis_reservas()
            pausar()
        elif opcion == "4" and mis_reservas:
            editar_mis_reservas()
            pausar()
        elif opcion == "5" and mis_reservas:
            cancelar_mis_reservas()
            pausar()
        elif (opcion == "6" and mis_reservas) or (opcion == "3" and not mis_reservas):
            print(f"Hasta luego, {usuario_sesion['nombre']}.")
            usuario_sesion = None
            return
        else:
            print("Opción inválida. Intenta nuevamente.")
            pausar()


def menu_principal():
    while True:
        print("\n" + "=" * 54)
        print("       SISTEMA DE RESERVAS DEL RESTAURANTE")
        print("=" * 54)
        print("1. Crear cuenta")
        print("2. Iniciar sesión")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()
        if opcion == "1":
            crear_cuenta()
            pausar()
        elif opcion == "2":
            if iniciar_sesion():
                if usuario_sesion.get("rol") == "admin":
                    menu_admin()
                else:
                    menu_usuario()
            else:
                pausar()
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")
            pausar()


if __name__ == "__main__":
    menu_principal()
