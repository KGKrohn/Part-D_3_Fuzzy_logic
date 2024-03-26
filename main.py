# https://simpful.readthedocs.io/en/latest/index.html
from simpful import *

import matplotlib.pylab as plt
from numpy import linspace, array

FS = FuzzySystem()

# Mean delay Input
M_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=0.1, d=0.3), term="VS")
M_2 = FuzzySet(function=Triangular_MF(a=0.1, b=0.3, c=0.5), term="S")
M_3 = FuzzySet(function=Trapezoidal_MF(a=0.4, b=0.6, c=0.7, d=0.7), term="M")
FS.add_linguistic_variable("mean_delay",
                           LinguisticVariable([M_1, M_2, M_3], concept="mean_delay Quality",
                                              universe_of_discourse=[0, 1]))

FS.plot_variable("mean_delay", outputfile='mean_delay', TGT=None, highlight=None, ax=None,
                 xscale='linear')

# Utility Input
F_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=0.1, d=0.3), term="ranchid")
F_2 = FuzzySet(function=Triangular_MF(a=0, b=10, c=10), term="delicious")
F_3 = FuzzySet(function=Trapezoidal_MF(a=0, b=10, c=10), term="delicious")
FS.add_linguistic_variable("utilisation_factor",
                           LinguisticVariable([F_1, F_2], concept="utilisation_factor quality",
                                              universe_of_discourse=[0, 1]))
FS.plot_variable("utilisation_factor", outputfile='utilisation_factor', TGT=None, highlight=None, ax=None,
                 xscale='linear')

# Servers
S_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=5), term="poor")
S_2 = FuzzySet(function=Triangular_MF(a=0, b=5, c=10), term="good")
S_3 = FuzzySet(function=Triangular_MF(a=5, b=10, c=10), term="excellent")
FS.add_linguistic_variable("mean_delay",
                           LinguisticVariable([S_1, S_2, S_3], concept="mean_delay Quality",
                                              universe_of_discourse=[0, 1]))

FS.plot_variable("mean_delay", outputfile='mean_delay', TGT=None, highlight=None, ax=None,
                 xscale='linear')

# Spares Output
T_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=10), term="small")
T_2 = FuzzySet(function=Triangular_MF(a=0, b=10, c=20), term="average")
T_3 = FuzzySet(function=Trapezoidal_MF(a=10, b=20, c=25, d=25), term="generous")
FS.add_linguistic_variable("number_of_spares",
                           LinguisticVariable([T_1, T_2, T_3], concept="Recommended Tip",
                                              universe_of_discourse=[0, 5]))

FS.produce_figure(outputfile='Nr_Spares', max_figures_per_row=4)

# Sugeno: We know that consequent in sugeno can be constant or a function
# FS.set_crisp_output_value("small", 5)
# FS.set_crisp_output_value("average", 15)
# FS.set_crisp_output_value("generous", 25)
# OR
# FS.set_output_function("generous", "Food+Service+5")

# Define fuzzy rules
R_1 = "IF (Service IS poor) OR (Food IS ranchid) THEN (Tip IS small)"
R_2 = "IF (Service IS good) THEN (Tip IS average)"
R_3 = "IF (Service IS excellent) OR (Food IS delicious) THEN (Tip IS generous)"
FS.add_rules([R_1, R_2, R_3])

# Read inputs from user
FS.set_variable("Service", input('How was the service 0-10?\n'))
FS.set_variable("Food", input('How was the food 0-10?\n'))

# Make inference
print(FS.Mamdani_inference(["Tip"]))

# For Sugeno
# print(FS.Sugeno_inference(["Tip"]))

# Rule firing strength
print(FS.get_firing_strengths())

# FS.plot_variable("Service", outputfile='Service', TGT=1.5, highlight=None, ax=None, xscale = 'linear')

# FS.plot_variable("Food", outputfile='Food', TGT=8.5, highlight=None, ax=None, xscale = 'linear')

input_values = {
    "Service": [5, 5, 5],
    "Food": [6, 6, 6],
}

print(FS.get_firing_strengths(input_values=input_values))

# Plotting surface
xs = []
ys = []
zs = []
DIVs = 20
for x in linspace(0, 10, DIVs):
    for y in linspace(0, 10, DIVs):
        FS.set_variable("Food", x)
        FS.set_variable("Service", y)
        tip = FS.inference()['Tip']
        xs.append(x)
        ys.append(y)
        zs.append(tip)
xs = array(xs)
ys = array(ys)
zs = array(zs)

# from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xx, yy = plt.meshgrid(xs, ys)

ax.plot_trisurf(xs, ys, zs, vmin=0, vmax=25, cmap='gnuplot2')
ax.set_xlabel("Food")
ax.set_ylabel("Service")
ax.set_zlabel("Tip")
ax.set_title("Simpful", pad=20)
ax.set_zlim(0, 25)
plt.tight_layout()
plt.show()

# What todo: Introduce a new linguistic input variable “comfort” and add 2 - 3
# membership functions
# for this input(comfort) variable.Plot the membership functions for this third input variable.Construct some
# rules by including this newly introduced input variable.Display the rules.Evaluate the new fis and observe
# the difference in the result.Generate fuzzy inference system output surface.
