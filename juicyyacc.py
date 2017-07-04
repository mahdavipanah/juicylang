"""
juicylang - Juicy programming language written in Python using PLY
Author : Hamidreza Mahdavipanah
Version: 1.0.0
Repository: http://github.com/mahdavipanah/juicylang
License : MIT License
"""
from colorama import init as colorama_init, Fore
import ply.yacc as yacc
from juicylex import tokens, find_column as lex_find_column


# Computes column
#     p is a production rule's stack
#     i is the number of item in p
def find_column(p, i):
    last_cr = p.lexer.lexdata.rfind('\n', 0, p.lexpos(i))
    if last_cr < 0:
        last_cr = 0
    column = (p.lexpos(i) - last_cr) + 1
    return column


# Check types for operator and operands
def check_int_float_operands(p):
    # If something is none then it's error has been reported
    if p[1] is None or p[3] is None:
        return False

    if (type(p[1]) not in {int, float}) or (type(p[3]) not in {int, float}):
        print(Fore.YELLOW + ("Operator '" + Fore.BLACK + p[2] +
                             Fore.YELLOW + "' is only defined for 'int' and 'float' in line {} column {}").format(
            p.lineno(2), find_column(p, 2))
              )
        return False

    return True


def boolexpr(expr):
    if expr is None:
        return None

    if type(expr) is str:
        return True if len(expr) > 0 else False

    return True if expr != 0 else False


# Initialize colorama
colorama_init(autoreset=True)

# A map that contains variables and their values
variables = {}
# Contains the last error number happened in runtime environment
runtime_err = 0
# A stack containing running states
# It gets used for disabling interpreting in if and while statements
running = [True]


# Get's a symbol from variables dictionary and shows error if not exists
def get_symbol(p, i):
    # Get symbol's value form variables dictionary
    symbol_val = variables.get(p[i], None)
    # If symbol does not exist
    if symbol_val is None:
        print(Fore.RED + "Variable '" + Fore.BLACK + p[1] + Fore.RED
              + "' is not defined in line {} column {}".format(p.lineno(1), find_column(p, 1)))
    else:
        return symbol_val

    return None


precedence = (
    ('right', 'ASSIGN'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('right', 'UMINUS'),  # Unary minus operator
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('right', 'BOOL'),
)


# Program's starting point
def p_s(p):
    """s : '{' p '}'"""
    pass


# Program's main body
def p_p(p):
    """
    p : stmt p
      | expr ';' p
      | boolexpr ';' p
      |
    """
    pass


def p_stmt(p):
    """
    stmt : PRINT '(' print_arguments ')' ';'
    """
    if not running[-1]:
        return

    if p[3] is not None:
        print(p[3])


def p_print_arguments(p):
    """
    print_arguments : expr ',' print_arguments
                    | boolexpr ',' print_arguments
                    | boolexpr
                    | expr
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    # Second rule
    if len(p) == 2:
        p[0] = str(p[1])
    # First rule
    else:
        if p[3] is not None and p[1] is not None:
            p[0] = str(p[1]) + p[3]


def p_stmt_if(p):
    """
    stmt : IF '(' boolexpr ')' '{' ifA p ifB '}' ELSE '{' ifC p ifB '}'
    """
    pass


def p_ifA(p):
    """
    ifA :
    """
    global running
    # If current state is not running
    if not running[-1]:
        running.append(False)
    # Push evaluated value as running state
    else:
        running.append(p[-3])


def p_ifB(p):
    """
    ifB :
    """
    global running
    running.pop()


def p_ifC(p):
    """
    ifC :
    """
    global running
    # If current state is not running
    if not running[-1]:
        running.append(False)
    # Push not(evaluated value) as running state
    else:
        running.append(not p[-9])


def p_stmt_while(p):
    """
    stmt : WHILE '(' boolexpr ')' '{' whileA p whileB '}'
    """
    pass


def p_whileA(p):
    """
    whileA :
    """
    global running
    # If current state is not running
    if not running[-1]:
        running.append(False)
    # Push evaluated value as running state
    else:
        running.append(p[-3])


def p_whileB(p):
    """
    whileB :
    """
    global running
    running.pop()

    if running[-1] and p[-5]:
        p.lexer.lexpos = parser.symstack[-7].lexpos


def p_boolexpr_and(p):
    """
    boolexpr : boolexpr AND boolexpr
    """
    if p[1] is not None and p[3] is not None:
        p[0] = p[1] and p[3]


def p_boolexpr_or(p):
    """
    boolexpr : boolexpr OR boolexpr
    """
    if not running[-1]:
        return

    if p[1] is not None and p[3] is not None:
        p[0] = p[1] or p[3]


def p_boolexpr_not(p):
    """
    boolexpr : NOT boolexpr
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = not p[2]


def p_boolexpr_bool(p):
    """
    boolexpr : BOOL expr
    """
    if not running[-1]:
        return

    p[0] = boolexpr(p[2])


def p_boolexpr_bool_boolexpr(p):
    """
    boolexpr : BOOL boolexpr
    """
    if not running[-1]:
        return

    p[0] = p[2]


def p_boolexpr_not_expr(p):
    """
    boolexpr : NOT expr
    """
    if not running[-1]:
        return

    expr_bool = boolexpr(p[2])
    if expr_bool is not None:
        p[0] = not expr_bool


def p_boolexpr_paran(p):
    """
    boolexpr : '(' boolexpr ')'
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = p[2]


def p_boolexpr_true_false(p):
    """
    boolexpr : TRUE
             | FALSE
    """
    if not running[-1]:
        return

    p[0] = True if p[1] == 'true' else False


def p_boolexpr_comparison(p):
    """
    boolexpr : comparison
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    p[0] = True if type(p[1]) is not bool else False


def p_comparison_gt(p):
    """
    comparison : comparisonA '>' expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if p[1] == False:
            p[0] = False
        else:
            p[0] = p[3] if p[1] > p[3] else False


def p_comparison_lt(p):
    """
    comparison : comparisonA '<' expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if p[1] == False:
            p[0] = False
        else:
            p[0] = p[3] if p[1] < p[3] else False


def p_comparison_eq(p):
    """
    comparison : comparisonA '=' expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if p[1] == False:
            p[0] = False
        else:
            p[0] = p[3] if p[1] == p[3] else False


def p_comparison_neq(p):
    """
    comparison : comparisonA NOTEQUAL expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if p[1] == False:
            p[0] = False
        else:
            p[0] = p[3] if p[1] != p[3] else False


def p_comparison_le(p):
    """
    comparison : comparisonA LE expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if p[1] == False:
            p[0] = False
        else:
            p[0] = p[3] if p[1] <= p[3] else False


def p_comparison_ge(p):
    """
    comparison : comparisonA GE expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if p[1] == False:
            p[0] = False
        else:
            p[0] = p[3] if p[1] >= p[3] else False


def p_comparisonA(p):
    """
    comparisonA : comparison
                | expr
    """
    if not running[-1]:
        return

    p[0] = p[1]


def p_expr_plus(p):
    """
    expr : expr '+' expr
    """
    if not running[-1]:
        return

    if p[1] is not None and p[3] is not None:
        p[0] = p[1] + p[3]


def p_expr_minus(p):
    """
    expr : expr '-' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] - p[3]


def p_expr_mul(p):
    """
    expr : expr '*' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] * p[3]


def p_expr_div(p):
    """
    expr : expr '/' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] / p[3]


def p_expr_pow(p):
    """
    expr : expr '^' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = pow(p[1], p[3])


def p_expr_symbol(p):
    """
    expr : SYMBOL
    """
    if not running[-1]:
        return

    # Get symbol's value
    sym_val = get_symbol(p, 1)
    # If symbol does not exist
    if sym_val is not None:
        p[0] = sym_val


def p_expr(p):
    """
    expr : INT
         | FLOAT
         | STRING
    """
    if not running[-1]:
        return

    p[0] = p[1]


def p_expr_paran(p):
    """
    expr : '(' expr ')'
    """
    if not running[-1]:
        return

    p[0] = p[2]


def p_expr_unary_minus(p):
    """
    expr : '-' expr %prec UMINUS
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = -p[2]


def p_expr_len(p):
    """
    expr : LEN '(' expr ')'
    """
    if not running[-1]:
        return

    if p[3] is not None:
        if type(p[3]) is str:
            p[0] = len(p[3])
        else:
            print(Fore.RED + "'len' only accepts string in line {} column {}".format(p.lineno(1), find_column(p, 1)))


def p_expr_to_str(p):
    """
    expr : TO_STR '(' expr ')'
    """
    if not running[-1]:
        return

    if p[3] is not None:
        p[0] = str(p[3])


def p_expr_err(p):
    """
    expr : ERR '(' ')'
    """
    global runtime_err

    if not running[-1]:
        return

    p[0] = runtime_err


def p_expr_to_int(p):
    """
    expr : TO_INT '(' expr ')'
    """
    global runtime_err

    if not running[-1]:
        return

    if p[3] is not None:
        try:
            p[0] = int(p[3])
        except ValueError:
            runtime_err = 1
        else:
            runtime_err = 0


def p_expr_to_float(p):
    """
    expr : TO_FLOAT '(' expr ')'
    """
    global runtime_err

    if not running[-1]:
        return

    if p[3] is not None:
        try:
            p[0] = float(p[3])
        except ValueError:
            runtime_err = 1
        else:
            runtime_err = 0


def p_expr_input(p):
    """
    expr : INPUT '(' expr ')'
         | INPUT '(' ')'
    """
    if not running[-1]:
        return

    prompt = str(p[3]) if len(p) > 4 else ''
    p[0] = input(prompt)


def p_expr_str_index(p):
    """
    expr : expr '[' expr ']'
    """
    if not running[-1]:
        return

    if p[1] is None or p[2] is None:
        return

    if type(p[1]) is not str:
        print(Fore.RED + "Value is not indexable in line {} column {}".format(p.lineno(2), find_column(p, 2)))
    else:
        if type(p[3]) is not int:
            print(Fore.RED + "Index is not 'int' in line {} column {}".format(p.lineno(4), find_column(p, 4)))
        # Everything is ok
        else:
            # Check if index is out of range
            if p[3] >= len(p[1]):
                print(Fore.RED + "Index is out of range in line {} column {}".format(p.lineno(4), find_column(p, 4)))
            else:
                p[0] = p[1][p[3]]


def p_expr_assign(p):
    """
    expr : SYMBOL ASSIGN expr
    """
    if not running[-1]:
        return

    if p[3] is not None:
        variables[p[1]] = p[3]
        p[0] = p[3]


def p_expr_str_subscript(p):
    """
    expr : expr '[' expr_or_empty ':' expr_or_empty ']'
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    if type(p[1]) is not str:
        print(Fore.RED + "Value is not subscriptable in line {} column {}".format(p.lineno(2), find_column(p, 2)))
    else:
        if p[3] is not None and type(p[3]) is not int:
            print(Fore.RED + "Index is not 'int' in line {} column {}".format(p.lineno(2), find_column(p, 2)))
            return
        if p[5] is not None and type(p[5]) is not int:
            print(Fore.RED + "Index is not 'int' in line {} column {}".format(p.lineno(4), find_column(p, 4)))
            return
        # Everything is ok
        else:
            p[0] = p[1][p[3]:p[5]]


def p_expr_or_empty(p):
    """
    expr_or_empty : expr
                  |
    """
    if not running[-1]:
        return

    if len(p) == 2:
        p[0] = p[1]


# Build the parser
parser = yacc.yacc()
