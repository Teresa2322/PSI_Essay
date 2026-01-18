import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

rng = np.random.default_rng()

psi_initial = np.zeros(5)
psi_final = np.array([])

N_its = 1 #number of times to apply Error 
p_i = 0.2 #probability of bit flip

for N_i in range(1,N_its + 1):
	for i in range(len(psi_initial)):
    		p = rng.random()
    		if p <= p_i and psi_initial[i] == 0.0:
        		psi_initial[i] = 1.0
    		elif p <= p_i and psi_initial[i] == 1.0:
        		psi_initial[i] = 0.0

psi_noisy = psi_initial.copy()

print("Qubit after",N_its," noise passes is: ", psi_noisy)

#syndrome calculation

len_psi = len(psi_initial)

syndr_arr = np.zeros( len_psi - 1 )

for i in range(0, len_psi - 1): #this range is fine cause indices below add 1 to the last
	if psi_initial[i] != psi_initial[i+1]:
		syndr_arr[i] = 1

print("syndrome array is ", syndr_arr) 

psi_decoded = psi_noisy.copy()


