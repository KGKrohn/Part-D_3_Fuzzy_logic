import numpy as np


def hot_valve(valve_input, last_u, dt):
    u = last_u + (valve_input * dt)  # Calculate the integrator
    k = 1  # constant scaling
    u2 = 1  # variation
    u = np.clip(u, 0.15, 2)  # set upper and lower limits
    flow_rate_hot = k * u * ((k * u) <= u2) + u2 * ((k * u) > u2)
    return flow_rate_hot, u


def cold_valve(valve_input, last_u, dt):
    u = last_u + (valve_input * dt)  # Calculate the integrator
    k = 1  # constant scaling
    u2 = 1  # variation
    u = np.clip(u, 0.15, 2)  # set upper and lower limits
    flow_rate_cold = k * u * ((k * u) <= u2) + u2 * ((k * u) > u2)
    return flow_rate_cold, u


def flow_rate_calc(flow_rate_hot, flow_rate_cold):  # Combine the flowrates
    flow_rate = flow_rate_hot + flow_rate_cold
    return flow_rate


def temp_calc(flow_rate_hot, hot, flow_rate_cold, cold):  # equation from MATLAB
    temp = (flow_rate_hot * hot + flow_rate_cold * cold) / (flow_rate_hot + flow_rate_cold)
    return temp
