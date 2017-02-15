import os
os.system('nose2 --junit-xml')
#os.system('nose2 --junit-xml > terminal-ouput.txt')

type query ::= SELECT <exp> FROM CORP WHERE <exp>
type exp ::= Val of col | Operation of (opeator, exp...)
type col ::= value(name_of_column)
type operator ::= ...

value table :

query -> queries
exp -> 
col -> a, b, ...