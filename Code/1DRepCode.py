
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math 

rng = np.random.default_rng()

psi_initial = np.zeros(10,  dtype=int )

N_its = 1 #number of times to apply Error 
p_i = 0.2 #probability of bit flip

#psi_initial[0] = 1

#should maybe be defining this as functions actually 

for N_i in range(1,N_its + 1):
	for i in range(1,len(psi_initial)):
    		p = rng.random()
    		if p <= p_i and psi_initial[i] == 0:
        		psi_initial[i] = 1
    		elif p <= p_i and psi_initial[i] == 1:
        		psi_initial[i] = 0

psi_noisy = psi_initial.copy()

print("Qubit after",N_its," noise passes is: ", psi_noisy)

#syndrome calculation

len_psi = len(psi_initial)

syndr_arr = np.zeros( len_psi - 1, dtype = int)
err_arr = [] # position of error (in non python index notation) on syndrome 

for i in range(0, len_psi - 1): #this range is fine cause indices below add 1 to the last
	if psi_initial[i] != psi_initial[i+1]:
		syndr_arr[i] = 1
		err_arr.append(i+1)

print("syndrome array is ", syndr_arr) 
print("error position is", err_arr)
#parity check flags ah wait thats just for syndrome extraction again 

psi_decoded = psi_noisy.copy()


err_arr_f = err_arr.copy()
err_arr_b = err_arr[::-1].copy() #wait this was silly, but keep reversal for reference

print("Forward error array:", err_arr_f)
print("Backward error array:", err_arr_b)

def even_or_odd(n):
  if n % 2 == 0:
    return 0
  else:
    return 1 #as a flag for oddness

Nerr = len(err_arr)



flips_backwards = []
flips_forwards = []

for i in range(0,Nerr - 1, 2):
	a_f = err_arr_f[i]
	b_f = err_arr_f[i+1]
	b_b = err_arr_b[i]
	a_b = err_arr_b[i+1]
	print("[",a_f,",", b_f,"]")
	print("[",a_b,",",b_b,"]")
	for j in range(a_f+1,b_f+1):
		flips_forwards.append(j)
	for k in range(a_b,b_b): #check, but I think this works because 
		flips_backwards.append(k)

print("forward flips", flips_forwards)
print("backwards flips:", flips_backwards)

x_f = []
x_b = []

if even_or_odd(Nerr) == 1:
	for k in range(err_arr_f[-1],len(psi_noisy)): #double check this indexing
		x_f.append(k)
	for l in range(err_arr_b[-1],len(psi_noisy)):
		x_b.append(l)
flips_forwards.extend(x_f)
flips_backwards.extend(x_b)

print("forward flips", flips_forwards)
print("backwards flips:", flips_backwards)

