import unittest


def gen_parikh_set(w, k, sigma_size=2):
    """Generates the P_k set of the given w word."""

    pi_k_set = set()
    n = len(w)
    assert k <= n
    t = [0] * sigma_size
    # create the first slice
    for i in xrange(k):
        t[w[i]] += 1
    pi_k_set.add(tuple(t))
    for i in xrange(1, n - k + 1):
        t[w[i - 1]] -= 1
        t[w[i + k - 1]] += 1
        pi_k_set.add(tuple(t))
    return pi_k_set


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


class TestParikhSets(unittest.TestCase):
    @staticmethod
    def str_to_tuple(astr):
        return tuple(map(lambda c: ord(c) - ord("a"), astr))

    def verify_parikh_sets(self, pi1, pi2):
        self.assertEqual(len(pi1), len(pi2))
        for k in xrange(len(pi1)):
            self.assertEqual(pi1[k], pi2[k])

    def test_gen_parikh_set(self):
        s1 = self.str_to_tuple("aaba")
        pi11 = [{(1, 0), (0, 1)}, {(2, 0), (1, 1)}, {(2, 1)}, {(3, 1)}]
        pi12 = [gen_parikh_set(s1, k) for k in xrange(1, len(s1) + 1)]
        self.verify_parikh_sets(pi11, pi12)

        s2 = self.str_to_tuple("aabac")
        pi21 = [{(1, 0, 0), (0, 1, 0), (0, 0, 1)}, {(2, 0, 0), (1, 1, 0), (1, 0, 1)}, {(2, 1, 0), (1, 1, 1)},
                {(3, 1, 0), (2, 1, 1)}, {(3, 1, 1)}]
        pi22 = [gen_parikh_set(s2, k, 3) for k in xrange(1, len(s2) + 1)]
        self.verify_parikh_sets(pi21, pi22)

        s3 = self.str_to_tuple("aaaaaa")
        pi31 = [{(1,)}, {(2,)}, {(3,)}, {(4,)}, {(5,)}, {(6,)}]
        pi32 = [gen_parikh_set(s3, k, 1) for k in xrange(1, len(s3) + 1)]
        self.verify_parikh_sets(pi31, pi32)

    def test_check_parikh_set_monotonicity(self):
        pi = {
            1: {(1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0),
                (0, 0, 0, 0, 0, 1)},
            2: {(1, 1, 0, 0, 0, 0), (1, 0, 1, 0, 0, 0), (1, 0, 0, 0, 1, 0), (0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 1),
                (0, 0, 1, 0, 1, 0)},
            3: {(1, 1, 1, 0, 0, 0), (1, 1, 0, 0, 1, 0), (1, 0, 1, 1, 0, 0), (0, 0, 1, 1, 1, 0), (1, 0, 0, 0, 1, 1),
                (0, 0, 1, 0, 1, 1), (1, 0, 1, 0, 1, 0)},
            4: {(1, 1, 1, 1, 0, 0), (1, 1, 0, 0, 1, 1), (1, 1, 1, 0, 1, 0), (1, 0, 1, 1, 1, 0), (1, 0, 1, 0, 1, 1),
                (0, 0, 1, 1, 1, 1)},
            5: {(1, 1, 1, 1, 1, 0), (1, 1, 1, 0, 1, 1), (1, 0, 1, 1, 1, 1)},
            6: {(1, 1, 1, 1, 1, 1)}}

        for k in xrange(1, 5):
            assert check_parikh_set_monotonicity(pi, k, 6)


if __name__ == '__main__':
    unittest.main()
