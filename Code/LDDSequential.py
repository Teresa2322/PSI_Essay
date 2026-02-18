import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

rng = np.random.default_rng()

p_i = 0.7  #probability of bit flip
N_s = 30
J = 1

def Noise(psi,p_i):
	for i in range(1,len(psi)):
    		if rng.random() <= p_i:
        		psi[i] = 1
	return psi

psi_initial = Noise(np.zeros(N_s, dtype = int),p_i)

max_decode = math.floor((len(psi_initial)-1)/2)

len_psi = len(psi_initial)

def syndrome_calc(psi):
	syndr_arr = np.ones(len(psi) - 1, dtype = int) #in terms of 1s in this case
	for i in range(0, len_psi - 1): #0-indexing here
		if psi[i] != psi[i+1]: #flag domain walls with 1
			syndr_arr[i] = -1
	return syndr_arr

psi_decoded = psi_initial.copy()

def Decode_step(i, psi, synd_arr):
	psi_d = psi.copy()
	if  i == 0:
		DE_i = 2*J*synd_arr[0]
	elif i == len(psi) - 1:
		DE_i = 2*J*synd_arr[i - 1] #adjust from psi to synd indices 
	else:
		DE_i = 2*J*(synd_arr[i] + synd_arr[i-1]) 
	if DE_i < 0:
		psi_d[i] = psi_d[i]^1 #accept flip at site i
	elif DE_i > 0:
		pass #reject flip at site i 
	elif DE_i == 0:
		if rng.random() < 0.5:
			psi_d[i] = psi_d[i]^1 #randomly accept or reject flip
	#RETHINK INDEXING!! syndrome is len(psi)-1
	return psi_d

def Decoding_full(psi):
	psi_len = len(psi)
	nit = 0
	state_hist = [psi]
	synd_hist = [syndrome_calc(psi)]
	#num_domain_walls = np.sum(syndrome == -1)
	psi_d = psi.copy()
	while (sum(psi_d) != 0 and sum(psi_d) != psi_len and nit < 10000):
		for i in rng.permutation(psi_len): #for i in range(0, psi_len - 1):
			psi_i = Decode_step(i, psi_d, syndrome_calc(psi_d))
			psi_d = psi_i
		state_hist.append(psi_d)
		nit += 1
		synd_hist.append(syndrome_calc(psi_d))
	return psi_d, nit, state_hist, synd_hist

psi_final, nit, spin_history, syndrome_history = Decoding_full(psi_decoded)

spin_hist_arr = np.array(spin_history)
synd_hist_arr = np.array(syndrome_history)

plt.figure(1)

cmap = ListedColormap(["white", "blue"])
im = plt.imshow(spin_hist_arr, interpolation = 'nearest', cmap = cmap, vmin = 0, vmax = 1, aspect='auto')
cbar = plt.colorbar(im, ticks=[0, 1])
cbar.ax.set_yticklabels(['0', '1'])
plt.xlabel("Site index")
plt.xticks(np.arange(N_s))
plt.yticks(np.arange(0, nit+1, 1))
plt.gca().set_xticklabels([])
plt.gca().set_yticklabels([])

plt.ylabel("Decoding step")
plt.title(f"State Evolution, p_i = {p_i}, N_i = {nit} ")

plt.show()

plt.figure(2)

cmap = ListedColormap(["white", "blue"])
plt.imshow(synd_hist_arr, aspect='auto')
plt.xlabel("Site index")
plt.xticks(np.arange(N_s - 1))
plt.gca().set_xticklabels([])

plt.ylabel("Decoding step")
plt.title("Syndrome Evolution During Decoding")


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

