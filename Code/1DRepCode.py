
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math 

rng = np.random.default_rng()

psi_initial = np.zeros(15,  dtype=int )

N_its = 1 #number of times to apply Error 
p_i = 0.2 #probability of bit flip

psi_initial[0] = 1

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
err_arr = []

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

print("Error array:", err_arr_f)
#print("Error array:", err_arr_b)

def even_or_odd( n ):
  if number % 2 == 0:
    return 0
  else:
    return 1 #as a flag for oddness

Nerr = len(err_arr)

for i in range(0,Nerr - 1, 2):
	a_f = err_arr_f[i]
	b_f = err_arr_f[i+1]
	a_b = err_arr_b[i]
	b_b = err_arr_b[i+1]
	print("[",a_f,",", b_f,"]")
	#print("[",a_b,b_b,"]")
