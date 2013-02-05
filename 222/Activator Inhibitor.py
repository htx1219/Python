from udacityplots import *

diffusion_coefficient_a = 0.0005 # m2 / s
diffusion_coefficient_b = 0.004 # m2 / s

length = 1. # meters; domain extends from 0 to length
size = 30 # number of points per dimension of the grid
dx = length / size

# Pick a time step below the threshold of instability
h = 0.2 * dx ** 2 / max(diffusion_coefficient_a, diffusion_coefficient_b) # s
end_time = 20. # s

@show_plot
def pattern():
    numpy.random.seed(42)
    a_old = numpy.random.normal(0., 0.03, [size, size])
    b_old = numpy.random.normal(0., 0.03, [size, size])
    a_new = a_old.copy()
    b_new = b_old.copy()

    num_steps = int(end_time / h)
    for step in range(num_steps):
        for j in range(size):
            j_plus = j + 1
            j_minus = j - 1
            # Task 1: Treat j_plus and j_minus so that they are the coordinates of the next cell in the corresponding 
            # direction -- taking a possible wrap-around into account (periodic boundary conditions).
            
            j_plus = (j+1)%size
            j_minus = (j-1)%size
            
            for i in range(size):
                i_plus = i + 1
                i_minus = i - 1
                # Task 2: Similar to task 1, but now for i_plus and i_minus
                
                i_plus = i_plus % size
                i_minus = i_minus % size
                
                # your code here
                
                a0 = a_old[j, i]
                b0 = b_old[j, i]
                
                # Task 3: Implement the explicit finite-difference scheme for the activator-inhibitor model.
                a_new[j, i] = a0 + h*diffusion_coefficient_a*(a_old[j_plus, i]+a_old[j_minus, i]+a_old[j, i_minus]+a_old[j, i_plus] - 4*a0)/dx**2 + h*(1-a0**2)*a0 - h*b0
                b_new[j, i] = b0 + h*diffusion_coefficient_b*(b_old[j_plus, i]+b_old[j_minus, i]+b_old[j, i_minus]+b_old[j, i_plus] - 4*b0)/dx**2 + h*a0 - h*b0*0.7
                
        a_old, b_old, a_new, b_new = a_new, b_new, a_old, b_old
   
    dimensions = [0, length, 0, length]
                 
    axes = matplotlib.pyplot.subplot(121)
    matplotlib.pyplot.imshow(a_old, cmap = matplotlib.cm.winter, origin = 'lower', extent = dimensions)
    matplotlib.pyplot.colorbar()
    axes.set_title('a')
    axes.set_xlabel('x in m')
    axes.set_ylabel('y in m')

    axes = matplotlib.pyplot.subplot(122)
    matplotlib.pyplot.imshow(b_old, cmap = matplotlib.cm.winter, origin = 'lower', extent = dimensions)
    matplotlib.pyplot.colorbar()
    axes.set_title('b')
    axes.set_xlabel('x in m')
    axes.set_ylabel('y in m')
    
    return a_old, b_old

pattern()
