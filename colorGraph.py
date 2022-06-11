
from pickle import TRUE
import random
from turtle import color
from igraph import *

# COLORS
colorsli = ["#ff0000","#0000ff","#00ff00","#000000","#FF00CC","#CC6600","#FFFF00","#33FFCC","#FFFFFF","#555555","#663333","#863FF8"
    ,"#2F55DC","#4B9BCB","#43FF47","#6369FD","#FF3A97","#58F719","#0B13F0","#D2DF94","#C94667","#6CB81E","#17E9D3","#34B703","#6FC0BF"]
## Create graph
## add vertices and edges
def remove_edge(g,i,j):
    g.delete_edges([(i,j)])

g = Graph()
g.add_vertices(5)
g.add_edges([(0,1),(0,2),(1,4),(4,3),(1,3),(0,4)])
layout = g.layout("kk")
print(g.ecount())
print(g.neighbors(0))
remove_edge(g,0,1)
print(g.ecount())
print(g.neighbors(0))
print(g)


color_list = []  # Color list
colorid = 0
### imported variables for using while coloring graph
#g.vs["color"] ="-1"
#print(g.vs["color"])

#vertex_degree_list = []  # first: vertex num, second: vertex degree
#sortedVertexList = [] # sorted vertex list
#color_list = [""] * g.vcount()  # Color list
#colorsli = ["red","blue","green","black","purple"]
#colorid = 0

## Create 2d list with vertex number and its degree information
def create_vertex_degree_list(g,vertex_degree_list):
    index = 0
    for i in g.vs.degree():
        vertex_degree_list.append([index,i])
        index += 1

## After creating vertex_degree_list with its vertex number and degree information
## This function sort this 2d vertex degree list according to the its degree in decreasing order
def create_sorted_vertex_list(vertex_degree_list):
    sortedV = sorted(vertex_degree_list,key=lambda l:l[1], reverse=True) # Sort vertexes
    return sortedV

## This is the main algorithm for welsh powell coloring
## It takes my graph, sortedvertexlist(according to the vertices degrees), color_list
## colorsli and colorid. Then produce color_list.
## this color_list contains all color for all vertices
## for example color_list[0] gives first vertex color in our graph
def welsh_powell_coloring_algorithm(g,sortedVertexList):
    global colorsli
    global color_list
    global colorid
    while(len(sortedVertexList) > 0):
        currentSelectedVertexList = []
        index = 0
        for i in sortedVertexList:
            if(index == 0): #first elem
                currentSelectedVertexList.append(i)
            else:
                vertexNum = i[0]
                flag = True
                for j in currentSelectedVertexList:
                    if(g.are_connected(vertexNum,j[0])):
                        flag = False
                        break
                if(flag):
                    currentSelectedVertexList.append(i)        
            index += 1
        #print(currentSelectedVertexList)
        for i in currentSelectedVertexList:
            color_list[i[0]] = colorsli[colorid]

        colorid += 1    
        newList = [x for x in sortedVertexList if (x not in currentSelectedVertexList)]
        sortedVertexList = newList
    return colorid
## Remove selected vertices
#g.delete_edges([(0,1)])
#print(g.vs.degree())

## after creating color list this function basicly plot my graph
def plot_graph(g,layout,color_list):
    plot(g,layout=layout,vertex_color=color_list)

## Run welsh_powell_algorithm
def run_welsh_powell_algorithm(g,layout):
    global colorsli
    global colorid
    global color_list
    ## init variables
    vertex_degree_list = []  # first: vertex num, second: vertex degree
    sortedVertexList = [] # sorted vertex list
    color_list = [""] * g.vcount()  # Color list
    colorid = 0


    create_vertex_degree_list(g,vertex_degree_list)
    sortedVertexList = create_sorted_vertex_list(vertex_degree_list)
    print(sortedVertexList)
    colorCount = welsh_powell_coloring_algorithm(g,sortedVertexList)
    #print(str(colorCount) + " color used for graph coloring")
    #plot_graph(g,layout,color_list)
    return sortedVertexList[0] 
    
def find_max_adj(g2,deletedOne):
    max = 0
    index = 0
    for i in g2.neighbors(deletedOne):
        length = len(g2.neighbors(i))
        if(length > max):
            max = length
            index = i
    return index
## RUN ##
#run_welsh_powell_algorithm(g,layout)

#g.delete_edges([(1,4)])
#run_welsh_powell_algorithm(g,layout)
g2 = Graph.GRG(10, 10)
layout2 = g2.layout("kk")

k = int(input("Enter k colorable value:"))
print("Start edge count : "+ str(g2.ecount()))
plot(g2,layout=layout2)
## loop start
while(True):
    maxDegVer = run_welsh_powell_algorithm(g2,layout2)

    ## Check k colorable now
    if(colorid <= k):
        ## if yes we have an answer
        break
    else:
        
        ## if not remove an edge from max degree and back to loop
        remove_edge(g2,maxDegVer[0],find_max_adj(g2,maxDegVer[0]))

plot_graph(g2,layout2,color_list)
print("End edge count : "+ str(g2.ecount()))