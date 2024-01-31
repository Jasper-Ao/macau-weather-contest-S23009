from tkinter import *

nodes_list = []
class create_node:
    def __init__(self, name: str, pos: tuple, aqi: int) -> None:
        self.name = name
        self.x, self.y = pos
        self.aqi = aqi
        self.connected_nodes = []
        
        def draw_node(x, y):
            x0 = x - 15
            y0 = y - 15
            x1 = x + 15
            y1 = y + 15

            self.circle = main_canvas.create_oval(x0, y0, x1, y1, outline='black', fill='white')
            self.text = main_canvas.create_text(x,y, text=name, fill='red', font='Arial')
        draw_node(self.x, self.y)

        nodes_list.append(self)

def connect_nodes(start_node, end_node, distance, xtilt=0, ytilt=0):
    start_node.connected_nodes.append((end_node.name, distance))
    end_node.connected_nodes.append((start_node.name, distance))

    x0, y0 = start_node.x, start_node.y
    x1, y1 = end_node.x, end_node.y
    
    main_canvas.create_line(x0,y0, x1,y1, fill='red', width=3)
    main_canvas.create_text((start_node.x+end_node.x)/2 + xtilt, (start_node.y+end_node.y)/2 + ytilt, text=f'{str(distance)}m', fill='red', font='Arial')

    main_canvas.tag_raise(start_node.circle)
    main_canvas.tag_raise(start_node.text)
    main_canvas.tag_raise(end_node.circle)
    main_canvas.tag_raise(end_node.text)

def name_to_node(name):
    for node in nodes_list:
        if node.name == name: return node

root = Tk()
main_canvas = Canvas(root, width=876,height=656)
main_canvas.pack()
bg = PhotoImage(file="python/test/images/pcms layout simple.png")
main_canvas.create_image(439,329, image=bg)


node_a = create_node('A', (265,310), 18)
node_b = create_node('B', (270,490), 32)
node_c = create_node('C', (455,250), 23)
node_d = create_node('D', (620,520), 56)
node_e = create_node('E', (720,185), 48)

connect_nodes(node_a, node_b, 25, xtilt=-25)
connect_nodes(node_a, node_c, 32, ytilt=-20)
connect_nodes(node_b, node_d, 45, ytilt=-15)
connect_nodes(node_c, node_d, 42, xtilt=25)
connect_nodes(node_c, node_e, 38, ytilt=-15)
connect_nodes(node_d, node_e, 42, xtilt=-25)

aqi_dict = {node.name: node.aqi for node in nodes_list}

aqi_tilts = [(0,-30), (-30,0), (-10,-25), (30,-10), (0,-30)]
for node, (xtilt, ytilt) in zip(nodes_list, aqi_tilts):
    main_canvas.create_text(node.x + xtilt, node.y + ytilt, text=str(node.aqi), fill='blue', font='Arial')

nodes_network = {node.name: node.connected_nodes for node in nodes_list}

def a_star(start_node, stop_node):
        open_set = set(start_node) 
        closed_set = set()
        g = {}
        parents = {}

        g[start_node] = 0
        parents[start_node] = start_node
         
        while len(open_set) > 0:
            n = None
            for v in open_set:
                if n == None or g[v] + weighted_aqi_dict[v] < g[n] + weighted_aqi_dict[n]:
                    n = v
              
            if n == stop_node or nodes_network[n] == None: pass
            else:
                for (m, weight) in get_neighbors(n):
                    if m not in open_set and m not in closed_set:
                        open_set.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight 
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n

                            if m in closed_set:
                                closed_set.remove(m)
                                open_set.add(m)
 
            if n == None: return None
            if n == stop_node:
                path = []
 
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
 
                path.append(start_node)
                path.reverse()

                return path

            open_set.remove(n)
            closed_set.add(n)

        return None

def get_neighbors(v):
    if v in nodes_network:
        return nodes_network[v]
    else:
        return None


# input starting position, ending position and weight here
start_pos = 'B'
end_pos = 'E'
weight = 1


weighted_aqi_dict = {key: val*weight for key, val in aqi_dict.items()}
nodes_path = []
for node_name in a_star(start_pos, end_pos):
    for node in nodes_list: nodes_path.append(name_to_node(node_name))

for node0, node1 in zip(nodes_path[:-1], nodes_path[1:]):
    main_canvas.create_line(node0.x,node0.y, node1.x,node1.y, fill='blue', width=4)

    main_canvas.tag_raise(node0.circle)
    main_canvas.tag_raise(node0.text)
    main_canvas.tag_raise(node1.circle)
    main_canvas.tag_raise(node1.text)


root.mainloop()
