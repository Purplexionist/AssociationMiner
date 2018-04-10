# Course:      CSC 466
# Instructor:  Dekhtyar
# Assignment:  Mining Association Rules
# Term:        Spring 2018
import sys

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
def findCounts(totLines, curSet, minSup, n, count):
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
	fTemp = set()
	for i in curSet:
		if count[i]/n > minSup:
			fTemp.add(i)
	return fTemp


#lhs is the left hand itemset of the association, and rhs is the right hand set (only one item in this lab) of the association.
def confidence(lhs,rhs,totLines,counts):
	unionCount = 0
	lhsCount = 0
	for line in totLines:
		market_basket = line.split(", ")[1:]
		market_basket[-1] = market_basket[-1].strip()
		market_basket = set(market_basket)

		s = lhs.union(rhs)
		if set(s) <= market_basket:
		    #add tuples to preserve order of tuple and not create keys with different ordering
			unionCount += 1
		if lhs <= market_basket:
			lhsCount += 1
	return unionCount/lhsCount


def main ():
	if len(sys.argv) < 2:
		print("Usage: python3 assoc.py <file name>")
		sys.exit(0)

	f = open(sys.argv[1], "r")
	lines = f.readlines()
	f.close()
	n = len(lines)
	curCount = {}
	minSup = 0.05
	minConf = 0.7
	k = 1

	#generate T, the market basket dataset
	for line in lines:
		market_basket = line.split(", ")[1:]
		market_basket[-1] = market_basket[-1].strip()
		for item in market_basket:
			item = tuple([item])
			if item in curCount:
				curCount[item] += 1
			else:
				curCount[item] = 1

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
		tempSet = candidateGen(oldSet, k)
		supportReduce = findCounts(lines, tempSet, minSup, n, curCount)
		if len(supportReduce) > 0:
			F.append(supportReduce)
			k += 1
		oldSet = supportReduce

	maxSkylines = []
	r = 0
	for x in range(len(F)-1, -1, -1):
		Fx = F[x]
		for f in Fx:
			maxSkylines.append(set(f))
			f = tuple(sorted(tuple(f)))
			if len(f) >=2:

				for s in list(f):

					lhs = set(f) - {s}
					rhs = {s}

					if maximalSkylineCheck(set(f), maxSkylines):
						continue

					conf = curCount[f]/curCount[tuple(sorted(tuple(lhs)))]
					supp = curCount[f]/n

					r += 1

					if conf > minConf:
						print("Rule", r, lhs,"==>",rhs,"Support:", supp, "Confidence: %.2f" % conf)
			else:
				continue

	print(maxSkylines)
	return



#curCount is the the dictionary that contains tuples of strings for keys and has integer for values
#use curCount when computing the association rules


#=============================GenRules============================
#lhs is the left hand itemset of the association, and rhs is the right hand set (only one item in this lab) of the association.
def confidence(lhs,rhs,totLines,counts):
	unionCount = 0
	lhsCount = 0
	s = lhs.union(rhs)
	for line in totLines:
		market_basket = line.split(", ")[1:]
		market_basket[-1] = market_basket[-1].strip()
		market_basket = set(market_basket)

		if set(s) <= market_basket:
			#add tuples to preserve order of tuple and not create keys with different ordering
			unionCount += 1
		if lhs <= market_basket:
			lhsCount += 1
	return unionCount/lhsCount

def support(lhs,rhs,totLines,counts,n):
	count = 0
	s = lhs.union(rhs)
	for line in totLines:
		market_basket = line.split(", ")[1:]
		market_basket[-1] = market_basket[-1].strip()
		market_basket = set(market_basket)

		if set(s) <= market_basket:
			#add tuples to preserve order of tuple and not create keys with different ordering
			count += 1
	return count/n


def maximalSkylineCheck(s, maxSkylines):
	for m in maxSkylines:
		if s < m:
			return True
	return False


if __name__ == "__main__":
	main()
