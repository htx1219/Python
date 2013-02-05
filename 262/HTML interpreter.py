import ply.lex as lex
import ply.yacc as yacc
import jstokens
import jsgrammar
import graphics as graphics
import jsinterp 

def interpret(trees): # Hello, friend
    for tree in trees: # Hello,
        # ("word-element","Hello")
        nodetype=tree[0] # "word-element"
        if nodetype == "word-element":
            graphics.word(tree[1]) 
        elif nodetype == "tag-element":
            # <b>Strong text</b>
            tagname = tree[1] # b
            tagargs = tree[2] # []
            subtrees = tree[3] # ...Strong Text!...
            closetagname = tree[4] # b
            if tagname != closetagname:
                graphics.warning("(mistmatched " + tagname + " " + closetagname + ")")
            else:
                graphics.begintag(tagname, tagargs)
                interpret(subtrees)
                graphics.endtag()
        elif nodetype == "javascript-element":
            jstext = node[1]
            jslexer = lex.lex(module = jstokens)
            jsparser = yacc.yacc(module=jsgrammar)
            jstree = jsparser.parse(jstext, lexer=jslexer)
            result = jsinterp.interpret(jstree)
            graphics.word(result)
##            if False:
##                print jstext
##            jslexer.input(jstext)
##            while True:
##                tok = jslexer.token()
##                if not tok: break
##                print tok

            jsparser = yacc.yacc(module=jsgrammar,tabmodule="parsetabjs")
            jsast = jsparser.parse(jstext,lexer=jslexer)
            result = jsinterp.interpret(jsast)
            graphics.word(result) 
            ## WHAT'S HERE?



# Note that graphics.initialize and finalize will only work surrounding a call
# to interpret

graphics.initialize() # Enables display of output.\
interpret([("word-element","Hello")])
graphics.finalize() # Enables display of output.
