#!/usr/bin/env python
# coding: utf-8

# # Modeling and Simulation in Python
# Christopher Pham: Modeling COVID-19 in Santa Clara County
# Using the model from Chapter 11
# 
# Chapter 11
# Copyright 2017 Allen Downey
# 
# License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0)

# In[2]:


get_ipython().system('pip install pint')
# Configure Jupyter so figures appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Configure Jupyter to display the assigned value after an assignment
get_ipython().run_line_magic('config', "InteractiveShell.ast_node_interactivity='last_expr_or_assign'")

# import functions from the modsim.py module
from modsim import *


# ### SIR implementation
# 
# We'll use a `State` object to represent the number (or fraction) of people in each compartment.

# In[3]:


init = State(S=1-200/60e6-20/60e6-1/60e6-2/60e6, I=200/60e6, D=20/60e6, A=1/60e6, R=2/60e6, T=0, H=0, E=0)


# To convert from number of people to fractions, we divide through by the total.

# In[4]:


init /= sum(init)


# `make_system` creates a `System` object with the given parameters.

# In[5]:


def make_system(alpha, beta, delta, gamma, epsilon, theta, zeta, eta, mu, nu, tau, lamda, rho, kappa, ksi, sigma):
    """Make a system object for the SIR model.
    
    beta: contact rate in days
    gamma: recovery rate in days
    
    returns: System object
    """
    init = State(S=1-200/60e6-20/60e6-1/60e6-2/60e6, I=200/60e6, D=20/60e6, A=1/60e6, R=2/60e6, T=0, H=0, E=0)
    init /= sum(init)

    t0 = 0
    t_end = 7 * 28  # 28 more weeks

    return System(init=init, t0=t0, t_end=t_end,
                  alpha=alpha, beta=beta, delta=delta, gamma=gamma,
                  epsilon=epsilon, theta=theta, zeta=zeta, eta=eta,
                  mu=mu, nu=nu, tau=tau, lamda=lamda,
                  rho=rho, kappa=kappa, ksi=ksi, sigma=sigma)


# Here's an example with hypothetical values for alpha, beta, delta, gamma, epsilon, theta, zeta, eta, mu, nu, tau, lamda, rho, kappa, ksi, sigma.

# In[6]:

alpha = 0.57
beta = 0.011
delta = 0.011 
gamma = 0.456
epsilon = 0.171
theta = 0.371
zeta = 0.125
eta = 0.125
mu = 0.017
nu = 0.027
tau = 0.01
lamda = 0.034
rho = 0.034
kappa = 0.017
ksi = 0.017
sigma = 0.017 

system = make_system(alpha, beta, delta, gamma, epsilon, theta, zeta, eta, mu, nu, tau, lamda, rho, kappa, ksi, sigma)


# The update function takes the state during the current time step and returns the state during the next time step.

# In[7]:


def update_func(state, t, system):
    """Update the SIR model.
    
    state: State with variables S, I, R
    t: time step
    system: System with beta and gamma
    
    returns: State object
    """
    s, i, d, a, r, t, h, e = state

    infected1 = system.alpha * i * s
    infected2 = (system.epsilon + system.ksi + system.lamda) * i
    infected3 = system.epsilon * i
    infected4 = system.zeta * i
    infected5 = system.lamda * i
    
    diagnosed1 = system.beta * d * s
    diagnosed2 = (system.eta + system.rho) * d
    diagnosed3 = system.eta * d
    diagnosed4 = system.rho * d
    
    ailing1 = system.gamma * a * s
    ailing2 = (system.theta + system.mu + system.kappa) * a
    ailing3 = system.theta * a
    ailing4 = system.mu * a
    ailing5 = system.kappa * a
    
    recognized1 = system.delta * r * s
    recognized2 = (system.nu + system.ksi) * r
    recognized3 = system.nu * r
    recognized4 = system.ksi * r
    
    threatened = (system.nu + system.ksi) * t
    threatened1 = system.sigma * t
    
    extinct = system.tau * t
    
    s -= infected1 + diagnosed1 + ailing1 + recognized1
    i += (infected1 + diagnosed1 + ailing1 + recognized1) - infected2
    d += infected3 - diagnosed2
    a += infected4 - ailing2
    r += diagnosed3 + ailing3 - recognized2
    t += ailing4 + recognized3 - threatened
    h += infected5 + diagnosed4 + ailing5 + recognized4 + threatened1
    e += extinct
    
    return State(S=s, I=i, D=d, A=a, R=r, T=t, H=h, E=e)


# To run a single time step, we call it like this:

# In[8]:


state = update_func(init, 0, system)


# Now we can run a simulation by calling the update function for each time step.

# In[9]:


def run_simulation(system, update_func):
    """Runs a simulation of the system.
    
    system: System object
    update_func: function that updates state
    
    returns: State object for final state
    """
    state = system.init
    
    for t in linrange(system.t0, system.t_end):
        state = update_func(state, t, system)
        
    return state


# The result is the state of the system at `t_end`

# In[10]:


run_simulation(system, update_func)


# **Exercise**  Suppose the County lifts the Shelter in Place order now.  After 28 weeks, how many students, total, have been infected?
# 
# Hint: what is the change in `S` between the beginning and the end of the simulation?

# In[11]:


# Solution goes here


# ### Using TimeSeries objects

# If we want to store the state of the system at each time step, we can use one `TimeSeries` object for each state variable.

# In[12]:


def run_simulation(system, update_func):
    """Runs a simulation of the system.
    
    Add three Series objects to the System: S, I, R
    
    system: System object
    update_func: function that updates state
    """
    S = TimeSeries()
    I = TimeSeries()
    D = TimeSeries()
    A = TimeSeries()
    R = TimeSeries()
    T = TimeSeries()
    H = TimeSeries()
    E = TimeSeries()

    state = system.init
    t0 = system.t0
    S[t0], I[t0], D[t0], A[t0], R[t0], T[t0], H[t0], E[t0] = state
    
    for t in linrange(system.t0, system.t_end):
        state = update_func(state, t, system)
        S[t+1], I[t+1], D[t+1], A[t+1], R[t+1], T[t+1], H[t+1], E[t+1] = state
    
    return S, I, D, A, R, T, H, E


# Here's how we call it.

# In[13]:

alpha = 0.57
beta = 0.011
delta = 0.011 
gamma = 0.456
epsilon = 0.171
theta = 0.371
zeta = 0.125
eta = 0.125
mu = 0.017
nu = 0.027
tau = 0.01
lamda = 0.034
rho = 0.034
kappa = 0.017
ksi = 0.017
sigma = 0.017 

system = make_system(alpha, beta, delta, gamma, epsilon, theta, zeta, eta, mu, nu, tau, lamda, rho, kappa, ksi, sigma)
S, I, D, A, R, T, H, E = run_simulation(system, update_func)


# And then we can plot the results.

# In[14]:


def plot_results(S, I, D, A, R, T, H, E):
    """Plot the results of a SIR model.
    
    S: TimeSeries
    I: TimeSeries
    R: TimeSeries
    """
    plot(S, '--', label='Susceptible')
    plot(I, '-', label='Infected')
    plot(D, ':', label='Diagnosed')
    plot(A, '--', label='Ailing')
    plot(R, '-', label='Recognized')
    plot(T, ':', label='Threatened')
    plot(H, '--', label='Healed')
    plot(E, '-', label='Extinct')
    decorate(xlabel='Time (days)',
             ylabel='Fraction of population')


# Here's what they look like.

# In[19]:


plot_results(S, I, D, A, R, T, H, E)
savefig('D:/Spring 2022/SIR-Fig01.pdf')


# ### Using a DataFrame

# Instead of making three `TimeSeries` objects, we can use one `DataFrame`.
# 
# We have to use `row` to selects rows, rather than columns.  But then Pandas does the right thing, matching up the state variables with the columns of the `DataFrame`.

# In[20]:


def run_simulation(system, update_func):
    """Runs a simulation of the system.
        
    system: System object
    update_func: function that updates state
    
    returns: TimeFrame
    """
    frame = TimeFrame(columns=system.init.index)
    frame.row[system.t0] = system.init
    
    for t in linrange(system.t0, system.t_end):
        frame.row[t+1] = update_func(frame.row[t], t, system)
    
    return frame


# Here's how we run it, and what the result looks like.

# In[21]:

alpha = 0.57
beta = 0.011
delta = 0.011 
gamma = 0.456
epsilon = 0.171
theta = 0.371
zeta = 0.125
eta = 0.125
mu = 0.017
nu = 0.027
tau = 0.01
lamda = 0.034
rho = 0.034
kappa = 0.017
ksi = 0.017
sigma = 0.017 

system = make_system(alpha, beta, delta, gamma, epsilon, theta, zeta, eta, mu, nu, tau, lamda, rho, kappa, ksi, sigma)
results = run_simulation(system, update_func)
results.head()


# We can extract the results and plot them.

# In[22]:


plot_results(results.S, results.I, results.D, results.A, results.R, results.T, results.H, results.E)


# In[ ]:




