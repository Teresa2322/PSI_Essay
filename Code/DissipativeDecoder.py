import numpy as np
import scipy as sp
import math 

rng = np.random.default_rng()

psi_initial = np.zeros(20,  dtype=int )
 
p_i = 0.5 #probability of bit flip

max_decode = math.floor((len(psi_initial)-1)/2)

for i in range(1,len(psi_initial)):
    	p = rng.random()
    	if p <= p_i and psi_initial[i] == 0:
        	psi_initial[i] = 1
    	elif p <= p_i and psi_initial[i] == 1:
        	psi_initial[i] = 0

psi_noisy = psi_initial.copy()

print("Noisy state:", psi_noisy)

#syndrome calculation

len_psi = len(psi_initial)

syndr_arr = np.zeros(len_psi - 1, dtype = int)
err_arr = [] # position of error on syndrome (1-indexing) 

for i in range(0, len_psi - 1): #0-indexing here
	if psi_initial[i] != psi_initial[i+1]: #flag domain walls with 1
		syndr_arr[i] = 1
		err_arr.append(i+1)

print("Syndrome: ", syndr_arr) 

psi_decoded = psi_noisy.copy()

print("decoded psi", psi_decoded)


