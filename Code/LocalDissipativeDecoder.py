import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt

rng = np.random.default_rng()

p_i = 0.3  #probability of bit flip

J = 1

def Noise(psi,p_i):
	for i in range(1,len(psi)):
    		p = rng.random()
    		if p <= p_i and psi[i] == 0:
        		psi[i] = 1
    		elif p <= p_i and psi[i] == 1:
        		psi[i] = 0
	return psi

psi_initial = Noise(np.zeros(20, dtype = int),p_i)
max_decode = math.floor((len(psi_initial)-1)/2)

print("initial noisy psi", psi_initial)
#syndrome calculation

len_psi = len(psi_initial)

def syndrome_calc(psi):
	syndr_arr = np.ones(len(psi) - 1, dtype = int) #in terms of 1s in this case
	for i in range(0, len_psi - 1): #0-indexing here
		if psi[i] != psi[i+1]: #flag domain walls with 1
			syndr_arr[i] = -1
	return syndr_arr

print("trial of syndrome array function", syndrome_calc(psi_initial))

psi_decoded = psi_initial.copy()

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

def Decoding_single_step(psi,Errloc):
	psi_decode = psi.copy()
	for i in Errloc:
		psi_decode[i] = psi_decode[i]^1
	return psi_decode

def Decoding_full(psi_decoded):
	nit = 0
	while (sum(psi_decoded) != 0 and sum(psi_decoded) != len_psi and nit < 2500):
		psi = Decoding_single_step(psi_decoded,Decode_step(syndrome_calc(psi_decoded)))
		psi_decoded = psi
		nit += 1
	return psi_decoded, nit


print("psi decoded:", Decoding_full(psi_decoded)[0])
print("Number of iterations:", Decoding_full(psi_decoded)[1])

nit_arr = []
for i in range(100):
	psi_n = Noise(np.zeros(20, dtype = int),p_i)
	print(psi_n)
	nit_arr.append(Decoding_full(psi_n)[1])

plt.figure(1)
plt.title(f"Histogram: Bit Flip Probability {p_i}")
plt.hist(nit_arr, bins = 100)
plt.xlabel("Number of Decoding Iterations")
plt.show()
