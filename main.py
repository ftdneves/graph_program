import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import Graph as graph


# aplicar funcao abre uma janela com o canvas duplicado e o grafico modificado (canvas so para display, caminho com cor diferente)
# fazer um manual ou label com os botoes que da pra usar
# nao pode criar dois caminhos mesma aresta
# canvas tamanho igual ao do frame
# save and open functions
# find closest is bugging: try to filter by tag or something

# save functions: define how i'm going to save the graph : FRED

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("PyGraph")
        #configuring and adding the menu bar
        menu=tk.Menu(self)
        file_menu=tk.Menu(menu,tearoff=0)
        file_menu.add_command(label="New file")
        file_menu.add_command(label="Open",command=self.choose_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save",command=self.save_file)
        file_menu.add_command(label="Save as...",command=self.save_as_file)
        menu.add_cascade(label="File",menu=file_menu)
        algorithm_menu=tk.Menu(menu,tearoff=0)
        algorithm_menu.add_command(label="Is Eulerian", command=self.draw_eulerian)
        algorithm_menu.add_command(label="Depth-first Search (DFS)", command=self.draw_dfs)
        algorithm_menu.add_command(label="Hamiltonian Circuit", command=self.draw_ham)
        algorithm_menu.add_command(label="Prim", command=self.draw_prim)
        menu.add_cascade(label="Algorithm",menu=algorithm_menu)
        menu.add_command(label="About",command=self.about)
        menu.add_command(label="Quit",command=self.quit)
        self.config(menu=menu)

        self.canvas = tk.Canvas(self, height=800, width=800, bg="white")
        frame = tk.Frame(self)

        # used for dragging vertices
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # variables
        self._graph = graph.Graph(0)
        self._edges = [] # contains reference for every edge created
        self._edgeText = dict()
        self._nodes = [] # contains reference for every node created
        self._nodeText = dict()
        self._leftEdges = dict() # used to update edge position on moving a vertex :: index = edge ref, value = node ref of the leftmost end of the edge
        self._rightEdges = dict() # used to update edge position on moving a vertex :: index = edge ref, value = node ref of the rightmost end of the edge
        self._node_count = -1
        self.line_start=None
        self._selectedEdge = None # reference for when you click an edge to edit its weight

        # binds

        # if double button to delete node glitches switch to keyboard
        #self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        #self.canvas.bind("<Key>", self.delete_node)

        self.canvas.bind("<Button-2>", self.draw_node)
        self.canvas.tag_bind("edge", "<ButtonPress-1>", self.open_edge_window)
        self.canvas.tag_bind("node", "<Double-Button-1>", self.delete_node)
        self.canvas.tag_bind("node", "<Button-3>", self.connect_node)
        self.canvas.tag_bind("node", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("node", "<B1-Motion>", self.on_token_motion)

        self.canvas.pack()
        frame.pack(fill=tk.BOTH)

    def generate_graph(self):
        for v in self._nodes:
            self._graph.addVertex()
        for e in self._edges:
            left = self._nodes.index(self._leftEdges[e]) # left node index
            right = self._nodes.index(self._rightEdges[e]) # right node index
            weight = int(self.canvas.gettags(e)[1])
            self._graph.addEdge(left, right, weight)
    
    def draw_eulerian(self):
        print("EULERIAN PATH WINDOW")

    def draw_dfs(self):
        print("DFS WINDOW canvas")

    def draw_ham(self):
        print("HAMILTON CYCLE WINDOW canvas")

    def draw_prim(self):
        self.primwindow = tk.Toplevel(self)
        self.primcanvas = tk.Canvas(self.primwindow, height=800, width=800, bg="white")
        self.primcanvas.pack()

        for id in self.canvas.find_all():
            item_type = self.canvas.type(id)
            position = self.canvas.coords(id)
            options = self.canvas.itemconfigure(id)

            if item_type == "text":
                self.primcanvas.create_text(position, options)
            elif item_type == "oval":
                self.primcanvas.create_oval(position, options)
            elif item_type == "line":
                self.primcanvas.create_line(position, options)

    #functions of the menubar
    def choose_file(self):
        filetypes=(("Plain text files","*.txt"),
                    ("All files", "*"))
        filename=fd.askopenfilename(title="Open file",
                initialdir="/",
                filetypes=filetypes)
        if filename:
            print(filename)

    def save_file(self):
        contents=self.text.get(1.0,tk.END)
        new_file=fd.asksaveasfile(title="Save file",
                    defaultextension=".txt",
                    filetypes=(("Text files","*.txt"),))
        if new_file:
            new_file.write(contents)
            new_file.close()

    def save_as_file(self):
        contents=self.text.get(1.0,tk.END)
        new_file=fd.asksaveasfilename(title="Save file as",
                    defaultextension=".txt",
                    filetypes=(("Text files","*.txt"),))
        if new_file:
            new_file.write(contents)
            new_file.close()

    def quit(self):
        if messagebox.askyesno('Quit','Do you really want to quit?'):
            self.destroy()

    def about(self):
        messagebox.showinfo("PyGraph","\n PyGraph \n\n\n Version: 1.0 \n Github: https://github.com/ftdneves/graph_program.git")        

    def on_token_press(self, event):
        '''Beginning drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        # moving the text along with the node
        self.canvas.move(self._nodeText[self._drag_data["item"]], delta_x, delta_y)

        # moving the edges along with the node
        # if the edge end is the current node being dragged: update its position
        for e in self._leftEdges:
            if(self._leftEdges[e] == self._drag_data["item"]):
                if "loop" in self.canvas.gettags(e):
                    # if the edge is a loop use different method to move it and its text
                    self.canvas.move(e, delta_x, delta_y)
                    self.canvas.move(self._edgeText[e], delta_x, delta_y)
                else:
                    # if it is a normal edge get original coordinates and update half of it
                    original = self.canvas.coords(e)
                    self.canvas.coords(e, event.x, event.y, original[2], original[3])
                    # some really bad but functioning code to move edge weight text
                    int_x = (event.x + original[2]) / 2
                    int_y = (event.y + original[3]) / 2
                    self.canvas.coords(self._edgeText[e], int_x-15, int_y-15)
                
        for e in self._rightEdges:
            if(self._rightEdges[e] == self._drag_data["item"]):
                if "loop" in self.canvas.gettags(e):
                    # everything was already moved in the first for
                    pass
                else:
                    # if it is a normal edge get original coordinates and update half of it
                    original = self.canvas.coords(e)
                    self.canvas.coords(e, original[0], original[1], event.x, event.y)
                    # some really bad but functioning code to move edge weight text
                    int_x = (event.x + original[0]) / 2
                    int_y = (event.y + original[1]) / 2
                    self.canvas.coords(self._edgeText[e], int_x-15, int_y-15)

    def draw_node(self, event):
        # calculate node position placement
        x, y = event.x, event.y
        bbox = (x + 20, y + 20, x - 20, y - 20)
        # increments node count
        self._node_count += 1

        #draws node on canvas
        self._nodes.append(self.canvas.create_oval(*bbox, fill="#77c777", activefill="#90EE90", tags=("node", self._node_count)))

        #draws node text on canvas
        # nodeText = dictionary where index = last node created and value = text
        self._nodeText[self._nodes[-1]] = self.canvas.create_text(x, y, fill="black", font="Helvetica 12 bold", text=self._node_count)

    def connect_node(self, event):
        # get mouse position
        x, y = event.x, event.y
        
        if not self.line_start:
            # this is the first click -> leftmost edge end
            # get mouse position and reference of the node selected
            self.line_start = (x,y)
            self.firstnode = self.canvas.find_closest(x, y)[0]
            # highlights the selected node
            self.canvas.itemconfig(self.firstnode, fill='#ff726f', activefill='#ff726f')
        else:
            # this is the second click -> rightmost edge end
            x_origin, y_origin = self.line_start
            self.line_start = None
            
            # check if the edge created is a loop
            if self.firstnode == self.canvas.find_closest(x, y)[0]:
                # draws an oval instead of a line
                x1,y1,x2,y2 = self.canvas.coords(self.firstnode)
                edge = self.canvas.create_oval(x2-15, y2-15, x2-70, y2-70, fill='', activeoutline="red", width=3, tags=("edge", 1, "loop"))
                self.canvas.tag_lower(edge)

                # saves the edge reference
                self._edges.append(edge)
                self._edgeText[self._edges[-1]] = self.canvas.create_text(x2-70, y2-75, fill="black", font="Helvetica 10 bold", text="1")
            else:
                # not a loop -> draw a line connecting both selected nodes
                edge = self.canvas.create_line(x_origin, y_origin, x, y, activefill="red", width=3, tags=("edge", 1))
                self.canvas.tag_lower(edge)

                # saves the edge reference
                self._edges.append(edge)

                # calculating position for the edge text
                int_x = (x_origin + x) / 2
                int_y = (y_origin + y) / 2
                self._edgeText[self._edges[-1]] = self.canvas.create_text(int_x-15, int_y-15, fill="black", font="Helvetica 10 bold", text="1")

            # used to update edge position when dragging a node
            self._leftEdges[edge] = self.firstnode
            self._rightEdges[edge] = self.canvas.find_closest(x, y)[0]

            # remove highlight from firstnode
            self.canvas.itemconfig(self.firstnode, fill="#77c777", activefill="#90EE90")

    def delete_node(self, event):
        x, y = event.x, event.y
        # finding the selected node and its text
        node = self.canvas.find_closest(x, y)[0]
        nodetext = self._nodeText[node]
        # deleting node from canvas and variables
        self.canvas.delete(node)
        self.canvas.delete(nodetext)
        self._nodes.remove(node)
        self._nodeText.pop(node)

        # searching and removing any edge bound to the selected node
        edgestoremove = list()

        for e in self._leftEdges:
            if(self._leftEdges[e] == node):
                if e not in edgestoremove:
                    edgestoremove.append(e)
        for e in self._rightEdges:
            if(self._rightEdges[e] == node):
                if e not in edgestoremove:
                    edgestoremove.append(e)
        
        for e in edgestoremove:
            self.canvas.delete(e)
            self.canvas.delete(self._edgeText[e])
            self._edges.remove(e)
            self._leftEdges.pop(e)
            self._rightEdges.pop(e)
            self._edgeText.pop(e)

    def open_edge_window(self, event):
        # get mouse position
        x, y = event.x, event.y
        # save edge reference
        self._selectedEdge = self.canvas.find_closest(x, y)[0]
        # draw window and form
        self.edgewindow = tk.Toplevel(self)
        self.edgewindow.geometry("400x200") 
        self.edgewindow.title("Edit Edge Weight")
        self.weight = tk.StringVar()
        self.weight.set(int(self.canvas.gettags(self._selectedEdge)[1]))
        tk.Label(self.edgewindow, text="Edge Weight").pack(padx=5,pady=2)
        tk.Entry(self.edgewindow, textvariable=self.weight).pack(padx=5,pady=2)
        tk.Button(self.edgewindow, text="Submit", command=self.submit).pack(padx=5,pady=2)
        tk.Button(self.edgewindow, text="Delete Edge", command=self.delete_edge).pack(padx=5,pady=2)
    
    def submit(self):
        if "loop" in self.canvas.gettags(self._selectedEdge):
            self.canvas.itemconfig(self._selectedEdge, tags=("edge", self.weight.get(), "loop"))
        else:
            self.canvas.itemconfig(self._selectedEdge, tags=("edge", self.weight.get()))
        self.canvas.itemconfigure(self._edgeText[self._selectedEdge], text=str(self.weight.get()))
        self.edgewindow.destroy()
    
    def delete_edge(self):
        self.canvas.delete(self._selectedEdge)
        self.canvas.delete(self._edgeText[self._selectedEdge])
        self._edges.remove(self._selectedEdge)
        self._leftEdges.pop(self._selectedEdge)
        self._rightEdges.pop(self._selectedEdge)
        self._edgeText.pop(self._selectedEdge)
        self.edgewindow.destroy()

app = App()
app.iconbitmap('resources/img/graph.ico')
app.mainloop()