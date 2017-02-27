def clause_gen(clause, table, cols):
    loc = 0
    if len(clause[loc:]) > 0 and clause[loc] == "from":
        loc += 1
        if len(clause[loc:]) > 0 and clause[loc] == "where":
            loc += 1
            return "FROM " + table + " WHERE "
        elif len(clause[loc:]) > 0 and clause[loc] == "order by":
            # for the order by clause cols are needed
            return_string = "FROM " + table + " ORDER BY "
            while len(clause[loc:]) > 0:
                loc += 1
                if (clause[loc] == "asc" or clause[loc] == "desc") and len(clause[loc + 1:]) > 0:
                    return_string += clause[loc] + ","
                else:
                    return_string += clause[loc]
            return return_string
    elif len(clause[loc:]) > 0 and clause[loc] == "aggregate":
        if not cols:
            return
        loc += 1
        if len(clause[loc:]) > 0 and clause[loc] == "from":
            loc += 1
            if len(clause[loc:]) > 0 and clause[loc] == "order by":
                loc += 1
                if len(clause[loc:]) == 0:
                    return_string = "FROM " + table + " GROUP BY {}".format((','.join(cols)))
                    return return_string
                elif len(clause[loc:]) > 0 and clause[loc] == "where":
                    return_string = "FROM " + table + " GROUP BY {} WHERE ".format((','.join(cols)))
                    return return_string

    pass
