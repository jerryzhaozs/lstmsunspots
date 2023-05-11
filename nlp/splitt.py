import re

def split_sentences(text):
    """
    Split English sentences by using re.
    """
    # define punctuation marks
    punctuations = ['!', '.', '?']
    
    # define exceptions to sentence endings
    exceptions = ['Mr.', 'Mrs.', 'Dr.', 'Ms.', 'Inc.', 'Fig.', 'i.e.', 'e.g.', 'vs.', 'etc.']
    
    # define regex pattern
    pattern = "(?<!\S)(" + '|'.join(exceptions) + "|[\w\s'\"]+)(?:" + '|'.join(punctuations) + ")(?!\w)"
    
    # split text
    sentences = re.findall(pattern, text)
    return [sentence.strip() for sentence in sentences]

text = "Water-splashing Festival is one of the most important festivals in the world, which is popular among Dai people of China and the southeast Asia. It has been celebrated by people for more than 700 years and now this festival is an necessary way for people to promote the cooperation and communication among countries."

print(split_sentences(text))