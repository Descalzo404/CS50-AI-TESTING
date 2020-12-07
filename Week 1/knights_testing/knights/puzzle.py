from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a Knight and a Knave."
knowledge0 = And(
    # ---> Rules for the game
    Or(AKnight, AKnave), #A can be a Knight or a Knave
    Implication(AKnight, Not(AKnave)), #If A is a Knight than he can't be a Knave
    Implication(AKnave, Not(AKnight)), #If A is a Knave than he can't be a Knight

    # ---> Frases for the puzzle

    # A can be a Knight if and only if he is both a Knave and a Knight
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both Knaves."
# B says nothing.
knowledge1 = And(
    # ---> Rules for the game
    Or(AKnight, AKnave), #A can be a Knight or a Knave
    Implication(AKnight, Not(AKnave)), #If A is a Knight than he can't be a Knave
    Implication(AKnave, Not(AKnight)), #If A is a Knave than he can't be a Knight

    Or(BKnight, BKnave), #B can be a Knight or a Knave
    Implication(BKnight, Not(BKnave)), #If B is a Knight than he can't be a Knave
    Implication(BKnave, Not(BKnight)), #If B is a Knave than he can't be a Knight

    # ---> Frases for the puzzle

    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # ---> Rules for the game

    Or(AKnight, AKnave), #A can be a Knight or a Knave
    Implication(AKnight, Not(AKnave)), #If A is a Knight than he can't be a Knave
    Implication(AKnave, Not(AKnight)), #If A is a Knave than he can't be a Knight

    Or(BKnight, BKnave), #B can be a Knight or a Knave
    Implication(BKnight, Not(BKnave)), #If B is a Knight than he can't be a Knave
    Implication(BKnave, Not(BKnight)), #If B is a Knave than he can't be a Knight

    # ---> Frases for the puzzle

    # A is a Knight if and only if A and B are both Knights or they are both Knaves
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # B is a Knight if and only if A is a Knight and B a Knave or the other way around
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
    
)

# Puzzle 3
# A says either "I am a Knight." or "I am a Knave.", but you don't know which.
# B says "A said 'I am a Knave'."
# B says "C is a Knave."
# C says "A is a Knight."
knowledge3 = And(
    # ---> Rules for the game
    Or(AKnight, AKnave), #A can be a Knight or a Knave
    Implication(AKnight, Not(AKnave)), #If A is a Knight than he can't be a Knave
    Implication(AKnave, Not(AKnight)), #If A is a Knave than he can't be a Knight

    Or(BKnight, BKnave), #B can be a Knight or a Knave
    Implication(BKnight, Not(BKnave)), #If B is a Knight than he can't be a Knave
    Implication(BKnave, Not(BKnight)), #If B is a Knave than he can't be a Knight

    Or(CKnight, CKnave), #C can be a Knight or a Knave
    Implication(CKnight, Not(CKnave)), #If C is a Knight than he can't be a Knave
    Implication(CKnave, Not(CKnight)), #If C is a Knave than he can't be a Knight

    # ---> Frases for the puzzle

    # A is a knight if and only if he said the truth (that he is either a knight or a knave)
    Biconditional(AKnight, Or(AKnight, AKnave)),

    # B is a Knight if and only if A said that A is a Knave
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    # B is a Knight if and only if C is a Knave
    Biconditional(BKnight, CKnave),

    # C is a Knight if and only if A is a Knight
    Biconditional(CKnight, AKnight)

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
