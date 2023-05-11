def minDistance(word1, word2):
    n = len(word1)
    m = len(word2)
    
    # 有一个字符串为空串
    if n * m == 0:
        return n + m
    
    # DP 数组
    D = [ [0] * (m + 1) for _ in range(n + 1)]
    
    # 边界状态初始化
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    
    ######## Begin ########
    for i in range(1, n+1):
        for j in range(1, m+1):
            if word1[i-1] == word2[j-1]:  # 如果当前字符相等
                D[i][j] = D[i-1][j-1]  # 则最小编辑距离不变
            else:
                D[i][j] = min(D[i-1][j], D[i][j-1], D[i-1][j-1]) + 1  # 否则取替换、删除、插入中的最小值，并加一
    ######## End ########
    return D[n][m]

s1 = input()
s2 = input()
ans = minDistance(s1, s2)
print(ans)