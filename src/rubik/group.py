from typing import List, Optional, Tuple
from copy import deepcopy
from itertools import combinations, product
from rubik.permutation import Permutation
from rubik.state import Rubik
from rubik.coloring import Color
from tqdm import tqdm


O = Rubik().act(Color.O).permutation(subgroup='vertex')
B = Rubik().act(Color.B).permutation(subgroup='vertex')
Y = Rubik().act(Color.Y).permutation(subgroup='vertex')
W = Rubik().act(Color.W).permutation(subgroup='vertex')
G = Rubik().act(Color.G).permutation(subgroup='vertex')
R = Rubik().act(Color.R).permutation(subgroup='vertex')
E = Permutation()

VERTEX_GEN_PERMUTATION = {
    'O': Rubik().act(Color.O).permutation(subgroup='vertex'),
    'B': Rubik().act(Color.B).permutation(subgroup='vertex'),
    'Y': Rubik().act(Color.Y).permutation(subgroup='vertex'),
    'W': Rubik().act(Color.W).permutation(subgroup='vertex'),
    'G': Rubik().act(Color.G).permutation(subgroup='vertex'),
    'R': Rubik().act(Color.R).permutation(subgroup='vertex'),
}


Lexica = dict[str, Permutation]
Swap = Tuple[int, int]


def word_simplify_4_deg(word):
    """ Удалить 4-буквенные повторения из слова. """
    n = len(word)
    gens = ['O', 'B', 'Y', 'W', 'G', 'R']
    gens = list(VERTEX_GEN_PERMUTATION)

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
    """ Вычислить слова всех двойных перестановок вершин. """

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

    res_col = deepcopy(VERTEX_GEN_PERMUTATION)
    for col, p in deepcopy(VERTEX_GEN_PERMUTATION).items():
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
    """ Подгруппа перестановок вершин. """

    def __init__(self):
        self.colors = VERTEX_GEN_PERMUTATION
        self.helpers = rubik_double_swaps()

    def word2permutation(self, word: str) -> Permutation:
        """ Вычислить перестановку по слову. """
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
        """ Вычислить слово по перестановке. """
        res_word = ''
        swaps_list = perm.swaps()

        if len(swaps_list) % 2 != 0:
            # perm нечетная перестановка. Домножаем ее на нечетную перестановку
            # O, чтобы итог получился четным.
            swaps_list = (perm * self.colors['O']).swaps()
            res_word = 'O'

        while len(swaps_list) > 1:
            left = swaps_list[-2]
            right = swaps_list[-1]
            word = self.word_eliminating_pair(left, right)
            res_word = word_simplify_4_deg(res_word + word)
            swaps_list = swaps_list[:-2]

        return res_word

if __name__ == '__main__':

    rdw = rubik_double_swaps()

    OE = Permutation().apply_cycle([9, 20, 13, 17])
    BE = Permutation().apply_cycle([9, 10, 11, 12])
    YE = Permutation().apply_cycle([10, 17, 14, 18])
    RE = Permutation().apply_cycle([11, 18, 15, 19])
    WE = Permutation().apply_cycle([12, 19, 16, 20])
    GE = Permutation().apply_cycle([13, 16, 15, 14])

    o = O * OE
    b = B * BE
    y = Y * YE
    r = R * RE
    w = W * WE
    g = G * GE

    act = {'O': o, 'B': b, 'Y': y, 'R': r, 'W': w, 'G': g}

    def word(ws: str) -> Permutation:
        p = Permutation()
        for w in ws:
            w = w.upper()
            p *= act[w]
        return p

    # d_words = dict()
    # for a, c in product(act, act):
    #     ws = a + c
    #     p = word(ws)
    #     if p.deg() % 5 == 0:
    #         print(ws, ':', p ** 3)
    #         d_words[ws.lower()] = p

    def dim(xs, n):
        return product(*[xs for _ in range(n)])

    # for arr in dim(act, 5):
    #     ws = ''
    #     p = Permutation()
    #     for w in arr:
    #         ws += w
    #         p *= act[w]

    #     print(ws, p)

    def l2wp(arr: List[str]) -> (str, Permutation):
        ws = ''
        p = Permutation()
        for w in arr:
            ws += w
            p *= act[w]
        return ws, p

    # d_7_dict = dict()
    # d_5_dict = dict()
    # for arr in dim(act, 5):
    #     w, p = l2wp(arr)
    #     if p.deg() % 7 == 0:
    #         d_7_dict[w] = p
    #     if p.deg() % 5 == 0:
    #         d_5_dict[w] = p

    # l_7 = len(d_7_dict)
    # l_5 = len(d_5_dict)
    # print(f'7: {l_7} and 5: {l_5}')

    # for w1, w2 in product(d_7_dict, d_5_dict):
    #     ws = w1 + w2
    #     p = d_7_dict[w1] * d_5_dict[w2]
    #     q = p * p
    #     if q.deg() == 3 and len(q.cycles()) == 1:
    #         print('->', ws, p)

    #     ws = w2 + w1
    #     p = d_5_dict[w2] * d_7_dict[w1]
    #     q = p * p
    #     if q.deg() == 3 and len(q.cycles()) == 1:
    #         print('<-', ws, p)

    un = set()
    for arr in tqdm(dim(act, 12), total=6**12):
        w, p = l2wp(arr)
        q = p ** 1
        if q.len() == 3:
            print(w, q)
            c = q.cycles()[0]
            c.sort()
            tup = tuple(c)
            if tup[0] > 0:
                un.add(tup)

    # un = set()
    # with open('actions_lib', 'r') as f:
    #     for ws in f:
    #         ws = ws.strip()
    #         p = word(ws)
    #         q = p ** 2
    #         c = q.cycles()[0]
    #         c.sort()
    #         tup = tuple(c)
    #         if tup[0] > 8:
    #             un.add(tup)

    # print("search unknow elem") 
    # for t in combinations(range(9, 21), 3):
    #     if t in un:
    #         continue
    #     print('unknown', t)
