from turtle import color
from igraph import *


g = Graph()
g.add_vertices(5)
g.add_edges([(0,1),(0,2),(1,4),(4,3),(1,3),(0,4)])
layout = g.layout("kk")

uncolored_vertex_list = []  # first: vertex num, second: vertex degree
colored_vertex_list = []

# COLORS
colorsli = ["#ff0000","#0000ff","#00ff00","#000000","#FF00CC","#CC6600","#FFFF00","#33FFCC","#FFFFFF","#555555","#663333","#863FF8"
    ,"#2F55DC","#4B9BCB","#43FF47","#6369FD","#FF3A97","#58F719","#0B13F0","#D2DF94","#C94667","#6CB81E","#17E9D3","#34B703","#6FC0BF"]
colorid = 0

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

def create_vertex_degree_list(g,vertex_degree_list):
    index = 0
    for i in g.vs.degree():
        vertex_degree_list.append([index,i,0])
        index += 1


def plot_graph(g,layout,color_list):
    plot(g,layout=layout,vertex_color=color_list)

def sortAccordingSatur(uncList):
    uncolored_vertex_list = sorted(uncList,key=lambda x: (x[2],x[1]),reverse = True)
    return uncolored_vertex_list

def dsatur_algo(g,uncolored_vertex_list,colorsli):
    global color_list
    global colorid
    uncolored_vertex_list = []
    returnMaxDegree = []
    create_vertex_degree_list(g,uncolored_vertex_list)
    count = 0
    while(len(uncolored_vertex_list) > 0):
        uncolored_vertex_list = sortAccordingSatur(uncolored_vertex_list)
        colorThisVertex = uncolored_vertex_list[0]
        if(count == 0):
            returnMaxDegree = uncolored_vertex_list[0].copy()
            count += 1
        #print(uncolored_vertex_list)
        ## Find adj vertices to colored one
        index = 0
        adj = []
        for i in g.vs():
            if(g.are_connected(colorThisVertex[0],index) and index != colorThisVertex[0]):
                adj.append(index)
            index += 1
        #print(adj)


        ## Find color
        color = ""
        for i in colorsli:
            flag = True
            for j in adj:
                if(color_list[j] == i):
                    flag= False
                    break
            if(flag):
                color = i
                break
        #print(color) 
        ## give its color
        color_list[colorThisVertex[0]] = color    

        ## recalculate its adj saturs.
        for i in adj:
            ind = -1
            if(color_list[i] == ""):
                ind = 0
                for j in uncolored_vertex_list:
                    if(j[0] == i):
                        break
                    ind += 1
            
            if(ind != -1):        
                uncolored_vertex_list[ind][2] += 1   
        print(uncolored_vertex_list)
        uncolored_vertex_list.pop(0)      
    colorid = len(set(color_list))
    return returnMaxDegree

#plot_graph(g,layout,["red"])
g2 = Graph.GRG(10, 10)
layout2 = g2.layout("kk")

k = int(input("Enter k colorable value:"))
print("Start edge count : "+ str(g2.ecount()))
plot(g2,layout=layout2)

while(True):
    color_list = [""] * g2.vcount()  # Color list
    maxDegVer = dsatur_algo(g2,uncolored_vertex_list,colorsli)
    ## Check k colorable now
    if(colorid <= k):
        ## if yes we have an answer
        break
    else:
        
        ## if not remove an edge from max degree and back to loop
        remove_edge(g2,maxDegVer[0],find_max_adj(g2,maxDegVer[0]))

plot_graph(g2,layout2,color_list)
print("End edge count : "+ str(g2.ecount()))