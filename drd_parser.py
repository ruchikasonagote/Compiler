import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

precedence = (
    ("left", 'ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN'),
    ("left", 'EQ', 'NEQ', 'GT', 'LT', 'LTE', 'GTE'),
    ("left", 'ADD', 'SUB'),
    ("left", 'MUL', 'DIV', 'MOD'),
    ("left", "'"),
    ("right", ':'),
    ("right", 'ID', '['),
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("right", 'USUB')
)

def p_error(p):
    if p:
        raise Exception("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, "?", p.type, p.value))
    else:
        raise Exception("Unexpected end of input")


def p_start(p):
    """
    start : function_defs main 
    """
    p[0] = AST.Start(p.lineno(1), p[1])

def p_function_defs_single(p):
    "function_defs : function_def "
    p[0] = [p[1]]

def p_function_defs_multiple(p):
    "function_defs : function_defs function_def"
    p[0] = p[1]
    p[0].append(p[2])

def p_main(p):  
    "main : VOID MAIN '(' ')' '{' program '}'"
    p[0] = AST.Main(p.lineno(1), p[6])

def p_function_def(p):
    "function_def : FUNC ID '(' list ')' '{' program '}'"
    p[0] = AST.Func(p.lineno(1), AST.Id(p.lineno(1), p[2]), p[4], p[7])


def p_program(p):
    "program : stmt"
    p[0] = AST.Block(p.lineno(1), [p[1]])

def p_program_rest(p):
    "program : program stmt"
    block = p[1]
    block.stmts.append(p[2])
    p[0] = block

def p_simple_stmt(p):
    "stmt : expr ';'"
    p[0] = p[1]

def p_return(p):
    "stmt : RETURN expr ';'"
    p[0] = AST.Return(p.lineno(1), p[2])

def p_break(p):
    "stmt : STOP ';'"
    p[0] = AST.Stop(p.lineno(1))

def p_continue(p):
    "stmt : SKIP ';'"
    p[0] = AST.Skip(p.lineno(1))

def p_empty(p):
    """
    stmt : ';'
         | '{' '}'
    """
    p[0] = AST.Block(p.lineno(1), [])


def p_stmt_list_head(p):
    "stmt_list : stmt"
    p[0] = AST.Block(p.lineno(1), [p[1]])

def p_stmt_list_tail(p):
    "stmt_list : stmt_list stmt"
    p[0] = p[1]
    p[0].stmts.append(p[2])

def p_block(p):
    "stmt : '{' stmt_list '}'"
    p[0] = p[2]


def p_print(p):
    "stmt : OUT list ';'"
    p[0] = AST.Out(p.lineno(1), p[2])

def p_intnum(p):
    "expr : INTNUM"
    p[0] = AST.IntNum(p.lineno(1), p[1])

def p_floatnum(p):
    "expr : FLOATNUM"
    p[0] = AST.FloatNum(p.lineno(1), p[1])

def p_str(p):
    "expr : STR"
    p[0] = AST.String(p.lineno(1), p[1])

def p_binexpr(p):
    """
    expr : expr ADD expr
         | expr SUB expr
         | expr MUL expr
         | expr DIV expr
         | expr MOD expr

         | expr GT expr
         | expr LT expr
         | expr GTE expr
         | expr LTE expr
         | expr EQ expr
         | expr NEQ expr
    """
    p[0] = AST.BinExpr(p.lineno(2), p[2], p[1], p[3])

def p_function_call(p):
    """
    expr : ID '(' list ')'
         | ID '(' ')'
    """
    if len(p) == 5:
        p[0] = AST.FnCall(p.lineno(1), AST.Id(p.lineno(1), p[1]), p[3])
    else:
        p[0] = AST.FnCall(p.lineno(1), AST.Id(p.lineno(1), p[1]), [])


def p_assign(p):
    """
    expr : lvalue ASSIGN expr 
         | lvalue ADD_ASSIGN expr
         | lvalue SUB_ASSIGN expr
         | lvalue MUL_ASSIGN expr
         | lvalue DIV_ASSIGN expr
         | lvalue MOD_ASSIGN expr
    """
    p[0] = AST.AssignExpr(p.lineno(1), p[2], p[1], p[3])

def p_transpose(p):
    """
    expr : expr "'"
    """
    p[0] = AST.Transposition(p.lineno(1), p[1])

def p_id(p):
    "lvalue : ID"
    p[0] = AST.Id(p.lineno(1), p[1])

def p_unary_minus(p):
    "expr : SUB expr %prec USUB"
    p[0] = AST.UnaryMinus(p.lineno(1), p[2])


def p_epxr(p):
    "expr : lvalue"
    p[0] = p[1]

def p_parentheses(p):
    "expr : '(' expr ')'"
    p[0] = p[2]


def p_ref(p):
    "lvalue : expr '[' list ']'"
    p[0] = AST.Ref(p.lineno(2), p[1], p[3])

def p_empty_vector(p):
    "expr : '[' ']'"
    p[0] = AST.Vector(p.lineno(1), [])

def p_vector(p):
    "expr : '[' list ']'"
    p[0] = AST.Vector(p.lineno(1), p[2])

def p_list(p):
    """
    list : expr
         | range
    """
    
    p[0] = [p[1]]

def p_list_cont(p):
    """
    list : list ',' expr
         | list ',' range
    """
    p[0] = p[1]
    p[0].append(p[3])

def p_if(p):
    "stmt : IFF '(' expr ')' stmt %prec IFX"
    p[0] = AST.IfStmt(p.lineno(1), p[3], p[5])

def p_if_else(p):
    "stmt : IFF '(' expr ')' stmt ELSE stmt"
    p[0] = AST.IfStmt(p.lineno(1), p[3], p[5], p[7])

def p_while(p):
    "stmt : UNTIL '(' expr ')' stmt"
    p[0] = AST.UntilLoop(p.lineno(1), p[3], p[5])

def p_range(p):
    "range : expr ':' expr"
    p[0] = AST.Range(p.lineno(1), p[1], p[3])

def p_for(p):
    "stmt : FOR '(' ID ASSIGN range ')' stmt"
    p[0] = AST.ForLoop(p.lineno(1), AST.Id(p.lineno(1), p[3]), p[5], p[7])


parser = yacc.yacc()
