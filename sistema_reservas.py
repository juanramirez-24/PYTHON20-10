from datetime import datetime

# SISTEMA DE RESERVAS DEL RESTAURANTE
# Solo Python: listas y diccionarios. No utiliza SQL ni bases de datos externas.
# Los datos se mantienen en memoria y se pierden al cerrar el programa.

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
usuario_sesion = None


def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede quedar vacío.")


def leer_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"Ingresa un número igual o superior a {minimo}.")
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")


def pausar():
    input("\nPresiona ENTER para continuar...")


def crear_cuenta():
    """Solo se permite crear una cuenta en esta versión del sistema."""
    global siguiente_usuario_id

    if usuarios:
        print("\nYa existe una cuenta. Inicia sesión para continuar.")
        return

    print("\n=== CREAR CUENTA ===")
    nombre = leer_texto("Nombre completo: ")
    documento = leer_texto("Documento: ")
    telefono = leer_texto("Número de teléfono: ")
    contrasena = leer_texto("Crea una contraseña: ")

    usuarios.append({
        "id": siguiente_usuario_id,
        "nombre": nombre,
        "documento": documento,
        "telefono": telefono,
        "contrasena": contrasena,
    })
    siguiente_usuario_id += 1
    print("\n¡Cuenta creada correctamente!")
    print("Ahora solo estará disponible la opción «Iniciar sesión».")


def iniciar_sesion():
    global usuario_sesion

    if not usuarios:
        print("\nPrimero debes crear una cuenta.")
        return False

    print("\n=== INICIAR SESIÓN ===")
    documento = leer_texto("Documento: ")
    contrasena = leer_texto("Contraseña: ")

    for usuario in usuarios:
        if usuario["documento"] == documento and usuario["contrasena"] == contrasena:
            usuario_sesion = usuario
            print(f"\n¡Bienvenido/a, {usuario['nombre']}!")
            return True

    print("Documento o contraseña incorrectos.")
    return False


def mostrar_mesas():
    print("\n=== MESAS DEL RESTAURANTE ===")
    for mesa in mesas:
        print(
            f"Mesa {mesa['numero']} | Capacidad: {mesa['capacidad']} "
            f"comensales | Ubicación: {mesa['ubicacion']}"
        )


def mesa_ocupada(mesa_id, fecha, hora):
    return any(
        reserva["mesa_id"] == mesa_id
        and reserva["fecha"] == fecha
        and reserva["hora"] == hora
        and reserva["estado"] == "Confirmada"
        for reserva in reservas
    )


def solicitar_fecha_hora():
    while True:
        fecha = input("Fecha (AAAA-MM-DD): ").strip()
        hora = input("Hora (HH:MM, formato 24 horas): ").strip()
        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if fecha_hora < datetime.now():
                print("La fecha y hora deben ser futuras.")
                continue
            return fecha, hora
        except ValueError:
            print("Formato inválido. Ejemplo: 2026-12-15 y 19:30.")


def crear_reserva():
    global siguiente_reserva_id

    print("\n=== CREAR RESERVA ===")
    mostrar_mesas()
    fecha, hora = solicitar_fecha_hora()
    comensales = leer_entero("Cantidad de comensales: ")

    disponibles = [
        mesa for mesa in mesas
        if mesa["capacidad"] >= comensales
        and not mesa_ocupada(mesa["id"], fecha, hora)
    ]

    if not disponibles:
        print("\nNo hay mesas disponibles para esa fecha, hora y cantidad de comensales.")
        return

    print("\nMesas disponibles:")
    for mesa in disponibles:
        print(
            f"ID {mesa['id']} | Mesa {mesa['numero']} | "
            f"Capacidad: {mesa['capacidad']} | {mesa['ubicacion']}"
        )

    ids_disponibles = [mesa["id"] for mesa in disponibles]
    while True:
        mesa_id = leer_entero("ID de la mesa que deseas reservar: ")
        if mesa_id in ids_disponibles:
            mesa = next(m for m in disponibles if m["id"] == mesa_id)
            break
        print("Selecciona un ID de las mesas disponibles.")

    print("\n=== RESUMEN DE LA RESERVA ===")
    print(f"Cliente: {usuario_sesion['nombre']}")
    print(f"Documento: {usuario_sesion['documento']}")
    print(f"Mesa: {mesa['numero']} ({mesa['ubicacion']})")
    print(f"Fecha: {fecha} | Hora: {hora} | Comensales: {comensales}")

    continuar = input("\n¿Deseas continuar al pago simulado? (s/n): ").strip().lower()
    if continuar != "s":
        print("Reserva cancelada antes del pago.")
        return

    print("\n=== PAGO SIMULADO ===")
    print("Este sistema no realiza cobros reales.")
    resultado = input("Escribe 'pagar' para simular un pago exitoso: ").strip().lower()

    if resultado != "pagar":
        print("No se pudo completar el pago. No se guardó ninguna reserva.")
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


def consultar_reservas():
    print("\n=== MIS RESERVAS ===")
    mis_reservas = [
        reserva for reserva in reservas
        if reserva["usuario_id"] == usuario_sesion["id"]
    ]

    if not mis_reservas:
        print("Todavía no tienes reservas.")
        return

    for reserva in mis_reservas:
        mesa = next(m for m in mesas if m["id"] == reserva["mesa_id"])
        print(
            f"Reserva #{reserva['id']} | Mesa {mesa['numero']} "
            f"({mesa['ubicacion']}) | Fecha: {reserva['fecha']} | "
            f"Hora: {reserva['hora']} | Comensales: "
            f"{reserva['cantidad_comensales']} | Estado: {reserva['estado']}"
        )


def cancelar_reserva():
    print("\n=== CANCELAR RESERVA ===")
    mis_reservas = [
        reserva for reserva in reservas
        if reserva["usuario_id"] == usuario_sesion["id"]
        and reserva["estado"] == "Confirmada"
    ]

    if not mis_reservas:
        print("No tienes reservas confirmadas para cancelar.")
        return

    for reserva in mis_reservas:
        mesa = next(m for m in mesas if m["id"] == reserva["mesa_id"])
        print(
            f"Reserva #{reserva['id']} | Mesa {mesa['numero']} | "
            f"{reserva['fecha']} a las {reserva['hora']}"
        )

    reserva_id = leer_entero("Número de reserva que deseas cancelar: ")
    for reserva in mis_reservas:
        if reserva["id"] == reserva_id:
            reserva["estado"] = "Cancelada"
            print("Reserva cancelada correctamente.")
            return

    print("No se encontró una reserva confirmada con ese número en tu cuenta.")


def menu_usuario():
    while usuario_sesion is not None:
        print("\n" + "=" * 46)
        print(f"  BIENVENIDO/A, {usuario_sesion['nombre'].upper()}")
        print("=" * 46)
        print("1. Ver mesas y ubicaciones")
        print("2. Crear reserva")
        print("3. Consultar mis reservas")
        print("4. Cancelar reserva")
        print("5. Cerrar sesión")

        opcion = input("\nSelecciona una opción: ").strip()
        if opcion == "1":
            mostrar_mesas()
            pausar()
        elif opcion == "2":
            crear_reserva()
            pausar()
        elif opcion == "3":
            consultar_reservas()
            pausar()
        elif opcion == "4":
            cancelar_reserva()
            pausar()
        elif opcion == "5":
            print(f"Hasta luego, {usuario_sesion['nombre']}.")
            return
        else:
            print("Opción inválida. Intenta nuevamente.")


def menu_principal():
    while True:
        print("\n" + "=" * 46)
        print("     SISTEMA DE RESERVAS DEL RESTAURANTE")
        print("=" * 46)

        if not usuarios:
            print("1. Crear cuenta")
            print("2. Iniciar sesión")
            print("0. Salir")
            opcion = input("\nSelecciona una opción: ").strip()

            if opcion == "1":
                crear_cuenta()
                pausar()
            elif opcion == "2":
                iniciar_sesion()
                if usuario_sesion is not None:
                    menu_usuario()
                else:
                    pausar()
            elif opcion == "0":
                print("¡Gracias por utilizar el sistema!")
                break
            else:
                print("Opción inválida. Intenta nuevamente.")
                pausar()
        else:
            # Después de crear la cuenta, se oculta «Crear cuenta».
            print("1. Iniciar sesión")
            print("0. Salir")
            opcion = input("\nSelecciona una opción: ").strip()

            if opcion == "1":
                if iniciar_sesion():
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
