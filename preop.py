from utils.vocab import Vocab

zh = 'zh_core_web_sm'
en = 'en_core_web_md'
zh_train = 'dataset/train.zh'
en_train = 'dataset/train.en'

zh_valid = 'dataset/valid.zh'
en_valid = 'dataset/valid.en'

zh_vocab = Vocab()
en_vocab = Vocab()

zh_vocab.create(zh_train, zh)
zh_vocab.create(zh_valid, zh)

en_vocab.create(en_train, en)
en_vocab.create(en_valid, en)

zh_vocab.save('dataset/zh_vocab.pkl')
en_vocab.save('dataset/en_vocab.pkl')