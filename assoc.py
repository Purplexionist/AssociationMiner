# Name:        Steven Liu
# Course:      CSC 466
# Instructor:  Dekhtyar
# Assignment:  Mining Association Rules
# Term:        Spring 2018

def main():
   grocery_driver()

   return
   
   
def grocery_driver():
   I = ['milk', 'cookies', 'eggs', 'bread', 'beer']
   t1 = {'milk', 'cookies'}
   t2 = {'milk', 'cookies', 'bread'}
   t3 = {'bread', 'beer'}
   t4 = {'milk', 'eggs'}
   t5 = {'cookies', 'eggs'}
   T = [t1, t2, t3, t4, t5]
   
   #print(support('milk', T))
   Apriori(T, I, .6)
   return

# i - itemset to find support
# T - list of sets (market baskets)
# returns float 
def support(i, T):
   sup = 0
   for t in T:
      if i in t:
         sup += 1
         
   sup = sup * 100 / len(T)
   return sup

# T - list of sets (market baskets)
# I - list of strings (items)
def Apriori(T, I, minSup):
   F = [i for i in I if support(i, T) >= minSup]
   k = 2
   
   while F[k - 1] is not None:
      C_k = candidateGen(F[k-1], k - 1)
      if C_k is not 0:
         for c in C_k:
            count[c] = 0
         for t in T:
            for c in C_k:
               if c in t:
                  count[c] += 1
                  
         #
      k += 1
   return
      

# F - list of frequent items
# k - length of itemset
# returns
def candidateGen(F , k):
   C = None
   
   #for f1, f2 in F if 
     
      
if __name__ == "__main__":
   main()
   