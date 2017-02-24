def predicate_gen(predicate):
    loc = 0
    if len(predicate[loc:]) > 0 and predicate[loc] == "JOIN":
        return "JOIN "
    return ''