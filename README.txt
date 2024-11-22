This project is NOT DONE YET; Not correct in all possible grammars of this format.

This program was made for my compiler theory and language design course. 

This program computes the FIRST() and FOLLOW() sets for a given grammar. 

The FIRST() and FOLLOW() sets are used in parsing algorithms to help determine the structure of a language during syntax analysis. 

The FIRST() set of a grammar production represents the set of terminals that can appear at the beginning of any string derived from that symbol, 
The FOLLOW() set of a grammar production represents the terminals that can appear immediately after that symbol in some derivation.

These sets aid in constructing parsing tables for LL and LR parsers, ensuring that parsers can handle input predictably and resolve ambiguities in parsing strings in the language of the grammar.
