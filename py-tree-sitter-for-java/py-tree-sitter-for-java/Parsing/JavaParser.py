
'''
Created on Nov 8, 2022

@author: mohammed
'''


from tree_sitter import Language, Parser

from os import path

import csv


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
src = open("/home/mohammed/Downloads/Hotel-Management-Project-Java-master/Main.java", "r")
content_list = src.readlines()
#print(content_list)

#git.Repo.clone_from("https://github.com/mah80/Person.git", "/home/mohammed/Examples/Test/")



#Clear the files
##################################################################
filename = ["/home/mohammed/Documents/JavaParser Files/Class Attributes.csv",
            "/home/mohammed/Documents/JavaParser Files/Class Methods.csv",
            "/home/mohammed/Documents/JavaParser Files/Method Parameters.csv",
            "/home/mohammed/Documents/JavaParser Files/Method Local Variables.csv"
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




#===============================================================================
def attributeCheck(attributesList):
    sensitive_attributes = []
    with open(r'/home/mohammed/Examples/Person/Dictionary.txt', 'r') as file:
        attributes = file.read()
        for i in range(len(attributesList)):
            if attributesList[i] in attributes:
                sensitive_attributes.append(attributesList[i])
                #num += 1
                #print(attributesList[i])
        #print(num, "/", len(attributesList))
    return sensitive_attributes
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
            
    


#The classAttributesFinder method that accept the node (which is a class_body type) to look for its attributes 
#and write the class name along with its attributes in a file (/home/mohammed/Documents/JavaParser Files/Class Attributes.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name 
#then it is followed by its attributes
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
    with open('/home/mohammed/Documents/JavaParser Files/Class Attributes.csv', 'a') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(attribute_names)
        file.close()
#===============================================================================
            


#The classMethodsFinder() method that accept the node (which is a class_body type) and the class name
#to look for its methods and write the class name along with its methods in a file (/home/mohammed/Documents/JavaParser Files/Class Methods.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name 
#then it is followed by its methods
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

    
    with open('/home/mohammed/Documents/JavaParser Files/Class Methods.csv', 'a') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(method_names)
        file.close()
        
    return classMethods
             
#===============================================================================
    
   

#The methodParametersFinder() method that accept the node (which is a class_body type), the class name, and a list of its methods
#to look for the parameters of each method and write them in a file (/home/mohammed/Documents/JavaParser Files/Method Parameters.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name,
#the second cell is the method name, then it is followed by the method parameters
############################################################################# 
def methodParametersFinder(node, className, class_methods):

    #method_nodes = []
    method_structures = []

    with open('/home/mohammed/Documents/JavaParser Files/Method Parameters.csv', 'a') as file:
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

            

###Extract each parameter from the capture and put it in a list after the class name and the method name
#to save them later in the file
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



#The methodLocalVariablesFinder method that accepts the node to check it, if it is a "method_declaration" then it looks for 
#its local variables to save them in a file (/home/mohammed/Documents/JavaParser Files/Method Local Variables.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name,
#the second cell is the method name, then it is followed by the method local variables
############################################################################# 
def methodLocalVariablesFinder(node, className, class_methods):

    method_structures = []
    
    
    with open('/home/mohammed/Documents/JavaParser Files/Method Local Variables.csv', 'a') as file:
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
                methodParameterName = nodeNameFinder(node_captured.parent.child_by_field_name('name').start_point, node_captured.parent.child_by_field_name('name').end_point)
                methodLocalVar_names.append(methodParameterName)
############################################################################################        

                
            writer.writerow(methodLocalVar_names)
                
        
    file.close() 

#######################################################################################                         
  
    
#The sensitiveClassSummary function accepts the order number (sequence number) of the sensitive class, the class name, and its sensitive attributes
# to put all of them in a list as a summary 
#####################################################################################
def sensitiveClassSummary(seq_Num, className, sensitiveAttributes):
    summaryList = []
    
    summaryList.append(seq_Num)
    summaryList.append(className)
    summaryList.append(sensitiveAttributes)
    
    return summaryList
#####################################################################################

    



#Invoke the traverse_tree function to look for the class attributes 
#===============================================================================     


for node in traverse_tree(tree):                #Call the traverse_tree() method to look for any class structure in the Java file
        if node.type == "class_body":           #Check the type of the node

            class_methods = []                  #Define a list for the set of methods in the class

            
            class_name = nodeNameFinder(node.parent.child_by_field_name('name').start_point, node.parent.child_by_field_name('name').end_point)
            
            #class_attributes = classAttributesFinder(node)
            
            classAttributesFinder(node, class_name)
            
            class_methods = classMethodsFinder(node, class_name)
            
            methodParametersFinder(node, class_name, class_methods)
            
            methodLocalVariablesFinder(node, class_name, class_methods)
            




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
