import jieba
import pickle

with open('C:\\Users\\Administrator\\Desktop\\sys\\server\\emotion\\lreg.pkl', 'rb') as f:
    lreg = pickle.load(f)
with open('C:\\Users\\Administrator\\Desktop\\sys\\server\\emotion\\tfidf_vectorizer.pkl', 'rb') as f:
    fitted_tfidf_vectorizer = pickle.load(f)

def getEmotion(a):
    b=jieba.lcut(a)
    c=''
    for i in b:
        c+=i
        c+=' '
    d=[]
    d.append(c)
    x_input=fitted_tfidf_vectorizer.transform(d)
    p=lreg.predict(x_input)
    if p==0:
        return '喜悦'
    elif p==1:
        return '愤怒'
    elif p==2:
        return '厌恶'
    else:
        return '低落'

# print(getEmotion('岂有此理，我还从来没见过这么嚣张的人呢'))