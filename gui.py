from asyncio.windows_events import NULL
import sys
from tokenize import Double
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QLabel,QFrame,QComboBox,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from igraph import *
from threading import Thread
import time

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Max K Colorable Subgraph Problem'
        self.left = 600
        self.top = 350
        self.width = 400
        self.height = 600
        self.g2 = NULL
        self.layout2 = NULL
        
        self.g3 = NULL
        self.k = 1
        self.colorsli = ["#ff0000","#0000ff","#00ff00","#000000","#FF00CC","#CC6600","#FFFF00","#33FFCC","#FFFFFF","#555555","#663333","#863FF8"
                        ,"#2F55DC","#4B9BCB","#43FF47","#6369FD","#FF3A97","#58F719","#0B13F0","#D2DF94","#C94667","#6CB81E","#17E9D3","#34B703","#6FC0BF","#1F374C",
                        "#5CDBFF","#7AD06D","#A26F55","#58169E","#CCEA28","#B3EAA8","#B5EC06"]
        self.currentMaxColor = 0
        self.colors = []

        ## DSatur
        self.colorid= 0
        self.color_list = NULL
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        ## Create "Number of Vertex" text
        self.text1 = QLabel("Number of Vertex:",self)
        self.text1.move(20,20)
        # Create textbox
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(140, 20)
        self.textbox1.resize(240,30)

        ## Create "Graph Density:" text
        self.text2 = QLabel("Graph Density:",self)
        self.text2.move(20,70)
        
        ## Create graph density textbox
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(140, 70)
        self.textbox2.resize(240,30)

        # Create a button in the window
        self.button = QPushButton('Create Input Graph', self)
        self.button.move(140,120)
        self.button.resize(240,30)

        ## Create button for plot input graph
        self.button2 = QPushButton('Show Input Graph',self)
        self.button2.move(140,160)
        self.button2.resize(240,30)

        
        
        ## Draw line
        self.line1 = QFrame(self)
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setLineWidth(1)
        self.line1.move(20,200)
        self.line1.resize(360,1)

        ## Create Color K value text
        self.text3 = QLabel("K Colorable Value:",self)
        self.text3.move(20,210)
        ## Create k value Textbox
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(140, 210)
        self.textbox3.resize(240,30)

        ## Create Choose algorithm text
        self.text4 = QLabel("Choose Algorithm:",self)
        self.text4.move(20,260)

        ## Create select algorithm panel
        self.combo = QComboBox(self)
        self.combo.addItem("DSatur Algorithm")
        self.combo.addItem("Greedy Algorithm")
        self.combo.move(140,260)
        self.combo.resize(240,30)

        ## Create button for create output graph
        self.button3 = QPushButton('Create Output Graph',self)
        self.button3.move(140,310)
        self.button3.resize(240,30)

        ## Create button for show output graph
        self.button4 = QPushButton('Show Output Graph',self)
        self.button4.move(140,350)
        self.button4.resize(240,30)

        ## Output Text
        self.text5 = QLabel("Output Terminal:",self)
        self.text5.move(20,385)

        ## Create output screen

        self.outputScreen = QTextEdit(self)
        self.outputScreen.move(20,415)
        self.outputScreen.resize(360,160)

        # connect button to function on_click
        self.button.clicked.connect(self.create_input_graph)  ## CREATE INPUT GRAPH
        self.button2.clicked.connect(self.show_input_graph)   ## PLOT INPUT GRAPH
        self.button3.clicked.connect(self.create_output_graph)
        self.button4.clicked.connect(self.show_output_graph)

        self.show()
    
    ## This just create input graph
    @pyqtSlot()
    def create_input_graph(self):
        vertex_count = int(self.textbox1.text())
        graph_density = float(self.textbox2.text())
        print(vertex_count)
        print(graph_density)
        self.textbox1.setText("")
        

        self.g2 = Graph.GRG(vertex_count, graph_density)
        self.layout2 = self.g2.layout("kk")
        
        self.outputScreen.setText("A graph has "+ str(vertex_count) +" vertices and " + str(self.g2.ecount())+" edges created.")
        #print("Start edge count : "+ str(self.g2.ecount()))
        #plot(self.g2,layout=self.layout2)


        #textboxValue = self.textbox1.text()
        #QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        #self.textbox1.setText("")

    @pyqtSlot()
    def show_input_graph(self):
        print("Start edge count : "+ str(self.g2.ecount()))
        t1 = Thread(target=self.plotting_input)
        t1.start()
        #plot(self.g2,layout=self.layout2)
        
    
    @pyqtSlot()
    def show_output_graph(self):
        if(self.combo.currentText() == "Greedy Algorithm"):
            plot(self.g3,layout=self.layout2,vertex_color = self.colors)
        else:
            plot(self.g3,layout=self.layout2,vertex_color = self.color_list)
    def plotting_input(self):
        plot(self.g2,layout=self.layout2)

    @pyqtSlot()
    def create_output_graph(self):
        start_time = time.time()
        if(self.combo.currentText() == "Greedy Algorithm"):
            self.k = int(self.textbox3.text())
            self.g3 = self.g2.copy() 
            self.colors = []
            self.currentMaxColor = 0
            while(True):

                self.currentMaxColor = 0
                self.colors = self.greedy_graph_coloring()
                #print(currentMaxColor)
                if(self.k >= self.currentMaxColor):
                    break
                else:
                    maxDeg_vertex_index = 0
                    maxDegree = 0
                    for i in range(self.g3.vcount()):
                        if(self.g3.degree(i) > maxDegree):
                            maxDegree = self.g3.degree(i)
                            maxDeg_vertex_index = i
                    self.remove_edge(self.g3,maxDeg_vertex_index,self.g3.neighbors(maxDeg_vertex_index)[0])    
        else:
            self.g3 = self.g2.copy() 
            self.k = int(self.textbox3.text())
            while(True):
                
                self.color_list = [""] * self.g3.vcount()  # Color list
                maxDegVer = self.dsatur_algo()
                ## Check k colorable now
                if(self.colorid <= self.k):
                    ## if yes we have an answer
                    break
                else:
                    
                    ## if not remove an edge from max degree and back to loop
                    self.remove_edge(self.g3,maxDegVer[0],self.find_max_adj(self.g3,maxDegVer[0]))
        self.outputScreen.setText("A solution has found.\nEdge Count: "+ str(self.g3.ecount())+"\nVertex count: "+ str(self.g3.vcount()) + "\n"+ str(self.g2.ecount()-self.g3.ecount())+" edges removed" +
        "\nTime: "+ str((time.time() - start_time)))
        
    def remove_edge(self,g,i,j):
        g.delete_edges([(i,j)])


    def find_max_adj(self,g2,deletedOne):
        max = 0
        index = 0
        for i in g2.neighbors(deletedOne):
            length = len(g2.neighbors(i))
            if(length > max):
                max = length
                index = i
        return index


    ## MAX K COLORABLE SUBGRAPH ALGORITHMS
    def greedy_graph_coloring(self):
        
        color_list = [""] * self.g3.vcount()  # Color list
        

        color_list[0] = self.colorsli[self.currentMaxColor]
        self.currentMaxColor += 1

        for i in range(1,self.g3.vcount()):
            ## get next vertices adj vertices and check first available color
            adjVertices = self.g3.neighbors(i)
            for j in range(0,len(self.colorsli)): ## This is constant time
                if(j+1 > self.currentMaxColor):
                    self.currentMaxColor += 1
                    if(self.currentMaxColor > self.k):
                        return [-1]
                flag = True
                
                for z in adjVertices:
                    if(color_list[z] == self.colorsli[j]):
                        flag = False
                        break
                if(flag):
                    color_list[i] = self.colorsli[j]
                    break
        
        return color_list

    def dsatur_algo(self):
        uncolored_vertex_list = []
        returnMaxDegree = []
        self.create_vertex_degree_list(uncolored_vertex_list)
        count = 0
        while(len(uncolored_vertex_list) > 0):
            uncolored_vertex_list = self.sortAccordingSatur(uncolored_vertex_list)
            colorThisVertex = uncolored_vertex_list[0]
            if(count == 0):
                returnMaxDegree = uncolored_vertex_list[0].copy()
                count += 1
            #print(uncolored_vertex_list)
            ## Find adj vertices to colored one
            index = 0
            adj = []
            for i in self.g3.vs():
                if(self.g3.are_connected(colorThisVertex[0],index) and index != colorThisVertex[0]):
                    adj.append(index)
                index += 1
            #print(adj)


            ## Find color
            color = ""
            for i in self.colorsli:
                flag = True
                for j in adj:
                    if(self.color_list[j] == i):
                        flag= False
                        break
                if(flag):
                    color = i
                    break
            #print(color) 
            ## give its color
            self.color_list[colorThisVertex[0]] = color    

            ## recalculate its adj saturs.
            for i in adj:
                ind = -1
                if(self.color_list[i] == ""):
                    ind = 0
                    for j in uncolored_vertex_list:
                        if(j[0] == i):
                            break
                        ind += 1
                
                if(ind != -1):        
                    uncolored_vertex_list[ind][2] += 1   
            #print(uncolored_vertex_list)
            uncolored_vertex_list.pop(0)      
        self.colorid = len(set(self.color_list))
        return returnMaxDegree

    
    def create_vertex_degree_list(self,vertex_degree_list):
        index = 0
        for i in self.g3.vs.degree():
            vertex_degree_list.append([index,i,0])
            index += 1

    
    def sortAccordingSatur(self,uncList):
        uncolored_vertex_list = sorted(uncList,key=lambda x: (x[2],x[1]),reverse = True)
        return uncolored_vertex_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
