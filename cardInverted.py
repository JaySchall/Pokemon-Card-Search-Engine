#Regex for code: .+?(?=,)
#Regex for simplifying: (.+?(?=,"))|[^\w\s']+   .*png,"|[^\w\s']+|'s
import re
import Stemmer
datafile = open("train.csv", "r")
stem = Stemmer.Stemmer("english")
worddict = {}

for line in datafile:

    line = re.sub(""".*png,"|[^\w\s']+|'s""",' ',line)
    currentwords  = {}
    for word in line.split():
        word = stem.stemWord(word.lower())
        if word not in worddict:
            currentwords[word] = 0
            worddict[word] = [0, 1, 0]
        elif word not in currentwords:
            currentwords[word] = 0
            worddict[word][1] += 1
datafile.close()

wordtuple = sorted(worddict.items())
l = 0
dictionaryfile = open("dictionary.txt", "w")
for word in wordtuple:
    dictionaryfile.write(word[0] + "\n")
    worddict[word[0]][2] = l
    l+=1 
dictionaryfile.close()

print("hi")

indexwords = {}
datafile = open("train.csv", "r")
for line in datafile:
    currentwords  = {}
    code = ""
    try:
        code = (line.split(","))[0]
    except:
        print("WARNING: empty line")
        continue
    line = re.sub(""".*png,"|[^\w\s']+|'s""",' ',line)
    for word in line.split():
        word = stem.stemWord(word.lower())
        if word not in indexwords:
            indexwords[word] = [worddict[word][2], worddict[word][1],  []]
            currentwords[word] = 1
        if word not in currentwords:
            currentwords[word] = 1
        else:
            currentwords[word] += 1

    for word in currentwords:
        indexwords[word][2].append((code, currentwords[word]))

docsfile = open("docs.txt", "w")
wordtuple = sorted(indexwords.items())
docNumber = 0
count = 0
file = "inverted" + str(docNumber) +".txt"
invertfile = open(file, "w")
final = ""
for word in wordtuple:
    final = word[0]
    invertfile.write(str(word[1][0]) + " " + word[0] + " " + str(word[1][1]))
    word[1][2].sort(key=lambda a: a[1], reverse = True)
    for item in word[1][2]:
        invertfile.write(" " + str(item))
    invertfile.write("\n")
    count+=1
    if count >= 500:
        count = 0
        docNumber+=1
        docsfile.write(word[0] + "\n")
        invertfile.close()
        file = "inverted" + str(docNumber) +".txt"
        invertfile = open(file, "w")
docsfile.write(final + "\n")
invertfile.close()