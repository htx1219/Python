import ply.lex as lex
import ply.yacc as yacc
import jstokens
import jsgrammar

def optimize(tree): # Expression trees only
    etype = tree[0]
    if etype == "binop":
        # Fix this code so that it handles a + ( 5 * 0 )
        # recursively! QUIZ!
        a = optimize(tree[1])
        op = tree[2]
        b = optimize(tree[3])
        if (op == "*" and b == ("number","1")) or (op == "+" and b == ("number","0")):
            return a
        if (op == "*" and a == ("number","1")) or (op == "+" and a == ("number","0")):
            return b
        elif op == "*" and (a == ("number","0") or b == ("number","0")):
            return ("number","0")
        elif op == '-' and a == b:
            return ("number", '0')
        elif a[0] == 'number' and b[0] == 'number':
            if op == "+":
                return ("number", str(float(a[1])+float(b[1])))
            if op == "-":
                return ("number", str(float(a[1])-float(b[1])))
            if op == "*":
                return ("number", str(float(a[1])*float(b[1])))
        return tree
    return tree
    
##
##print optimize(("binop",("number","5"),"*",("number","1"))) == ("number","5")
##print optimize(("binop",("number","5"),"+",("number","1")))
##print optimize(("binop",("number","5"),"*",("number","0"))) == ("number","0")
##print optimize(("binop",("number","5"),"+",("number","0"))) == ("number","5")
##print optimize(("binop",("number","5"),"+",("binop",("number","5"),"*",("number","0")))) == ("number","5")

def interpret(trees):
    global_env = (None, {"javascript output":''})
    for elt in trees:
        eval_elt(elt, global_env)
    return (global_env[1])["javascript output"]

def eval_stmts(stmts,env): 
    for stmt in stmts:
        #print stmts[0]
        eval_stmt(stmt,env) 
   
def eval_stmt(tree, environment):
    stmttype = tree[0]
    #print 'stmt:', stmttype
    if stmttype == 'return':
        return_exp = tree[1]
        retval = eval_exp(return_exp, environment)
        raise Exception(retval)
    elif stmttype == 'while':
        while eval_exp(tree[1], environment):
            eval_stmts(tree[2], environment)
    elif stmttype == "exp": 
        eval_exp(tree[1],environment)
    elif stmttype == "assign":
        # ("assign", "x", ("binop", ..., "+",  ...)) <=== x = ... + ...
        variable_name = tree[1]
        right_child = tree[2]
        new_value = eval_exp(right_child, environment)
        env_update(environment, variable_name, new_value)
    elif stmttype == 'var':
        vname = tree[1]
        rhs = tree[2]
        environment[1][vname] = eval_exp(rhs, environment)
    elif stmttype == "if-then-else": # if x < 5 then A;B; else C;D;
        conditional_exp = tree[1] # x < 5
        then_stmts = tree[2] # A;B;
        else_stmts = tree[3] # C;D;
        if eval_exp(conditional_exp, environment):
            eval_stmts(then_stmts, environment)
        else:
            eval_stmts(else_stmts, environment)
        #add_to_env(environment, fname, fvalue)
    elif stmttype == "if-then": # if x < 5 then A;B; else C;D;
        conditional_exp = tree[1] # x < 5
        then_stmts = tree[2] # A;B;
        if eval_exp(conditional_exp, environment):
            eval_stmts(then_stmts, environment)
    else:
        print "ERROR: unknown statement type ",
        print stmttype

def eval_elt(tree, env):
    elttype = tree[0]
    #print 'elt: ', elttype
    if elttype == 'function':
        fname = tree[1]
        fparams = tree[2]
        fbody = tree[3]
        fvalue = ('function', fparams, fbody, env)
        env[1][fname] = fvalue
    elif elttype == 'stmt':
        eval_stmt(tree[1], env)
    else:
        print 'ERROR: eval_elt: unkown element ' + elt

def eval_exp(exp, env):
    etype = exp[0]
    #print 'exp:', etype
    if etype == "number":
        return float(exp[1])
    elif etype == "string":
        return exp[1] 
    elif etype == "true":
        return True
    elif etype == "false":
        return False
    elif etype == "not":
        return not(eval_exp(exp[1], env))
    elif etype == 'function':
        fparams = exp[1]
        fbody = exp[2]
        return ("function", fparams, fbody, env)
    elif etype == "binop":
        a = eval_exp(exp[1], env)
        op = exp[2]
        b = eval_exp(exp[3], env)
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == "%":
            return a%b
        elif op == "==":
            return a==b
        elif op == "<=":
            return a<=b
        elif op == "<":
            return a<b
        elif op == ">=":
            return a>=b
        elif op == ">":
            return a>b
        elif op == "&&":
            return a and b
        elif op == "||":
            return a or b
        else:
            print "ERROR: unknown binary operator ",
            print op
            exit(1)
    elif etype == 'identifier':
        vname = exp[1]
        value = env_lookup(vname,env)
        if value == None:
            print "ERROR: unbound variable " + vname
        else:
            return value
    elif etype == 'call':
        fname = exp[1]
        args = exp[2]
        if fname == 'write':
            #print 'met write'
            argval = eval_exp(args[0], env)
            output_sofar = env_lookup("javascript output", env)
            env_update(env, "javascript output", output_sofar + '\n'+str(argval))
            return None
        fvalue = env_lookup(fname, env)
        if fvalue[0] == "function":
            # ("function", params, body, env)
            fparams = fvalue[1]
            fbody = fvalue[2]
            fenv = fvalue[3]
            if len(fparams) != len(args):
                print "ERROR: wrong number of args", fname
            else:
                #QUIZ: Make a new environment frame
                new_env = (fenv, {})
                for i in range(len(fparams)):
                    new_env[1][fparams[i]] = eval_exp(args[i], env)
                try:
                    eval_stmts(fbody, new_env)
                    # QUIZ : Evaluate the body
                    return None
                except Exception as return_value:
                    return return_value
        else:
            print  "ERROR: call to non-function"
    else:
        print 'ERROR: unknown expression type ',
        print etype
        return None

def env_lookup(vname, env):
    if vname in env[1]:
        return (env[1])[vname]
    elif env[0] == None:
        return None
    else:
        return env_lookup(vname, env[0])

def env_update(env, vname, value):
    if vname in env[1]:
        env[1][vname] = value
    elif not env[0] == None:
        env_update(vname, value, env[0])

def make_exception():
    try:
        print "joseph"
        y = 1/0
        raise Exception(22)
        print 'heller'
    except Exception as problem:
        print "didn't work: we caught"
        print problem


##sqrt = ("function",("x"),(("return",("binop",("identifier","x"),"*",("identifier","x"))),),{})
##environment = (None,{"sqrt":sqrt})
##print eval_stmt(("call","sqrt",[("number","2")]),environment)   

def get_tree(jstext):
    jslexer = lex.lex(module = jstokens)
    jsparser = yacc.yacc(module=jsgrammar)
    jstree = jsparser.parse(jstext, lexer=jslexer)
    return jstree

jslexer = lex.lex(module=jstokens)

def test_lexer(input_string):
  jslexer.input(input_string)
  result = [ ] 
  while True:
    tok = jslexer.token()
    if not tok: break
    result = result + [tok.type]
  return result

jstext1 = """
function sqrt(x){
return x*x;
}
write(sqrt(2));
"""

jstext2 = """
var x = 2;
x = 5;
write(x+3);
var y = function(q){return(q*q);};
write(y(x));
"""

jstext = """
var x = 5;
while (x > 0){
write(x);
x = x - 1;
};
"""

jstree = get_tree(jstext)
print jstree
print interpret(jstree)
