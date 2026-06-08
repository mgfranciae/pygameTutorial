import random
import msvcrt
import sys

# ============================================================================
# FUNCIONES DE UTILIDAD (Responsabilidad única: operaciones básicas)
# ============================================================================

def generar_aleatorio(limite_inferior, limite_superior):
    """
    Genera un número aleatorio dentro del rango especificado.
    
    Principio aplicado: Single Responsibility (SRP)
    - Esta función solo se encarga de generar el número, nada más.
    - Es reutilizable en cualquier contexto que necesite aleatoriedad.
    
    Args:
        limite_inferior: Valor mínimo del rango (inclusive)
        limite_superior: Valor máximo del rango (inclusive)
    
    Returns:
        int: Número aleatorio generado
    """
    numero_generado = random.randint(limite_inferior, limite_superior)
    return numero_generado


def verificar_en_intervalo(limite_inferior, limite_superior, numero):
    """
    Valida si un número está dentro del rango permitido.
    
    Principio aplicado: Open/Closed (OCP)
    - La función está cerrada a modificación pero abierta a extensión
    - Puede usarse con cualquier rango sin cambiar su código interno.
    
    Args:
        limite_inferior: Valor mínimo del rango
        limite_superior: Valor máximo del rango
        numero: Número a verificar
    
    Returns:
        bool: True si está en el rango, False en caso contrario
    """
    if limite_inferior <= numero <= limite_superior:
        return True
    else:
        return False


# ============================================================================
# FUNCIONES DE CONFIGURACIÓN (Responsabilidad: setup del juego)
# ============================================================================

def solicitar_limite(mensaje, minimo_permitido=1):
    """
    Solicita al usuario un valor numérico con validación.
    
    Principio aplicado: DRY (Don't Repeat Yourself)
    - Evita duplicar código de validación de entrada.
    - Se reutiliza para pedir ambos límites.
    
    Args:
        mensaje: Texto a mostrar al usuario
        minimo_permitido: Valor mínimo aceptable (default: 1)
    
    Returns:
        int: Valor numérico válido ingresado por el usuario
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo_permitido:
                return valor
            else:
                print(f"⚠️  El valor debe ser al menos {minimo_permitido}. Intenta de nuevo.\n")
        except ValueError:
            print("⚠️  Entrada inválida. Por favor, ingresa un número entero.\n")


def configurar_juego():
    """
    Permite al usuario definir los parámetros del juego.
    
    Principio aplicado: Single Responsibility (SRP)
    - Esta función solo se encarga de la configuración, no de ejecutar el juego.
    - Separa la lógica de setup de la lógica de ejecución.
    
    Returns:
        tuple: (limite_inferior, limite_superior, max_intentos)
    """
    print("\n" + "="*60)
    print("🎮 CONFIGURACIÓN DEL JUEGO")
    print("="*60)
    
    # Solicitar límites con validación
    limite_inferior = solicitar_limite(" Ingresa el límite INFERIOR del rango: ")
    
    # El límite superior debe ser mayor al inferior
    while True:
        limite_superior = solicitar_limite("📍 Ingresa el límite SUPERIOR del rango: ")
        if limite_superior > limite_inferior:
            break
        print(f"⚠️  El límite superior debe ser mayor que {limite_inferior}. Intenta de nuevo.\n")
    
    # Solicitar cantidad de intentos
    max_intentos = solicitar_limite("🎯 ¿Cuántos intentos deseas tener? (mínimo 1): ", minimo_permitido=1)
    
    return limite_inferior, limite_superior, max_intentos


# ============================================================================
# FUNCIONES DE INTERFAZ (Responsabilidad: mostrar información al usuario)
# ============================================================================

def mostrar_bienvenida(limite_inferior, limite_superior, max_intentos):
    """
    Muestra el mensaje de bienvenida e instrucciones del juego.
    
    Principio aplicado: Separation of Concerns
    - La presentación visual está separada de la lógica del juego.
    - Fácil de modificar sin afectar la mecánica del juego.
    """
    print("\n" + "="*60)
    print("🎲 ¡BIENVENIDO AL JUEGO DE ADIVINANZA! 🎲")
    print("="*60)
    print(f"\n INSTRUCCIONES:")
    print(f"   • He pensado un número entre {limite_inferior} y {limite_superior}")
    print(f"   • Tienes {max_intentos} intentos para adivinarlo")
    print(f"   • Te daré pistas si tu número es muy alto o muy bajo")
    print(f"   • Presiona ESC en cualquier momento para salir del juego")
    print("="*60 + "\n")


def mostrar_estado_intentos(intentos_restantes, max_intentos):
    """
    Muestra el progreso actual de intentos.
    
    Args:
        intentos_restantes: Intentos que quedan disponibles
        max_intentos: Total de intentos permitidos
    """
    intentos_usados = max_intentos - intentos_restantes
    barra_progreso = "█" * intentos_usados + "░" * intentos_restantes
    print(f"\n📊 Progreso: [{barra_progreso}] {intentos_restantes} intento(s) restante(s)")


def solicitar_numero_usuario(limite_inferior, limite_superior):
    """
    Solicita y valida la entrada del usuario.
    
    Principio aplicado: Single Responsibility (SRP)
    - Solo se encarga de obtener un número válido del usuario.
    - No evalúa si es correcto, solo valida el formato y rango.
    
    Returns:
        int: Número válido ingresado por el usuario
    """
    while True:
        try:
            numero = int(input("\n🔢 Ingresa tu número: "))
            
            # Validar que esté en el rango permitido
            if verificar_en_intervalo(limite_inferior, limite_superior, numero):
                return numero
            else:
                print(f"⚠️  El número debe estar entre {limite_inferior} y {limite_superior}")
                
        except ValueError:
            print("⚠️  Entrada inválida. Por favor, ingresa un número entero.")


def evaluar_intento(numero_usuario, numero_secreto):
    """
    Compara el número del usuario con el número secreto y da pistas.
    
    Principio aplicado: Single Responsibility (SRP)
    - Solo evalúa, no modifica estado ni controla flujo.
    - Retorna información para que el llamador decida qué hacer.
    
    Returns:
        str: 'correcto', 'mayor', o 'menor'
    """
    if numero_usuario == numero_secreto:
        return 'correcto'
    elif numero_usuario < numero_secreto:
        print("📈 ¡El número secreto es MAYOR!")
        return 'menor'
    else:
        print("📉 ¡El número secreto es MENOR!")
        return 'mayor'


def mostrar_resultado_final(gano, numero_secreto, intentos_usados, max_intentos):
    """
    Muestra el mensaje de victoria o derrota.
    
    Args:
        gano: Boolean indicando si el usuario ganó
        numero_secreto: El número que debía adivinar
        intentos_usados: Cantidad de intentos utilizados
        max_intentos: Máximo de intentos permitidos
    """
    print("\n" + "="*60)
    if gano:
        print("🎉 ¡FELICIDADES! ¡HAS GANADO! 🎉")
        print(f"   Adivinaste el número {numero_secreto} en {intentos_usados} intento(s)")
        
        # Mensaje especial si lo logró en el primer intento
        if intentos_usados == 1:
            print("   ¡Impresionante! ¡Lo lograste en el primer intento! ")
    else:
        print("💀 ¡FIN DEL JUEGO! 💀")
        print(f"   Te quedaste sin intentos.")
        print(f"   El número secreto era: {numero_secreto}")
    print("="*60 + "\n")


# ============================================================================
# FUNCIONES DE CONTROL DE FLUJO (Responsabilidad: gestionar el juego)
# ============================================================================

def detectar_tecla_esc():
    """
    Verifica si se presionó la tecla ESC.
    
    Returns:
        bool: True si se presionó ESC, False en caso contrario
    """
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        # ESC tiene código ASCII 27
        if ord(tecla) == 27:
            return True
    return False


def ejecutar_ronda(limite_inferior, limite_superior, max_intentos):
    """
    Ejecuta una partida completa del juego.
    
    Principio aplicado: Single Responsibility (SRP)
    - Esta función maneja toda la lógica de una ronda.
    - El llamador no necesita conocer los detalles internos.
    
    Args:
        limite_inferior: Valor mínimo del rango
        limite_superior: Valor máximo del rango
        max_intentos: Número máximo de intentos permitidos
    
    Returns:
        bool: True si el usuario quiere jugar otra ronda, False si quiere salir
    """
    # Generar el número secreto para esta ronda
    numero_secreto = generar_aleatorio(limite_inferior, limite_superior)
    intentos_restantes = max_intentos
    
    # Mostrar bienvenida con los parámetros actuales
    mostrar_bienvenida(limite_inferior, limite_superior, max_intentos)
    
    # Bucle principal de la ronda
    while intentos_restantes > 0:
        # Verificar si el usuario quiere salir
        if detectar_tecla_esc():
            print("\n\n👋 Saliendo del juego... ¡Hasta pronto!")
            return False
        
        # Mostrar estado actual
        mostrar_estado_intentos(intentos_restantes, max_intentos)
        
        # Solicitar número al usuario
        numero_usuario = solicitar_numero_usuario(limite_inferior, limite_superior)
        
        # Evaluar el intento
        resultado = evaluar_intento(numero_usuario, numero_secreto)
        
        # Verificar si ganó
        if resultado == 'correcto':
            intentos_usados = max_intentos - intentos_restantes + 1
            mostrar_resultado_final(True, numero_secreto, intentos_usados, max_intentos)
            return True  # Gano, preguntar si quiere continuar
        
        # Restar un intento
        intentos_restantes -= 1
    
    # Si llega aquí, se agotaron los intentos
    mostrar_resultado_final(False, numero_secreto, max_intentos, max_intentos)
    return True  # Perdió, pero puede jugar otra ronda


def preguntar_continuar():
    """
    Pregunta al usuario si desea jugar otra ronda.
    
    Returns:
        bool: True si quiere continuar, False si quiere salir
    """
    print("\n" + "-"*60)
    respuesta = input("¿Deseas jugar otra ronda? (s/n): ").strip().lower()
    print("-"*60)
    
    return respuesta == 's'


# ============================================================================
# PROGRAMA PRINCIPAL (Orquestación del flujo del juego)
# ============================================================================

print("\n" + "🎮" * 30)
print("   JUEGO DE ADIVINANZA - PYTHON")
print("🎮" * 30)

# Configurar el juego (obtener parámetros del usuario)
limite_inferior, limite_superior, max_intentos = configurar_juego()

# Bucle principal del juego (se repite hasta que el usuario decida salir)
juego_activo = True

while juego_activo:
    # Ejecutar una ronda del juego
   #COMPLETAR
    
    # Si el usuario presionó ESC durante la ronda, salir inmediatamente
    if not ronda_completada:
       #COMPLETAR
    
    # Preguntar si desea jugar otra ronda
    if not preguntar_continuar():
        print("\n👋 ¡Gracias por jugar! ¡Hasta la próxima!")
        juego_activo = False
    else:
        # Opcional: permitir reconfigurar el juego
        reconfigurar = input("\n¿Deseas cambiar la configuración del juego? (s/n): ").strip().lower()
        # COMPLETAR

print("\n✅ Programa finalizado correctamente.\n")