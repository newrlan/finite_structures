from typing import List
from copy import deepcopy


class Permutation:
    _perm = dict()

    def apply(self, k):
        return self._perm.get(k, k)

    def _from_cycle(self, cycle: List[int]):
        pass

    def __mul__(self, cycle: List[int]):

        res = Permutation()
        res._perm = deepcopy(self._perm)

        if len(cycle) == 0:
            return res

        cycle_perm = {a: b for a, b in zip(cycle, cycle[1:])}
        cycle_perm[cycle[-1]] = cycle[0]

        m_2 = max(cycle_perm)
        m_1 = 0 if len(self._perm) == 0 else max(self._perm)
        n = max(m_1, m_2)

        for k in range(n+1):
            k_ = self.apply(k)
            k__ = cycle_perm.get(k_, k_)
            if k == k__:
                if k in res._perm:
                    del res._perm[k]
                continue

            res._perm[k] = k__

        return res

    def cycles(self):
        seen = set(self._perm.keys())
        answer = []

        while len(seen) > 0:
            cycle = []
            head = seen.pop()
            cycle.append(head)
            k = self.apply(head)
            while k != head:
                cycle.append(k)
                seen.remove(k)
                k = self.apply(k)
            answer.append(cycle)

        return answer

    def __repr__(self):
        if len(self._perm) == 0:
            return '( )'
        cycles = self.cycles()

        def one_cycle(arr):
            return '(' + ' '.join([str(x) for x in arr]) + ')'

        return ' '.join([one_cycle(arr) for arr in cycles])


