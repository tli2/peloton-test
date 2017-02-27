import itertools


# this method generates the combinations for the range len(table_columns)
# it then generates all the permutations for each possible combination
def generate_column_options(table_columns):
    # First yield the star
    yield '*'
    # Now yield all the remaining options
    col_combinations = []
    for x in range(len(table_columns[0])):
        col_combinations.append(itertools.combinations(table_columns[0], x))
    for x in range(1, len(col_combinations)):
        for comb in col_combinations[x]:
            for z in itertools.permutations(comb):
                if z != len(col_combinations) - 1:
                    z += ('',) * ((len(col_combinations) - 1) - x)
                return_string = ""
                for i in range(len(z)):
                    if i > 0 and z[i] != '':
                        return_string = return_string + "," + z[i]
                    else:
                        return_string += z[i]
                yield return_string + ''
