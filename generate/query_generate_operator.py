def operator_gen(operator):
    loc = 0
    if len(operator[loc:])>0 and operator[loc] == "Wildcard":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "Alias":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "Arithmetic":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "Set":
        pass
    elif len(operator[loc:])>0 and operator[loc] == "String":
        pass
    elif len(operator[loc:]) > 0 and operator[loc] == "Comparison":
        loc += 1
        if not len(operator[loc:]) > 0:
            return ['=', '>', '<', '<=', '>=', '!=']
        elif len(operator[loc:]) > 0 and operator[loc] == "Logical":
            pass
        elif len(operator[loc:]) > 0 and operator[loc] == "Equality":
            return ['=']
        elif len(operator[loc:]) > 0 and operator[loc] == "Greater Than":
            return ['>']
        elif len(operator[loc:]) > 0 and operator[loc] == "Less Than":
            return ['<']
        elif len(operator[loc:]) > 0 and operator[loc] == "Less Than or Equal To":
            return ['<=']
        elif len(operator[loc:]) > 0 and operator[loc] == "Greater Than or Equal To":
            return ['>=']
        elif len(operator[loc:]) > 0 and operator[loc] == "Not Equal To":
            return ['!=']
    elif len(operator[loc:])>0 and operator[loc] == "Logical":
        loc += 1
        if len(operator[loc:]) > 0 and operator[loc] == "Conjunction":
            return ['AND']
        elif len(operator[loc:]) > 0 and operator[loc] == "Disjunction":
            return ['OR']
        elif len(operator[loc:])>0 and operator[loc] == "Negation":
            return ['NOT']
    # should indicate that the requested generation is wrong
    return 'ERROR'