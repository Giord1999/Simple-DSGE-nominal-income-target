import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# Model Parameters
beta = 0.9
capital_share = 0.6 
depreciation_rate = 0.07  # Depreciation rate
initial_productivity = 1
initial_ngdp = 100  # Initial NGDP
target_ngdp_growth = 0.04  # Target NGDP growth rate
initial_output = initial_productivity * ((1 - beta + depreciation_rate * beta) / (capital_share * initial_productivity * beta))**(capital_share / (capital_share - 1))  # Initial output determined by the production function
initial_capital_stock = ((1 - beta + depreciation_rate * beta) / (capital_share * initial_productivity * beta))**(1 / (capital_share - 1))
productivity_shock_mean = 0.1  # Mean of the productivity shock
productivity_shock_std = 0.05  # Standard deviation of the productivity shock
shock_persistence = 0.8  # Persistence of the shock (AR(1) parameter)
initial_wage = (1-capital_share)* (initial_output/initial_capital_stock) # Initial nominal wage
time_periods = 100  # Number of time periods for the simulation
wage_adj = 0.5  # Parameter to account for nominal wage rigidity

# Calculate equilibrium R
equilibrium_R = (1 - beta + beta * depreciation_rate) / beta

# Calculate investment rate
investment_rate = depreciation_rate * initial_capital_stock

# Arrays to store simulated values
ngdp_values = np.zeros(time_periods)
ngdp_growth_values = np.zeros(time_periods)
real_gdp_growth_values = np.zeros(time_periods)
price_growth_values = np.zeros(time_periods)
wage_values = np.zeros(time_periods)
real_wage_growth_values = np.zeros(time_periods)
investment_values = np.zeros(time_periods)
capital_stock_values = np.zeros(time_periods)
unemployment_rate_values = np.zeros(time_periods)
consumption_values = np.zeros(time_periods)
R_t_values = np.zeros(time_periods)
capital_intensity_values = np.zeros(time_periods)

ngdp_values[0] = initial_ngdp
ngdp_growth_values[0] = 0
real_gdp_growth_values[0] = 0
price_growth_values[0] = 0
wage_values[0] = initial_wage
real_wage_growth_values[0] = 0
investment_values[0] = 0
capital_stock_values[0] = initial_capital_stock
unemployment_rate_values[0] = 0
consumption_values[0] = initial_ngdp - (depreciation_rate * initial_capital_stock)
capital_intensity_values[0] = initial_capital_stock / (initial_output * (1 + real_gdp_growth_values[0]))

# Function to generate a random shock value based on AR(1) process
def generate_productivity_shock(persistence, mean, std, previous_shock, initial_value):
    return persistence * (previous_shock - initial_value) + initial_value + (1 - persistence) * np.random.normal(mean, std)

# Cobb-Douglas production function
def cobb_douglas(output, capital_share, productivity):
    return output**(1 - capital_share) * productivity**capital_share

# Calculate initial real GDP
initial_real_gdp = cobb_douglas(initial_output, capital_share, initial_productivity)

# Simulation of NGDP targeting with stochastic productivity shock (AR(1))
previous_shock = initial_productivity  # Initialize previous shock value

for t in range(1, time_periods):
    # Target NGDP growth
    ngdp_growth = ngdp_values[t-1] * target_ngdp_growth
    # Update NGDP value
    ngdp_values[t] = ngdp_values[t-1] + ngdp_growth
    # NGDP growth rate
    ngdp_growth_values[t] = ngdp_growth / ngdp_values[t-1]

    # Generate productivity shock
    productivity_shock = generate_productivity_shock(shock_persistence, productivity_shock_mean, productivity_shock_std, previous_shock, initial_productivity)
    previous_shock = productivity_shock  # Update previous shock value

    # Productivity with stochastic shock
    productivity = productivity_shock
    # Real GDP growth rate
    real_gdp_growth = cobb_douglas(initial_output, capital_share, productivity) - initial_real_gdp
    # Real GDP growth rate
    real_gdp_growth_values[t] = real_gdp_growth / initial_real_gdp

    # Price growth rate
    price_growth = ngdp_growth_values[t] - real_gdp_growth_values[t]
    price_growth_values[t] = price_growth

    # Nominal wage growth
    nominal_wage_growth = wage_adj * (price_growth + target_ngdp_growth)
    # Real wage growth
    real_wage_growth = nominal_wage_growth - price_growth
    real_wage_growth_values[t] = real_wage_growth

    # Calculate equilibrium real wage
    equilibrium_real_wage = wage_values[t-1] / (1 + price_growth_values[t])

    # Calculate unemployment rate based on real wage deviation from equilibrium
    unemployment_rate = 0.065 + (wage_values[t-1] - equilibrium_real_wage) / equilibrium_real_wage
    unemployment_rate_values[t] = unemployment_rate

    # Investment as the difference between output and consumption
    investment_values[t] = cobb_douglas(initial_output, capital_share, productivity) - consumption_values[t]

    # Update capital stock
    capital_stock_values[t] = capital_stock_values[t-1] + investment_values[t] - depreciation_rate * capital_stock_values[t-1]

    # Update R_t based on the current productivity shock and capital stock
    R_t = capital_share**productivity * capital_stock_values[t]**(capital_share - 1)
    R_t_values[t] = R_t/10

    # Calculate intensity of capital based on real GDP
    capital_intensity = capital_stock_values[t] / (initial_real_gdp * (1 + real_gdp_growth_values[t]))
    capital_intensity_values[t] = capital_intensity

    # Calculate the growth rate of capital intensity
    capital_intensity_growth = capital_intensity_values[t] / capital_intensity_values[t-1] - 1

    # Calculate the increase in NGDP due to capital intensity growth
    ngdp_increase = capital_share * capital_intensity_growth * ngdp_values[t-1]

    # Update NGDP value to account for the increase
    ngdp_values[t] += ngdp_increase

    # Calculate consumption at t+1 based on the updated R_t
    consumption_next_period = beta * (R_t + 1 - depreciation_rate) * consumption_values[t-1]

    # Store the calculated consumption for the next period
    consumption_values[t] = consumption_next_period

    # Update nominal wage with wage rigidity
    wage_values[t] = wage_values[t-1] * (1 + wage_adj * (capital_share * capital_intensity_growth))

# Save the results into Excel
results_df = pd.DataFrame({
    'Period': range(1, time_periods + 1),
    'Price_Growth_Rate': price_growth_values,
    'Real_GDP_Growth_Rate': real_gdp_growth_values,
    'Real_Wage_Growth_Rate': real_wage_growth_values,
    'Unemployment_Rate': unemployment_rate_values,
    'Rental_Rate_of_Capital': R_t_values,
    'Capital_Intensity': capital_intensity_values
})

# Creare i subplot con spaziatura tra i subplot
fig, axs = plt.subplots(3, 2, figsize=(12, 12), sharex=True)
plt.subplots_adjust(hspace=0.5, wspace=0.3)

# Impostare il font family per tutti i subplot
mpl.rcParams['font.family'] = 'cmr10'
mpl.rcParams['axes.formatter.use_mathtext'] = True

# Plot della Price Growth Rate
axs[0, 0].plot(range(1, time_periods + 1), price_growth_values, label='Price Growth Rate')
axs[0, 0].set_ylabel('Percent')
axs[0, 0].set_title('Price Growth Rate')

# Plot della Real GDP Growth Rate
axs[0, 1].plot(range(1, time_periods + 1), real_gdp_growth_values, label='Real GDP Growth Rate')
axs[0, 1].set_ylabel('Percent')
axs[0, 1].set_title('Real GDP Growth Rate')

# Plot della Real Wage Growth Rate
axs[1, 0].plot(range(1, time_periods + 1), real_wage_growth_values, label='Real Wage Growth Rate')
axs[1, 0].set_ylabel('Percent')
axs[1, 0].set_title('Real Wage Growth Rate')

# Plot dell'Unemployment Rate
axs[1, 1].plot(range(1, time_periods + 1), unemployment_rate_values, label='Unemployment Rate', linestyle="--")
axs[1, 1].set_ylabel('Percent')
axs[1, 1].set_title('Unemployment Rate')

# Plot del Rental rate of capital
axs[2, 0].plot(range(1, time_periods + 1), R_t_values, label='Rental rate of capital', linestyle="--", color="navy")
axs[2, 0].set_ylabel('Percent')
axs[2, 0].set_title('Rental rate of capital')

# Plot della Consumption
axs[2, 1].plot(range(1, time_periods + 1), consumption_values, label='Consumption', linestyle="--", color="green")
axs[2, 1].set_ylabel('Percent')
axs[2, 1].set_title('Consumption')

# Visualizzare i subplot
plt.show()