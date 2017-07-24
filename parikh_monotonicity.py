from itertools import combinations
from parikh_sets import find_shortest_word


def pi_union(pi_i, pi_j, sigma_size=2):
    rset = set()
    for e1 in pi_i:
        for e2 in pi_j:
            rset.add(tuple(e1[i] + e2[i] for i in xrange(sigma_size)))
    return rset


def pi_minus(pi_i, pi_j, sigma_size=2):
    """i >= j"""
    rset = set()
    for e1 in pi_i:
        for e2 in pi_j:
            rset.add(tuple(e1[i] - e2[i] for i in xrange(sigma_size)))
    return rset


def check_parikh_set_monotonicity(pi, k, sigma_size):
    for i in xrange(1, k / 2 + 1):
        j = k - i
        pi_i_plus_pi_j = pi_union(pi[i], pi[j], sigma_size)
        # print pi_i_plus_pi_j
        # check whether P_{i+j} \subseteq Pi_i + Pi_j property holds
        if not pi[k].issubset(pi_i_plus_pi_j):
            return False

    for j in xrange(k, 0, -1):
        for i in xrange(j - 1, 0, -1):
            pi_j_minus_pi_i = pi_minus(pi[j], pi[i], sigma_size)
            # check whether Pi{i-j} \subseteq Pi_i - Pi_j
            if not pi[j - i].issubset(pi_j_minus_pi_i):
                return False
    return True


def gen_pi_k(k, sigma_size=2):
    """Generates the possible pi_k (k-length) elements, with the given alphabet size."""

    t = [0] * sigma_size
    t[-1] = k
    last_index = sigma_size - 1
    yield tuple(t)
    while last_index != 0 or t[0] < k:
        if last_index == 0:
            p, t[0] = t[0], 0
            i = 1
            while t[i] == 0:
                i += 1
            t[i] -= 1
            t[i - 1] = p + 1
            last_index = i - 1
        else:
            t[last_index] -= 1
            last_index -= 1
            t[last_index] += 1
        yield tuple(t)


def starting_pi_elements(sigma_size=2):
    pi_elements = []
    poss_elements = [element for element in gen_pi_k(1, sigma_size=sigma_size)]
    for j in xrange(1, len(poss_elements) + 1):
        for c in combinations(poss_elements, r=j):
            pi_elements.append({1: set(c)})
    return pi_elements


def create_new_good_pi_sets(n, sigma_size, pi):
    for i in xrange(1, n + 1):
        for pelements in combinations(gen_pi_k(n, sigma_size=sigma_size), r=i):
            pi[n] = set(pelements)
            if check_parikh_set_monotonicity(pi, n, sigma_size):
                yield pi.copy()


def gen_monotonic_pi_sets(sigma_size=2):
    """Generates monotonic PI sets."""

    good_pi_sets = starting_pi_elements(sigma_size)
    n = 2
    while True:
        print "searching %ith..." % n
        new_good_pi_sets = []
        for pi in good_pi_sets:
            for act_pi_set in create_new_good_pi_sets(n, sigma_size, pi.copy()):
                yield act_pi_set
                new_good_pi_sets.append(act_pi_set)
        good_pi_sets = new_good_pi_sets
        n += 1


def find_exception(sigma_size=2):
    """Attempt to find an exception pi set - that is monoton but not realizable by any word."""

    i = 0
    cnt = 0
    alen = 0
    for pi in gen_monotonic_pi_sets(sigma_size=sigma_size):
        # print pi
        if len(pi) > alen:
            alen = len(pi)
            print cnt
            cnt = 0
        if pi and find_shortest_word(pi) is None:
            # print pi
            cnt += 1
        #     break
        i += 1
find_exception(2)