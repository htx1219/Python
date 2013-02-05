import math
from udacityplots import *

## Change h from 0.01 to 0.1 for submitting
h = 0.1 # s
mass_quarter_car = 250. # kg
mass_effective_wheel = 20. # kg
g = 9.81 # m / s2

end_time = 5. # s
num_steps = int(end_time / h)

def friction_coeff(slip):
    return 1.1 * (1. - math.exp(-20. * slip)) - 0.4 * slip

def solve(w1, c, d, f, k): # returns the solution w2
    if k >= 0.: # don't spin the wheel backward!
        return 0.
    else: # implement Newton-Raphson
        w_old = w1
        done = False           
        while not done:
            w_new = w_old - (c * w_old + d * math.exp(f * w_old) + k) / (c + d * f * math.exp(f * w_old))
            done = (math.fabs(w_new - w_old) < math.fabs(w_new + w_old) * 1e-12) 
            w_old = w_new
        return w_new

@show_plot(8, 8)
def wheel_slip():
    w = numpy.zeros(num_steps + 1) # m / s
    v = numpy.zeros(num_steps + 1) # m / s
    x = numpy.zeros(num_steps + 1) # m
    times = h * numpy.array(range(num_steps + 1))

    axes_x = matplotlib.pyplot.subplot(411)
    axes_v = matplotlib.pyplot.subplot(412)
    axes_w = matplotlib.pyplot.subplot(413)
    axes_s = matplotlib.pyplot.subplot(414)

    axes_x.set_ylabel('Position\nin m', multialignment = 'center')
    axes_v.set_ylabel('Car velocity\nin m/s', multialignment = 'center')
    axes_w.set_ylabel('Wheel velocity\nin m/s', multialignment = 'center')
    axes_s.set_ylabel('Wheel\nslip', multialignment = 'center')
    axes_s.set_xlabel('Time in s')
    axes_s.set_ylim(0., 1.)
    b_values = numpy.arange(70., 190.1, 30.) # m / s2
    for b in b_values:
        x[0] = 0.
        v[0] = 120. * 1000. / 3600. # 120 km / h    
        w[0] = v[0]
        
        for step in range(num_steps):
            if v[step] < 0.01: # Did we already come to a complete stop?
                break
            s = max(0., 1. - w[step] / v[step]) # clamps the value at zero to reduce numerical instability
            force = friction_coeff(s) * mass_quarter_car * g
            v[step + 1] = v[step] - h * force / mass_quarter_car
            x[step + 1] = x[step] + h * v[step]
            
            # change the following from Forward Euler to Backward Euler and include the above solver
            gem = g*mass_quarter_car/mass_effective_wheel
            c = 1.-0.4*h*gem/v[step+1]
            d = h*gem*1.1*math.exp(-20.)
            f = 20./v[step+1]
            k = h*b - h*0.7*gem - w[step]
            #c = max(0., c)
            #d = max(0., d)
            #f = max(0., f)
            #k = max(0., k)
            
            w[step+1] = solve(w[step], c, d, f, k)
            #w[step + 1] = w[step] + h * (force / mass_effective_wheel - b)
            w[step + 1] = max(0., w[step + 1]) # clamps the value of w at zero so that the brake can't spin the wheel backward

        axes_x.plot(times[:step], x[:step])
        axes_v.plot(times[:step], v[:step])
        axes_w.plot(times[:step], w[:step])
        axes_s.plot(times[:step], 1. - w[:step] / v[:step])
        p = int((0.35 + 0.4 * (b - b_values[0]) / (b_values[-1] - b_values[0])) * num_steps)
        axes_x.annotate(b, (times[p], x[p]),
                               xytext = (-30, -30), textcoords = 'offset points',
                               arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3, rad = 0.2', shrinkB = 0.))

    return x, v, w

x, v, w = wheel_slip()
