#!/usr/bin/python
 
import sys
import os
import csv
import string
 
if len( sys.argv ) < 2 :
    sys.stderr.write( sys.argv[ 0 ]  + 
                      ": usage - "   + 
                      sys.argv[ 0 ]  + " [.csv file name]\n" )
    sys.exit()
 
if not os.path.exists(sys.argv[ 1 ]):
    sys.stderr.write( sys.argv[ 1 ] + " not found \n" )
    sys.exit()
 
 
with open( sys.argv[ 1 ], 'rb') as csvfile:
    table_string = ""
    reader       = csv.reader( csvfile )
    
    for row in reader:
        table_string += "<tr>" + \
                          "<td>" + \
                              string.join( row, "</td><td>" ) + \
                          "</td>" + \
                        "</tr>\n"
    
    sys.stdout.write( table_string )
    f = open(sys.argv[ 2], 'w')
    f.write(table_string) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call it