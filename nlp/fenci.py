import requests
import json

# 调用Stanford CoreNLP API接口进行句法分析
def stanford_parse(text):
    url = 'http://localhost:9000/?properties={"annotators":"parse","outputFormat":"json"}'
    data = text.encode('utf-8')
    r = requests.post(url, data=data)
    result = r.text
    return json.loads(result)

# 提取复杂句的句法结构
def extract_syntax(parse):
    syntax = []
    tokens = parse['sentences'][0]['tokens']
    dependencies = parse['sentences'][0]['enhancedPlusPlusDependencies']
    for dep in dependencies:
        if dep['dep'] != "ROOT":
            source = tokens[dep['governor']-1]
            target = tokens[dep['dependent']-1]
            syntax.append((source['word'], source['pos'], dep['dep'], target['word'], target['pos']))
    return syntax

# 测试代码
text = "Although he is very rich, he lives a simple life."
parse = stanford_parse(text)
syntax = extract_syntax(parse)
print(syntax)
