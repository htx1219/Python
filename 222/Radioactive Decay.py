import math
from udacityplots import *

h = 10. # days
lifetime_bi = 5. / math.log(2.) # days
lifetime_po = 138. / math.log(2) # days

end_time = 5.0 * 365. # days
num_steps = int(end_time / h)
times = h * numpy.array(range(num_steps + 1))

def radioactive_decay():
    # numbers of atoms
    bi = numpy.zeros(num_steps + 1)
    po = numpy.zeros(num_steps + 1)
    pb = numpy.zeros(num_steps + 1)

    bi[0] = 1e24
    po[0] = 0.
    pb[0] = 0.

    for step in range(num_steps):
        # Task: Insert the Backward (!) Euler computation for the radioactive decay.
        bi[step + 1] = bi[step]/(1+h/lifetime_bi)
        po[step + 1] = (po[step]+ h*bi[step+1]/lifetime_bi)/(1+h/lifetime_po) 
        pb[step + 1] = pb[step] + h*po[step+1]/lifetime_po
        
    return bi, po, pb

bi, po, pb = radioactive_decay()

@show_plot
def plot_decay():
    bi_plot = matplotlib.pyplot.plot(times, bi)
    po_plot = matplotlib.pyplot.plot(times, po)
    pb_plot = matplotlib.pyplot.plot(times, pb)
    matplotlib.pyplot.figlegend((bi_plot, po_plot, pb_plot), ('$^{210}$Bi', '$^{210}$Po', '$^{206}$Pb'), 'upper right')

    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Time in days')
    axes.set_ylabel('Number of atoms')
    matplotlib.pyplot.xlim(xmin = 0.)
    matplotlib.pyplot.ylim(ymin = 0.)

plot_decay()
