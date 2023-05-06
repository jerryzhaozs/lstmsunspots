from stanfordcorenlp import StanfordCoreNLP
#如果要用其他语言，需要单独设置
nlp = StanfordCoreNLP(r'C:\Users\Administrator\Desktop\dogcat\stanford-corenlp-4.5.4')
nlp_ch= StanfordCoreNLP(r'C:\Users\Administrator\Desktop\dogcat\stanford-corenlp-4.5.4', lang='zh')
sen='Hello I am AAA'
print(nlp_ch.pos_tag(sen))
print(nlp_ch.parse(sen))
