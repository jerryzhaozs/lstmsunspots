import math
from grammar import Pcfg


class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar):
        """
        Initialize a new parser instance from a grammar. 
        """
        self.grammar = grammar

    def parse_with_backpointers(self, tokens):
        """
        Parse the input tokens and return a parse table and a probability table.
        """
        n = len(tokens)
        pi = dict()  # Initialzie the backpointers table
        probs = dict()  # Initialzie the probabilities table
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                pi[(i, j)] = dict()
                probs[(i, j)] = dict()

        for i, word in enumerate(tokens):
            for key, values in self.grammar.rhs_to_rules.items():
                # key: 包含终结符的一元数组，例如('friday',)，或包含两个非终结符的二元数组('FRIDAY','AFTERNOON')
                # values: 对给定BC，有规则A1->BC，A2->BC，则values的值为[(A1,(B,C),p1),(A2,(B,C),P2)]，对给定非终极符a，有规则A1->a，A2->a，则values的值为[(A1,(a,),p1),(A2,(a,),p2)]。p为统计得到的该规则使用的概率
                if word == key[0]:
                    for items in values:
                        pi[(i, i + 1)][items[0]] = word
                        probs[(i, i + 1)][items[0]] = math.log(items[2])    # 概率取对数，将乘法运算改变为加法

        # for length=2…n:
        #     for i=0…(n-length):
        #         j = i + length
        #         for k=i+1…j-1:
        #             for A ∈ N:
        #               M={A|A->BC∈R and B ∈ pi[i,k] and C∈ pi[k,j]
        #               pi[i,j]=pi[i,j] union M
        #                   ---or (put probability into consideration)---
        #               pi[i,j,A] = max P(A->BC)*pi[i,k,B]*pi[k,j,C]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length
                for k in range(i + 1, j):
                    for key, values in self.grammar.rhs_to_rules.items():   # 遍历推理规则的集合，确定现在观察的一对输入能否被规约
                        for B in pi[(i, k)]:
                            for C in pi[(k, j)]:
                                if key[0] == B and key[1] == C:  # A->BC∈R，找到了推理规则可以规约正观察的词
                                    for items in values:
                                        probability = math.log(items[2]) + probs[(i, k)][B] + probs[(k, j)][C]
                                        if items[0] in pi[(i, j)]:  # 若在决策表的ij处已记录了一种方法
                                            #任务：在决策表pi的ij处记录概率最大的规约方法，在表probs的ij处记录最大概率
                                            #********** Begin **********#
                                            if probability > probs[(i, j)][items[0]]:
                                                pi[(i, j)][items[0]] = ((key[0], i, k), (key[1], k, j))
                                                probs[(i, j)][items[0]] = probability
                                            #**********  End  **********#
                                        else:
                                            pi[(i, j)][items[0]] = ((key[0], i, k), (key[1], k, j))  # pi[i,j]= M
                                            probs[(i, j)][items[0]] = probability
        return pi, probs


def get_tree(chart, i, j, nt):
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
    if type(chart[(i, j)][nt]) == str:
        return (nt, chart[(i, j)][nt])
    left_child = chart[(i, j)][nt][0]
    right_child = chart[(i, j)][nt][1]
    return (nt, (get_tree(chart, left_child[1], left_child[2], left_child[0])),
            (get_tree(chart, right_child[1], right_child[2], right_child[0])))


# if __name__ == "__main__":
#     with open('/data/workspace/myshixun/src/atis3.pcfg', 'r') as grammar_file:
#         grammar = Pcfg(grammar_file)
#         parser = CkyParser(grammar)
#         toks = ['flights', 'from', 'miami', 'to', 'cleveland', '.']
#         table, probs = parser.parse_with_backpointers(toks)
#         tree = get_tree(table, 0, len(toks), grammar.startsymbol)  # dynamic programming
#         print(tree)
        # ('TOP', ('NP', ('NP', 'flights'), ('NPBAR', ('PP', ('FROM', 'from'), ('NP', 'miami')), ('PP', ('TO', 'to'), ('NP', 'cleveland')))), ('PUN', '.'))
