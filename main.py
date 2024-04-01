from simpful import *
import matplotlib.pylab as plt
from numpy import linspace, array
import controller as ctr
import time

FS = FuzzySystem()
# Input Water temp
S_1 = FuzzySet(function=Trapezoidal_MF(a=-20, b=-20, c=-15, d=0), term="cold")
S_2 = FuzzySet(function=Triangular_MF(a=-10, b=0, c=10), term="good")
S_3 = FuzzySet(function=Trapezoidal_MF(a=0, b=15, c=20, d=20), term="hot")
FS.add_linguistic_variable("Temp", LinguisticVariable([S_1, S_2, S_3], concept="Water temp",
                                                      universe_of_discourse=[-30, 30]))
FS.plot_variable("Temp", outputfile='Temp', TGT=None, highlight=None, ax=None, xscale='linear')

# Input Waterflow
F_1 = FuzzySet(function=Trapezoidal_MF(a=-1, b=-1, c=-0.8, d=0), term="soft")
F_2 = FuzzySet(function=Triangular_MF(a=-0.4, b=0, c=0.4), term="good")
F_3 = FuzzySet(function=Trapezoidal_MF(a=0, b=0.8, c=1, d=1), term="hard")
FS.add_linguistic_variable("Flow", LinguisticVariable([F_1, F_2, F_3], concept="Waterflow",
                                                      universe_of_discourse=[-1, 1]))
FS.plot_variable("Flow", outputfile='Flow', TGT=None, highlight=None, ax=None, xscale='linear')

# Mamdani: Define fuzzy sets, linguistic variables and universe of discoures foroutput cold
T_1 = FuzzySet(function=Triangular_MF(a=-1, b=-0.6, c=-0.3), term="closeFast")
T_2 = FuzzySet(function=Triangular_MF(a=-0.6, b=-0.3, c=0), term="closeSlow")
T_3 = FuzzySet(function=Triangular_MF(a=-0.3, b=0, c=0.3), term="steady")
T_4 = FuzzySet(function=Triangular_MF(a=0, b=0.3, c=0.6), term="openSlow")
T_5 = FuzzySet(function=Triangular_MF(a=0.3, b=0.6, c=1), term="openFast")
FS.add_linguistic_variable("cold", LinguisticVariable([T_1, T_2, T_3, T_4, T_5], concept="Water cold",
                                                      universe_of_discourse=[-1, 1]))

# Mamdani: Define fuzzy sets, linguistic variables and universe of discoures foroutput hot
H_1 = FuzzySet(function=Triangular_MF(a=-1, b=-0.6, c=-0.3), term="closeFast")
H_2 = FuzzySet(function=Triangular_MF(a=-0.6, b=-0.3, c=0), term="closeSlow")
H_3 = FuzzySet(function=Triangular_MF(a=-0.3, b=0, c=0.3), term="steady")
H_4 = FuzzySet(function=Triangular_MF(a=0, b=0.3, c=0.6), term="openSlow")
H_5 = FuzzySet(function=Triangular_MF(a=0.3, b=0.6, c=1), term="openFast")
FS.add_linguistic_variable("hot", LinguisticVariable([H_1, H_2, H_3, H_4, H_5], concept="Hot cold",
                                                     universe_of_discourse=[-1, 1]))
FS.produce_figure(outputfile='Hot water regulator', max_figures_per_row=4)

# Define fuzzy rules
R_1 = "IF (Temp IS cold) AND (Flow IS soft) THEN (cold IS openSlow)"
R_2 = "IF (Temp IS cold) AND (Flow IS soft) THEN (hot IS openFast)"
R_3 = "IF (Temp IS cold) AND (Flow IS good) THEN (cold IS closeSlow)"
R_4 = "IF (Temp IS cold) AND (Flow IS good) THEN (hot IS openSlow)"
R_5 = "IF (Temp IS cold) AND (Flow IS hard) THEN (cold IS closeFast)"
R_6 = "IF (Temp IS cold) AND (Flow IS hard) THEN (hot IS closeSlow)"
R_7 = "IF (Temp IS good) AND (Flow IS soft) THEN (cold IS openSlow)"
R_8 = "IF (Temp IS good) AND (Flow IS soft) THEN (hot IS openSlow)"
R_9 = "IF (Temp IS good) AND (Flow IS good) THEN (cold IS steady)"
R_10 = "IF (Temp IS good) AND (Flow IS good) THEN (hot IS steady)"
R_11 = "IF (Temp IS good) AND (Flow IS hard) THEN (cold IS closeSlow)"
R_12 = "IF (Temp IS good) AND (Flow IS hard) THEN (hot IS closeSlow)"
R_13 = "IF (Temp IS hot) AND (Flow IS soft) THEN (cold IS openFast)"
R_14 = "IF (Temp IS hot) AND (Flow IS soft) THEN (hot IS openSlow)"
R_15 = "IF (Temp IS hot) AND (Flow IS good) THEN (cold IS openSlow)"
R_16 = "IF (Temp IS hot) AND (Flow IS good) THEN (hot IS closeSlow)"
R_17 = "IF (Temp IS hot) AND (Flow IS hard) THEN (cold IS closeSlow)"
R_18 = "IF (Temp IS hot) AND (Flow IS hard) THEN (hot IS closeFast)"
FS.add_rules([R_1, R_2, R_3, R_4, R_5, R_6, R_7, R_8, R_9, R_10, R_11, R_12, R_13, R_14, R_15, R_16, R_17, R_18])

# Start variables
FS.set_variable("Temp", 0)
FS.set_variable("Flow", 0)
set_temp = 20
set_cold = 10
set_hot = 30
set_flow = 0
start_time = time.time()
prev_cold = 00
prev_hot = 00
runtime = 0
last_time = 0.1
dt = 0
x = []
y = []
z = []
flow_set = []
temp_set = []

while True:  # the environment
    dt = time.time() - last_time
    last_time = time.time()
    if 3 <= runtime <= 8:  # Step-response
        set_temp = 23
        set_flow = 0.7
    else:
        set_temp = 20
        set_flow = 0.5

    cold = FS.inference()['cold']  # Get the outputs from the fuzzylogic
    hot = FS.inference()['hot']  # Get the outputs from the fuzzylogic

    flow_rate_hot, hot_mem = ctr.hot_valve(hot, prev_hot, dt)  # Logic for the valves
    flow_rate_cold, cold_mem = ctr.cold_valve(cold, prev_cold, dt)  # Logic for the valves
    prev_hot = hot_mem  # To integrate the loop needs memory and without classes this is the easiest way
    prev_cold = cold_mem  # To integrate the loop needs memory and without classes this is the easiest way

    temp = ctr.temp_calc(flow_rate_hot, set_hot, flow_rate_cold, set_cold)  # Calculate the temperatur
    flow_rate = ctr.flow_rate_calc(flow_rate_hot, flow_rate_cold)  # calculate the flowrate

    error_set_temp = temp - set_temp  # calc the temp error
    error_flow_rate = flow_rate - set_flow  # calc the flow error

    FS.set_variable("Temp", error_set_temp)  # input the error into the fuzzy logic
    FS.set_variable("Flow", error_flow_rate)  # input the error into the fuzzy logic

    runtime = time.time() - start_time  # define runtime
    # Gather data
    x.append(runtime)
    y.append(temp)
    z.append(flow_rate)
    temp_set.append(set_temp)
    flow_set.append(set_flow)
    if runtime > 15:  # Set stoptime
        break

# Plot all data
xs = array(x)
ys = array(y)
zs = array(z)
temp_set_s = array(temp_set)
flow_set_s = array(flow_set)
plt.plot(xs, zs, label='Read flow', color='blue')
plt.plot(xs, flow_set_s, label='Set flow', color='green')
plt.xlabel('Time')
plt.ylabel('Flow')
plt.legend()
plt.title('Set flow and read flow vs Time')
plt.tight_layout()
plt.show()

plt.show()
plt.plot(xs, ys, label='Read temp', color='red')
plt.plot(xs, temp_set_s, label='Set temp', color='orange')
plt.xlabel('Time')
plt.ylabel('Temp')
plt.legend()
plt.title('Set temp and read temp vs Time')
plt.tight_layout()
plt.show()
