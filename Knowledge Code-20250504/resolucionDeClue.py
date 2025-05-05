from logic import *

# Definición de personajes
mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

# Definición de habitaciones
ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

# Definición de armas
knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

# Lista de todos los símbolos
symbols = characters + rooms + weapons

# Función para verificar el conocimiento
def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}: YES")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

# Conocimiento inicial: debe haber un personaje, una habitación y un arma
knowledge = And(
    Or(mustard, plum, scarlet),  # Un personaje
    Or(ballroom, kitchen, library),  # Una habitación
    Or(knife, revolver, wrench)  # Un arma
)

# Cartas iniciales conocidas (no están en el sobre)
knowledge.add(And(
    Not(mustard),  # Col. Mustard no está en el sobre
    Not(kitchen),  # La cocina no está en el sobre
    Not(revolver)  # El revólver no está en el sobre
))

# Cartas desconocidas (al menos una de estas está en el sobre)
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench)
))

# Más conocimiento conocido
knowledge.add(Not(plum))  # Prof. Plum no está en el sobre
knowledge.add(Not(ballroom))  # El salón de baile no está en el sobre

# Verificar el conocimiento
check_knowledge(knowledge)