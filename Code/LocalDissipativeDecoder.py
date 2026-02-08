import numpy as np
import scipy as sp
import math 

rng = np.random.default_rng()

psi_initial = np.zeros(20,  dtype=int )

p_i = 0.3 #probability of bit flip

J = 1

max_decode = math.floor((len(psi_initial)-1)/2)

for i in range(1,len(psi_initial)):
    	p = rng.random()
    	if p <= p_i and psi_initial[i] == 0:
        	psi_initial[i] = 1
    	elif p <= p_i and psi_initial[i] == 1:
        	psi_initial[i] = 0

psi_noisy = psi_initial.copy()

print("initial noisy psi", psi_noisy)
#syndrome calculation

len_psi = len(psi_initial)

def syndrome_calc(psi):
	syndr_arr = np.ones(len_psi - 1, dtype = int) #in terms of 1s in this case
	for i in range(0, len_psi - 1): #0-indexing here
		if psi_initial[i] != psi_initial[i+1]: #flag domain walls with 1
			syndr_arr[i] = -1
	return syndr_arr

print("trial of syndrome array function", syndrome_calc(psi_noisy))

psi_decoded = psi_noisy.copy()

def DeltaH_i(Si, Sim):
	return 2*J*(Si + Sim)

def DeltaH_edge(Si):
	return 2*J*Si

def Decode_step(synd_arr):
	flip_arr = []
	for i in range(len(synd_arr)):

		if  i == 0:
			DE_i = DeltaH_edge(synd_arr[i])
		elif i == len(synd_arr) - 1:
			DE_i = DeltaH_edge(synd_arr[i])
		else:
			DE_i = DeltaH_i(synd_arr[i],synd_arr[i-1])
		if DE_i < 0:
			#accept flip at site i 
			flip_arr.append(i)
		elif DE_i > 0:
			#reject flip at site i 
			pass
		elif DE_i == 0:
			if rng.random() < 0.5:
				flip_arr.append(i)
			#randomly accept of reject flip
	return flip_arr

def Denoise(psi,Errloc):
	psi_decode = psi.copy()
	for i in Errloc:
		psi_decode[i] = psi_decode[i]^1
	return psi_decode

for i in range(2):
	psi = Denoise(psi_decoded,Decode_step(syndrome_calc(psi_decoded)))
	print("psi:", psi)
	psi_decoded = psi


