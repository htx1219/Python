import numpy
import matplotlib.pyplot

#from udacityplots import * # ...and comment out this line

def forward_euler():
    h = 0.1 # s
    g = 9.81 # m / s2

    num_steps = 50

    t = numpy.zeros(num_steps + 1)
    x = numpy.zeros(num_steps + 1)
    v = numpy.zeros(num_steps + 1)

    for step in range(num_steps):
        t[step + 1] = t[step]+h ###Your code here.
        x[step + 1] = x[step]+h*v[step]###Your code here.
        v[step + 1] = v[step]-h*g ###Your code here.
    return t, x, v

t, x, v = forward_euler()

#@show_plot # Remove this line when running locally
def plot_me():
    axes_height = matplotlib.pyplot.subplot(211)
    matplotlib.pyplot.plot(t, x)
    axes_velocity = matplotlib.pyplot.subplot(212)
    matplotlib.pyplot.plot(t, v)
    axes_height.set_ylabel('Height in m')
    axes_velocity.set_ylabel('Velocity in m/s')
    axes_velocity.set_xlabel('Time in s')
    # Uncomment the line below when running locally.
    matplotlib.pyplot.show() 

#plot_me()

earth_mass = 5.97e24 # kg
moon_mass = 7.35e22 # kg
gravitational_constant = 6.67e-11 # N m2 / kg2


def acceleration(moon_position, spaceship_position):
    d_E = numpy.linalg.norm(spaceship_position)
    d_M = numpy.linalg.norm(spaceship_position-moon_position)
    ac_E_n = gravitational_constant*earth_mass/(d_E)**2
    ac_M_n = gravitational_constant*moon_mass/(d_M)**2
    ac_E = ac_E_n * (-spaceship_position)/d_E
    ac_M = ac_M_n * (moon_position-spaceship_position)/d_M
    return ac_E+ac_M
