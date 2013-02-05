webpage = """<html>
<h1>Level One Headings Use (H1) Tags</h1> 
<p>Paragraphs use (P) tags. Unordered lists use (UL) tags.
<ul>
  <li> List items use (LI) tags. </li>
  <li> Text can be <b>bold (B) </b>, <i>italic (I)</i>, <small>small (SMALL)</small>, <big>big (BIG)</big>, or look like a <tt>typewriter (TT)</tt>.</li>
  <li> There are also ordered list that use (OL) tags. Let's make one nested inside our current list item.
  <ol><li> Text can also be <strong> strong (STRONG)</strong> or <em>emphasized (EM)</em>, which typically renders like bold and italics. </li>
      <li> Webpages can have <a href = "target">hyperlinks (A HERF = "target") </a>.</li></ol>
  <li> It is also possible to include images <img src = "cs262.png"></img> (IMG SRC = "cs262.png")</li>
</ul>
</p>
<p>We'll finish off with one last paragraph.</p>
</html> 
"""

# Display the page!

import ply.lex as lex
import ply.yacc as yacc
import htmltokens
import htmlgrammar
import htmlinterp
import graphics as graphics
import jstokens


htmllexer = lex.lex(module=htmltokens) 
htmlparser = yacc.yacc(module=htmlgrammar,tabmodule="parsetabhtml") 
ast = htmlparser.parse(webpage,lexer=htmllexer) 
jslexer = lex.lex(module=jstokens) 
graphics.initialize() # Enables display of output.
htmlinterp.interpret(ast) 
graphics.finalize() # Enables display of output.
