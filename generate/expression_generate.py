

def expression_gen(expression, col):
    loc = 0
    if len(expression[loc:]) > 0 and expression[loc] == "aggregation expression":
        loc += 1
        if len(expression[loc:]) > 0 and expression[loc] == "sum":
            pass
        elif len(expression[loc:]) > 0 and expression[loc] == "count":
            pass
        elif len(expression[loc:]) > 0 and expression[loc] == "min":
            pass
        elif len(expression[loc:]) > 0 and expression[loc] == "max":
            pass
        elif len(expression[loc:]) > 0 and expression[loc] == "avg":
            return ',AVG(' + col + ')'
        elif len(expression[loc:]) > 0 and expression[loc] == "stddev":
            pass
        elif len(expression[loc:]) > 0 and expression[loc] == "var":
            pass
    elif len(expression[loc:]) > 0 and expression[loc] == "case expression":
        pass
    elif len(expression[loc:]) > 0 and expression[loc] == "function expression":
        pass

