# Demo

This project aims to define statements for the existing knowledge bases  
(`knowledge0` to `knowledge3`) which could correctly describe the state of  
the 4 Puzzles (Puzzle 0 to Puzzle 3). And last but not least, solve the  
puzzles by running the procedure.

## Structure

The context of the knowledge bases are written as the same structure. Each  
knowledge base is built by 3 parts:

1. **Character Statements**. Each sentence said by the character is created  
as statement contructed with existing Symbol defined by the question itself.

2. **Facts**. Basic logic to be followed (definition of a Knight and Knave  
puzzle) are added into the knowledge base.

3. **Conditions for the Statements**. Here we use the Character Statements  
defined above to build some conditional statements, which is to defined the  
conditions for Character Statements to be `True`, and add them into the  
knowledge base.
