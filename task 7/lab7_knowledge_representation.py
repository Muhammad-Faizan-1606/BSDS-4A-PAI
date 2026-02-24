facts = []
facts.append('water is liquid')
facts.append('cat is animal')
facts.append('dog is animal')
facts.append('paris is city')

print('facts')
for f in facts:
    print(f)

procedures = {}
procedures['make tea'] = ['boil water','add tea','wait 5 min']
procedures['walk'] = ['stand up','move left foot','move right foot']

print('procedures')
for p in procedures:
    print(p)
    for step in procedures[p]:
        print(step)

semantic = {}
semantic['cat'] = ['animal','mammal','pet']
semantic['dog'] = ['animal','mammal','pet']
semantic['water'] = ['liquid','drink']

print('semantic')
for s in semantic:
    print(s)
    for r in semantic[s]:
        print(r)

episodes = []
episodes.append('visited paris 2020')
episodes.append('learned python 2023')

print('episodes')
for e in episodes:
    print(e)

print('inference')

entity = 'cat'
for f in facts:
    parts = f.split(' is ')
    if parts[0] == entity:
        print(entity + ' is ' + parts[1])
        
        if parts[1] == 'animal':
            print('animals breathe')

entity = 'water'
for f in facts:
    parts = f.split(' is ')
    if parts[0] == entity:
        print(entity + ' is ' + parts[1])
        
        if parts[1] == 'liquid':
            print('liquids flow')

print('done')

nodes = []
edges = []

nodes.append('cat')
nodes.append('dog')
nodes.append('animal')
nodes.append('water')
nodes.append('liquid')

edges.append(['cat','is_a','animal'])
edges.append(['cat','has','fur'])
edges.append(['dog','is_a','animal'])
edges.append(['water','is_a','liquid'])

print('knowledge graph')
print(nodes)

print('query cat')
for e in edges:
    if e[0] == 'cat':
        print(e[1] + ' ' + e[2])

print('query dog')
for e in edges:
    if e[0] == 'dog':
        print(e[1] + ' ' + e[2])

print('done')
