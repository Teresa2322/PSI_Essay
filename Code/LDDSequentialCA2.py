import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from tqdm import tqdm
import timeit

rng = np.random.default_rng()

N_s = 250 #number of sites
J = 1 #Ising Hamiltonian parameter

pi_arr = np.linspace(0,0.50,10)

success_arr = []
success_p_arr = []

for p_i in pi_arr:
	success_arr.clear()
	for t in tqdm(range(401), desc = "sampling for mean"):
		def Noise(psi,p):
			return np.where(rng.random(len(psi)) <= p, -1, psi)
		
		psi_initial = Noise(np.ones(N_s, dtype = int),p_i)
		len_psi = len(psi_initial)

		def syndrome_calc(psi):
			syndr_arr = []
			for i in range(0, len_psi - 1):
				syndr_arr.append(psi[i]*psi[i+1])
			return syndr_arr

		def s_i(psi_m, psi_p): #where m and p are psi values
			return psi_m*psi_p #this is a bit silly but I wanna keep syndrome language?

		def Decode_step(i, psi):
			#psi_d = psi.copy()
			if  i == 0:
				DE_i = 2*J*s_i(psi[0],psi[1]) 
			elif i == len_psi - 1:
				DE_i = 2*J*s_i(psi[len_psi - 2], psi[len_psi - 1]) 
			else:
				DE_i = 2*J*(s_i(psi[i-1],psi[i]) + s_i(psi[i],psi[i+1])) 
			if DE_i < 0:
				psi[i] *= -1
			elif DE_i > 0:
				pass
			elif DE_i == 0:
				if rng.random() < 0.5:
					psi[i] *= -1
			return psi
		def Decoding_full(psi):
			psi_len = len(psi)
			nit = 0
			#state_hist = [psi]
			psi_d = psi.copy()
			while (np.abs(sum(psi_d)) != psi_len and nit < 1000000):
				for i in rng.permutation(psi_len):
					psi_i = Decode_step(i, psi_d)
					psi_d = psi_i
				#state_hist.append(psi_d)
				nit += 1
			return psi_d, nit #state_hist #synd_hist

		psi_final, nit  = Decoding_full(psi_initial)
		#print("final psi", psi_final)
		#print("nit final", nit)
		if sum(psi_final) == len_psi:
			success_arr.append(1)
	average_success = np.sum(success_arr)/400
	#print("success array is:", success_arr)
	success_p_arr.append(1 - average_success)

plt.scatter(pi_arr, success_p_arr)
plt.ylabel("failure probability")
plt.xlabel("pi")
plt.show()


'''
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
plt.title(f"{N_s} state Evolution, p_i = {p_i}, N_i = {nit} ")

plt.show()
'''
plt.figure(2)

'''
cmap = ListedColormap(["white", "blue"])
plt.imshow(synd_hist_arr, aspect='auto')
plt.xlabel("Site index")
plt.xticks(np.arange(N_s - 1))
plt.gca().set_xticklabels([])

plt.ylabel("Decoding step")
plt.title("Syndrome Evolution During Decoding")
'''

#histogram to analyze number of iterations/scalability
'''
n_arr = []
for i in range(100):
	psi_n = Noise(np.zeros(N_s, dtype = int),p_i)
	n_arr.append(Decoding_full(psi_n)[1])

plt.figure(2)
plt.title(f"Histogram: Bit Flip Probability {p_i}")
plt.hist(n_arr, bins = 20)
plt.xlabel("Number of Decoding Iterations")
plt.show()
'''
