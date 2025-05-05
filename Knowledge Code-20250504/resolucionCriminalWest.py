import itertools

class Symbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

class Not:
    def __init__(self, operand):
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

def resolve(ci, cj):
    resolved = set()
    for di in ci:
        for dj in cj:
            if di == Not(dj) or Not(di) == dj:
                new_clause = (ci - {di}) | (cj - {dj})
                if new_clause:  # Solo añadir si la nueva cláusula no es vacía
                    resolved.add(frozenset(new_clause))
    return resolved

def resolution(clauses):
    new = set()
    while True:
        pairs = list(itertools.combinations(clauses, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for resolvent in resolvents:
                if resolvent not in clauses and resolvent not in new:
                    print(f"Nueva cláusula formada de {ci} y {cj}: {resolvent}")
            if frozenset() in resolvents:
                return True, "Se encontró una contradicción. West es un criminal."
            new = new.union(resolvents)
        # Condición de salida si no se encuentran nuevas cláusulas
        if new.issubset(clauses) or not new:
            return False, "No se encontró una contradicción; no se pudo demostrar que West es un criminal."
        clauses = clauses.union(new)

# Definición de cláusulas en CNF
clausulas = set([
    # Es un crimen para un norteamericano vender armas a naciones hostiles
    frozenset([Not(Symbol("American(West)")), Not(Symbol("Armas(x)")), Not(Symbol("Vende(West, x, Nono)")), Not(Symbol("Hostil(Nono)")), Symbol("Criminal(West)")]),
    
    # Nono tiene misiles
    frozenset([Symbol("Tiene(Nono, m)"), Symbol("Misil(m)")]),
    
    # Si algo es un misil, entonces es un arma
    frozenset([Not(Symbol("Misil(m)")), Symbol("Armas(m)")]),
    
    # Si alguien es enemigo de América, entonces es hostil
    frozenset([Not(Symbol("Enemigo(x, America)")), Symbol("Hostil(x)")]),
    
    # West es norteamericano
    frozenset([Symbol("American(West)")]),
    
    # Nono es enemigo de América
    frozenset([Symbol("Enemigo(Nono, America)")]),
    
    # West vendió misiles a Nono
    frozenset([Symbol("Vende(West, m, Nono)")]),
    
    # Negación de la hipótesis: West no es un criminal
    frozenset([Not(Symbol("Criminal(West)"))])
])

# Aplicar el algoritmo de resolución a las cláusulas
resultado, mensaje = resolution(clausulas)
print(mensaje)