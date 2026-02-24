facts = []
facts.append(['symptom','john','fever'])
facts.append(['symptom','john','cough'])
facts.append(['symptom','john','headache'])
facts.append(['symptom','mary','fever'])
facts.append(['symptom','mary','rash'])

print('expert system')

john_symptoms = []
for f in facts:
    if f[1] == 'john':
        john_symptoms.append(f[2])

print('john symptoms')
print(john_symptoms)

if 'fever' in john_symptoms and 'cough' in john_symptoms and 'headache' in john_symptoms:
    print('john has flu')

mary_symptoms = []
for f in facts:
    if f[1] == 'mary':
        mary_symptoms.append(f[2])

print('mary symptoms')
print(mary_symptoms)

if 'fever' in mary_symptoms and 'rash' in mary_symptoms:
    print('mary has measles')

print('done')

words = ['the','cat','chases','the','dog']

print('parsing')

pos = 0

if pos < len(words) and words[pos] == 'the':
    pos = pos+1
    print('found determiner')

if pos < len(words) and (words[pos] == 'cat' or words[pos] == 'dog'):
    pos = pos+1
    print('found noun')

if pos < len(words) and (words[pos] == 'chases' or words[pos] == 'sees'):
    pos = pos+1
    print('found verb')

if pos < len(words) and words[pos] == 'the':
    pos = pos+1
    print('found determiner')

if pos < len(words) and (words[pos] == 'cat' or words[pos] == 'dog' or words[pos] == 'ball'):
    pos = pos+1
    print('found noun')

if pos == len(words):
    print('valid sentence')
else:
    print('invalid')

print('done')
