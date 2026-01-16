import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

rng = np.random.default_rng()

psi_initial = np.zeros(5)
psi_final = np.array([])

for q in psi_initial:
	p = rng.random() #produces random number between 0 and 1
	if p <= 0.6:
		q = 1
	print("bit is ", q) 
	psi_final = np.append(psi_final, q)

print("Qubit after one noise pass", psi_final)
