from common import randop
def expression_gen(expression, int_cols, varChar_cols):
    loc = 0
    if len(expression[loc:]) > 0 and expression[loc] == "aggregation expression":
        loc += 1
        if len(expression[loc:]) > 0 and expression[loc] == "sum":
            return 'SUM(' + int_cols[randop.create_random_int(0,len(int_cols)-1)] + ')'
        elif len(expression[loc:]) > 0 and expression[loc] == "count":
            return 'count(' + int_cols[randop.create_random_int(0,len(int_cols)-1)] + ')'
        elif len(expression[loc:]) > 0 and expression[loc] == "min":
            return 'MIN(' + int_cols[randop.create_random_int(0,len(int_cols)-1)] + ')'
        elif len(expression[loc:]) > 0 and expression[loc] == "max":
            return 'MAX(' + int_cols[randop.create_random_int(0,len(int_cols)-1)] + ')'
        elif len(expression[loc:]) > 0 and expression[loc] == "avg":
            return 'AVG(' + int_cols[randop.create_random_int(0,len(int_cols)-1)] + ')'
        elif len(expression[loc:]) > 0 and expression[loc] == "stddev":
            pass
        elif len(expression[loc:]) > 0 and expression[loc] == "var":
            pass
    elif len(expression[loc:]) > 0 and expression[loc] == "case expression":
        pass
    elif len(expression[loc:]) > 0 and expression[loc] == "function expression":
        pass
