"""
Created on Fri Apr 4 03:34:58 2019
@author: ME

"""

from __future__ import print_function
import sys
import re

OPERATORS  = { ':' : 'COLON', ';' : 'SEMI', ':=' : 'ASSIGN', ',' : 'COMMA', '(' : 'LPAREN' , ')' : 'RPAREN', '+' : 'ADD' , 
		   '-' : 'SUB' , '*' : 'MULT', '/' : 'DIV'}
operator_keys = OPERATORS.keys()
KEYWORDS   = ['PROGRAM','BEGIN','END','VAR','INTEGER','REAL']

LITERALS   = ['0','1','2','3','4','5','6','7','8','9','10']

CONST = 'CONST'
ID = 'ID'
ERROR = "Invalid Syntax ... '{token}' "

def LexicalResult(file_data,list_of_tokens):

	error_flag = 0
	list_of_tokens=[]
	lines = file_data.split('\n')

	for line in lines :
		head, sep, tail = line.partition('#')
		if not head:
			continue
		line=head.strip()
		
		tokens = re.split('(\W+)',line)
		for token in tokens :
			token = ''.join(token.split())
			if token.isspace() or not token:
				continue
			if token in operator_keys:
				#print(OPERATORS[token]) 
				list_of_tokens.append(OPERATORS[token])
			elif token in KEYWORDS:
				#print (token)
				list_of_tokens.append(token)
			elif token in LITERALS or token.isnumeric():
				#print (CONST)
				list_of_tokens.append(CONST)
			elif (token.isalnum()):
				#print (ID)
				list_of_tokens.append(ID)
				
			else :
				i = 0
				while(i<len(token)):
					if token[i] in operator_keys :
						if(i+1<len(token)) :
							token1 = token[i].__add__(token[i + 1])
							if(token1.__eq__(":=")):
								#print(OPERATORS[token1])
								list_of_tokens.append(OPERATORS[token1])
								i=i+2
							else:
								#print(OPERATORS[token[i]])
								list_of_tokens.append(OPERATORS[token[i]])
								i = i + 1
						else:
							#print(OPERATORS[token[i]])
							list_of_tokens.append(OPERATORS[token[i]])
							i = i+1
					else :
						 #print(ERROR.format(token=token[i]))
						 list_of_tokens.append(ERROR.format(token=token[i]))
						 error_flag = 1
						 break
			if error_flag == 1:
				break
		if error_flag == 1 :
		   break
		
	return list_of_tokens


#!/usr/bin/env python2

# -*- coding: utf-8 -*-

"""
Created on Tue Apr 5 15:44:35 2019


@author: ME

"""



import numpy as np

def LL1(list_of_tokens):

	n = 15

	m = 21

	table = np.ndarray((n, m), object)

	RowIdxHash = {
				  "START":0,"BLOCK":1,"DECLARATIONS":2,"VARDECLARATIONS'":3,"VARDECLARATIONS":4,"N":5,"TYPESPEC":6,"BLOCKSTATEMENTS":7,"STATEMENTS":8,"STATEMENT":9,"ASSIGNMENT":10,"EXPRESSION":11,"EXPRESSION'":12,"TERM":13,"STATEMENT'":14
				
	 }


	ColIdxHash = {

			"BEGIN":0,"CONST":1,"ID":2,"ADD":3,"MULT":4,"SUB":5,"DIV":6,"SEMI":7,"COLON":8,"LPAREN":9,"RPAREN":10,"$":11,"ASSIGN":12, "COMMA":13,"PROGRAM":14,"VAR":15,"INTEGER":16,"REAL":17,"END":18,"epsilon":19,"$":20
			}
	for row in range(15):
		for col in range(21):
			table[row][col]=0

	table[0][14]=["PROGRAM","ID","SEMI","BLOCK"]
	table[1][0]=["DECLARATIONS","BLOCKSTATEMENTS"]
	table[1][15]=["DECLARATIONS","BLOCKSTATEMENTS"]
	table[2][0]=["epsilon"]
	table[2][15]=["VAR","VARDECLARATIONS","SEMI","VARDECLARATIONS'"]
	table[3][0]=["epsilon"]
	table[3][2]=["epsilon","VARDECLARATIONS","SEMI","VARDECLARATIONS'"]
	table[4][2]=["ID","N","COLON","TYPESPEC"]
	table[5][8]=["epsilon"]
	table[5][13]=["COMMA","ID","N"]
	table[6][16]=["INTEGER"]
	table[6][17]=["REAL"]
	table[7][0]=["BEGIN","STATEMENTS","END"]
	table[8][2]=["STATEMENT","STATEMENT'"]
	table[9][2]=["ASSIGNMENT"]
	table[9][7]=["epsilon"]
	table[10][2]=["ID","ASSIGN","EXPRESSION","SEMI"]
	table[11][1]=["TERM","EXPRESSION'"]
	table[11][2]=["TERM","EXPRESSION'"]
	table[11][9]=["TERM","EXPRESSION'"]
	table[12][3]=["ADD","TERM","EXPRESSION'"]
	table[12][4]=["MULT","TERM","EXPRESSION'"]
	table[12][5]=["SUB","TERM","EXPRESSION'"]
	table[12][6]=["DIV","TERM","EXPRESSION'"]
	table[12][7]=["epsilon"]
	table[12][10]=["epsilon"]
	table[13][1]=["CONST"]
	table[13][2]=["ID"]
	table[13][9]=["LPAREN","EXPRESSION","RPAREN"]
	table[14][2]=["STATEMENTS"]
	table[14][18]=["epsilon"]

	#initialize the stack 
	stack=[]
	stack.append('$')
	stack.append('START')
	status="Code compiled successfully"
	k=0 
	list_of_tokens.append('$')
	#print(stack,list_of_tokens)
	l=len(list_of_tokens)
	while (1):
		print(stack,list_of_tokens[k])
		if(stack[-1]in ColIdxHash):
			if(stack[-1]=="epsilon"):
				stack.pop()
			if(stack[-1]==list_of_tokens[k]):
				stack.pop()
				k=k+1
				
				
		elif(stack[-1] in RowIdxHash):
			if list_of_tokens[k] in RowIdxHash:
				y= table[RowIdxHash[stack[-1]]] [RowIdxHash[list_of_tokens[k]]]
			elif list_of_tokens[k] in ColIdxHash :
				y= table[RowIdxHash[stack[-1]]] [ColIdxHash[list_of_tokens[k]]]
			if(y):
				stack.pop()
				y=y[::-1]
				for i in y:
					stack.append(i)
					
			else:
			    status="Invalid Syntax ... "+list_of_tokens[k]
			    return status
		if(stack[-1]=='$' or list_of_tokens[k]=='$'):
			break
		
	if(stack[-1]=='$'):
		if(list_of_tokens[k]=='$'):
			return status
		else:
			status="Invalid Syntax ... "+ list_of_tokens[k]
			return status
	else:
		status="Invalid Syntax ... None"
		return status
	

def main():
	text_file = open(sys.argv[1], 'r')
	file_data = text_file.read()
	list_of_tokens=[]
	list_of_tokens=LexicalResult(file_data,list_of_tokens)
	print(list_of_tokens)
	status=LL1(list_of_tokens)
	print(status)
	#text_file.close()
		   
     
        
        
        
        
    
if __name__ == '__main__':
	main()
