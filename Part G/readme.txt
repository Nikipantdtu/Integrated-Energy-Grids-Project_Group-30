1. Model Modifications

New Energy Carrier: Introduced CH4 (Natural Gas) and created dedicated gas buses for DE, FR, CH, and AT.

Linear Gas Transport: Replaced physical AC lines with Link components for cross-border gas pipelines. This means gas transport is strictly linearly optimized, without being restricted by Kirchhoff’s laws or loop flows.

Sector Coupling: Connected the electrical and gas buses using Power-to-Gas (P2G) and Open Cycle Gas Turbines (OCGT), both modelled as Link components.

External Gas Market: Modelled an external gas supply by adding a Generator to the CH4 buses, allowing the system to buy gas from outside.

2. New Parameters

Gas Price: Set at 17.3 €/MWh (based on 2017 European benchmark prices).

Conversion Efficiencies: Applied the specific efficiencies for P2G (~60%)

CAPEX: Updated the annualized capital costs for the coupling infrastructure (Pipelines, P2G, OCGT, and Gas Storage).

3. Key Results

Gas crushes Electricity in transport: The gas network transported 809 TWh, nearly 5 times the 162 TWh transported by the AC grid! The solver heavily favored expanding cheap pipelines to bypass the heavily congested electrical grid.

P2G is dead (for now): The optimized capacity for P2G was exactly 0 MW. At a cheap gas import price of 17.3 €/MWh, it makes zero economic sense to use electricity to produce synthetic methane.

Gas generation dominates, Nuclear phases out: Because gas is so cheap and there is no CO2 penalty yet, the model built massive OCGT capacities (especially in France, ~81 GW) and completely phased out expensive base-load generation like nuclear.