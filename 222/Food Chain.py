# Create a simple model of a food chain with two species of fish, 
# one a predator and the other its prey.  Things to keep in mind: 
# Prey multiplies at a certain rate; prey is consumed by predators;
# predators die of old age; predators multiply depending on the amount 
# of prey; predators are being harvested.  Calculate A, B, C, and D 
# using the following information: the growth rate of the prety is 0.5/year;
# the average lifespan of a predator is 5 years; the predator and prey 
# populations will remain constant over time once there are 5.0*10^6 tons 
# of prey and 1.0*10^6 tons of predator.  Use the Forward Euler Method to 
# find out how each population changes over time.  Assuming that A, B, C, D, 
# and the initial amounts of both fish are uncertain by +/-10%, determine 
# which of these factors has the largest impact on the maximum amount of prey.
# Please note that food_chain should show how predator and prey 
# populations change with time depending on these six factors, and the function
# should also pair each factor with the proper color.  Also, set result_up and
# result_down equal to the maximum prey values calculated when the parameters are
# at +10% and -10%, respectively.  
#

import math
from udacityplots import *

base_values = {'A': 0.5, # fill this in (1 / year)
               'B': 0.5e-6, # fill this in (1 / year ton)
               'C': 1./5, # fill this in (1 / year)
               'D': 0.04e-6, # fill this in (1 / year ton)
               'prey initial amount': 4.0e6, # tons
               'predator initial amount': 0.9e6 # tons
              }

colors = {'A': 'r',
          'B': 'm',
          'C': 'b',
          'D': 'c',
          'prey initial amount': 'y',
          'predator initial amount': 'k'          
         }

end_time = 50. # years
h = 0.01 # years
num_steps = int(end_time / h)
times = h * numpy.array(range(num_steps + 1))

prey = numpy.zeros(num_steps + 1)
predator = numpy.zeros(num_steps + 1)

@show_plot(8, 8)
def sensitivity_analysis():
    axes_prey = matplotlib.pyplot.subplot(211)
    axes_predator = matplotlib.pyplot.subplot(212)
    axes_predator.set_xlabel('Time in years')
    axes_prey.set_ylabel('Amount of prey in tons')
    axes_predator.set_ylabel('Amount of predator in tons')
    matplotlib.pyplot.show()
    most_critical_parameter = ''
    worst_difference = 0.

    def food_chain(values, color):
        prey[0] = values['prey initial amount']
        predator[0] = values['predator initial amount'] 
        for step in range(num_steps):
            prey[step + 1] = prey[step] + h*values['A']*prey[step] - h*values['B']*prey[step]*predator[step]
            predator[step + 1] = predator[step] - h*values['C']*predator[step] + h*values['D']*prey[step]*predator[step]
        axes_prey.plot(times, prey, c = color)
        axes_predator.plot(times, predator, c = color)
        return numpy.max(prey)

    for key in base_values.keys(): # take into account the uncertainties of the 6 factors
        color = colors[key]    
        one_value_down = base_values.copy()
        one_value_down[key] = base_values[key]*0.9
        
        result_down = food_chain(one_value_down, color)

        one_value_up = base_values.copy()
        one_value_up[key] = base_values[key]*1.1
        
        result_up = food_chain(one_value_up, color)
        
        difference = math.fabs(result_up - result_down)
        if difference > worst_difference:
            worst_difference = difference
            most_critical_parameter = key
    print most_critical_parameter, result_up, result_down
    return

sensitivity_analysis()
