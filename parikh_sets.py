from collections import deque, defaultdict
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


def is_connected(g):
    """The graph is connected iff we can reach from every node every other one."""
    assert len(g) > 0
    start = next(g.iterkeys())
    q = deque([start])
    was = {start}
    while q:
        n = q.popleft()
        for v in g[n]:
            if v not in was:
                was.add(v)
                q.append(v)
    return len(g) == len(was)


def is_parikh_less(p1, p2):
    """Returns true if p1 is <= p2 for each entry k of p1 (Parikh-vector)."""

    assert len(p1) == len(p2)
    for k in xrange(len(p1)):
        if p1[k] > p2[k]:
            return False
    return True


def build_graph_from_pi(pi):
    """Builds "poset" graph from the given Parikh sets."""

    g = defaultdict(lambda: [])
    for k in xrange(1, len(pi)):
        for p1 in pi[k]:
            for p2 in pi[k + 1]:
                if is_parikh_less(p1, p2):
                    g[p1].append(p2)
                    g[p2].append(p1)
    return g


def find_shortest_word(pi):
    """From the given pi_k sets finds the shortest w word that shares the same pi_k sets. Returns None if it cannot be
    realized."""

    # if the graph is not connected => there is no solution
    if not is_connected(build_graph_from_pi(pi)):
        return None

    # size of the alphabet
    sigma_size = len(next(iter(pi[1])))
    q = deque([()])
    while q:
        w = q.popleft()
        # if len(w) > len(pi) * 2:
        #     return None
        # check whether the current word did not generate more elements in pi_k
        equal = True
        for k in xrange(1, min(len(w), len(pi)) + 1):
            pik = gen_parikh_set(w, k, sigma_size)
            if len(pik) > len(pi[k]):
                break
            elif len(pik) < len(pi[k]):
                if not pik.issubset(pi[k]):
                    break
                equal = False
            elif not pik.issubset(pi[k]):
                break
        else:
            # if the pi sets are the same => return shortest word
            if equal and len(w) >= len(pi):
                return w
            for j in xrange(sigma_size):
                q.append(w + (j,))
    return None


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

    spider = {
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

    def test_check_parikh_set_monotonicity(self):
        for k in xrange(1, 5):
            assert check_parikh_set_monotonicity(TestParikhSets.spider, k, 6)

    def test_find_shortest_word(self):
        self.assertIsNone(find_shortest_word(TestParikhSets.spider))
        self.assertIsNone(find_shortest_word({1: {(1, 0), (0, 1)}, 2: {(2, 0), (0, 2)}}))


if __name__ == '__main__':
    unittest.main()
