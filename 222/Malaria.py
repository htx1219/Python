from udacityplots import *

h = 0.1 # days
end_time = 400. # days
num_steps = int(end_time / h)
times = h * numpy.array(range(num_steps + 1))

total_humans = 1e8
total_mosquitoes = 1e10

def prevent_malaria():
    bites_per_day_and_mosquito = 0.1 # 1 / (day * mosquito)
    transmission_probability_mosquito_to_human = 0.3 # probability
    transmission_probability_human_to_mosquito = 0.5 # probability
    human_recovery_time = 70.0 # days
    mosquito_lifetime = 10.0 # days
    bite_reduction_by_net = 0.9 # probability

    infected_humans = numpy.zeros(num_steps + 1)
    infected_mosquitoes = numpy.zeros(num_steps + 1)

    infected_humans[0] = 0.
    infected_mosquitoes[0] = 1e6

    for step in range(num_steps):
        ###Your code here.
        net_factor = 1.
        if step*h >= 100.:
            net_factor = 1-bite_reduction_by_net
            
        infected_humans[step + 1] = infected_humans[step] - h*infected_humans[step]/human_recovery_time + h*net_factor*bites_per_day_and_mosquito*transmission_probability_mosquito_to_human*(total_humans-infected_humans[step])*infected_mosquitoes[step]/total_humans
        infected_mosquitoes[step + 1] = infected_mosquitoes[step] - h*infected_mosquitoes[step]/mosquito_lifetime+h*net_factor*bites_per_day_and_mosquito*transmission_probability_human_to_mosquito*(total_mosquitoes-infected_mosquitoes[step])*infected_humans[step]/total_humans

    return infected_humans, infected_mosquitoes

infected_humans, infected_mosquitoes = prevent_malaria()

@show_plot
def plot_me():
    humans_plot = matplotlib.pyplot.plot(times, infected_humans / total_humans)
    mosquitoes_plot = matplotlib.pyplot.plot(times, infected_mosquitoes / total_mosquitoes)
    matplotlib.pyplot.figlegend((humans_plot, mosquitoes_plot), ('Humans', 'Mosquitoes'), 'upper right')

    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Time in days')
    axes.set_ylabel('Fraction infected')
    matplotlib.pyplot.xlim(xmin = 0.)
    matplotlib.pyplot.ylim(ymin = 0.)
    
plot_me()
