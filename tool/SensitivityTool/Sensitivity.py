
'''
Created on Nov 8, 2022

@author: mohammed
'''


from tree_sitter import Language, Parser

from os import path

import csv

import os

import pandas as pd

# Load the Java language grammar
Language.build_library(
    'build/my-languages.so',
    [
        './tool/SensitivityTool/tree-sitter-java'
    ]
)

JAVA_LANGUAGE = Language('build/my-languages.so', 'java')

#Create the parser and configure it with the language object
#=============================================================================== 
parser = Parser()
parser.set_language(JAVA_LANGUAGE)




################################################################################
#####################        Main callable function        #####################
################################################################################

# Define global variables

content_list = [] # Variable to load the code as a list
OUTPUT_DIR = ""
CONFIG_DIR = "Config/"

def analyzer(project_directory, projectID, keywords=None):
    #Take the path of the source code from the user to collect the .java files and save them in a single file for parsing
    #===============================================================================
    # List of file extensions to include
    file_extensions = [ '.java']

    # List to store file contents
    file_contents = []

    # Accessing global vars
    global content_list
    global OUTPUT_DIR
    OUTPUT_DIR =  os.path.join("Output",projectID)


    # Recursively traverse directories
    for root, directories, files in os.walk(project_directory):
        for file in files:
            if file.startswith('__MACOSX/') or file.startswith('._'):
                continue
            file_path = os.path.join(root, file)
            if os.path.splitext(file_path)[1] in file_extensions:
                file_contents.append(process_file(file_path))
    

    # Combine file contents into a single string then write to a new file

    combined_contents = '\n'.join(file_contents)
    with open('combined_input.txt', 'w', encoding='utf-8') as f:
    #with open('combined_input.txt', 'w') as f:
        f.write(combined_contents)
    src = open("combined_input.txt", "r", encoding='utf-8')
    #src = open("combined_input.txt", "r")
    content_list = src.readlines()

    f.close()


    print(len(content_list))
    
    #Clear all the files before writing the new data. These files are created to save the results of the parsing process
    ##################################################################
    filename = [
        # Class Attributes.csv
        # Structure: Class Name (string), Attribute Name (string)
        "Class Attributes.csv",
        
        # Class Methods.csv
        # Structure: Class Name (string), Method Name (string)
        "Class Methods.csv",
        
        # Method Parameters_Class.csv
        # Structure: Class Name (string), Method Name (string), Parameter Names (string) of the method
        "Method Parameters_Class.csv",
        
        # Method Local Variables_Class.csv
        # Structure: Class Name (string), Method Name (string), Local Variable Names (string) of the method
        "Method Local Variables_Class.csv",
        
        # Method Assignment Variables_Class.csv
        # Structure: Class Name (string), Method Name (string), identifiers/atributte Names (string) in the method body
        "Method Local Identifiers_Class.csv",
        
        # Sensitive Classes.csv
        # Structure: Class Name (string), Sensitive Attribute Name (string)
        "Sensitive Classes.csv",
        
        # Sensitive Local Variables-Based Methods_Class.csv
        # Structure: Class Name (string), Method Name (string), Local Variable Names (string) of the method
        "Sensitive Local Variables-Based Methods_Class.csv",
        
        # Sensitive Parameters-Based Methods_Class.csv
        # Structure: Class Name (string), Method Name (string), Parameter Name (string) of the method
        "Sensitive Parameters-Based Methods_Class.csv",
        
        # Sensitive Assignment Variables-Based Methods_Class.csv
        # Structure: Class Name (string), Method Name (string), Sensitive Identifier/Attribute Names (string)
        "Sensitive Local Identifiers-Based Methods_Class.csv",
        
        # Interface Attributes.csv
        # Structure: Interface Name (string), Attribute Names (string)
        "Interface Attributes.csv",
        
        # Interface Methods.csv
        # Structure: Interface Name (string), Method Names (string)
        "Interface Methods.csv",
        
        # Sensitive Interfaces.csv
        # Structure: Interface Name (string), Sensitive Attribute Names (string)
        "Sensitive Interfaces.csv",
        
        # Method Parameters_Interface.csv
        # Structure: Interface Name (string), Method Name (string), Parameter Names (string) of the method
        "Method Parameters_Interface.csv",

        
        
        # Sensitive Parameters-Based Methods_Interface.csv
        # Structure: Interface Name (string), Method Name (string), Parameter Names (string) of the method
        "Sensitive Parameters-Based Methods_Interface.csv",
        
        
        # Enumeration Attributes.csv
        # Structure: Enumeration Name (string), Enum Constants (string)
        "Enumeration Enum Constants.csv",
        
        
        # Enumeration Methods.csv
        # Structure: Enumeration Name (string), Method Name (string)
        "Enumeration Methods.csv",
        
        
        
        # Sensitive Enumerations.csv
        # Structure: Enumeration Name (string), Sensitive Attribute Names (string)
        "Sensitive Enumerations.csv",
        
        
        # Method Parameters_Enumeration.csv
        # Structure: Enumeration Name (string), Method Name (string), Parameter Names (string) of the method
        "Method Parameters_Enumeration.csv",
        
        
        # Method Local Variables_Enumeration.csv
        # Structure: Enumeration Name (string), Method Name (string), Local Variable Names (string) of the method
        "Method Local Variables_Enumeration.csv",
        
        
        # Method Assignment Variables_Enumeration.csv
        # Structure: Enumeration Name (string), Method Name (string), Identifiers/Attribute Names (string) in the method body
        "Method Local Identifiers_Enumeration.csv",
        
        
        # Sensitive Parameters-Based Methods_Enumeration.csv
        # Structure: Enumeration Name (string), Method Name (string), Parameter Names (string) of the method
        "Sensitive Parameters-Based Methods_Enumeration.csv",
        
        
        # Sensitive Local Variables-Based Methods_Enumeration.csv
        # Structure: Enumeration Name (string), Method Name (string), Local Variable Names (string) of the method
        "Sensitive Local Variables-Based Methods_Enumeration.csv",
        
        
        # Sensitive Assignment Variables-Based Methods_Enumeration.csv
        # Structure: Enumeration Name (string), Method Name (string), Identifiers/Attribute Names (string) in the method body
        "Sensitive Local Identifiers-Based Methods_Enumeration.csv",
        
        
        
        # Statistics.csv
        # Structure: Statistic Name (string), Value (integer)
        "Software Statistics.csv",
        
        # Type Statistic.csv
        # Structure: Type Name (string), Count (integer)
        "Classifier Statistic.csv",
        
        
        # Sorted Normalized Type Statistic.csv
        # Structure: Type Name (string), Count (integer)
        "Sorted Normalized Type Statistic.csv",
        
        
        # Normalized Type Statistic.csv
        # Structure: Type Name (string), Count (integer)
        "Normalized Type Statistic.csv",
        
        
        # 'Sensitivity Ratio Statistic.csv',
        
        # 'Normalized Sensitivity Ratio Statistic.csv',
        
        # 'Sorted Normalized Sensitivity Ratio Statistic.csv'
    ]
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filePath in filename:
        
    ####opening the file with w+ mode truncates the file
        f = open(os.path.join(OUTPUT_DIR,filePath), "w+")
        f.close()
    ###################################################################

    #===============================================================================


    def read_callable(byte_offset, point):
        row, column = point
        if row >= len(content_list) or column >= len(content_list[row]):
            return None
        return content_list[row][column:].encode('utf8')


    #Parse the code by calling the reading method
    #===============================================================================
    tree = parser.parse(read_callable)
    #===============================================================================


    #Print the root node of the tree
    #===============================================================================
    root_node = tree.root_node
    #===============================================================================



    #Get the children number (node number) of the root
    #===============================================================================
    nodes_number = root_node.child_count
    #===============================================================================

    #Invoke the traverse_tree function to look for the class attributes 
    #===============================================================================     

    typeNames = []
    classNames = []
    interfaceNames = []
    enumNames = []

    for node in traverse_tree(tree):                #Call the traverse_tree() method to look for any class structure in the Java file
        
            ####################################################################
            #The CLASS section_Beginning
            ####################################################################
            if node.type == 'class_declaration':
                

                type = 'Class'

                class_methods = []                  #Define a list for the set of methods in the class

                
                #Find the class name to use it in each call of the following methods
                ####################################################################
                class_name = nodeNameFinder(node.child_by_field_name('name').start_point, node.child_by_field_name('name').end_point)
                ####################################################################
                classNames.append(class_name)
            
                
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
                methodParametersFinderForClass(node, class_name, class_methods)
                ####################################################################
                
                
                #Find the local variables of the method
                ####################################################################
                methodLocalVariablesTypeFinderForClass(node, class_name, class_methods)
                ####################################################################
                
                #Find the local assignments of the method
                ####################################################################
                methodLocalAssignmentsFinderForClass(node, class_name, class_methods)
                ####################################################################
            
        
            ####################################################################
            #The CLASS section_End
            ####################################################################
            
            
            
            ####################################################################
            
            
            
            ####################################################################
            #The INTERFACE section_Beginning
            ####################################################################
            elif node.type == 'interface_declaration':
                
                type = 'Interface'
                
                interface_methods = []                  #Define a list for the set of methods in the interface
                
                #Find the interface name to use it in each call of the following methods
                ####################################################################
                interface_name = nodeNameFinder(node.child_by_field_name('name').start_point, node.child_by_field_name('name').end_point)
                ####################################################################
                interfaceNames.append(interface_name)
                
                
                #Find the attributes of the interface
                ####################################################################
                interfaceAttributesFinder(node, interface_name)
                ####################################################################
                
                
                
                #Find the methods of the interface
                ####################################################################
                interface_methods = interfaceMethodsFinder(node, interface_name)
                ####################################################################
            
            
                #Find the parameters of the method
                ####################################################################
                methodParametersFinderForInterface(node, interface_name, interface_methods)
                ####################################################################
            
            
            
            ####################################################################
            #The INTERFACE section_End
            ####################################################################
            
            
            
            ####################################################################
            
            
            
            ####################################################################
            #The ENUMERATION section_Beginning
            ####################################################################
            elif node.type == 'enum_declaration':
                
                type = 'Enumeration'
                
                enumeration_methods = []                  #Define a list for the set of methods in the enumeration
                
                
                #Find the enumeration name to use it in each call of the following methods
                ####################################################################
                enum_name = nodeNameFinder(node.child_by_field_name('name').start_point, node.child_by_field_name('name').end_point)
                ####################################################################
                enumNames.append(enum_name)
                
                
                #Find the attributes of the interface
                ####################################################################
                enumAttributesFinder(node, enum_name)
                ####################################################################
                
                
                #Find the methods of the enumeration
                ####################################################################
                enumeration_methods = enumMethodsFinder(node, enum_name)
                ####################################################################
                
                
                
                # #Find the parameters of the method
                # ####################################################################
                # methodParametersFinderForEnumeration(node, enum_name, enumeration_methods)
                # ####################################################################
                
                
                # #Find the local variables of the method
                # ####################################################################
                # methodLocalVariablesTypeFinderForEnumeration(node, enum_name, enumeration_methods)
                # ####################################################################
                
                
                
                # #Find the local assignments of the method
                # ####################################################################
                # methodLocalAssignmentsFinderForEnumeration(node, enum_name, enumeration_methods)
                # ####################################################################
                
                
            ####################################################################
            #The ENUMERATION section_End
            ####################################################################
            
            ####################################################################
                    


    #Add the class/interface/enumeration names together to the typeNames list
    ####################################################################
    typeNames.append(classNames)
    typeNames.append(interfaceNames)
    typeNames.append(enumNames)
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
    sensitiveMethodLocalVariablesTypeCheck()
    ####################################################################


    #Find the sensitive methods based on the local identifiers (which can be attributes) used in the method body
    ####################################################################
    sensitiveMethodLocalAssignmentsCheck()
    ####################################################################



    #Find the statistics of the whole software
    ####################################################################
    #softwareStatistics(classNames, interfaceNames)
    softwareStatistics(classNames, interfaceNames, enumNames)
    ####################################################################



    #Count the sensitivity level of each class/interface/enumeration based on the number of its attributes, the number of its 
    # sensitive attributes, the number of its methods, and the number of its sensitive methods
    ####################################################################
    for type in typeNames:
        if type == classNames:
            typeStatistic(classNames, 'Class')
        elif type == interfaceNames:
            typeStatistic(interfaceNames, 'Interface')
        elif type == enumNames:
            typeStatistic(enumNames, 'Enumeration')
    ####################################################################

    #Add a header to the Classifier Statistic.csv file
    ####################################################################
    addFileHeader('Classifier Statistic.csv', ['Classifiers', 'Number of Attributes', 'Number of Sensitive Attributes', 'Number of Methods', 'Number of Sensitive Methods'])
    ####################################################################


    #Normalize the sensitivity level of each class/interface/enumeration based on the number of its attributes, the number of its
    # sensitive attributes, the number of its methods, and the number of its sensitive methods
    ####################################################################
    normalizeData()
    ####################################################################

    # calculateRatio()

    # normalizeSenRatio()


    #Sort the normalized sensitive classes/interface/enumerations based on the sensitivity level value
    ####################################################################
    sortSensitiveClasses()
    ####################################################################

    #===============================================================================

    #===============================================================================

    return OUTPUT_DIR








# Read file content and return it
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


#Use the reading function to read the source code file from
#the buffer and return it as bytes object encoded as UTF8
#### This function is available in https://github.com/tree-sitter/py-tree-sitter ####
#===============================================================================



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



#Walking the Syntax Tree of the method
#### This function is available in https://github.com/tree-sitter/py-tree-sitter/issues/33 ####
#===============================================================================
def traverse_method(sub_tree):
    cursor = sub_tree.walk()
 
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







#The nodeNameFinder function that accept the start point and the end point of a node to slice 
#the code and extract the actual text (actual name) of the node in the original code
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
            
    


##############################################################################
####################THE START OF THE CLASS PARSING FUNCTIONS##################
##############################################################################




#The classAttributesFinder function that accepts the node (which is a class_body type) to look for its attributes 
#and writes the class name along with its attributes in a file (Output/Class Attributes.csv)
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
        attributeName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
        attribute_names.append(attributeName)
############################################################################################



#Open the Class Attributes file to write the class name in the first cell followed by the class attributes
####################################################################
#===============================================================================
    with open(os.path.join(OUTPUT_DIR,'Class Attributes.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(attribute_names)
        file.close()
#===============================================================================
            


#The classMethodsFinder() function that accepts the node (which is a class_body type) and the class name
#to look for its methods and writes the class name along with its methods in a file (Output/Class Methods.csv)
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
        methodName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
        method_names.append(methodName)
        classMethods.append(methodName)
############################################################################################     

    
    with open(os.path.join(OUTPUT_DIR,'Class Methods.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(method_names)
        file.close()
        
    return classMethods
             
#===============================================================================
    


#The methodParametersFinderForClass() function that accepts the node (which is a class_body type), the class name, and a list of its methods
#to look for the parameters of each method and write them in a file (Output/Method Parameters_Class.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name,
#the second cell is the method name, then it is followed by the method parameters
############################################################################# 
def methodParametersFinderForClass(node, className, class_methods):

    method_structures = []

    with open(os.path.join(OUTPUT_DIR,'Method Parameters_Class.csv'), 'a', newline='') as file:
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
          (type_identifier) @parameter_name
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
                methodParameterName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
                methodParameter_names.append(methodParameterName)
############################################################################################
                
            writer.writerow(methodParameter_names)
                
        
    file.close() 

#############################################################################    



#The methodLocalVariablesTypeFinderForClass function that accepts the node (which is a class_body type), the class name, and a list of its methods
#to look for the types of each local variable in each method and write them in a file (Output/Method Local Variables_Class.csv)
#The structure of the csv file is created as follows: Each class takes a row of the file, the first cell of the row is the class name,
#the second cell is the method name, then it is followed by the method local variables
############################################################################# 
def methodLocalVariablesTypeFinderForClass(node, className, class_methods):

    method_structures = []
    
    
    with open(os.path.join(OUTPUT_DIR,'Method Local Variables_Class.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')

 
###A query to look for all the methods in the class
###################################################### 
        methodStructure_query = JAVA_LANGUAGE.query("""
          (class_body
          (method_declaration) @method_structure
          )
        """)
###################################################### 



###A query to look for the type of all local variables of any method in the class
######################################################      
        methodLocalVariablesType_query = JAVA_LANGUAGE.query("""
          (block
          (local_variable_declaration
          (type_identifier) @variable_type
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
            methodLocalVarType_names = []
            methodLocalVarType_names.append(className)
            methodLocalVarType_names.append(class_methods[m])
            localVariablesTypeCaptures = methodLocalVariablesType_query.captures(method_structures[m])
            
            
            for row in localVariablesTypeCaptures:
                node_captured = next(iter(row))
                methodLocalVariableTypeName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
                methodLocalVarType_names.append(methodLocalVariableTypeName)

############################################################################################        

                
            writer.writerow(methodLocalVarType_names)
                
        
    file.close() 

#######################################################################################                         
  


#The methodLocalAssignmentsFinderForClass function that accepts the node (which is a class_body type), the class name, and a list of its methods
#to look for any use of an identifier (which can be an attribute in the same class) and write them in a file (Output/Method Local Identifiers_Class.csv) The structure of the csv file is created as follows:
# Each class takes a row of the file, the first cell of the row is the class name, the second cell is the method name, 
##then it is followed by the identifiers that are used in the method body
############################################################################# 
def methodLocalAssignmentsFinderForClass(node, className, class_methods):

    method_structures = []
    ClassAttributesPath = 'Class Attributes.csv'
    
    with open(os.path.join(OUTPUT_DIR,'Method Local Identifiers_Class.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')

 
###A query to look for all the methods in the class
###################################################### 
        methodStructure_query = JAVA_LANGUAGE.query("""
          (class_body
          (method_declaration) @method_structure
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

            

###Extract each left variable of the assignment from the capture and put it in a list after the class name and the method name
#to save them later in the file
############################################################################################        
        for m in range(len(method_structures)):
            methodLocalAssignmentVariables_names = []
            methodLocalAssignmentVariables_names.append(className)
            methodLocalAssignmentVariables_names.append(class_methods[m])
            for n in traverse_method(method_structures[m]):    ####NEW
                if n.type == 'identifier':
                    leftIdentifierName = nodeNameFinder(n.start_point, n.end_point)

                    flag = searchForSensitiveAssignmentMethod(ClassAttributesPath, leftIdentifierName, className)
                    if flag:
                    #if searchForSensitiveAssignmentMethod(ClassAttributesPath, leftIdentifierName, className) != None:
                        methodLocalAssignmentVariables_names.append(leftIdentifierName)

              
############################################################################################        

                
            writer.writerow(methodLocalAssignmentVariables_names)
                
        
    file.close() 

#######################################################################################




########################################################################################
####################THE END OF THE CLASS PARSING FUNCTIONS##############################
########################################################################################



########################################################################################



########################################################################################
####################THE START OF THE INTERFACE PARSING FUNCTIONS########################
########################################################################################




#The interfaceAttributesFinder function that accepts the node (which is a interface_body type) to look for its attributes 
#and writes the interface name along with its attributes in a file (Output/Interface Attributes.csv)
#The structure of the csv file is created as follows: Each interface takes a row of the file, the first cell of the row is the interface name followed by its attributes
############################################################################# 
def interfaceAttributesFinder(node, interfaceName):
    attribute_names = []
    
    attribute_names.append(interfaceName)
    
###A query to look for all the attributes in the interface
###################################################### 
    attributeName_query = JAVA_LANGUAGE.query("""
      (interface_body
      (constant_declaration
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
        attributeName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
        attribute_names.append(attributeName)
############################################################################################



#Open the Class Attributes file to write the interface name in the first cell followed by the interface attributes
####################################################################
#===============================================================================
    with open(os.path.join(OUTPUT_DIR,'Interface Attributes.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(attribute_names)
        file.close()
#===============================================================================




#The interfaceMethodsFinder() function that accepts the node (which is a interface_body type) and the interface name
#to look for its methods and writes the interface name along with its methods in a file (Output/Interface Methods.csv)
#The structure of the csv file is created as follows: Each interface takes a row of the file, the first cell of the row is the interface name followed by its methods
#===============================================================================
def interfaceMethodsFinder(node, interfaceName):

    classMethods = []
    
    method_names = []
    
    method_names.append(interfaceName)

###A query to look for all the methods in the interface
######################################################    
    methodName_query = JAVA_LANGUAGE.query("""
      (interface_body
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
        methodName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
        method_names.append(methodName)
        classMethods.append(methodName)
############################################################################################     

    
    with open(os.path.join(OUTPUT_DIR,'Interface Methods.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(method_names)
        file.close()
        
    return classMethods
             
#===============================================================================



#The methodParametersFinderForInterface() function that accepts the node (which is a interface_body type), the interface name, and a list of its methods
#to look for the parameters of each method and write them in a file (Output/Method Parameters_Interface.csv)
#The structure of the csv file is created as follows: Each interface takes a row of the file, the first cell of the row is the interface name,
#the second cell is the method name, then it is followed by the method parameters
############################################################################# 
def methodParametersFinderForInterface(node, className, class_methods):

    #method_nodes = []
    method_structures = []

    with open(os.path.join(OUTPUT_DIR,'Method Parameters_Interface.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')


###A query to look for all the methods in the interface
######################################################
        methodStructure_query = JAVA_LANGUAGE.query("""
          (interface_body
          (method_declaration) @method_structure
          )
        """)
######################################################



###A query to look for all the parameters of any method in the interface
######################################################   
        methodParameters_query = JAVA_LANGUAGE.query("""
          (method_declaration
          (formal_parameters
          (formal_parameter
          (type_identifier) @parameter_name
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

            

###Extract each parameter from the capture and put it in a list after the interface name and the method name to save them later in the file
############################################################################################        
        for m in range(len(method_structures)):
            methodParameter_names = []
            methodParameter_names.append(className)
            methodParameter_names.append(class_methods[m])
            methodCaptures = methodParameters_query.captures(method_structures[m])
            
            for row in methodCaptures:
                node_captured = next(iter(row))
                methodParameterName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
                methodParameter_names.append(methodParameterName)
############################################################################################
                
            writer.writerow(methodParameter_names)
                
        
    file.close() 

#############################################################################





########################################################################################
####################THE END OF THE INTERFACE PARSING FUNCTIONS##########################
########################################################################################




########################################################################################




##########################################################################################
####################THE START OF THE ENUMERATION PARSING FUNCTIONS########################
##########################################################################################







#The enumAttributesFinder function that accepts the node (which is a enum_body type) to look for its attributes 
#and writes the enumeration name along with its attributes in a file (Output/Enumeration Attributes.csv)
#The structure of the csv file is created as follows: Each enumeration takes a row of the file, the first cell of the row is the enumeration name followed by its attributes
############################################################################# 
def enumAttributesFinder(node, enumName):
    attribute_names = []
    
    attribute_names.append(enumName)
    
###A query to look for all the attributes in the enumeration
###################################################### 
    attributeName_query = JAVA_LANGUAGE.query("""
      (enum_body
      (enum_constant
      (identifier) @attribute_name
      )
      )
    """)
######################################################
    
    captures = attributeName_query.captures(node)

###Extract each attribute from the capture and put it in a list to save it later in the file
############################################################################################    
    for row in captures:
        node_captured = next(iter(row))
        attributeName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
        attribute_names.append(attributeName)
############################################################################################



#Open the Class Attributes file to write the enumeration name in the first cell followed by the enumeration attributes
####################################################################
#===============================================================================
    with open(os.path.join(OUTPUT_DIR,'Enumeration Enum Constants.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(attribute_names)
        file.close()
#===============================================================================




#The enumMethodsFinder() function that accepts the node (which is a enum_body type) and the enumeration name
#to look for its methods and writes the enumeration name along with its methods in a file (Output/Enumeration Methods.csv)
#The structure of the csv file is created as follows: Each enumeration takes a row of the file, the first cell of the row is the enumeration name followed by its methods
#===============================================================================
def enumMethodsFinder(node, enumName):

    classMethods = []
    
    method_names = []
    
    method_names.append(enumName)

###A query to look for all the methods in the enumeration
######################################################    
    methodName_query = JAVA_LANGUAGE.query("""
      (enum_body
      (enum_body_declarations
      (method_declaration
      (identifier) @method_name
      ) 
      )
      )
    """)
###################################################### 
    
    
    methodNameCaptures = methodName_query.captures(node)
    

###Extract each attribute from the capture and put it in a list to save it later in the file
############################################################################################     
    for row in methodNameCaptures:
        node_captured = next(iter(row))
        methodName = nodeNameFinder(node_captured.start_point, node_captured.end_point)
        method_names.append(methodName)
        classMethods.append(methodName)
############################################################################################     

    
    with open(os.path.join(OUTPUT_DIR,'Enumeration Methods.csv'), 'a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(method_names)
        file.close()
        
    return classMethods
             
#===============================================================================



##########################################################################################
####################THE END OF THE ENUMERATION PARSING FUNCTIONS##########################
##########################################################################################





#The keywordsCheck() function that accepts a term (word) and a path of csv file. The fucntion looks for the term in the csv file, if it is existed, the function 
#returns True. Otherwise, it returns False. The function uses case-insensitive search.
#######################################################################################  
def keywordsCheck(term, path):
    
    b = False
    term = term.lower()
    with open(path, 'r') as KWfile:
        
        keywordsReader = csv.reader(KWfile)
        
        for row in keywordsReader:
            for cell in row:
                if term in map(str.lower, row):
                #if term == cell:
                        b = True
                        break
    
    KWfile.close()
    
    return b
#######################################################################################      
          
        
        
 
#The searchForSensitiveClassInstance() function that accepts the path of the Sensitive Classes file and the term (which is a class name) to look for the term in the file.
#If the term is existed in the file as the first element in the row, then the function returns true.
# Otherwise, it returns false.
#######################################################################################
def searchForSensitiveClassInstance(path, term):
    b = False
    print("OUTPut: ", os.path.join(OUTPUT_DIR,path))
    print(os.path.exists(os.path.join(OUTPUT_DIR,path)))
    
    with open(os.path.join(OUTPUT_DIR,path), 'r') as SCfile:
            
            sensitiveClassesReader = csv.reader(SCfile)
            
            for row in sensitiveClassesReader:
                if term == row[0]:
                    b = True
                    break
    SCfile.close()
    return b
#######################################################################################
    
 
 
    


##The sensitiveClassCheck() function that checks the attributes of each class/interface/enumeration whether are sensitive (existed in Keywords 
##Dictionary file). If yes, then the function writes the class/interface/enumeration name and its sensitive attributes in a csv file.
#===============================================================================
def sensitiveClassCheck():

    keywordsDictionaryPath = 'Config/Keywords Dictionary.csv'
    inputPath = ['Class Attributes.csv', 'Enumeration Enum Constants.csv']
    outputPath = ['Sensitive Classes.csv', 'Sensitive Enumerations.csv']
    
    for inputPath, outputPath in zip(inputPath, outputPath):
        with open (os.path.join(OUTPUT_DIR,inputPath), 'r') as CAfile, open (os.path.join(OUTPUT_DIR,outputPath), 'a', newline='') as SCfile:
        
            classAttributesReader = csv.reader(CAfile)
            sensitiveClassesWriter = csv.writer(SCfile, dialect='excel')

            for i in classAttributesReader:    ###Read the Class Attributes file line by line (Each line in the file represents a class record)
    #       
                temp = []
                sensitive_classes = []
                temp = i
                
                if len(temp) > 1:             ###If the class has at least one attribute, then it will be sent to the keywordsCheck() function.
                                                ###Any class without attributes will not be sent.
                                                
                    sensitive_classes.append(temp[0])     ###Add the class name as a first element in the row
                    for i in temp[1:]:
                        flag = keywordsCheck(i, keywordsDictionaryPath)
                        if flag:
                            sensitive_classes.append(i)
                
                if len(sensitive_classes) > 1:                            ###Only the class with at least one sensitive attributes will be saved in the file
                    sensitiveClassesWriter.writerow(sensitive_classes)

    CAfile.close()
    SCfile.close()
 
#===========================================================================
#===============================================================================




#The sensitiveMethodParametersCheck() function that checks the parameters of each method whether they are sensitive.
##If yes, then the function writes the method name and its sensitive parameters in a csv file. The function works for classes, interfaces, and enumerations.
#===============================================================================
def sensitiveMethodParametersCheck():
    
    
    sensitiveClassesPath = 'Sensitive Classes.csv'
    inputPath = ['Method Parameters_Class.csv', 'Method Parameters_Interface.csv']
    outputPath = ['Sensitive Parameters-Based Methods_Class.csv', 'Sensitive Parameters-Based Methods_Interface.csv']
    
    for inputPath, outputPath in zip(inputPath, outputPath):
        with open (os.path.join(OUTPUT_DIR,inputPath), 'r') as MPfile, open (os.path.join(OUTPUT_DIR,outputPath), 'a', newline='') as SPBMfile:
        
            methodParametersReader = csv.reader(MPfile)
            sensitiveParametersBasedMethodWriter = csv.writer(SPBMfile, dialect='excel')

                
                
            for i in methodParametersReader:        ###Read the Method Parameters file line by line (Each line in the file 
                                                    ###represents a method record)
        
                temp = []
                sensitive_methods = []
                temp = i
            
                if len(temp) > 2:                  ###If the method has at least one parameter, then it will be sent to the keywordsCheck() function.
                                                ###Any method without parameters will not be sent.
                    
                    
                    sensitive_methods.append(temp[0])  ###Add the class name as a first element in the row
                    sensitive_methods.append(temp[1])   ###Add the method name as a second element in the row
                    for i in temp[2:]:
                        flag = searchForSensitiveClassInstance(sensitiveClassesPath, i)
                       
                        if flag:
                            sensitive_methods.append(i)
                            
                        
                
                if len(sensitive_methods) > 2:                             ###Only the method with at least one sensitive parameter will be saved in the file
                    sensitiveParametersBasedMethodWriter.writerow(sensitive_methods)
       
    MPfile.close()
    SPBMfile.close()
 
#===========================================================================
#===============================================================================





#The sensitiveMethodLocalVariablesTypeCheck() function that checks the local variables of each method (in the Method Local Variables file) whether they are 
#sensitive. If yes, then the function writes the method name and its sensitive local variables in a csv file. The function works for both classes and enumerations.
#===============================================================================
def sensitiveMethodLocalVariablesTypeCheck():
    
    sensitiveClassesPath = 'Sensitive Classes.csv'
    inputPath = ['Method Local Variables_Class.csv']
    outputPath = ['Sensitive Local Variables-Based Methods_Class.csv']
    
    
    for inputPath, outputPath in zip(inputPath, outputPath):
        with open (os.path.join(OUTPUT_DIR,inputPath), 'r') as MLVfile, open (os.path.join(OUTPUT_DIR,outputPath), 'a', newline='') as SLVBMfile:
        
            methodLocalVariablesReader = csv.reader(MLVfile)
            sensitiveLocalVariablesBasedMethodWriter = csv.writer(SLVBMfile, dialect='excel')
                
                
            for i in methodLocalVariablesReader:        ###Read the Method Local Variables file line by line (Each line in the file represents a method record)
        
                temp = []
                sensitive_methods = []
                temp = i
            
                if len(temp) > 2:                       ###If the method has at least one local variable, then it will be sent to the keywordsCheck() function.
                                                    ###Any method without local variables will not be sent.
                    
                    
                    
                    sensitive_methods.append(temp[0])  ###Add the class name as a first element in the row
                    sensitive_methods.append(temp[1])  ###Add the method name as a second element in the row
                    for i in temp[2:]:
                        flag = searchForSensitiveClassInstance(sensitiveClassesPath, i)
                        if flag:
                            sensitive_methods.append(i)
                            
                        
                
                if len(sensitive_methods) > 2:          ###Only the method with at least one sensitive local variable will be saved in the file
                    sensitiveLocalVariablesBasedMethodWriter.writerow(sensitive_methods)
       
    MLVfile.close()
    SLVBMfile.close()
 
#===========================================================================






#The sensitiveMethodLocalAssignmentsCheck() function that checks the local identifiers (which can be attributes) of each method whether they are 
#sensitive. If yes, then the function writes the method name and its sensitive local identifiers in a csv file. The function works for both classes and enumerations.
#===============================================================================
def sensitiveMethodLocalAssignmentsCheck():
    
    sensitiveClassesPath = ['Sensitive Classes.csv', 'Sensitive Enumerations.csv']
    inputPath = ['Method Local Identifiers_Class.csv', 'Method Local Identifiers_Enumeration.csv']
    outputPath = ['Sensitive Local Identifiers-Based Methods_Class.csv', 'Sensitive Local Identifiers-Based Methods_Enumeration.csv']
    
    for sensitiveClassesPath, inputPath, outputPath in zip(sensitiveClassesPath, inputPath, outputPath):
        with open (os.path.join(OUTPUT_DIR,inputPath), 'r') as MAVfile, open (os.path.join(OUTPUT_DIR,outputPath), 'a', newline='') as SAVBMfile:
        
            methodAssignmentVariablesReader = csv.reader(MAVfile)
            sensitiveAssignmentVariablesBasedMethodWriter = csv.writer(SAVBMfile, dialect='excel')
                
                
            for i in methodAssignmentVariablesReader:        ###Read the Method Local Assignment Variables file line by 
                                                            ##line (Each line in the file represents a method record)
        
                temp = []
                sensitive_methods = []
                temp = i
            
                if len(temp) > 2:                       ###If the method has at least one local assignment variable, then it will 
                                                        ##be sent to the keywordsCheck() function.
                                                        ###Any method without local variables will not be sent.
                    
                    
                    
                    sensitive_methods.append(temp[0])  ###Add the class name as a first element in the row
                    sensitive_methods.append(temp[1])  ###Add the method name as a second element in the row
                    for i in temp[2:]:
                        flag = searchForSensitiveAssignmentMethod(sensitiveClassesPath, i, temp[0])
                        if flag:
                            sensitive_methods.append(i)
                            
                        
                
                if len(sensitive_methods) > 2:          ###Only the method with at least one sensitive local
                                                        ##assignment variable will be saved in the file
                    sensitiveAssignmentVariablesBasedMethodWriter.writerow(sensitive_methods)
       
    MAVfile.close()
    SAVBMfile.close()
 
#===========================================================================




##The searchForSensitiveMethod function that accepts the file path of a csv file (which is a sensitive methods file) and a class name. The function looks for the class name
# in the file. If it exists, the function returns the method name of that class. Otherwise, it returns None.
#===============================================================================
def searchForSensitiveMethod(path, className):
    
    senMethods = []
    
    with open(os.path.join(OUTPUT_DIR,path), 'r') as file:
        file_reader = csv.reader(file)
        
        for row in file_reader:
            if (row[0] == className):
                senMethods.append(row[1])
    file.close()
    return senMethods
            
#===============================================================================
                
               

    

##The searchForSensitiveAssignmentMethod function that accepts the file path of a csv file, the 
##sensitive attribute, and the class name to look for the sensitive attribute in 
##the file. If it exists, the function returns the method name that contains the sensitive attribute.
#===============================================================================
def searchForSensitiveAssignmentMethod(file_path, sensitiveAttribute, className):
    
    with open(os.path.join(OUTPUT_DIR,file_path), 'r') as file:
        file_reader = csv.reader(file)
        
        for row in file_reader:
            if (sensitiveAttribute in row) and (row[0] == className):
                return 1
                #return row[1]
    file.close()
#===============================================================================

    



##The typeStatistic() function that counts the sensitivity level of each class/interface/enumeration based on its sensitive attributes and 
##its sensitive methods. It takes the required data of each class/interface/enumeration from its files which were created from the other functions above.
##The output of the function is a csv file (Output/Classifier Statistic.csv) that contains the class/interface/enumeration name, the number of its attributes, the number of 
# its sensitive attributes, the number of its methods, and the number of its sensitive methods.
#===============================================================================
def typeStatistic(classNames, type):
    
    if type == 'Class':
        senMethFileForClass = ['Sensitive Local Variables-Based Methods_Class.csv', 'Sensitive Parameters-Based Methods_Class.csv', 'Sensitive Local Identifiers-Based Methods_Class.csv']
        senTypeFile = 'Sensitive Classes.csv'
        typeAttributesFile = 'Class Attributes.csv'
        typeMethodsFile = 'Class Methods.csv'
    elif type == 'Interface':
        senMethFileForClass = ['Sensitive Parameters-Based Methods_Interface.csv']   
        senTypeFile = 'Sensitive Interfaces.csv'
        typeAttributesFile = 'Interface Attributes.csv'
        typeMethodsFile = 'Interface Methods.csv'
    elif type == 'Enumeration':
        senMethFileForClass = ['Sensitive Local Variables-Based Methods_Enumeration.csv', 'Sensitive Parameters-Based Methods_Enumeration.csv', 'Sensitive Local Identifiers-Based Methods_Enumeration.csv']   
        senTypeFile = 'Sensitive Enumerations.csv'
        typeAttributesFile = 'Enumeration Enum Constants.csv'
        typeMethodsFile = 'Enumeration Methods.csv'

    with open (os.path.join(OUTPUT_DIR,senTypeFile), 'r') as SCfile, open (os.path.join(OUTPUT_DIR,typeAttributesFile), 'r') as CAfile, open (os.path.join(OUTPUT_DIR,'Classifier Statistic.csv'), 'a', newline='') as TSfile:
        
        sensitiveClassesReader = csv.reader(SCfile)
        classAttributesReader = csv.reader(CAfile)
        typeStatisticWriter = csv.writer(TSfile, dialect='excel')
 
        # Add header to Classifier Statistic.csv file
        #typeStatisticWriter.writerow(['Classifiers', 'Number of Attributes', 'Number of Sensitive Attributes', 'Number of Methods', 'Number of Sensitive Methods'])
        
        senClasses = []
        for i in sensitiveClassesReader:                    ##Take every sensitive class from the file
            sensitiveMethod = []                            ##Define a list for the sensitive methods in the class
            sensitiveAssignmentBasedMethod = []             ##Define a list for the sensitive assignment based methods in the class
            sensitiveMethodsUnion = []
            classAttributesCounter = 0
            classMethodsCounter = 0

            
            sensitiveClass = []
            sensitiveClass = i
            noOfSensitiveAttributes = len(sensitiveClass) - 1
            className = sensitiveClass[0]
            senClasses.append(className)
            
            
            
            for l in classAttributesReader:                 ##Count the number of attributes and the ratio of sensitive attributes in each class
                classAttributes = []                        
                classAttributes = l
                if className in classAttributes:
                    classAttributesCounter = len(classAttributes) - 1
                    break
            
           
            classMethodsCounter = methodCounter(typeMethodsFile, className)  ##Count the number of methods in the class
            
            ##Find the sensitive local variable/parameter based methods in each class
            for file in senMethFileForClass:
                sensitiveMethod.extend(searchForSensitiveMethod(file, className))
            sensitiveMethod = removeDuplication(sensitiveMethod)
            while (None in sensitiveMethod):
                sensitiveMethod.remove(None)

                         

            ##Find the total number of sensitive methods number/ratio in each class
            sensitiveMethodsUnion = list(set(set(sensitiveMethod)).union(set(sensitiveAssignmentBasedMethod)))
            
            

            typeStatisticWriter.writerow([className, classAttributesCounter, noOfSensitiveAttributes, classMethodsCounter, len(sensitiveMethodsUnion)])         
 

        ##Count the sensitivity level of the class which has only sensitive methods (local variable or parameter based method)
        for cn in classNames:
            if cn not in senClasses:
                temp = []
                for path in senMethFileForClass[:2]:
                    temp.extend(searchForSensitiveMethod(path, cn))
                if  len(temp) > 0:
                    sensitiveMethodsUnion = removeDuplication(temp)
                    typeStatisticWriter.writerow([cn, methodCounter(typeAttributesFile, cn), 0, methodCounter(typeMethodsFile, cn), len(sensitiveMethodsUnion)])
                
                elif len(temp) == 0:
                    typeStatisticWriter.writerow([cn, methodCounter(typeAttributesFile, cn), 0, methodCounter(typeMethodsFile, cn), 0])
        
        SCfile.close()
        CAfile.close()
        TSfile.close()


        #addFileHeader('Output/Classifier Statistic.csv')
#===============================================================================
        
 

##The methodCounter() function that accepts the class name and gives back the number of its methods
#=============================================================================== 
def methodCounter(path, className):
    
    counter = 0
    with open(os.path.join(OUTPUT_DIR,path), 'r') as CMfile:
         classMethodsReader = csv.reader(CMfile)
         
         for row in classMethodsReader:
             if (row[0] == className):
                 counter = len(row) - 1
    CMfile.close()
    return counter
#===============================================================================

 
        
##The removeDuplication() function that accepts any list of elements and gives back a list of the same elements but without duplication
#===============================================================================
def removeDuplication(elementsList):
    
    temp = []
    for method in elementsList:
        if method not in temp:
            temp.append(method)
    return temp
#===============================================================================

##The addFileHeader() function that accepts the file path and adds a header to the file
#===============================================================================
def addFileHeader(file_path, header):
    with open(os.path.join(OUTPUT_DIR,file_path), 'r') as infile:
        data = list(csv.reader(infile))

    with open(file_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(data)

    infile.close()
    outfile.close()
#===============================================================================



##The softwareStatistics() function that accepts the class/interface/enumeration name and gives back the number of classes/interfaces/enumerations,
# the number of sensitive classes, the number of attributes, the number of sensitive attributes, the number of methods, the number of sensitive methods,
# in the Java software source code and save them in a csv file (Output/Software Statistics.csv)
#===============================================================================
def softwareStatistics(classNames, interfaceNames, enumNames):
    
    classes = 0
    classAttributes = 0
    classMethods = 0
    sensitiveClasses = 0
    sensitiveAttributes = 0
    sensitiveMethods = 0
    
    with open(os.path.join(OUTPUT_DIR,'Software Statistics.csv'), 'w', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(['NUMBER OF CLASSIFIERS', 'NUMBER OF SENSITIVE CLASSES', 'NUMBER OF ATTRIBUTES', 'NUMBER OF SENSITIVE ATTRIBUTES', 'NUMBER OF METHODS', 'NUMBER OF SENSITIVE METHODS'])
        
        for className in classNames:
            classAttributes = classAttributes + methodCounter('Class Attributes.csv', className)
            classMethods = classMethods + methodCounter('Class Methods.csv', className)
            if searchForSensitiveClassInstance('Sensitive Classes.csv', className):
                sensitiveClasses = sensitiveClasses + 1
                sensitiveAttributes = sensitiveAttributes + methodCounter('Sensitive Classes.csv', className)
                sensitiveMethods = sensitiveMethods + methodCounter('Sensitive Local Variables-Based Methods_Class.csv', className) + methodCounter('Sensitive Parameters-Based Methods_Class.csv', className) + methodCounter('Sensitive Local Identifiers-Based Methods_Class.csv', className)
            classes = classes + 1
        
           
        for interfaceName in interfaceNames:
            classAttributes = classAttributes + methodCounter('Interface Attributes.csv', interfaceName)
            classMethods = classMethods + methodCounter('Interface Methods.csv', interfaceName)
            if searchForSensitiveClassInstance('Sensitive Interfaces.csv', interfaceName):
                sensitiveClasses = sensitiveClasses + 1
                sensitiveAttributes = sensitiveAttributes + methodCounter('Sensitive Interfaces.csv', interfaceName)
                sensitiveMethods = sensitiveMethods + methodCounter('Sensitive Parameters-Based Methods_Interface.csv', interfaceName)
            classes = classes + 1
        
        for enumName in enumNames:
            classAttributes = classAttributes + methodCounter('Enumeration Enum Constants.csv', enumName)
            classMethods = classMethods + methodCounter('Enumeration Methods.csv', enumName)
            if searchForSensitiveClassInstance('Sensitive Enumerations.csv', enumName):
                sensitiveClasses = sensitiveClasses + 1
                sensitiveAttributes = sensitiveAttributes + methodCounter('Sensitive Enumerations.csv', enumName)
                sensitiveMethods = sensitiveMethods + methodCounter('Sensitive Local Variables-Based Methods_Enumeration.csv', enumName) + methodCounter('Sensitive Parameters-Based Methods_Enumeration.csv', enumName) + methodCounter('Sensitive Local Identifiers-Based Methods_Enumeration.csv', enumName)
            classes = classes + 1
            
        writer.writerow([classes, sensitiveClasses, classAttributes, sensitiveAttributes, classMethods, sensitiveMethods])
    file.close()
#===============================================================================





##The normalizeData() function that normalizes the sensitivity level of each class/interface/enumeration based on the number of its attributes, 
# the number of its sensitive attributes, the number of its methods, and the number of its sensitive methods and save them in a csv file
# (Output/Normalized Type Statistic.csv). The normalization is applied individually for nomirator and denominator before findig the ratio.
#===============================================================================
def normalizeData():
        
        df = pd.read_csv(os.path.join(OUTPUT_DIR,'Classifier Statistic.csv'), header=None, skiprows=1)
        
        minAttrNum = df[1].min()
        maxAttrNum = df[1].max()
        minSensAttrNum = df[2].min()
        maxSensAttrNum = df[2].max()
        minMethNum = df[3].min()
        maxMethNum = df[3].max()
        minSensMethNum = df[4].min()
        maxSensMethNum = df[4].max()
        
        with open(os.path.join(OUTPUT_DIR,'Normalized Type Statistic.csv'), 'a', newline='') as NTSfile:
            normalizedTypeStatisticWriter = csv.writer(NTSfile, dialect='excel')
            normalizedTypeStatisticWriter.writerow(['CLASS NAME', 'NORMALIZED SENSITIVITY LEVEL'])
            
            for index, row in df.iterrows():
                if (maxAttrNum - minAttrNum) != 0:
                    normalizedAttrNum = (row[1] - minAttrNum) / (maxAttrNum - minAttrNum)
                elif maxAttrNum == 0 and minAttrNum == 0:
                    normalizedAttrNum = 0
                else:
                    normalizedAttrNum = 0.5 ## If maxAttrNum and minAttrNum are equal (but they are not zeros), then the normalized value is assumed as 0.5 (a middle value between 0 and 1)
                
                if (maxSensAttrNum - minSensAttrNum) != 0:
                    normalizedSensAttrNum = (row[2] - minSensAttrNum) / (maxSensAttrNum - minSensAttrNum)
                elif maxSensAttrNum == 0 and minSensAttrNum == 0:
                    normalizedSensAttrNum = 0
                else:
                    normalizedSensAttrNum = 0.5
                
                if (maxMethNum - minMethNum) != 0:
                    normalizedMethNum = (row[3] - minMethNum) / (maxMethNum - minMethNum)
                elif maxMethNum == 0 and minMethNum == 0:
                    normalizedMethNum = 0
                else:
                    normalizedMethNum = 0.5
                
                if (maxSensMethNum - minSensMethNum) != 0:
                    normalizedSensMethNum = (row[4] - minSensMethNum) / (maxSensMethNum - minSensMethNum)
                elif maxSensMethNum == 0 and minSensMethNum == 0:
                    normalizedSensMethNum = 0
                else:
                    normalizedSensMethNum = 0.5

                normalizedAttrNumRatio = 0
                normalizedMethNumRatio = 0
                
                if normalizedAttrNum != 0 and not pd.isnull(normalizedAttrNum):
                    #normalizedAttrNumRatio = (normalizedSensAttrNum / normalizedAttrNum)
                    #normalizedAttrNumRatio = min((normalizedSensAttrNum / normalizedAttrNum), 1)
                    normalizedAttrNumRatio = (normalizedSensAttrNum / normalizedAttrNum)
                #     if normalizedAttrNumRatio > 1:
                #         normalizedAttrNumRatio = 1
                # else:
                #     normalizedAttrNumRatio = 0
                

                
                if normalizedMethNum != 0 and not pd.isnull(normalizedMethNum):
                    #normalizedMethNumRatio = (normalizedSensMethNum / normalizedMethNum)
                    #normalizedMethNumRatio = min((normalizedSensMethNum / normalizedMethNum), 1)
                    normalizedMethNumRatio = (normalizedSensMethNum / normalizedMethNum)
                #     if normalizedMethNumRatio > 1:
                #         normalizedMethNumRatio = 1
                # else:
                #     normalizedMethNumRatio = 0
                

                normalizedSensitivityRatio = normalizedAttrNumRatio * 0.5 + normalizedMethNumRatio * 0.5
                # if normalizedSensitivityRatio > 1:
                #     normalizedSensitivityRatio = 1
                # else:
                #     normalizedSensitivityRatio = round(normalizedSensitivityRatio,2)
                normalizedTypeStatisticWriter.writerow([row[0], normalizedSensitivityRatio])

        NTSfile.close()

#===============================================================================
    



##The calculateRatio() function that calculates the sensitivity level (ratio) of each class/interface/enumeration 
# based on the number of its attributes, the number of its sensitive attributes, the number of its methods, and the number of its sensitive methods
# and save them in a csv file (Output/Sensitivity Ratio Statistic.csv)
#===============================================================================
# def calculateRatio():
            
#             df = pd.read_csv(os.path.join(OUTPUT_DIR,'Classifier Statistic.csv'), header=None)
            
#             with open(os.path.join(OUTPUT_DIR,'Sensitivity Ratio Statistic.csv'), 'a', newline='') as NRSfile:
#                 normalizedRatioStatisticWriter = csv.writer(NRSfile, dialect='excel')
#                 normalizedRatioStatisticWriter.writerow(['CLASS NAME', 'SENSITIVITY LEVEL'])
                
#                 for index, row in df.iterrows():
#                     attrRatio = 0
#                     methRatio = 0
                    
#                     if row[1] != 0:
#                         attrRatio = row[2] / row[1]
                    
#                     if row[3] != 0:
#                         methRatio = row[4] / row[3]
                    
#                     normalizedSensitivityRatio = (attrRatio * 0.5) + (methRatio * 0.5)

#                     normalizedRatioStatisticWriter.writerow([row[0], normalizedSensitivityRatio])
                    
#             NRSfile.close()
            
              
#===============================================================================                
                
         
                    
            

##The normalizeSenRatio() function that normalizes the sensitivity level of each class/interface/enumeration based 
# on the sensitivity level value and save them in a csv file (Output/Normalized Sensitivity Ratio Statistic.csv). The
# normalization is applied one time after finding the sensitivity ratio value.
#===============================================================================
# def normalizeSenRatio():
            
#             df = pd.read_csv(os.path.join(OUTPUT_DIR,'Sensitivity Ratio Statistic.csv'), header=None, skiprows=1)
            
#             minSenRatio = df[1].min()
#             maxSenRatio = df[1].max()
            
#             # print(minSenRatio)
#             # print(maxSenRatio)
            
#             with open(os.path.join(OUTPUT_DIR,'Normalized Sensitivity Ratio Statistic.csv'), 'a', newline='') as NSRSfile:
#                 normalizedSenRatioStatisticWriter = csv.writer(NSRSfile, dialect='excel')
#                 normalizedSenRatioStatisticWriter.writerow(['CLASS NAME', 'NORMALIZED SENSITIVITY LEVEL'])
                
#                 for index, row in df.iterrows():
#                     if (maxSenRatio - minSenRatio) != 0:
#                         normalizedSenRatio = (row[1] - minSenRatio) / (maxSenRatio - minSenRatio)
#                     elif maxSenRatio == 0 and minSenRatio == 0:
#                         normalizedSenRatio = 0
#                     else:
#                         normalizedSenRatio = 0.5
                    
#                     normalizedSenRatioStatisticWriter.writerow([row[0], normalizedSenRatio])
                    
#             NSRSfile.close()
#===============================================================================





##The sortSensitiveClasses() function that opens the Normalized Type Statistic.csv file to sort all the sensitive classes based on the
##sensitivity level value and write them in a new file (Sorted Normalized Type Statistic.csv)  
#===============================================================================
def sortSensitiveClasses():
    
    with open(os.path.join(OUTPUT_DIR,'Normalized Type Statistic.csv'), 'r') as USSCfile:
        USSCfileReader = csv.reader(USSCfile)
        next(USSCfileReader)  # Skip the header row
        #sortedSensitiveClasses = sorted(USSCfileReader, key=lambda row: row[1], reverse=True)
        sortedSensitiveClasses = sorted(USSCfileReader, key=lambda row: float(row[1]), reverse=True)
        
    with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Type Statistic.csv'), 'w', newline='') as SSCfile:
        SSCfileWriter = csv.writer(SSCfile)
        SSCfileWriter.writerows(sortedSensitiveClasses)
       
    USSCfile.close()
    SSCfile.close() 

    with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Type Statistic.csv'), 'r') as infile:
        data = infile.read()

    with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Type Statistic.csv'), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['CLASS NAME', 'SENSITIVITY LEVEL']) 
        outfile.write(data)
    
    # ####################################################################
        
    # with open(os.path.join(OUTPUT_DIR,'Normalized Sensitivity Ratio Statistic.csv'), 'r') as inNSRfile:
    #     data = csv.reader(inNSRfile)
    #     next(data)
    #     sortedSensitiveClasses = sorted(data, key=lambda row: row[1], reverse=True)
    #     #print(sortedSensitiveClasses)
    # with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Sensitivity Ratio Statistic.csv'), 'w', newline='') as outNSRfile:
    #     writer = csv.writer(outNSRfile)
    #     writer.writerows(sortedSensitiveClasses)
        
    # with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Sensitivity Ratio Statistic.csv'), 'r') as infile:
    #     data = infile.read()
        
    # with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Sensitivity Ratio Statistic.csv'), 'w', newline='') as outfile:
    #     writer = csv.writer(outfile)
    #     writer.writerow(['CLASS NAME', 'SENSITIVITY LEVEL']) 
    #     outfile.write(data)
    
    # ####################################################################
    
    # with open(os.path.join(OUTPUT_DIR,'Normalized Type Statistic.csv'), 'r') as inNTSfile:
    #     data = csv.reader(inNTSfile)
    #     next(data)
    #     sortedSensitiveClasses = sorted(data, key=lambda row: row[1], reverse=True)
    #     #print(sortedSensitiveClasses)
    # with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Type Statistic.csv'), 'w', newline='') as outNTSfile:
    #     writer = csv.writer(outNTSfile)
    #     writer.writerows(sortedSensitiveClasses)
        
    # with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Type Statistic.csv'), 'r') as infile:
    #     data = infile.read()
        
    # with open(os.path.join(OUTPUT_DIR,'Sorted Normalized Type Statistic.csv'), 'w', newline='') as outfile:
    #     writer = csv.writer(outfile)
    #     writer.writerow(['CLASS NAME', 'SENSITIVITY LEVEL']) 
    #     outfile.write(data)
        
    # inNTSfile.close()
    # outNTSfile.close()
    # inNSRfile.close()
    # outNSRfile.close()    
    infile.close()
    outfile.close()

#===============================================================================
