To run the tool, you need to create your own environment and install all the dependencies (Except tree-sitter which is already there).

When you run the tool, it asks you to enter a path of java project. By pressing enter, the tool will navigate through the main directory and collect all the .java files then put them in one file (combined_input.txt) for reading. The latter file is provided to tree-sitter to generate the Abstract Syntax Tree AST of the whole software.

**Structure Information:**
From the AST, the tool takes each class, finds its name, and saves it in a list that contains all classes to use it in the **Sensitivity Check** steps which are explained as follows:

1. Identify the attributes of each class and save them in a csv file (Class Attributes.csv). Each row in the file represents a class record, the first cell is the class name and every other cell is an attribute. If the class does not have attributes, then the row has only the class name.

2. Identify the methods of each class and save them in a csv file (Class Methods.csv). Each row in the file represents a class record, the first cell is the class name and every other cell is a method. If the class does not have methods (Which is not common), then the row has only the class name.

3. For every method in the class, identify the parameter types and save them in a csv file (Method Parameters.csv). Each row in the file represents a method record, the first cell is the class name, the second cell is the method name, and every other cell is a type of parameter. If the method does not have parameters, then the row has only class name and method name.

4. For every method in the class, identify the local variable types and save them in a csv file (Method Local Variables.csv). Each row in the file represents a method record, the first cell is the class name, the second cell is the method name, and every other cell is a type of local variable. If the method does not have local variables, then the row has only class name and method name.

5. For every method in the class, identify the local variable assignment (The variable on the left side of the assignment) and save them in a csv file (Method Assignment Variables.csv). Each row in the file represents a method record, the first cell is the class name, the second cell is the method name, and every other cell is a variable that is located on the left side of the assignment. If the method does not have assignments, then the row has only class name and method name.

**Sensitivity Check:**
After extracting the structure information, the tool starts to identify the sensitive classes as follows:

1. From Class Attributes.csv file, it checks the attributes of each class whether they are sensitive attributes (If they are existed in the Keywords Dictionary.csv file). The is classified as sensitive class if it has at least one sensitive attribute. The sensitive classes are saved in a csv file (Sensitive Classes.csv). Each row in the file represents a sensitive class record, the first cell is the sensitive class name, and every other cell is a sensitive attribute in the class.

2. To check the sensitivity of every method in the class, the tool considers three different cases which are: if the method has at least one object parameter which its type is sensitive (as classified in the previous step) then the method is classified as sensitive method. If the method has at least one local variable which is an instance of a sensitive class, then the method is classified as sensitive method. If the method has an assignment where the left side is a sensitive attribute of the same class, then the method is classified as sensitive method. The output of the three cases is saved in csv files, Sensitive Parameters-Based Methods.csv, Sensitive Local Variables-Based Methods.csv, and Sensitive Assignment Variables-Based Methods.csv, respectively. Every row in the file represnts a sensitive method record, the first cell is the class name, the second cell is the method name, and the other cells are the sensitive parameter/local variable/local assignment.

3. To measure the sensitivity level of each class, the tool checks if the class has only sensitive attributes, or if the class has sensitive attributes and sensitive methods, or if the class has only sensitive methods. The next formulas explain the computation:
   
   The ratio of sensitive attributes of the class = no. of sensitive attributes in the class/ no. of total attributes in the class

   The ratio of sensitive methods of the class = no. of sensitive methods in the class/ no. of total methods in the class

   The sensitivity level of the class = (The ratio of sensitive attributes of the class * 0.5) + (The ratio of sensitive methods of the class * 0.5)

The final sensitive classes are saved in a csv file (Unsorted Sensitive Classes.csv). Each row represents a sensitive class record, the first cell of the row is the class name, and the second cell is the sensitivity level. All the classes are sorted desendenly based on the sensitive level and they are saved in Sorted Sensitive Classes.csv file.
