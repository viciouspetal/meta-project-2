from reader import Reader


def cnf_parser(cnf_path):
    """

    :param cnf_path: path to CNF file from which SAT clauses and variable stat will be read
    :return: returns an array of arrays, where each element of the parent array represents a SAT clause
    """
    reader = Reader(cnf_path)
    in_data = reader.read()

    cnf = list()
    cnf.append(list())
    maxvar = 0

    for line in in_data:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c", "%"):
            for tok in tokens:
                lit = int(tok)
                maxvar = max(maxvar, abs(lit))
                if lit == 0:
                    cnf.append(list())
                else:
                    cnf[-1].append(lit)

    assert len(cnf[-1]) == 0
    cnf.pop()

    print(cnf)
    print(maxvar)
    return cnf

if __name__ == '__main__':
    path = './sat_data/uf20-01.cnf'
    cnf_parser(path)