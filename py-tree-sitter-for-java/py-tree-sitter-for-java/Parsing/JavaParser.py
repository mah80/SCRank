'''
Created on Nov 8, 2022

@author: mohammed
'''


from tree_sitter import Language, Parser

from os import path
import inspect


LIB_PATH = path.join("build", "my-languages.so")

#print("The current path is: %s" % path.abspath(LIB_PATH))
Language.build_library(
  # Store the library in the `build` directory
  LIB_PATH,
  # Include one or more languages
  [
 
    path.join("parsers", "tree-sitter-java"),
  ]
)


PY_LANGUAGE = Language(LIB_PATH, 'java')
     
parser = Parser()
parser.set_language(PY_LANGUAGE)

src = open("/home/mohammed/Examples/Person/src/person/PersonSerialization.java", "r")


content_list = src.readlines()
#print(content_list)

def read_callable(byte_offset, point):
    row, column = point
    if row >= len(content_list) or column >= len(content_list[row]):
        return None
    return content_list[row][column:].encode('utf8')

tree = parser.parse(read_callable)

#tree = parser.parse(parser, NULL, f.read())
     
root_node = tree.root_node
    
#assert root_node.type == 'module'

print(root_node.type)