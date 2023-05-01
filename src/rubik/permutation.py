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

        key_list = list(arr.keys())
        if len(key_list) != len(set(key_list)):
            return False

        val_list = list(arr.values())
        return len(val_list) == len(set(val_list))

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

    def apply_cycle(self, *cycles):
        perm = Permutation()
        for cycle in cycles:
            perm_dict = {a: b for a, b in zip(cycle, cycle[1:])}
            perm_dict[cycle[-1]] = cycle[0]
            perm = perm * Permutation(perm_dict)

        return self * perm

    def inverse(self):
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
        return len(self._perm)

    def swaps(self):
        cycles = self.cycles()
        res = []
        for cycle in cycles:
            h = cycle[0]
            for x in cycle[1:]:
                pair = tuple(sorted((h, x)))
                res.append(pair)
        return res


O = Permutation().apply_cycle([1, 2, 3, 4])     # noqa: E741
B = Permutation().apply_cycle([1, 5, 6, 2])
Y = Permutation().apply_cycle([1, 4, 8, 5])
W = Permutation().apply_cycle([3, 2, 6, 7])
G = Permutation().apply_cycle([4, 3, 7, 8])
R = Permutation().apply_cycle([5, 8, 7, 6])
E = Permutation()

Lexica = dict[str, Permutation]
Swap = Tuple[int, int]


def word_simplify_4_deg(word):
    n = len(word)
    gens = ['O', 'B', 'Y', 'W', 'G', 'R']

    def simplify(word):
        for w in gens:
            word = word.replace(f'{w}{w}{w}{w}', '')
        return word

    word_ = simplify(deepcopy(word))
    while len(word_) < n:
        n = len(word_)
        word_ = simplify(word_)

    return word_


def rubik_double_swaps() -> dict[Swap, dict[Swap, str]]:

    colors = {'O': O, 'B': B, 'Y': Y, 'W': W, 'G': G, 'R': R}

    def simplify_colors(colors: Lexica) -> Lexica:
        res = dict()
        for word, p in colors.items():
            word_ = word_simplify_4_deg(word)
            res[word_] = p
        return res

    def congugate(colors: Lexica) -> Lexica:
        res = deepcopy(colors)
        for col_1, p in colors.items():
            for col_2, q in colors.items():
                base_word = col_1 + col_2 + col_1
                res[col_1 + col_1 + base_word] = E / p * q * p
                res[base_word + col_1 + col_1] = p * q / p
        return simplify_colors(res)

    res_col = deepcopy(colors)
    for col, p in deepcopy(colors).items():
        word = ''.join([3 * x for x in col[::-1]])
        word = word_simplify_4_deg(word)
        res_col[word] = p.inverse()

    res_col = congugate(res_col)
    res_col = congugate(res_col)

    # По построению все перестановки в colors имеют степень 4 потому, что все
    # начальные перестановки имели степень 4, а новые слова мы создавали
    # сопряжением.

    mat = {pair: dict() for pair in combinations(range(1, 9), 2)}
    for w, p in res_col.items():
        cycle = p.cycles()
        a, b, c, d = cycle[0]
        ac = tuple(sorted([a, c]))
        bd = tuple(sorted([b, d]))
        word = word_simplify_4_deg(w + w)
        prew_word = mat[ac].get(bd)
        if prew_word is None or len(prew_word) > len(word):
            mat[ac][bd] = word
            mat[bd][ac] = word

    return mat


class RubikSmallGroup:
    def __init__(self):
        self.colors = {'O': O, 'B': B, 'Y': Y, 'W': W, 'G': G, 'R': R}
        self.helpers = rubik_double_swaps()

    def word2permutation(self, word: str) -> Permutation:
        perm = Permutation()
        for w in word:
            if w not in self.colors:
                raise ValueError(f"Word {word} isn't correct.")
            perm *= self.colors[w]
        return perm

    def word_eliminating_pair(self, left: Swap, right: Swap) -> str:
        """ Вернуть слово обратное к перестановке из двух свопов. """

        s1 = set(left)
        s2 = set(right)

        if not s1 & s2:
            # Если не пересекаются, значит коммутируют.
            return self.helpers[right][left]

        eight = set([i for i in range(1, 9)])
        points = list(eight - (s1 | s2))
        pair = tuple(sorted([points[0], points[1]]))

        # Движения к состоянию применяются справа на лево, поэтому сперва идет
        # правое слово, потом левое.
        right_ = tuple(sorted(right))
        left_ = tuple(sorted(left))
        word = self.helpers[right_][pair] + self.helpers[left_][pair]
        return word_simplify_4_deg(word)

    def permutation2word(self, perm: Permutation) -> str:
        res_word = ''
        swaps_list = perm.swaps()

        if len(swaps_list) % 2 != 0:
            # perm нечетная перестановка. Домножаем ее на нечетную перестановку
            # O, чтобы итог получился четным.
            swaps_list = (perm * O).swaps()
            res_word = 'O'

        while len(swaps_list) > 1:
            left = swaps_list[-2]
            right = swaps_list[-1]
            word = self.word_eliminating_pair(left, right)
            res_word = word_simplify_4_deg(res_word + word)
            swaps_list = swaps_list[:-2]

        return res_word


if __name__ == '__main__':

    mat = rubik_double_swaps()
    print(mat[(1, 7)])
