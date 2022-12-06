
'''
Created on Nov 8, 2022

@author: mohammed
'''


from tree_sitter import Language, Parser

from os import path


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
PY_LANGUAGE = Language(LIB_PATH, 'java')
#===============================================================================

     
#Create the parser and configure it with the language object
#=============================================================================== 
parser = Parser()
parser.set_language(PY_LANGUAGE)
#=============================================================================== 



#Read the source code file and put its content into a list
#===============================================================================

src = open("/home/mohammed/Examples/Person/src/person/PersonSerialization.java", "r")
content_list = src.readlines()
#print(content_list)


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
# print(root_node.sexp())
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
def attribute_check(attributesList):
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



#A function that accept the start point and the end point of a node to slice 
#the code and extract the actual text of the node in the original code
#===============================================================================
def node_text_finder(startPoint, endPoint):
    
    text = ""
    row1, column1 = startPoint
    row2, column2 = endPoint
    for i in range(row1, row2 +1):
        for j in range(column1, column2):
            text += content_list[i][j]
    
    return text
#===============================================================================
            
    




#Invoke the traverse_tree function to look for the class attributes 
#===============================================================================     
for node in traverse_tree(tree):
        if node.type == "class_body":
            k = 0
            class_attributes = []
            sensitive_attributes = []
            class_name = node_text_finder(node.parent.child_by_field_name('name').start_point, node.parent.child_by_field_name('name').end_point)
            while k < node.child_count:
                l = 0
                if node.children[k].type == "field_declaration":
                    
                    for l in range(node.children[k].child_count):
                        if node.children[k].children[l].type == "variable_declarator":
                           attribute_name = node_text_finder(node.children[k].children[l].start_point, node.children[k].children[l].end_point)
                           class_attributes.append(attribute_name)  
                    
                k = k + 1
                continue
            print("The number of attributes of class", class_name, "is ", len(class_attributes))
            print(class_attributes)
            sensitive_attributes = attribute_check(class_attributes)
            print("The Number of Sensitive Attributes in class", class_name, "is", len(sensitive_attributes), "/", len(class_attributes))
            print(sensitive_attributes)

#===============================================================================

#===============================================================================
