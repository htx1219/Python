import math
import numpy
import matplotlib.pyplot

earth_mass = 5.97e24 # kg
earth_radius = 6.378e6 # m (at equator)
gravitational_constant = 6.67e-11 # m3 / kg s2
moon_mass = 7.35e22 # kg
moon_radius = 1.74e6 # m
moon_distance = 400.5e6 # m (actually, not at all a constant)
moon_period = 27.3 * 24.0 * 3600. # s
moon_initial_angle = math.pi / 180. * -61. # radian

total_duration = 12. * 24. * 3600. # s
marker_time = 0.5 * 3600. # s
tolerance = 100000. # m



def moon_position(time):
# Task 1: Compute the moon's position (a vector) at time t. Let it start at moon_initial_angle, not on the horizontal axis.   
    ###Your code here.
    r_pass = 2*math.pi*time/moon_period
    r_total = r_pass+moon_initial_angle
    position = moon_distance*numpy.array([math.cos(r_total), math.sin(r_total)])

    return position

def acceleration(time, position):
# Task 2: Compute the spacecraft's acceleration due to gravity
	###Your code here.
    m_p = moon_position(time)
    r_E = numpy.linalg.norm(position)
    r_M = numpy.linalg.norm(position-m_p)
    a_E_N = gravitational_constant*earth_mass/r_E**2
    a_M_N = gravitational_constant*moon_mass/r_M**2
    
    acc = -position*a_E_N/r_E + (m_p-position)*a_M_N/r_M

    return acc  

# Task 5: (First see the other tasks below.) What is the appropriate boost to apply?
# Try -10 m/s, 0 m/s, 10 m/s, 50 m/s and 100 m/s and leave the correct amount in as you submit the solution.

axes = matplotlib.pyplot.gca()
axes.set_xlabel('Longitudinal position in m')
axes.set_ylabel('Lateral position in m')

def apply_boost():

    # Do not worry about the arrays position_list, velocity_list, and times_list.  
    # They are simply used for plotting and evaluating your code, so none of the 
    # code that you add should involve them.
    
    boost = 10. # m/s Change this to the correct value after everything else is done.
    position_list = [numpy.array([-6.701e6, 0.])] # m
    velocity_list = [numpy.array([0., -10.818e3])] # m / s
    times_list = [0]
    position = position_list[0]
    velocity = velocity_list[0]
    current_time = 0.
    h = 0.1 # s, set as initial step size right now but will store current step size
    h_new = h # s, will store the adaptive step size of the next step
    mcc2_burn_done = False
    dps1_burn_done = False

    while current_time < total_duration:
        #Task 3: Include a retrograde rocket burn at 101104 seconds that reduces the velocity by 7.04 m/s
        # and include a rocket burn that increases the velocity at 212100 seconds by the amount given in the variable called boost.                     
        
        
        if current_time>= 101104 and not mcc2_burn_done:
            v_N = numpy.linalg.norm(velocity)
            velocity = velocity*(v_N-7.04)/v_N
            mcc2_burn_done = True
            
        if current_time>= 212100 and not dps1_burn_done:
            v_N = numpy.linalg.norm(velocity)
            velocity = velocity*(v_N+boost)/v_N
            dps1_burn_done = True
        ###Your code here.

        #Task 4: Implement Heun's method with adaptive step size. Note that the time is advanced at the end of this while loop.
        acceleration0 = acceleration(current_time, position)    
        xE = position + h * velocity
        vE = velocity + h * acceleration0
        xH = position + h * 0.5 * (velocity + vE)
        vH = velocity + h * 0.5 * (acceleration0 + acceleration(current_time+h, xE))
        position = xH
        velocity = vH
        
        LTE = numpy.linalg.norm(xE-xH)+total_duration*numpy.linalg.norm(vE-vH)
        h_new = h*(tolerance/LTE)**0.5
        h_new = min(0.5 * marker_time, max(0.1, h_new)) # restrict step size to reasonable range

        
        current_time += h
        h = h_new
        position_list.append(position.copy())
        velocity_list.append(velocity.copy())
        times_list.append(current_time)

    return position_list, velocity_list, times_list, boost

position, velocity, current_time, boost = apply_boost()

def plot_path(position_list, times_list):
    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Longitudinal position in m')
    axes.set_ylabel('Lateral position in m')
    previous_marker_number = -1;
    for position, current_time in zip(position_list, times_list):
        #print position, position[0], position[1]
        if current_time >= marker_time * previous_marker_number:
            previous_marker_number += 1
            matplotlib.pyplot.scatter(position[0], position[1], s = 2., facecolor = 'r', edgecolor = 'none')
            moon_pos = moon_position(current_time)
            if numpy.linalg.norm(position - moon_pos) < 30. * moon_radius: 
                axes.add_line(matplotlib.lines.Line2D([position[0], moon_pos[0]], [position[1], moon_pos[1]], alpha = 0.3, c = 'g')) 
    axes.add_patch(matplotlib.patches.CirclePolygon((0., 0.), earth_radius, facecolor = 'none', edgecolor = 'b'))
    for i in range(int(total_duration / marker_time)):
        moon_pos = moon_position(i * marker_time)
        axes.add_patch(matplotlib.patches.CirclePolygon(moon_pos, moon_radius, facecolor = 'none', edgecolor = 'g', alpha = 0.7))

    matplotlib.pyplot.axis('equal')
    matplotlib.pyplot.show()

plot_path(position, current_time)
