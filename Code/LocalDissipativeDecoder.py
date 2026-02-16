import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt

rng = np.random.default_rng()

p_i = 0.1  #probability of bit flip

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
len_psi = len(psi_initial)

def syndrome_calc(psi):
	syndr_arr = np.ones(len(psi) - 1, dtype = int) #in terms of 1s in this case
	for i in range(0, len_psi - 1): #0-indexing here
		if psi[i] != psi[i+1]: #flag domain walls with 1
			syndr_arr[i] = -1
	return syndr_arr

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
			flip_arr.append(i) #accept flip at site i
		elif DE_i > 0:
			pass #reject flip at site i 
		elif DE_i == 0:
			if rng.random() < 0.5:
				flip_arr.append(i) #randomly accept or reject flip
	return flip_arr

def Decoding_single_step(psi,Errloc):
	psi_d = psi.copy()
	for i in Errloc:
		psi_d[i] = psi_d[i]^1
	return psi_d

def Decoding_full(psi):
	psi_len = len(psi)
	nit = 0
	spin_history = [psi]
	syndrome_history = [syndrome_calc(psi)]
	psi_d = psi.copy()
	while (sum(psi_d) != 0 and sum(psi_d) != psi_len and nit < 10000):
		psi_i = Decoding_single_step(psi_d,Decode_step(syndrome_calc(psi_d)))
		psi_d = psi_i #rethink this structure later
		nit += 1
		spin_history.append(psi_d)
		syndrome_history.append(syndrome_calc(psi_d))
	return psi_decoded, nit, spin_history, syndrome_history


#print("psi decoded:", Decoding_full(psi_decoded)[0])
#print("Number of iterations:", Decoding_full(psi_decoded)[1])
#print("Spin history", Decoding_full(psi_decoded)[2])
#print("Syndrome history", Decoding_full(psi_decoded)[3])

spin_hist_arr = np.array(Decoding_full(psi_decoded)[2])

#have to be able to collect this spin and syndrome array history for THE SAME RUN!!

plt.figure(1)
plt.imshow(spin_hist_arr, aspect='auto')
plt.xlabel("Spin index")
plt.ylabel("Decoding step")
plt.title("Spin Evolution During Decoding")

plt.show()

'''
Code for analyzing number of decoding steps 
needed for a given p_i

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
'''

