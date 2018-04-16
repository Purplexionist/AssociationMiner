# Course:      CSC 466
# Instructor:  Dekhtyar
# Assignment:  Mining Association Rules
# Term:        Spring 2018
import sys

def main ():
	if len(sys.argv) < 4:
		print("Usage: python3 assocmine.py [file] [minSup] [minConf] <etc>")
		sys.exit(0)

	f = open(sys.argv[1], "r")
	lines = f.readlines()
	f.close()
	n = len(lines)
	if(sys.argv[1] == "factor_baskets_sparse.csv"):
		n = n - 1
	curCount = {}
	minSup = float(sys.argv[2]) #around .05
	minConf = float(sys.argv[3]) #around .7
	k = 1
	bakeryCount = {}
	if len(sys.argv) > 4:
		if(sys.argv[4] == "goods.csv"):
			j = open(sys.argv[4], "r")
			goodLines = j.readlines()
			for line in goodLines[1:]:
				market_basket = line.split(",")
				bakeryCount[tuple([market_basket[0]])] = market_basket[2].replace("\"", "").replace("'","") + " " + market_basket[1].replace("\"", "").replace("'","")
			j.close()


	#generate T, the market basket dataset
	if(sys.argv[1] != "factor_baskets_sparse.csv"):
		for line in lines:
			market_basket = line.split(", ")[1:]
			market_basket[-1] = market_basket[-1].strip()
			for item in market_basket:
				item = tuple([item])
				if item in curCount:
					curCount[item] += 1
				else:
					curCount[item] = 1
	else:
		for line in lines[1:]:
			market_basket = line.split(",")[1:]
			market_basket[-1] = market_basket[-1].strip()
			for i in range(0, len(market_basket), 2):
				temp = market_basket[i]
				temp = tuple([temp])
				if temp in curCount:
					curCount[temp] += 1
				else:
					curCount[temp] = 1
	I = list(curCount.keys())
	#first run through of T
	F1 = set()
	for i in I:
		if curCount[i]/n > minSup:
			F1.add(i)
	oldSet = F1
	F = []
	F.append(F1)

	tempSet = set()

	#main loop of the program
	while len(oldSet) > 0:
		print("here boys")
		tempSet = candidateGen(oldSet, k)
		supportReduce = findCounts(lines, tempSet, minSup, n, curCount, sys.argv)
		if len(supportReduce) > 0:
			F.append(supportReduce)
			k += 1
		oldSet = supportReduce
	if(sys.argv[1] == "factor_baskets_sparse.csv"):
		return
	maxSkylines = []
	r = 0
	for x in range(len(F)-1, -1, -1):
		Fx = F[x]
		for f in Fx:
			if not maximalSkylineCheck(set(f), maxSkylines):
				maxSkylines.append(set(f))
			else:
				continue
			f = tuple(sorted(tuple(f)))
			if len(f) >=2:

				for s in list(f):

					lhs = set(f) - {s}
					rhs = {s}

					conf = curCount[f]/curCount[tuple(sorted(tuple(lhs)))]
					supp = curCount[f]/n

					r += 1

					if conf > minConf:
						if len(sys.argv) > 4:
							if(sys.argv[4] == "goods.csv"):
								finLeft = ""
								for myLHS in tuple(lhs):
									finLeft += bakeryCount[tuple([myLHS])] + ", "
								finLeft = finLeft[:-2]
								finRight = bakeryCount[tuple(rhs)]
								print("Rule", r, finLeft,"-->",finRight,"Support: %.3f" % supp, "Confidence: %.3f" % conf)
						else:
							print("Rule", r, lhs,"-->",rhs,"Support: %.3f" % supp, "Confidence: %.3f" % conf)
			else:
				continue
	if len(sys.argv) > 4:
		if(sys.argv[4] == "goods.csv"):
			for maxSet in maxSkylines:
				print("{", end = "")
				contents = ""
				for tup in maxSet:
					contents += bakeryCount[tuple([tup])] + ", "
				print(contents[:-2] + "}")
	else:
		print(maxSkylines)
	return


#==========================FrequentSubsets========================
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
def findCounts(totLines, curSet, minSup, n, count, sysArgv):
	if(sysArgv[1] != "factor_baskets_sparse.csv"):
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
	else:
		for line in totLines[1:]:
			market_basket = line.split(",")[1:]
			market_basket[-1] = market_basket[-1].strip()
			ansSet = []
			for i in range(0, len(market_basket), 2):
				ansSet.append(market_basket[i])
			ansSet = set(ansSet)
			for item in curSet:
				if set(item) <= ansSet:
					if item in count:
						count[item] += 1
					else:
						count[item] = 1

	fTemp = set()
	for i in curSet:
		if i in count:
			if (count[i]/n) > minSup:
				fTemp.add(i)
	return fTemp

#=============================GenRules============================
def maximalSkylineCheck(s, maxSkylines):
	for m in maxSkylines:
		if s < m:
			return True
	return False


if __name__ == "__main__":
	main()
