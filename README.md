To run the code, you need to create your own environment and install all the dependencies there.

When you run the code, it asks you to enter a path of java project. By pressing enter, the code will navigate through the main directory and collect all the .java files then put them in one file (combined_input.txt) for reading. The latter file is provided to tree-sitter to generate the Abstract Syntax Tree AST of the whole software.

From the AST, the code takes each class, finds its name, and save it in a list that contains all classes to use it in the sensitivity check steps which are explained as follows:




