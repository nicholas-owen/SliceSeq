from collections import defaultdict
from argparse import ArgumentParser

def find_after_break(expr, sigs):
    breakpoints = []
    # Pad by 1 so end caes don't automatically pass
    for break_sample in range(1, len(expr) - 1):
        sign = (expr[0] > expr[break_sample])
        for i1 in range(break_sample):
            for i2 in range(break_sample, len(expr)):
                if sigs[i1][i2] == False or (expr[i1] > expr[i2] != sign):
                    break
            # "else continue break" construct breaks out of outer loop as well
            else:
                continue
            break
        else:
            # Monotonic split means we made it through all pairs of samples
            breakpoints.append(break_sample)
    return breakpoints

def find_peak(expr, sigs):
    peak_points = []

    for peak_point in range(1, len(expr) - 1):
        if ((expr[peak_point - 1] < expr[peak_point] < expr[peak_point +1]) 
            or (expr [peak_point - 1] > expr[peak_point] > expr[peak_point + 1])):
            continue
            # This isn't the actual peak


        sign = 1 if expr[peak_point] > expr[peak_point - 1] else -1

        prepost = [False, False]
        for other in range(len(expr)):
            if other == peak_point:
                continue
            if sign * expr[peak_point] > sign * expr[other] and sigs[peak_point][other]:
                prepost[peak_point < other] = True
                # If peak_point < other , then update prepost[1] (post),
                # otherwise update prepost[0] (pre)
        if prepost == [True, True]:
            peak_points.append(peak_point)
    return peak_points


def test_case_1():
    "A monotonic increasing series of significance"

    expr = [0, 1, 2, 3, 4, 5]
    sigs = defaultdict(lambda: defaultdict(lambda: True))

    print "Case 1", find_after_break(expr, sigs), find_peak(expr, sigs)

def test_case_2():
    "A single, obvious breakpoint"

    expr = [0, 0, 0, 1, 1, 1]
    sigs = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
    sigs[0][0] = sigs[0][1] = sigs[0][2] = False
    sigs[0][3] = sigs[0][4] = sigs[0][5] = True
    sigs[1] = sigs[2] = sigs[0]
    sigs[3][0] = sigs[3][1] = sigs[3][2] = True
    sigs[3][3] = sigs[3][4] = sigs[3][5] = False
    sigs[4] = sigs[5] = sigs[3]

    print "Case 2:", find_after_break(expr, sigs), find_peak(expr, sigs)


def test_case_3():
    "A monotonic increasing series of no significance"

    expr = [0, 1, 2, 3, 4, 5]
    sigs = defaultdict(lambda: defaultdict(lambda: False))

    print "Case 3:", find_after_break(expr, sigs), find_peak(expr, sigs)


def test_case_4():
    "A single, obvious breakpoint, with noise"

    expr = [1, 3, 2, 15, 14, 17]
    sigs = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
    sigs[0][0] = sigs[0][1] = sigs[0][2] = False
    sigs[0][3] = sigs[0][4] = sigs[0][5] = True
    sigs[1] = sigs[2] = sigs[0]
    sigs[3][0] = sigs[3][1] = sigs[3][2] = True
    sigs[3][3] = sigs[3][4] = sigs[3][5] = False
    sigs[4] = sigs[5] = sigs[3]

    print "Case 4:", find_after_break(expr, sigs), find_peak(expr, sigs)

def test_case_5():
    "A rising peak in the middle, difference with neighbors not significant"
    expr = [2,3,4,3,2]
    sigs = {}
    sigs[0] = {0:False, 1:False, 2:True, 3:False, 4:False}
    sigs[1] = {0:False, 1:False, 2:False, 3:False, 4:False}
    sigs[2] = {0:True, 1:False, 2:False, 3:False, 4:True,}
    sigs[3] = sigs[1]
    sigs[4] = sigs[0]
    print "Case 5:", find_after_break(expr, sigs), find_peak(expr, sigs)


def test_case_6():
    "A falling peak in the middle, difference with neighbors not significant"
    expr = [5,4,3,4,5]
    sigs = {}
    sigs[0] = {0:False, 1:False, 2:True, 3:False, 4:False}
    sigs[1] = {0:False, 1:False, 2:False, 3:False, 4:False}
    sigs[2] = {0:True, 1:False, 2:False, 3:False, 4:True,}
    sigs[3] = sigs[1]
    sigs[4] = sigs[0]
    print "Case 6:", find_after_break(expr, sigs), find_peak(expr, sigs)

def test_case_7():
    "A falling peak in the middle, difference with neighbors not significant"
    expr = [5,4,3,4,5,6,7]
    sigs = {}
    sigs[0] = {0:False, 1:False, 2:True, 3:False, 4:False, 5: False, 6: True}
    sigs[1] = {0:False, 1:False, 2:False, 3:False, 4:False, 5: True, 6: True}
    sigs[2] = {0:True, 1:False, 2:False, 3:False, 4:True, 5: True, 6:True}
    sigs[3] = sigs[1]
    sigs[4] = sigs[0]
    sigs[5] = {0:False, 1:True, 2:True, 3:True, 4:False, 5: False, 6: False}
    sigs[6] = defaultdict(lambda:True)
    sigs[6][5] = sigs[6][6] = False
    print "Case 7:", find_after_break(expr, sigs), find_peak(expr, sigs)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--has-gene-id', '-g', action="store_true",
                        default=False)
    parser.add_argument('--testing', '-t', action="store_true", default=False)
    parser.add_argument("filename", help="File to operate on")

    args = parser.parse_args()
    return args

def process_file(args):

    expr_file = open(args.filename)
    expr_by_gene = defaultdict(lambda: dict())
    sig_by_gene = defaultdict(lambda: defaultdict(dict))

    # When there's a gene_id column, everything is shifted over by one.
    gene_name_idx = 1 + args.has_gene_id
    samp1_idx = 3 + args.has_gene_id
    samp2_idx = 4 + args.has_gene_id
    test_idx =  5 + args.has_gene_id
    expr1_idx = 6 + args.has_gene_id
    expr2_idx = 7 + args.has_gene_id
    sig_idx =  11 + args.has_gene_id

    expr_file.readline()
    for line in expr_file:
        data = line.split()
        gene_name = data[gene_name_idx]
        samp1 = data[samp1_idx]
        samp2 = data[samp2_idx]
        expr1 = float(data[expr1_idx])
        expr2 = float(data[expr2_idx])
        sig = data[sig_idx]
        expr_by_gene[gene_name][samp1] = float(expr1)
        expr_by_gene[gene_name][samp2] = float(expr2)
        sig_by_gene[gene_name][samp1][samp2] = (sig == 'yes')

    for gene in expr_by_gene:
        sigs = sig_by_gene[gene]
        expr = [expr_by_gene[gene][sample] for sample in sigs]
        print gene, find_after_break(expr, sigs), find_peak(expr, sigs)
    return expr_by_gene, sig_by_gene



if __name__ == "__main__":
    args = parse_args()
    if args.testing:
        locs = locals()
        for thing in sorted(locs.keys()):
            # need to iterate over keys because locals changes when we include thing
            if thing.startswith('test_case'):
                print thing
                locs[thing]()
    else:
        expr_by_gene, sig_by_gene = process_file(args)
