import sys
import math
import random

def square_root(x, eps = 0.00001):
    assert x >= 0
    y = math.sqrt(x)
    assert abs(square(y) - x) <= eps
    return y
    
def square(x):
    return x * x

def double(x):
    return abs(20 * x) + 10

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self):
        self.min  = None  # Minimum value seen
        self.max  = None  # Maximum value seen
        self.type = None
        self.set = set()
    
    # Invoke this for every value
    def track(self, value):
        if self.max == None:
            self.max, self.min = value, value
            self.type = value
        self.set.add(value)
        if value > self.max:
            self.max = value
        if value < self.min:
            self.min = value
        if type(value) != type(self.type):
            self.type = None
        else:
            self.type = value
            
    def __repr__(self):
        repr(self.type) + " " + repr(self.min) + ".." + repr(self.max)+ " " + repr(self.set)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}
        
    def track(self, frame, event, arg):
        if event == "call" or event == "return":
            # YOUR CODE HERE. 
            # MAKE SURE TO TRACK ALL VARIABLES AND THEIR VALUES
            # If the event is "return", the return value
            # is kept in the 'arg' argument to this function.
            # Use it to keep track of variable "ret" (return)
            funcname = frame.f_code.co_name
            if not self.vars.has_key(funcname):
                self.vars[funcname] = {}
                self.vars[funcname]['call']={'==':{None:None}, '>=':{None:None}, '<=':{None:None}}
                self.vars[funcname]['return'] = {'==':{None:None}, '>=':{None:None}, '<=':{None:None}}
                self.vars[funcname]['return']['ret'] = Range()
            loc = frame.f_locals
            init = False
            if self.vars[funcname]['return']['=='].keys() == [None]:
                init = True
            if event == 'call':
                for k in loc:
                    if not self.vars[funcname]['call'].has_key(k):
                        self.vars[funcname]['call'][k] = Range()
                    self.vars[funcname]['call'][k].track(loc[k])
                for k in loc:
                    for k2 in loc:
                        if k > k2 and type(self.vars[funcname][event][k].type) == type(self.vars[funcname][event][k2].type) and type(self.vars[funcname]['call'][k].type) != type(None):
                            
                            if init:
                                self.vars[funcname][event]['=='][(k, k2)] = True
                                self.vars[funcname][event]['<='][(k, k2)] = True
                                self.vars[funcname][event]['>='][(k, k2)] = True
                            if loc[k] > loc[k2]:
                                self.vars[funcname][event]['=='][(k, k2)] = False
                                self.vars[funcname][event]['<='][(k, k2)] = False
                            if loc[k] < loc[k2]:
                                self.vars[funcname][event]['=='][(k, k2)] = False
                                self.vars[funcname][event]['>='][(k, k2)] = False 
            else:
                for k in loc:
                    #if not self.vars[funcname]['call'].has_key(k):
                    if not self.vars[funcname]['return'].has_key(k):
                        self.vars[funcname]['return'][k] = Range()
                    self.vars[funcname]['return'][k].track(loc[k])
                self.vars[funcname]['return']['ret'].track(arg)
                loc['ret'] = arg
                for k in loc:
                    for k2 in loc:
                        if k > k2 and type(self.vars[funcname][event][k].type) == type(self.vars[funcname][event][k2].type) and type(self.vars[funcname][event][k].type) != type(None):
                            if init:
                                self.vars[funcname][event]['=='][(k, k2)] = True
                                self.vars[funcname][event]['<='][(k, k2)] = True
                                self.vars[funcname][event]['>='][(k, k2)] = True
                            if loc[k] > loc[k2]:
                                self.vars[funcname][event]['=='][(k, k2)] = False
                                self.vars[funcname][event]['<='][(k, k2)] = False
                            if loc[k] < loc[k2]:
                                self.vars[funcname][event]['=='][(k, k2)] = False
                                self.vars[funcname][event]['>='][(k, k2)] = False
            
            return self.track
    
    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.iteritems():
            for event, vars in events.iteritems():
                s += event + " " + function + ":\n"
        
                for var, range in vars.iteritems():
                    if var not in ['==', '>=', '<=']:
                        if range.type != None:
                            s += "    assert isinstance(" + var + ", type("+repr(range.type)+"))\n"# YOUR CODE
                        s += "    assert " + var + " in "+repr(range.set)+'\n'
                        s += "    assert "
                        if range.min == range.max:
                            s += var + " == " + repr(range.min)
                        else:
                            s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                        s += "\n"
                    # ADD HERE RELATIONS BETWEEN VARIABLES
                    # RELATIONS SHOULD BE ONE OF: ==, <=, >=
                    else:
                        # s += repr(var) + repr(range) + '\n'
                        for k in range:
                            if range[k]:
                                s += "    assert " + k[0] + " " + var+ " " + k[1] + "\n"
                    # s += "    assert " + var + " >= " + var2 + "\n"               
        return s

invariants = Invariants()
    
def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
for i in range(1, 10):
    r = int(random.random() * 1000) # An integer value between 0 and 999.99
    z = square_root(r, eps)
    z = square(z)
sys.settrace(None)
print invariants

##test_vars = [34.6363, 9.348, -293438.402]
##for i in test_vars:
###for i in range(1, 10):
##    z = double(i)
##sys.settrace(None)
##print invariants

# Example sample of a correct output:
"""
return double:
    assert isinstance(x, type(-293438.402))
    assert x in set([9.348, -293438.402, 34.6363])
    assert -293438.402 <= x <= 34.6363
    assert x <= ret
"""
