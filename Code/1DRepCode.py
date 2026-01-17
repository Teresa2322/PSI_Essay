import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

rng = np.random.default_rng()

psi_initial = np.zeros(20)
psi_final = np.array([])

N_its = 5 #number of times to apply Error 
p_i = 0.3 #probability of bit flip

print("Initial state", psi_initial)

for N_i in range(1,N_its + 1):
	for i in range(len(psi_initial)):
    		p = rng.random()
    		if p <= p_i and psi_initial[i] == 0.0:
        		psi_initial[i] = 1.0
    		elif p <= p_i and psi_initial[i] == 1.0:
        		psi_initial[i] = 0.0

print("Qubit after",N_its," noise passes is: ", psi_initial)

#some ideas: average sum over N_its? or maybe over p_i?
