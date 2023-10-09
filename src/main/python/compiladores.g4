grammar compiladores;

fragment LETRA: [A-Za-z];
fragment DIGITO: [0-9];

EQ: '=';
EQQ: '==';
NE: '!=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
PP: '++';
MM: '--';
MAS: '+';
MENOS: '-';
MUL: '*';
DIV: '/';
MOD: '%';
AND: '&&';
ORR: '||';
NOT: '!';
PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
PYC: ';';
COMA: ',';

NUMERO: DIGITO+;

INT: 'int';
DOUBLE: 'double';
WHILE: 'while';
IF: 'if';
FOR: 'for';
RETURN: 'return';
ID: (LETRA | '_') (LETRA | DIGITO | '_')*;
WS: [ \t\n\r] -> skip;
OTRO: .;

programa: instrucciones EOF;

instrucciones: instruccion instrucciones |;

instruccion:
	declaracion PYC
	| retornar PYC
	| asignacion PYC
	| if_stmt
	| while_stmt
	| for_stmt
	| bloque;

tdato: INT | DOUBLE;

operador: EQQ | NE | GT | LT | GE | LE;

declaracion: tdato ID definicion lista_var;

definicion: EQ NUMERO;

bloque: LLA instrucciones LLC;

lista_var: COMA ID definicion lista_var |;

asignacion: ID EQ (opar | oplo);

retornar: (RETURN ID) | (RETURN NUMERO);

while_stmt: WHILE PA oplo PC instruccion;

if_stmt: IF PA oplo PC instruccion;

for_stmt:
	(
		FOR PA (asignacion) PYC oplo PYC (
			ID (PP | MM)
			| asignacion
		) PC instruccion
	);

oplo: logic_expresion;

logic_expresion: logic_termino logic_expr;

logic_expr: ORR logic_termino logic_expr |;

logic_termino: logic_factor logic_term;

logic_term: AND logic_factor logic_term |;

logic_factor: factor | comp | (PA logic_expresion PC);

comp: opar operador opar | comp operador comp;

opar: expresion;

expresion: termino exp;

exp: MAS termino exp | MENOS termino exp |;

termino: factor term;

term: MUL factor term | DIV factor term | MOD factor term |;

factor: ((MENOS |) NUMERO)
	| ((MENOS |) ID)
	| funcion
	| PA expresion PC;

funcion: tdato ID PA ID PC;