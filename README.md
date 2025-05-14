Simple-python-compiler
======================

Simple python compiler is a school project, made at University of Pardubice (Czech Republic).

You can use it whatever you like, I don't bound you by any obligation.

Syntax
----------------------

stmtlist   := (statement)*

statement  :=    'if' condition stmtlist ['else' stmtlist] 'endif'
               | 'while' condition stmtlist 'endwhile'
               | label ':=' expression
               | 'print' expression

condition  := expression ('=='|'!='|'<'|'<='|'>'|'>=') expression

expression := term ('+'|'-'|'*'|'/' term)*

term       := label|digit