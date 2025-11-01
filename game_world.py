# 1 layer = background
# 2 layer = game world objects
# 3 layer = UI

world = [[], [], []]

def add_object(o, depth = 0):
     world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise ValueError('Cannot delete non existing object')