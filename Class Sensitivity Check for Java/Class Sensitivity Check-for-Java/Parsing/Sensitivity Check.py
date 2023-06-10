
'''
Created on Nov 8, 2022

@author: mohammed
'''


from tree_sitter import Language, Parser

from os import path

import csv

import pandas as pd


#from github import Github

#import git


#===============================================================================
#Use build_library method to compile the grammar of the language
#into a library and store it in build directory to be used by java
#### This method is available in https://github.com/tree-sitter/py-tree-sitter ####
#===============================================================================
LIB_PATH = path.join("build", "my-languages.so")

Language.build_library(
  # Store the library in the `build` directory
  LIB_PATH,
  # Include one or more languages
  [
 
    path.join("parsers", "tree-sitter-java"),
  ]
)

#===============================================================================
#Create an object from the language and load it into the project
#===============================================================================
JAVA_LANGUAGE = Language(LIB_PATH, 'java')
#===============================================================================

     
#Create the parser and configure it with the language object
#=============================================================================== 
parser = Parser()
parser.set_language(JAVA_LANGUAGE)
#=============================================================================== 



#Read the source code file and put its content into a list
#===============================================================================

#src = open("/home/mohammed/Examples/Person/src/person/PersonSerialization.java", "r")
#src = open("/home/mohammed/Downloads/Hotel-Management-Project-Java-master/Main.java", "r")
#src = open("/home/mohammed/Downloads/Shopping System/src/shopping/system/ShoppingSystem.java", "r")
#src = open("/home/mohammed/Downloads/Student/src/student/Student.java", "r")
#src = open("/home/mohammed/Downloads/Projects for Evaluation/PackrGUI-master/src/PackrGUI.java", "r")
#src = open("/home/mohammed/Downloads/Projects for Evaluation/commons-cli-master/src/main/java/org/apache/commons/cli/AlreadySelectedException.java", "r")
#src = open("/home/mohammed/Downloads/Projects for Evaluation/opencsv-master/src/au/com/bytecode/opencsv/bean/ColumnPositionMappingStrategy.java", "r")
src = open("/home/mohammed/Downloads/Projects for Evaluation/SquashBacktrace.java", "r")

content_list = src.readlines()
#print(content_list)

#git.Repo.clone_from("https://github.com/mah80/Person.git", "/home/mohammed/Examples/Test/")



#Clear the files
##################################################################
filename = ["/home/mohammed/Documents/Class Sensitivity Check Files/Class Attributes.csv",
            "/home/mohammed/Documents/Class Sensitivity Check Files/Class Methods.csv",
            "/home/mohammed/Documents/Class Sensitivity Check Files/Method Parameters.csv",
            "/home/mohammed/Documents/Class Sensitivity Check Files/Method Local Variables.csv",
            '/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Classes.csv',
            '/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Local Variables-Based Methods.csv',
            '/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Parameters-Based Methods.csv'
            ]

for filePath in filename:
    
####opening the file with w+ mode truncates the file
    f = open(filePath, "w+")
    f.close()
###################################################################



#===============================================================================
# src = open("/home/mohammed/Examples/Person/src/person/PersonSerialization.java", "rb")
# content_list = src.read()
# print(content_list)
# print(len(content_list))
#===============================================================================
#===============================================================================


#Use the reading function to read the source code file from
#the buffer and return it as bytes object encoded as UTF8
#### This function is available in https://github.com/tree-sitter/py-tree-sitter ####
#===============================================================================

def read_callable(byte_offset, point):
    row, column = point
    if row >= len(content_list) or column >= len(content_list[row]):
        return None
    return content_list[row][column:].encode('utf8')

#===============================================================================
# def read_callable(byte_offset, point):
#     return content_list[byte_offset:byte_offset+1]
#===============================================================================

#tree = parser.parse(read_callable)
#===============================================================================




#Walking the Syntax Tree
#### This function is available in https://github.com/tree-sitter/py-tree-sitter/issues/33 ####
#===============================================================================
def traverse_tree(tree):
    cursor = tree.walk()
 
    reached_root = False
    while reached_root == False:
        yield cursor.node
 
        if cursor.goto_first_child():
            continue
 
        if cursor.goto_next_sibling():
            continue
 
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
 
            if cursor.goto_next_sibling():
                retracing = False
#===============================================================================





#Parse the code by calling the reading method
#===============================================================================
tree = parser.parse(read_callable)
#===============================================================================
    


#Print the root node of the tree
#===============================================================================
root_node = tree.root_node
#print(root_node.type)
#===============================================================================



#Get the children number (node number) of the root
#===============================================================================
nodes_number = root_node.child_count
#===============================================================================



#Print the whole tree
#===============================================================================
#===============================================================================
#print(root_node.sexp())
#===============================================================================
#===============================================================================





#Print the first child in the tree and its next sibling
#===============================================================================
#===============================================================================
# first_child_in_the_tree = root_node.children[0]
# sibling_node = first_child_in_the_tree.next_sibling
# print(first_child_in_the_tree.type)
# print(sibling_node.type)
#===============================================================================
#===============================================================================
 
 
 
 
#Print all children (the nodes) of the tree
#===============================================================================
#===============================================================================
# for i in range(nodes_number):
#     print(root_node.children[i].type)
#===============================================================================
#===============================================================================




#The nodeNameFinder function that accept the start point and the end point of a node to slice 
#the code and extract the actual text of the node in the original code
#===============================================================================
def nodeNameFinder(startPoint, endPoint):
    
    text = ""
    row1, column1 = startPoint
    row2, column2 = endPoint
    for i in range(row1, row2 +1):
        for j in range(column1, column2):
            text += content_list[i][j]
    
    return text
#===============================================================================
            
    


#The classAttributesFinder function that accepts the node (which is a class_body type) to look for its attributes 
#and writes the class name along with its attributes in a file (/home/mohammed/Documents/JavaParser Files/Class Attributes.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name followed by its attributes
############################################################################# 
def classAttributesFinder(node, className):
    attribute_names = []
    
    attribute_names.append(className)
    
###A query to look for all the attributes in the class
###################################################### 
    attributeName_query = JAVA_LANGUAGE.query("""
      (class_body
      (field_declaration
      (variable_declarator
      (identifier) @attribute_name
      ) 
      )
      )
    """)
######################################################
    
    captures = attributeName_query.captures(node)

###Extract each attribute from the capture and put it in a list to save it later in the file
############################################################################################    
    for row in captures:
        node_captured = next(iter(row))
        attributeName = nodeNameFinder(node_captured.parent.child_by_field_name('name').start_point, node_captured.parent.child_by_field_name('name').end_point)
        attribute_names.append(attributeName)
############################################################################################



#Open the Class Attributes file to write the class name in the first cell followed by the class attributes
####################################################################
#===============================================================================
    with open('/home/mohammed/Documents/Class Sensitivity Check Files/Class Attributes.csv', 'a') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(attribute_names)
        file.close()
#===============================================================================
            


#The classMethodsFinder() function that accepts the node (which is a class_body type) and the class name
#to look for its methods and writes the class name along with its methods in a file (/home/mohammed/Documents/JavaParser Files/Class Methods.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name followed by its methods
#===============================================================================
def classMethodsFinder(node, className):

    classMethods = []
    
    method_names = []
    
    method_names.append(className)

###A query to look for all the methods in the class
######################################################    
    methodName_query = JAVA_LANGUAGE.query("""
      (class_body
      (method_declaration
      (identifier) @method_name
      ) 
      )
    """)
###################################################### 
    
    
    methodNameCaptures = methodName_query.captures(node)
    

###Extract each attribute from the capture and put it in a list to save it later in the file
############################################################################################     
    for row in methodNameCaptures:
        node_captured = next(iter(row))
        methodName = nodeNameFinder(node_captured.parent.child_by_field_name('name').start_point, node_captured.parent.child_by_field_name('name').end_point)
        method_names.append(methodName)
        classMethods.append(methodName)
############################################################################################     

    
    with open('/home/mohammed/Documents/Class Sensitivity Check Files/Class Methods.csv', 'a') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(method_names)
        file.close()
        
    return classMethods
             
#===============================================================================
    
   

#The methodParametersFinder() function that accepts the node (which is a class_body type), the class name, and a list of its methods
#to look for the parameters of each method and write them in a file (/home/mohammed/Documents/JavaParser Files/Method Parameters.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name,
#the second cell is the method name, then it is followed by the method parameters
############################################################################# 
def methodParametersFinder(node, className, class_methods):

    #method_nodes = []
    method_structures = []

    with open('/home/mohammed/Documents/Class Sensitivity Check Files/Method Parameters.csv', 'a') as file:
        writer = csv.writer(file, dialect='excel')


###A query to look for all the methods in the class
######################################################
        methodStructure_query = JAVA_LANGUAGE.query("""
          (class_body
          (method_declaration) @method_structure
          )
        """)
######################################################



###A query to look for all the parameters of any method in the class
######################################################   
        methodParameters_query = JAVA_LANGUAGE.query("""
          (method_declaration
          (formal_parameters
          (formal_parameter
          (identifier) @parameter_name
          )
          )
          )
        """)
######################################################   

    
        methodStructureCaptures = methodStructure_query.captures(node)

###Extract each method from the capture and put it in a list for the next use
############################################################################################        
        for methodStructure in methodStructureCaptures:
            method_captured = next(iter(methodStructure))
            method_structures.append(method_captured)
############################################################################################        

            

###Extract each parameter from the capture and put it in a list after the class name and the method name to save them later in the file
############################################################################################        
        for m in range(len(method_structures)):
            methodParameter_names = []
            methodParameter_names.append(className)
            methodParameter_names.append(class_methods[m])
            methodCaptures = methodParameters_query.captures(method_structures[m])
            
            for row in methodCaptures:
                node_captured = next(iter(row))
                methodParameterName = nodeNameFinder(node_captured.parent.child_by_field_name('name').start_point, node_captured.parent.child_by_field_name('name').end_point)
                methodParameter_names.append(methodParameterName)
############################################################################################
                
            writer.writerow(methodParameter_names)
                
        
    file.close() 

#############################################################################    



#The methodLocalVariablesFinder function that accepts the node (which is a class_body type), the class name, and a list of its methods
#to look for the local variables of each method and write them in a file (/home/mohammed/Documents/JavaParser Files/Method Local Variables.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name,
#the second cell is the method name, then it is followed by the method local variables
############################################################################# 
def methodLocalVariablesFinder(node, className, class_methods):

    method_structures = []
    
    
    with open('/home/mohammed/Documents/Class Sensitivity Check Files/Method Local Variables.csv', 'a') as file:
        writer = csv.writer(file, dialect='excel')

 
###A query to look for all the methods in the class
###################################################### 
        methodStructure_query = JAVA_LANGUAGE.query("""
          (class_body
          (method_declaration) @method_structure
          )
        """)
###################################################### 



###A query to look for all the local variables of any method in the class
######################################################      
        methodLocalVariables_query = JAVA_LANGUAGE.query("""
          (method_declaration
          (block
          (local_variable_declaration
          (variable_declarator
          (identifier) @variable_name
          )
          )
          )
          )
        """)
######################################################  
    
        methodStructureCaptures = methodStructure_query.captures(node)
 
 
###Extract each method from the capture and put it in a list for the next use
############################################################################################        
        for methodStructure in methodStructureCaptures:
            method_captured = next(iter(methodStructure))
            method_structures.append(method_captured)
############################################################################################        

            

###Extract each local variable from the capture and put it in a list after the class name and the method name
#to save them later in the file
############################################################################################        
        for m in range(len(method_structures)):
            methodLocalVar_names = []
            methodLocalVar_names.append(className)
            methodLocalVar_names.append(class_methods[m])
            methodCaptures = methodLocalVariables_query.captures(method_structures[m])
            
            for row in methodCaptures:
                node_captured = next(iter(row))
                methodLocalVariableName = nodeNameFinder(node_captured.parent.child_by_field_name('name').start_point, node_captured.parent.child_by_field_name('name').end_point)
                methodLocalVar_names.append(methodLocalVariableName)
############################################################################################        

                
            writer.writerow(methodLocalVar_names)
                
        
    file.close() 

#######################################################################################                         
  


#The keywordsCheck() function that accepts a term (which was extracted from a csv file) to look for it in Keywords Dictionary file. If it is existed, the function 
#returns True. Otherwise, it returns False.
#######################################################################################  
def keywordsCheck(term):
    
    b = False
    
    with open('/home/mohammed/Documents/Class Sensitivity Check Files/Keywords Dictionary.csv', 'r') as KWfile:
        
        keywordsReader = csv.reader(KWfile)
        
        for row in keywordsReader:
            for cell in row:
                if term == cell:
                        b = True
                        break
    
    KWfile.close()
    
    return b
#######################################################################################      
          
        
        
        
    


##The sensitiveClassCheck() function that checks the attributes of each class (in the Class Attributes file) whether are sensitive (existed in Keywords 
##Dictionary file). If yes, then the function writes the class name and its sensitive attributes in the Sensitive Classes file.
#===============================================================================
def sensitiveClassCheck():
    
    with open ('/home/mohammed/Documents/Class Sensitivity Check Files/Class Attributes.csv', 'r') as CAfile, open ('/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Classes.csv', 'a') as SCfile:
        
          classAttributesReader = csv.reader(CAfile)
          sensitiveClassesWriter = csv.writer(SCfile, dialect='excel')
#           
          for i in classAttributesReader:    ###Read the Class Attributes file line by line (Each line in the file represents a class record)
#       
              temp = []
              sensitive_classes = []
              temp = i
              
              if len(temp) > 1:             ###If the class has at least one attribute, then it will be sent to the keywordsCheck() function.
                                            ###Any class without attributes will not be sent.
                                            
                  sensitive_classes.append(temp[0])     ###Add the class name as a first element in the row
                  for i in temp[1:]:
                      flag = keywordsCheck(i)
                      if flag:
                          sensitive_classes.append(i)
              
              if len(sensitive_classes) > 1:                            ###Only the class with at least one sensitive attributes will be saved in the file
                  sensitiveClassesWriter.writerow(sensitive_classes)

    CAfile.close()
    SCfile.close()
 
#===========================================================================
#===============================================================================


#The sensitiveClassCheck() function that checks the parameters of each method (in the Method Parameters file) whether are sensitive (existed in Keywords 
##Dictionary file). If yes, then the function writes the method name and its sensitive parameters in the Sensitive Parameters-Based Methods file.
#===============================================================================
def sensitiveMethodParametersCheck():
    
    with open ('/home/mohammed/Documents/Class Sensitivity Check Files/Method Parameters.csv', 'r') as MPfile, open ('/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Parameters-Based Methods.csv', 'a') as SPBMfile:
        
        methodParametersReader = csv.reader(MPfile)
        sensitiveParametersBasedMethodWriter = csv.writer(SPBMfile, dialect='excel')
                
                
        for i in methodParametersReader:        ###Read the Method Parameters file line by line (Each line in the file represents a method record)
    
            temp = []
            sensitive_methods = []
            temp = i
           
            if len(temp) > 2:                  ###If the method has at least one parameter, then it will be sent to the keywordsCheck() function.
                                              ###Any method without parameters will not be sent.
                
                
                sensitive_methods.append(temp[0])  ###Add the method name as a first element in the row
                sensitive_methods.append(temp[1])   ###Add the method name as a second element in the row
                for i in temp[2:]:
                    flag = keywordsCheck(i)
                    if flag:
                        sensitive_methods.append(i)
                        
                    
               
            if len(sensitive_methods) > 2:                             ###Only the method with at least one sensitive parameter will be saved in the file
                sensitiveParametersBasedMethodWriter.writerow(sensitive_methods)
       
    MPfile.close()
    SPBMfile.close()
 
#===========================================================================
#===============================================================================



#The sensitiveMethodLocalVariablesCheck() function that checks the local variables of each method (in the Method Local Variables file) whether are 
#sensitive (existed in Keywords Dictionary file). If yes, then the function writes the method name and its sensitive local variables in
#the Sensitive Local Variables-Based Methods file.
#===============================================================================
def sensitiveMethodLocalVariablesCheck():
    
    with open ('/home/mohammed/Documents/Class Sensitivity Check Files/Method Local Variables.csv', 'r') as MLVfile, open ('/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Local Variables-Based Methods.csv', 'a') as SLVBMfile:
        
        methodLocalVariablesReader = csv.reader(MLVfile)
        sensitiveLocalVariablesBasedMethodWriter = csv.writer(SLVBMfile, dialect='excel')
                
                
        for i in methodLocalVariablesReader:        ###Read the Method Local Variables file line by line (Each line in the file represents a method record)
    
            temp = []
            sensitive_methods = []
            temp = i
           
            if len(temp) > 2:                       ###If the method has at least one local variable, then it will be sent to the keywordsCheck() function.
                                                   ###Any method without local variables will not be sent.
                
                
                
                sensitive_methods.append(temp[0])  ###Add the method name as a first element in the row
                sensitive_methods.append(temp[1])  ###Add the method name as a second element in the row
                for i in temp[2:]:
                    flag = keywordsCheck(i)
                    if flag:
                        sensitive_methods.append(i)
                        
                    
               
            if len(sensitive_methods) > 2:          ###Only the method with at least one sensitive local variable will be saved in the file
                sensitiveLocalVariablesBasedMethodWriter.writerow(sensitive_methods)
       
    MLVfile.close()
    SLVBMfile.close()
 
#===========================================================================
    


##The classSensitivityCount() function that counts the sensitivity level of each class based on its sensitive attributes and its sensitive methods. It takes
##the required data of each class from its files which were created from the other functions above
#===============================================================================
def classSensitivityCount():
    
    
    ##Open three csv files (Sensitive Classes.csv, Sensitive Local Variables-Based Methods.csv, Sensitive Parameters-Based Methods.csv) for reading
    with open ('/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Classes.csv', 'r') as SCfile, open ('/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Local Variables-Based Methods.csv', 'r') as SLVBMfile, open ('/home/mohammed/Documents/Class Sensitivity Check Files/Sensitive Parameters-Based Methods.csv', 'r') as SPBMfile, open ('/home/mohammed/Documents/Class Sensitivity Check Files/Class Attributes.csv', 'r') as CAfile, open('/home/mohammed/Documents/Class Sensitivity Check Files/Class Methods.csv', 'r') as CMfile:
        
        sensitiveClassesReader = csv.reader(SCfile)
        sensitiveLocalVariablesBasedMethodReader = csv.reader(SLVBMfile)
        sensitiveParametersBasedMethodReader = csv.reader(SPBMfile)
        classAttributesReader = csv.reader(CAfile)
        classMethodsReader = csv.reader(CMfile)
        
        
        
        for i in sensitiveClassesReader:                    ##Take every sensitive class from the file
            sensitiveLocalVariablesBasedMethod = []         ##Define a list for the sensitive local variables based methods in the class
            sensitiveParametersBasedMethod = []             ##Define a list for the sensitive parameters based methods in the class
            sensitiveLocalVariablesBasedMethodCounter = 0
            sensitiveParametersBasedMethodCounter = 0
            sensitiveClassMethods = 0
            classAttributesCounter = 0
            classMethodsCounter = 0
            sensitiveAttributesRatio = 0
            sensitiveMethodsRatio = 0
            sensitivityClassLevel = 0
            
            sensitiveClass = []
            sensitiveClass = i
            noOfSensitiveAttributes = len(sensitiveClass) - 1
            
            
            
            for l in classAttributesReader:                 ##Count the number of attributes and the ratio of sensitive attributes in each class
                classAttributes = []                        
                classAttributes = l
                if sensitiveClass[0] in classAttributes:
                    classAttributesCounter = len(classAttributes) - 1
                    break
            sensitiveAttributesRatio = noOfSensitiveAttributes/classAttributesCounter              
            
            
                    
            for m in classMethodsReader:                    ##Count the number of methods in each class
                classMethods = []
                classMethods = m
                if sensitiveClass[0] == classMethods[0]:
                    classMethodsCounter = len(classMethods) - 1
                    break   
            
            
            
            
            for j in sensitiveLocalVariablesBasedMethodReader:      ##Find the sensitive local variables based methods in each class
                sensitiveLocalVariables = []
                sensitiveLocalVariables = j
                
                className = sensitiveLocalVariables[0]
                for jj in sensitiveLocalVariables[2:]:                    
                    if sensitiveClass[0] == className and jj in sensitiveClass:
                        sensitiveLocalVariablesBasedMethod.append(sensitiveLocalVariables[1])
                        break
                       
                        
                        
                                            
                  
            for k in sensitiveParametersBasedMethodReader:          ##Find the sensitive parameters based methods in each class
                sensitiveParameters = []                            
                sensitiveParameters = k
                
                className = sensitiveParameters[0]
                for kk in sensitiveParameters[2:]:
                    if sensitiveClass[0] == className and kk in sensitiveClass:
                        sensitiveParametersBasedMethod.append(sensitiveParameters[1])
                        break
                      
                         
                        
                              
            sensitiveLocalVariablesBasedMethodCounter = len(sensitiveLocalVariablesBasedMethod)  ##Find the total number of sensitive methods number/ratio
            sensitiveParametersBasedMethodCounter = len(sensitiveParametersBasedMethod)          ##in each class
            for n in sensitiveLocalVariablesBasedMethod:
                if n in sensitiveParametersBasedMethod:
                    sensitiveLocalVariablesBasedMethodCounter -= 1         
            sensitiveClassMethods = sensitiveLocalVariablesBasedMethodCounter + sensitiveParametersBasedMethodCounter
            sensitiveMethodsRatio = sensitiveClassMethods/classMethodsCounter
            
            
            
            sensitivityClassLevel = (sensitiveAttributesRatio * 0.5) + (sensitiveMethodsRatio * 0.5)
                     
            print("The ratio of sensitive attributes in class ", sensitiveClass[0], " is ", sensitiveAttributesRatio)
             
            print("The ratio of sensitive methods in class ", sensitiveClass[0], " is ", sensitiveMethodsRatio)
            
            print("The sensitivity level of class ", sensitiveClass[0], " is ", sensitivityClassLevel)
            
            print("\n")

        
        
        SCfile.close()
        SLVBMfile.close()
        SPBMfile.close()
        CAfile.close()
        CMfile.close()
#===============================================================================
        
        
    






#Invoke the traverse_tree function to look for the class attributes 
#===============================================================================     


for node in traverse_tree(tree):                #Call the traverse_tree() method to look for any class structure in the Java file
    
        if node.type == 'class_declaration':
            

        

            class_methods = []                  #Define a list for the set of methods in the class

            
            #Find the class name to use it in each call of the following methods
            ####################################################################
            class_name = nodeNameFinder(node.child_by_field_name('name').start_point, node.child_by_field_name('name').end_point)
            ####################################################################
            #print(node.child_by_field_name('name'))
            print(class_name)            
            
            #Find the attributes of the class
            ####################################################################
            classAttributesFinder(node, class_name)
            ####################################################################
            
            
            #Find the methods of the class
            ####################################################################
            class_methods = classMethodsFinder(node, class_name)
            ####################################################################
            
            
            #Find the parameters of the method
            ####################################################################
            methodParametersFinder(node, class_name, class_methods)
            ####################################################################
            
            
            #Find the local variables of the method
            ####################################################################
            methodLocalVariablesFinder(node, class_name, class_methods)
            ####################################################################
            

#Find the sensitive classes based on the attributes
####################################################################
sensitiveClassCheck()
####################################################################


#Find the sensitive methods based on the parameters
####################################################################
sensitiveMethodParametersCheck()
####################################################################


#Find the sensitive methods based on the local variables
####################################################################
sensitiveMethodLocalVariablesCheck()
####################################################################

classSensitivityCount()

#Open the file for reading
#####################################################################
# Open file
#===============================================================================
# with open('/home/mohammed/Documents/students.csv') as file_obj:
#     
#     # Create reader object by passing the file
#     # object to reader method
#     reader_obj = csv.reader(file_obj)
#     
#     # Iterate over each row in the csv
#     # file using reader object
#     for row in reader_obj:
#         print(row)
#===============================================================================
######################################################################



#===============================================================================

#===============================================================================
