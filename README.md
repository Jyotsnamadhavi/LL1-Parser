# LL1-Parser
Top down LL1 parser




Sample TestCase
--------------------------------------------------------------------------------------------------------------------------
# This is a test program
PROGRAM Test;
VAR   
   num1   	: INTEGER;      ## this is an integer
   num2, num3   : INTEGER;
   num4         : REAL;         ## this is a float point 

BEGIN 
   num1 := 2;
   num2 := 3 * (3 + num1);
   num3 := 10 * num2;
   num4 := (num3 + (2 * num2)) / num1;
END

>>python Compiler.py test1.txt
Program has been parsed succesfully

Index   SymbolName  SymbolType
------------------------------
0	      num4		    ID
1	      num1		    ID
2	      num2		    ID
3	      num3		    ID
4	      Test		    ID
5	      10		      CONST
6	      3		        CONST
7	      2		        CONST
