from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# 1. Character Statements
# A says "I am both a knight and a knave."
kb0_stmt0 = And(AKnight, AKnave)

knowledge0 = And(
    # TODO
    # 2. Facts
    Or(AKnight, AKnave), 
    # 3. Conditions for the Statements
    Implication(AKnight, kb0_stmt0), 
    Implication(AKnave, Not(kb0_stmt0)), 
)

# Puzzle 1
# 1. Character Statements
# A says "We are both knaves."
kb1_stmt0 = And(AKnave, BKnave)
# B says nothing.
# Which means no sentence could be made.

knowledge1 = And(
    # TODO
    # 2. Facts
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    # 3. Conditions for the Statements
    Implication(AKnight, kb1_stmt0), 
    Implication(AKnave, Not(kb1_stmt0)), 
)

# Puzzle 2
# 1. Character Statements
# A says "We are the same kind."
kb2_stmt0 = Or(
    And(AKnight, BKnight), 
    And(AKnave, BKnave)
)
# B says "We are of different kinds."
kb2_stmt1 = Or(
    And(AKnight, BKnave), 
    And(AKnave, BKnight)
)

knowledge2 = And(
    # TODO
    # 2. Facts
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    # 3. Conditions for the Statements
    Implication(AKnight, kb2_stmt0), 
    Implication(AKnave, Not(kb2_stmt0)), 
    Implication(BKnight, kb2_stmt1), 
    Implication(BKnave, Not(kb2_stmt1)), 
)

# Puzzle 3
# 1. Character Statements
# A says either "I am a knight." or "I am a knave.", but you don't know which.
kb3_stmt0 = Or(AKnight, AKnave)
# B says "A said 'I am a knave'."
kb3_stmt1 = Biconditional(kb3_stmt0, AKnave) 
# B says "C is a knave."
kb3_stmt2 = CKnave
# C says "A is a knight."
kb3_stmt3 = AKnight

knowledge3 = And(
    # TODO
    # 2. Facts
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    Or(CKnight, CKnave), 
    # 3. Conditions for the Statements
    Implication(AKnight, kb3_stmt0), 
    Implication(AKnave, Not(kb3_stmt0)), 
    Implication(BKnight, kb3_stmt1), 
    Implication(BKnave, Not(kb3_stmt1)), 
    Implication(BKnight, kb3_stmt2), 
    Implication(BKnave, Not(kb3_stmt2)), 
    Implication(CKnight, kb3_stmt3), 
    Implication(CKnave, Not(kb3_stmt3)), 
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
