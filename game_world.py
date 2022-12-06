# game world
# 0: Background
# 1: Link and many objects
# 2: Monsters
# 3: UI

world = [[], [], [], [], []]
collision_group = dict()


def add_object(o, depth):
    world[depth].append(o)


def add_objects(o, depth):
    world[depth] += o


def remove_object(o, depth):
    for obj in world[depth]:
        if obj == o:
            world[depth].remove(obj)
            remove_collision_object(obj)
            del obj
            return
    raise ValueError('Trying destroy non existing object.')


def all_objects():
    for layer in world:
        for o in layer:
            yield o


def clear():
    for o in all_objects():
        remove_collision_object(o)
        del o
    for layer in world:
        layer.clear()


def add_collision_group(a, b, group):
    if group not in collision_group:
        collision_group[group] = [[], []]

    if a:
        if type(a) is list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)

    if b:
        if type(b) is list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)


def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
