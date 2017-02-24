def statement_gen(statement):
    loc = 0
    if statement[loc] == "Data Manipulation Statement":
        loc += 1
        if statement[loc] == "SELECT":
            loc += 1
            return "SELECT "
    return None