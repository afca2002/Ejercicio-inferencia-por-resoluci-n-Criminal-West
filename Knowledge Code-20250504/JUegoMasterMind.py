from logic import *

# Definir los colores disponibles
COLORES = ["red", "blue", "green", "yellow"]

# Crear símbolos para cada posición y color
def crear_simbolos():
    return {
        (pos, color): Symbol(f"P{pos}_{color}")
        for pos in range(4)
        for color in COLORES
    }

# Generar las reglas del juego
def generar_reglas(simbolos):
    reglas = And()

    # Cada posición debe tener exactamente un color
    for pos in range(4):
        reglas.add(Or(*[simbolos[(pos, color)] for color in COLORES]))
        for c1 in COLORES:
            for c2 in COLORES:
                if c1 != c2:
                    reglas.add(Implication(simbolos[(pos, c1)], Not(simbolos[(pos, c2)])))

    # Cada color debe aparecer exactamente una vez
    for color in COLORES:
        reglas.add(Or(*[simbolos[(pos, color)] for pos in range(4)]))
        for p1 in range(4):
            for p2 in range(4):
                if p1 != p2:
                    reglas.add(Implication(simbolos[(p1, color)], Not(simbolos[(p2, color)])))

    return reglas

# Evaluar un intento del jugador
def evaluar_intento(simbolos, intento, exactos, cercanos):
    conocimiento = And()

    # Agregar conocimiento sobre el intento
    for pos, color in enumerate(intento):
        conocimiento.add(simbolos[(pos, color)])

    # Agregar restricciones basadas en los resultados del intento
    if exactos > 0:
        conocimiento.add(Or(*[simbolos[(pos, intento[pos])] for pos in range(4)]))
    if cercanos > 0:
        conocimiento.add(Or(*[Not(simbolos[(pos, intento[pos])]) for pos in range(4)]))

    return conocimiento

# Resolver el juego
def jugar_mastermind():
    simbolos = crear_simbolos()
    reglas = generar_reglas(simbolos)

    print("¡Bienvenido a MasterMind con lógica proposicional!")
    print(f"Colores disponibles: {', '.join(COLORES)}")
    print("Intenta adivinar la combinación de 4 colores.")

    conocimiento = reglas
    intentos = 0

    while True:
        intento = input("\nIntroduce tu intento (colores separados por espacios): ").strip().lower().split()
        if len(intento) != 4 or any(color not in COLORES for color in intento):
            print(f"Entrada inválida. Asegúrate de usar 4 colores de la lista: {', '.join(COLORES)}")
            continue

        exactos = int(input("Introduce el número de colores exactos: "))
        cercanos = int(input("Introduce el número de colores cercanos: "))

        conocimiento = And(conocimiento, evaluar_intento(simbolos, intento, exactos, cercanos))
        intentos += 1

        # Verificar si se puede deducir la solución
        for pos in range(4):
            for color in COLORES:
                if model_check(conocimiento, simbolos[(pos, color)]):
                    print(f"Posición {pos + 1}: {color.upper()}")

        if exactos == 4:
            print(f"¡Felicidades! Adivinaste la combinación en {intentos} intentos.")
            break

# Iniciar el juego
if __name__ == "__main__":
    jugar_mastermind()