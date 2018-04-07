#generates candidates for screening
def candidateGen(oldSet, k):
	finalSet = set()
	oldList = list(tuple(oldSet))
	for i in range(0,len(oldList)-1):
		for j in range(i+1, len(oldList)):
			A = set(oldList[i])
			B = set(oldList[j])
			if len(A.union(B)) == k + 1:
				candidateUnion = A.union(B)
				flag = True
				for el in candidateUnion:
					#copy of candidateUnion, don't want to destroy the original
					test = set(candidateUnion)
					el = set([el])
					test = test - el
					test = tuple(sorted(tuple(test)))
					if(test not in  oldSet):
						flag = False
						break
				if flag:
					#add sorted tuple to preserve ordering and eliminate repeats
					#PYTHON PRO ALEX: can you sort a tuple w/o returning a list?
					finalSet.add(tuple(sorted(tuple(candidateUnion))))
	return finalSet

#finds the counts of each set in out market basket dataset
def findCounts(totLines, curSet, minSup, n):
	count = {}
	for line in totLines:
		market_basket = line.split(", ")[1:]
		market_basket[-1] = market_basket[-1].strip()
		market_basket = set(market_basket)
		for item in curSet:
			if set(item) <= market_basket:
			    #add tuples to preserve order of tuple and not create keys with different ordering
				if item in count:
					count[item] += 1
				else:
					count[item] = 1
	curI = list(count.keys())
	fTemp = set()
	for i in curI:
		if count[i]/n > minSup:
			fTemp.add(i)
	return fTemp
			
					

f = open("out1.csv", "r")
lines = f.readlines()
f.close()
n = len(lines)
curCount = {}
minSup = 0.05
k = 1

#generate T, the market basket dataset
for line in lines:
	market_basket = line.split(", ")[1:]
	market_basket[-1] = market_basket[-1].strip()
	for item in market_basket:
		if item in curCount:
			curCount[item] += 1
		else:
			curCount[item] = 1

I = list(curCount.keys())

#first run through of T
F1 = set()
for i in I:
	if curCount[i]/n > minSup:
		F1.add(tuple([i]))
oldSet = F1
F = []
F.append(F1)
#firstGen = candidateGen(oldSet, k)
#newF = findCounts(lines, firstGen, minSup, n)
#F.append(newF)
#k += 1
#secondGen = candidateGen(newF, k)
#finalF = findCounts(lines, secondGen, minSup, n)
tempSet = set()


#main loop of the program
while len(oldSet) > 0:
	tempSet = candidateGen(oldSet, k)
	supportReduce = findCounts(lines, tempSet, minSup, n)
	if len(supportReduce) > 0:
		F.append(supportReduce)
		k += 1
	oldSet = supportReduce
print(F)







