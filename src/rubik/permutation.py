from math import lcm
from typing import List, Optional, Tuple
from copy import deepcopy
from itertools import combinations


class Permutation:
    def __init__(self, perm: Optional[dict[int, int]] = None):
        if perm is not None and not self._is_correct(perm):
            raise ValueError("Map in dictionary isn't permutation.")
        self._perm = perm if perm is not None else dict()

    def apply(self, k):
        return self._perm.get(k, k)

    def _from_cycle(self, cycle: List[int]):
        pass

    def __mul__(self, perm):
        m_2 = 0 if len(perm._perm) == 0 else max(perm._perm)
        m_1 = 0 if len(self._perm) == 0 else max(self._perm)
        n = max(m_2, m_1)
        res = dict()

        for k in range(n+1):
            k_ = self.apply(k)
            k__ = perm.apply(k_)
            if k != k__:
                res[k] = k__

        return Permutation(res)

    @staticmethod
    def _is_correct(arr: dict[int, int]) -> bool:
        """ Проверка корректности задания перестановки через словарь. """

        key_list = list(arr.keys())
        if len(key_list) != len(set(key_list)):
            return False

        val_list = list(arr.values())
        return len(val_list) == len(set(val_list))

    def cycles(self):
        """ Циклы перестановки. """
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

    def apply_cycle(self, *cycles):
        """ Применить (справа) цикл к пермутации. """
        perm = Permutation()
        for cycle in cycles:
            perm_dict = {a: b for a, b in zip(cycle, cycle[1:])}
            perm_dict[cycle[-1]] = cycle[0]
            perm = perm * Permutation(perm_dict)

        return self * perm

    def inverse(self):
        """ Создать обратную пермутацию. """
        perm_dict = {b: a for a, b in self._perm.items()}
        return Permutation(perm_dict)

    def __pow__(self, k: int):
        if k == 0:
            return Permutation()

        if k < 0:
            perm = self.inverse()
        else:
            perm = Permutation(self._perm)

        cum = Permutation()
        k = abs(k)
        while k > 0:
            k, e = divmod(k, 2)
            if e == 1:
                cum *= perm
            perm *= perm

        return cum

    def __truediv__(self, perm):
        return self * perm.inverse()

    def len(self) -> int:
        "Количество элементов которые затрагивает перестановка."
        return len(self._perm)

    def swaps(self):
        """ Представить пермутацию в виде произведения перестановок. """
        cycles = self.cycles()
        res = []
        for cycle in cycles:
            h = cycle[0]
            for x in cycle[1:]:
                pair = tuple(sorted((h, x)))
                res.append(pair)
        return res

    def __eq__(self, p) -> bool:
        if self.len() != p.len():
            return False
        for k, v in self._perm.items():
            try:
                if p._perm[k] != v:
                    return False
            except KeyError:
                return False
        return True

    def deg(self) -> int:
        """ Степень перестановки. Минимальная степень в которой перестановка
        будет равна единице."""
        cycles_deg = [len(c) for c in self.cycles()]
        return lcm(*cycles_deg)
