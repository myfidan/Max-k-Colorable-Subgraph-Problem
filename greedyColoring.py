from igraph import *

# COLORS
colorsli = ["#ff0000","#0000ff","#00ff00","#000000","#FF00CC","#CC6600","#FFFF00","#33FFCC","#FFFFFF","#555555","#663333","#863FF8"
    ,"#2F55DC","#4B9BCB","#43FF47","#6369FD","#FF3A97","#58F719","#0B13F0","#D2DF94","#C94667","#6CB81E","#17E9D3","#34B703","#6FC0BF"]

def remove_edge(g,i,j):
    g.delete_edges([(i,j)])

def find_max_adj(g2,deletedOne):
    max = 0
    index = 0
    for i in g2.neighbors(deletedOne):
        length = len(g2.neighbors(i))
        if(length > max):
            max = length
            index = i
    return index

def greedy_graph_coloring(graph):
    global colorsli
    global currentMaxColor
    
    color_list = [""] * graph.vcount()  # Color list
    

    color_list[0] = colorsli[currentMaxColor]
    currentMaxColor += 1

    for i in range(1,graph.vcount()):
        ## get next vertices adj vertices and check first available color
        adjVertices = graph.neighbors(i)
        for j in range(0,len(colorsli)): ## This is constant time
            if(j+1 > currentMaxColor):
                currentMaxColor += 1
            flag = True
            
            for k in adjVertices:
                if(color_list[k] == colorsli[j]):
                    flag = False
                    break
            if(flag):
                color_list[i] = colorsli[j]
                break
    
    return color_list

g2 = Graph.GRG(10, 0.5)
layout2 = g2.layout("kk")
print(g2.get_adjacency())
k = int(input("Enter k colorable value:"))
print("Start edge count : "+ str(g2.ecount()))
colors = []
currentMaxColor = 0

while(True):

    currentMaxColor = 0
    colors = greedy_graph_coloring(g2)
    #print(currentMaxColor)
    if(k >= currentMaxColor):
        break
    else:
        maxDeg_vertex_index = 0
        maxDegree = 0
        for i in range(g2.vcount()):
            if(g2.degree(i) > maxDegree):
                maxDegree = g2.degree(i)
                maxDeg_vertex_index = i
        remove_edge(g2,maxDeg_vertex_index,find_max_adj(g2,maxDeg_vertex_index))



print("End edge count : "+ str(g2.ecount()))
plot(g2,layout=layout2,vertex_color=colors)
