# Simple-DSGE-nominal-income-target
In this model I simulate an RBC model with nominal wage rigidities and nominal income target for monetary policy. Inspired by George Selgin's book "Less than zero", I decided to show how negative inflation target can actually work by simulating a simple RBC model

The provided code simulates an economy using a dynamic stochastic general equilibrium (DSGE) model with a Cobb-Douglas production function and NGDP targeting based on those assumptions:

Production Function (Cobb-Douglas):
The economy's production is modeled using the Cobb-Douglas production function. This functional form is widely used in economics to represent the relationship between inputs (capital and labor) and output (GDP). The Cobb-Douglas production function is given by:

Y = A * (K^β) * (L^(1-β))

where:

Y represents output (GDP).
A denotes total factor productivity (TFP) or the level of technology.
K represents the capital stock in the economy.
L represents the labor input.
β is the capital share parameter, indicating the proportion of output attributed to capital (1-β represents the proportion attributed to labor).
NGDP Targeting:
The model assumes a monetary policy objective of targeting Nominal Gross Domestic Product (NGDP) growth at a fixed rate (target_ngdp_growth). NGDP is the total value of goods and services produced in the economy, not adjusted for inflation. By targeting NGDP growth, the central bank aims to stabilize the overall level of economic activity and control inflation.

Stochastic Productivity Shock (AR(1)):
To capture the uncertainty and randomness in the economy, the model includes a stochastic productivity shock. This shock follows an Autoregressive (AR(1)) process, meaning that its current value depends on its previous value with some persistence (shock_persistence). The productivity shock is generated randomly based on a mean (productivity_shock_mean) and standard deviation (productivity_shock_std). The shock represents temporary fluctuations in the productivity of the economy due to various factors such as technological advancements, external shocks, or business cycle fluctuations.

Consumption and Investment:
Consumption in the economy is determined by a dynamic equation that takes into account nominal wage rigidity (wage_adj). Investment is calculated as the difference between output and consumption. Both consumption and investment decisions are influenced by the productivity shock and NGDP growth rate.

Wage Determination and Unemployment:
The model includes a wage-setting mechanism with nominal wage rigidity. The nominal wage growth is adjusted based on the deviation of the real wage growth from a target rate, which includes the price growth rate and the NGDP target growth rate. This mechanism affects the labor market and, along with the real wage deviation, determines the unemployment rate.

Rental Rate of Capital and Capital Intensity:
The rental rate of capital (R_t) is calculated based on the capital stock and the productivity shock. It represents the return on capital for firms. The model also tracks the capital intensity, which measures the amount of capital used per unit of output. Capital intensity is influenced by changes in the capital stock and real GDP growth.

Economic Indicators and Visualization:
The model calculates various economic indicators: including price growth rate, real GDP growth rate, real wage growth rate, unemployment rate, rental rate of capital, and consumption. The code visualizes these indicators over time using subplots with matplotlib.

Simulation and Results:
The simulation is conducted over a fixed number of time periods (time_periods). The productivity shock and NGDP targeting mechanism drive the dynamics of the economy over time, resulting in fluctuations in economic indicators. The results are stored in arrays and then visualized through plots.

Overall, this economy is a simplified representation of a macroeconomic model with some realistic features, such as productivity shocks and NGDP targeting. It can be used to study the effects of different economic policies, shocks, and structural changes on key economic variables over time. However, it's important to note that the model's simplicity may limit its ability to capture all real-world complexities, and additional features or assumptions may be needed for more comprehensive analysis and policy simulations.
