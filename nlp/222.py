from nltk.parse.stanford import StanfordDependencyParser
from nltk.tree import Tree
from stanfordcorenlp import StanfordCoreNLP
import jieba
# 中文依存句法分析  https://corenlp.run/
test = "他感受到了中国经济发展的大潮"
res = jieba.lcut(test)
chi_parser=StanfordDependencyParser(r"E:\stanford-parser-full-2018-02-27\stanford-parser.jar",  r"E:\stanford-parser-full-2018-02-27\stanford-parser-3.9.1-models.jar",                                    r"E:\stanford-parser-full-2018-02-27\stanford-parser-3.9.1-models\edu\stanford\nlp\models\lexparser\chinesePCFG.ser.gz")
result = list(chi_parser.parse(res))
for row in result[0].triples():
    print(row)
with StanfordCoreNLP(r'E:\stanford-corenlp-full-2018-02-27', lang='zh') as nlp:
    Tree.fromstring(nlp.parse(test)).draw()