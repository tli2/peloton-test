def statement_gen(statement):
    loc = 0
    if len(statement[loc:]) > 0 and statement[loc] == "access control statement":
        loc += 1
        if len(statement[loc:]) > 0 and statement[loc] == "grant":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "revoke":
            pass
    elif len(statement[loc:]) > 0 and statement[loc] == "session management statement":
        if len(statement[loc:]) > 0 and statement[loc] == "connect":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "set":
            pass
    elif len(statement[loc:]) > 0 and statement[loc] == "data definition statement":
        loc += 1
        if len(statement[loc:]) > 0 and statement[loc] == "create":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "alter":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "drop":
            pass
    elif len(statement[loc:]) > 0 and statement[loc] == "data manipulation statement":
        loc += 1
        if len(statement[loc:]) > 0 and statement[loc] == "update":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "select":
            return "SELECT "
        elif len(statement[loc:]) > 0 and statement[loc] == "insert":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "delete":
            pass
    elif len(statement[loc:]) > 0 and statement[loc] == "transaction management statement":
        if len(statement[loc:]) > 0 and statement[loc] == "commit":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "rollback":
            pass
        elif len(statement[loc:]) > 0 and statement[loc] == "lock table":
            pass
    elif len(statement[loc:]) > 0 and statement[loc] == "import export statement":
        pass
    elif len(statement[loc:]) > 0 and statement[loc] == "procedural statement":
        if len(statement[loc:]) > 0 and statement[loc] == "call":
            pass

    return None
