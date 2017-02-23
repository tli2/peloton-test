from common import randop

def generate_clause(columns,col_type, rules):

    # check col_type and set columns
    if col_type == "VarChar":
        columns = columns[0]
    elif col_type == "Int":
        columns = columns[1]

    # check if performing a combination of Operator
    conjunction = False
    disjunction = False
    if rules[-1] == 'AND' and len(rules) != 1:
        rules = rules[:-1]
        conjunction = True
    elif rules[-1] == 'OR' and len(rules) != 1:
        rules = rules[:-1]
        disjunction = True

    if col_type == "VarChar":
        query_formatting = None
        for x in columns:
            for y in rules:
                query_formatting = [x, y]
                if y == 'IN':
                    temp_string = randop.create_random_string(randop.create_random_int(1, 20))
                    query_formatting.append("(" + temp_string + ")")
                elif conjunction:
                    query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))
                    query_formatting.append('AND')
                    query_formatting.append(columns[randop.create_random_int(0, len(columns) - 1)])
                    second_operator = rules[randop.create_random_int(0, len(rules) - 1)]
                    if second_operator == 'IN':
                        temp_string = randop.create_random_string(randop.create_random_int(1, 20))
                        query_formatting.append("(" + temp_string + ")")
                    else:
                        query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))
                elif disjunction:
                    query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))
                    query_formatting.append('OR')
                    query_formatting.append(columns[randop.create_random_int(0, len(columns) - 1)])
                    second_operator = rules[randop.create_random_int(0, len(rules) - 1)]
                    if second_operator == 'IN':
                        temp_string = randop.create_random_string(randop.create_random_int(1, 20))
                        query_formatting.append("(" + temp_string + ")")
                    else:
                        query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))
                else:
                    query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))

                # create the return string
                return_string = ""
                for i in range(len(query_formatting)):
                    if i > 0:
                        return_string += " " + query_formatting[i]
                    else:
                        return_string += query_formatting[i]
                yield return_string
    elif col_type == "Int":
        pass