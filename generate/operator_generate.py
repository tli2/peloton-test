def operator_gen(operator):
    loc = 0
    if len(operator[loc:])>0 and operator[loc] == "wildcard":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "alias":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "arithmetic":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "set":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "string":
        pass
    elif len(operator[loc:]) > 0 and operator[loc] == "comparison":
        loc += 1
        if not len(operator[loc:]) > 0:
            return ['=', '>', '<', '<=', '>=', '!=']
        elif len(operator[loc:]) > 0 and operator[loc] == "logical":
            loc += 1
            if len(operator[loc:]) > 0 and operator[loc] == "conjunction":
                return ['=', '>', '<', '<=', '>=', '!=','AND']
            elif len(operator[loc:]) > 0 and operator[loc] == "disjunction":
                return ['=', '>', '<', '<=', '>=', '!=','OR']
            elif len(operator[loc:]) > 0 and operator[loc] == "negation":
                return ['=', '>', '<', '<=', '>=', '!=','NOT']
        elif len(operator[loc:]) > 0 and operator[loc] == "equality":
                return ['=']
        elif len(operator[loc:]) > 0 and operator[loc] == "greater than":
            return ['>']
        elif len(operator[loc:]) > 0 and operator[loc] == "less Than":
            return ['<']
        elif len(operator[loc:]) > 0 and operator[loc] == "less than or equal to":
            return ['<=']
        elif len(operator[loc:]) > 0 and operator[loc] == "greater than or equal to":
            return ['>=']
        elif len(operator[loc:]) > 0 and operator[loc] == "not equal to":
            return ['!=']
    elif len(operator[loc:])>0 and operator[loc] == "logical":
        # this should be invalid
        pass
    pass