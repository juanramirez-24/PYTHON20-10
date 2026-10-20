from datetime import datetime

# Sistema de reservas de restaurante
# Solo Python: listas y diccionarios; no usa SQL ni bases de datos externas.
# Los datos se pierden al cerrar el programa.

usuarios = []
mesas = []
reservas = []
siguiente_usuario_id = 1
siguiente_mesa_id = 1
siguiente_reserva_id = 1


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


def registrar_usuario():
    global siguiente_usuario_id
    print("\n=== REGISTRO DE USUARIO ===")
    nombre = leer_texto("Nombre completo: ")
    documento = leer_texto("Documento: ")

    if any(u["documento"] == documento for u in usuarios):
        print("Error: ya existe un usuario con ese documento.")
        return

    telefono = leer_texto("Número de teléfono: ")
    usuarios.append({
        "id": siguiente_usuario_id,
        "telefono": telefono,
        "nombre": nombre,
        "documento": documento,
    })
    print(f"Usuario registrado correctamente. ID: {siguiente_usuario_id}")
    siguiente_usuario_id += 1


def registrar_mesa():
    global siguiente_mesa_id
    print("\n=== REGISTRO DE MESA ===")
    numero = leer_entero("Número de mesa: ")

    if any(m["numero"] == numero for m in mesas):
        print("Ya existe una mesa con ese número.")
        return

    capacidad = leer_entero("Capacidad (cantidad de comensales): ")
    ubicacion = leer_texto("Ubicación (salón, terraza, ventana, etc.): ")
    mesas.append({
        "id": siguiente_mesa_id,
        "numero": numero,
        "capacidad": capacidad,
        "ubicacion": ubicacion,
    })
    print(f"Mesa registrada correctamente. ID: {siguiente_mesa_id}")
    siguiente_mesa_id += 1


def mostrar_usuarios():
    print("\n=== USUARIOS ===")
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for u in usuarios:
        print(f"ID: {u['id']} | Nombre: {u['nombre']} | "
              f"Documento: {u['documento']} | Teléfono: {u['telefono']}")


def mostrar_mesas():
    print("\n=== MESAS ===")
    if not mesas:
        print("No hay mesas registradas.")
        return
    for m in mesas:
        print(f"ID: {m['id']} | Mesa N.º {m['numero']} | "
              f"Capacidad: {m['capacidad']} | Ubicación: {m['ubicacion']}")


def buscar_usuario(documento):
    for usuario in usuarios:
        if usuario["documento"] == documento:
            return usuario
    return None


def mesa_ocupada(mesa_id, fecha, hora):
    return any(
        r["mesa_id"] == mesa_id
        and r["fecha"] == fecha
        and r["hora"] == hora
        and r["estado"] == "Confirmada"
        for r in reservas
    )


def crear_reserva():
    global siguiente_reserva_id
    print("\n=== CREAR RESERVA ===")

    if not usuarios:
        print("Primero debes registrar un usuario.")
        return
    if not mesas:
        print("Primero debes registrar al menos una mesa.")
        return

    documento = leer_texto("Documento del usuario: ")
    usuario = buscar_usuario(documento)
    if usuario is None:
        print("No existe un usuario con ese documento. Regístralo primero.")
        return

    fecha_hora = None
    while fecha_hora is None:
        fecha = input("Fecha (AAAA-MM-DD): ").strip()
        hora = input("Hora (HH:MM, formato 24 horas): ").strip()
        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if fecha_hora < datetime.now():
                print("La fecha y hora deben ser futuras.")
                fecha_hora = None
        except ValueError:
            print("Formato inválido. Ejemplo: 2026-12-15 y 19:30.")

    comensales = leer_entero("Cantidad de comensales: ")
    disponibles = [
        m for m in mesas
        if m["capacidad"] >= comensales
        and not mesa_ocupada(m["id"], fecha, hora)
    ]

    if not disponibles:
        print("No hay mesas disponibles para esa fecha, hora y cantidad de comensales.")
        return

    print("\nMesas disponibles:")
    for m in disponibles:
        print(f"ID {m['id']} | Mesa N.º {m['numero']} | "
              f"Capacidad: {m['capacidad']} | {m['ubicacion']}")

    ids_disponibles = [m["id"] for m in disponibles]
    while True:
        mesa_id = leer_entero("ID de la mesa que deseas reservar: ")
        if mesa_id in ids_disponibles:
            mesa = next(m for m in disponibles if m["id"] == mesa_id)
            break
        print("Selecciona un ID de las mesas disponibles.")

    print("\n=== RESUMEN ===")
    print(f"Cliente: {usuario['nombre']}")
    print(f"Documento: {usuario['documento']}")
    print(f"Mesa: {mesa['numero']}")
    print(f"Fecha: {fecha} | Hora: {hora} | Comensales: {comensales}")

    continuar = input("¿Deseas continuar al pago simulado? (s/n): ").strip().lower()
    if continuar != "s":
        print("Reserva cancelada antes del pago.")
        return

    print("\n=== PAGO SIMULADO ===")
    print("Este programa no realiza cobros reales.")
    pago = input("Escribe 'pagar' para simular un pago exitoso: ").strip().lower()

    if pago != "pagar":
        print("No se pudo completar el pago. No se guardó ninguna reserva.")
        return

    reserva = {
        "id": siguiente_reserva_id,
        "fecha": fecha,
        "hora": hora,
        "mesa_id": mesa["id"],
        "usuario_id": usuario["id"],
        "cantidad_comensales": comensales,
        "estado": "Confirmada",
    }
    reservas.append(reserva)
    print(f"¡Reserva exitosa! Número de reserva: {siguiente_reserva_id}")
    siguiente_reserva_id += 1


def consultar_reservas():
    print("\n=== RESERVAS ===")
    if not reservas:
        print("No hay reservas registradas.")
        return

    for r in reservas:
        usuario = next((u for u in usuarios if u["id"] == r["usuario_id"]), None)
        mesa = next((m for m in mesas if m["id"] == r["mesa_id"]), None)
        nombre = usuario["nombre"] if usuario else "Usuario desconocido"
        numero_mesa = mesa["numero"] if mesa else "Mesa desconocida"
        print(f"Reserva #{r['id']} | Cliente: {nombre} | Mesa: {numero_mesa} | "
              f"Fecha: {r['fecha']} | Hora: {r['hora']} | "
              f"Comensales: {r['cantidad_comensales']} | Estado: {r['estado']}")


def cancelar_reserva():
    print("\n=== CANCELAR RESERVA ===")
    consultar_reservas()
    if not reservas:
        return

    reserva_id = leer_entero("ID de la reserva que deseas cancelar: ")
    for r in reservas:
        if r["id"] == reserva_id:
            if r["estado"] == "Cancelada":
                print("Esta reserva ya está cancelada.")
            else:
                r["estado"] = "Cancelada"
                print("Reserva cancelada correctamente.")
            return
    print("No se encontró una reserva con ese ID.")


def menu():
    while True:
        print("\n" + "=" * 46)
        print("     SISTEMA DE RESERVAS DEL RESTAURANTE")
        print("=" * 46)
        print("1. Registrar usuario")
        print("2. Registrar mesa")
        print("3. Ver usuarios")
        print("4. Ver mesas")
        print("5. Crear reserva")
        print("6. Consultar reservas")
        print("7. Cancelar reserva")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()
        if opcion == "1":
            registrar_usuario()
            pausar()
        elif opcion == "2":
            registrar_mesa()
            pausar()
        elif opcion == "3":
            mostrar_usuarios()
            pausar()
        elif opcion == "4":
            mostrar_mesas()
            pausar()
        elif opcion == "5":
            crear_reserva()
            pausar()
        elif opcion == "6":
            consultar_reservas()
            pausar()
        elif opcion == "7":
            cancelar_reserva()
            pausar()
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()
