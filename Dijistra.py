def Dijistra(sNode, dNode, adjacencyMatrix):
    path = []  
    n = len(adjacencyMatrix) 
    fmax = 999
    w = [[0 for i in range(n)] for j in range(n)]  
    book = [0 for i in range(n)]  
    dis = [fmax for i in range(n)] 
    book[sNode] = 1
    midpath = [-1 for i in range(n)]  
    for i in range(n):
        for j in range(n):
            if adjacencyMatrix[i][j] != 0:
                w[i][j] = adjacencyMatrix[i][j]
            else:
                w[i][j] = fmax
            if i == sNode and adjacencyMatrix[i][j] != 0:
                dis[j] = adjacencyMatrix[i][j]  
    for i in range(n - 1): 
        min = fmax
        u = 0
        for j in range(n):
            if book[j] == 0 and dis[j] < min:
                min = dis[j]
                u = j
        book[u] = 1
        for v in range(n):  
            if dis[v] > dis[u] + w[u][v]:
                dis[v] = dis[u] + w[u][v]
                midpath[v] = u  
    j = dNode 
    path.append(dNode)  

    while (midpath[j] != -1):
        path.append(midpath[j])
        j = midpath[j]
    path.append(sNode)
    path.reverse()  
    return path, dis[dNode]
# adjacencyMatrix=[[0, 1, 1, 0, 0, 0],
#             [0, 0, 1, 1, 0, 0],
#             [0, 0, 0, 0, 1, 0],
#             [0, 0, 1, 0, 1, 1],
#             [0, 0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0, 0]]
# path, dis = DijkstraRoad(0,3,adjacencyMatrix)
# print(path)
# print(dis)

def caculate_all(sNode, dNode, a):
    friend=[]
    for i in range(len(a[sNode])):
        if a[sNode][i]!=0:
            friend.append(i)
    
    num=0
    for item in friend:
        if a[dNode][item]!=0:
            num+=1
    
    return num
            