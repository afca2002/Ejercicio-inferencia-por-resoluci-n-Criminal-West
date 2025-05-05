# -*- coding: utf-8 -*-
"""
Resolución de Knights and Knaves (Caballeros y Canallas)

Este programa resuelve acertijos lógicos donde los personajes (A, B, C) pueden ser
caballeros (siempre dicen la verdad) o canallas (siempre mienten). Utiliza lógica proposicional
para determinar quién es quién en base a las declaraciones dadas.
"""

# Clase base para representar una oración lógica
class Sentence:
    def evaluate(self, model):
        """Evalúa si la oración lógica es verdadera en un modelo dado."""
        raise Exception("Método evaluate no implementado")

    def formula(self):
        """Devuelve la fórmula lógica como una cadena."""
        return ""

    def symbols(self):
        """Devuelve un conjunto de todos los símbolos en la oración lógica."""
        return set()

    @classmethod
    def validate(cls, sentence):
        """Valida que una oración sea una instancia de la clase Sentence."""
        if not isinstance(sentence, Sentence):
            raise TypeError("Debe ser una oración lógica (Sentence)")

    @classmethod
    def parenthesize(cls, s):
        """Agrega paréntesis a una expresión si no los tiene."""
        def balanced(s):
            """Verifica si una cadena tiene paréntesis balanceados."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"

# Clase para representar un símbolo lógico
class Symbol(Sentence):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        """Evalúa el valor del símbolo en el modelo dado."""
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"Variable {self.name} no está en el modelo")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}

# Clase para representar la negación lógica (¬)
class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        """Evalúa la negación del operando."""
        return not self.operand.evaluate(model)

    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        return self.operand.symbols()

# Clase para representar la conjunción lógica (∧)
class And(Sentence):
    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __repr__(self):
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    def evaluate(self, model):
        """Evalúa si todas las conjunciones son verdaderas."""
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts])

    def symbols(self):
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])

# Clase para representar la disyunción lógica (∨)
class Or(Sentence):
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        """Evalúa si al menos una disyunción es verdadera."""
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        return " ∨ ".join([Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts])

    def symbols(self):
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])

# Clase para representar la implicación lógica (=>)
class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        """Evalúa si la implicación es verdadera."""
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())

# Función para verificar si el conocimiento implica una consulta
def model_check(knowledge, query):
    """Verifica si la base de conocimiento implica la consulta."""

    def check_all(knowledge, query, symbols, model):
        """Verifica todos los modelos posibles."""
        if not symbols:
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:
            remaining = symbols.copy()
            p = remaining.pop()
            model_true = model.copy()
            model_true[p] = True
            model_false = model.copy()
            model_false[p] = False
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    symbols = set.union(knowledge.symbols(), query.symbols())
    return check_all(knowledge, query, symbols, dict())

# Definimos los símbolos para los personajes
AKnight = Symbol("A es Caballero")
AKnave = Symbol("A es Canalla")
BKnight = Symbol("B es Caballero")
BKnave = Symbol("B es Canalla")
CKnight = Symbol("C es Caballero")
CKnave = Symbol("C es Canalla")

# Base de conocimiento común
KnowledgeBase = And(
    Or(AKnight, AKnave),  # A es caballero o canalla
    Or(BKnight, BKnave),  # B es caballero o canalla
    Or(CKnight, CKnave),  # C es caballero o canalla
    Not(And(AKnight, AKnave)),  # A no puede ser ambos
    Not(And(BKnight, BKnave)),  # B no puede ser ambos
    Not(And(CKnight, CKnave))   # C no puede ser ambos
)

# Puzzle 0
knowledge0 = And(
    KnowledgeBase,
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
knowledge1 = And(
    KnowledgeBase,
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
knowledge2 = And(
    KnowledgeBase,
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight))),
    Implication(BKnave, Not(Or(And(BKnight, AKnave), And(BKnave, AKnight))))
)

# Evaluación de los puzzles
def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        for symbol in symbols:
            if model_check(knowledge, symbol):
                print(f"    {symbol}")

if __name__ == "__main__":
    main()