def clause_gen(clause):
    loc = 0
    if len(clause[loc:]) > 0 and clause[loc] == "FROM":
        loc += 1
        if len(clause[loc:]) > 0 and clause[loc] == "WHERE":
            loc += 1
            return "FROM " + TABLE + " WHERE "
    return ''