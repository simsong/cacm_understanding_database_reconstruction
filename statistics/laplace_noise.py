import numpy as np

#adds laplace noise to our synthetic data
#how to calibrate sensitivity?


array_size = 10
my_array = [80, 40, 70, 30, 90, 10, 10, 10, 40, 20]
#params for generator are (mean, decay, number to generate)
noise = np.random.laplace(0, 3, array_size)

if __name__ == '__main__':
    print("Noise is", noise)
    noise_added = [noise + my_array]
    print("new vals are", noise_added)

