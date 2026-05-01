import pypsa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import tempfile

# ==========================================
# 0. Environment and Path Configuration
# ==========================================
# Defining a temporary directory for solver files to avoid permission issues
safe_temp_dir = os.getcwd()

if not os.path.exists(safe_temp_dir):
    os.makedirs(safe_temp_dir)

os.environ['TMPDIR'] = safe_temp_dir
os.environ['TEMP'] = safe_temp_dir
os.environ['TMP'] = safe_temp_dir
tempfile.tempdir = safe_temp_dir

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ==========================================
# 1. Initialize Network and Snapshots
# ==========================================
n = pypsa.Network()

# Hourly snapshots for a full year (8760 hours)
snapshots = pd.date_range("2017-01-01 00:00", "2017-12-31 23:00", freq="H")
n.set_snapshots(snapshots)

# ==========================================
# 2. Build Multi-node Topology (Buses)
# ==========================================
countries = ["DE", "FR", "AT", "CH"]

# Add buses with a nominal voltage of 400 kV
for c in countries:
    n.add("Bus", c, v_nom=400)

# ==========================================
# 3. Add Interconnectors (HVAC Lines)
# ==========================================
interconnectors = {
    "AT-CH": {"bus0": "AT", "bus1": "CH", "s_nom": 2152.75},
    "AT-DE": {"bus0": "AT", "bus1": "DE", "s_nom": 4232.10},
    "CH-DE": {"bus0": "CH", "bus1": "DE", "s_nom": 7106.32},
    "CH-FR": {"bus0": "CH", "bus1": "FR", "s_nom": 2926.94},
    "DE-FR": {"bus0": "DE", "bus1": "FR", "s_nom": 4120.00}
}

for name, params in interconnectors.items():
    n.add("Line", name,
          bus0=params["bus0"],
          bus1=params["bus1"],
          s_nom=params["s_nom"],           # Fixed interconnection capacity
          s_nom_extendable=False,          # Disable capacity expansion for cross-border lines
          x=0.1)                           # Key parameter: Per-unit reactance

# ==========================================
# 4. Generator Configuration for Joint Optimization
# ==========================================
country_techs = {
    "DE": ["Wind Onshore", "Solar", "Fossil Hard coal", "Fossil Gas"], 
    "FR": ["Wind Onshore", "Solar", "Fossil Gas", "Nuclear"],
    "CH": ["Wind Onshore", "Solar", "Hydro Run-of-river and pondage", "Hydro Water Reservoir", "Hydro Pumped Storage"],
    "AT": ["Wind Onshore", "Solar", "Fossil Gas", "Hydro Run-of-river and pondage", "Hydro Water Reservoir", "Hydro Pumped Storage"]
}

costs = {
    "Wind Onshore": {"capital_cost": 103363.0, "marginal_cost": 0.01},
    "Solar": {"capital_cost": 49219.0, "marginal_cost": 0.01},
    "Fossil Gas": {"capital_cost": 66534.0, "marginal_cost": 55.38},      
    "Hydro Run-of-river and pondage": {"capital_cost": 270930.0, "marginal_cost": 0.01},
    "Hydro Water Reservoir": {"capital_cost": 160620.0, "marginal_cost": 0.01},
    "Fossil Hard coal": {"capital_cost": 135000.0, "marginal_cost": 40.0},
    "Nuclear": {"capital_cost": 450000.0, "marginal_cost": 12.0},
    "Hydro Pumped Storage": {"capital_cost": 160000.0, "marginal_cost": 2.0}
}

# List of Variable Renewable Energy Sources (VRES) requiring availability profiles (p_max_pu)
vres_techs = ["Wind Onshore", "Solar", "Hydro Run-of-river and pondage"]

def clean_datetime_index(df):
    if not isinstance(df.index, pd.DatetimeIndex):
        time_str = df.index.astype(str)
        # Handle time interval formats containing " - " (e.g., "00:00 - 01:00")
        if time_str.str.contains(' - ').any():
            time_str = time_str.str.split(' - ').str[0]
        # Remove timezone suffixes like " (CET)" or " (CEST)"
        time_str = time_str.str.replace(r'\s*\(.*?\)', '', regex=True)
        # Force parsing using "Day/Month/Year" format
        df.index = pd.to_datetime(time_str, dayfirst=True)
    return df

# Iterate through countries to populate data
for c in countries:
    # 1. Import and process load data
    df_path = os.path.join(script_dir, f"{c}_Load_d).csv") # Ensure filename matches local file naming convention
    load_df = pd.read_csv(df_path, index_col=0)
    load_df = clean_datetime_index(load_df)
    
    # Clean numeric format (remove commas and convert to float)
    load_series = load_df['Actual Total Load (MW)'].astype(str).str.replace(',', '')
    load_series = pd.to_numeric(load_series, errors='coerce')

    # Resample to hourly and align with network snapshots
    hourly_load = load_series.resample('1h').mean()
    hourly_load = hourly_load.reindex(n.snapshots).fillna(0) 

    n.add("Load", f"{c}_load",
          bus=c,
          p_set=hourly_load.values)
    
    # 2. Import generation data and convert to generator units
    df_path = os.path.join(script_dir, f"{c}_Gene_d).csv")
    gene_df = pd.read_csv(df_path, index_col=0) 
    gene_df = clean_datetime_index(gene_df)
    
    for tech in country_techs[c]:
        cost = costs[tech]
        
        tech_df = gene_df[gene_df['Production Type'] == tech]

def clean_datetime_index(df):
    if not isinstance(df.index, pd.DatetimeIndex):
        time_str = df.index.astype(str)
        # Handle time interval formats containing " - " (e.g., "00:00 - 01:00")
        if time_str.str.contains(' - ').any():
            time_str = time_str.str.split(' - ').str[0]
        # Remove timezone suffixes like " (CET)" or " (CEST)"
        time_str = time_str.str.replace(r'\s*\(.*?\)', '', regex=True)
        # Force parsing using "Day/Month/Year" format
        df.index = pd.to_datetime(time_str, dayfirst=True)
    return df

# Iterate through countries to populate data
for c in countries:
    # 1. Import and process load data
    df_path = os.path.join(script_dir, f"{c}_Load_d).csv") # Ensure filename matches local file naming convention
    load_df = pd.read_csv(df_path, index_col=0)
    load_df = clean_datetime_index(load_df)
    
    # Clean numeric format (remove commas and convert to float)
    load_series = load_df['Actual Total Load (MW)'].astype(str).str.replace(',', '')
    load_series = pd.to_numeric(load_series, errors='coerce')

    # Resample to hourly and align with network snapshots
    hourly_load = load_series.resample('1h').mean()
    hourly_load = hourly_load.reindex(n.snapshots).fillna(0) 

    n.add("Load", f"{c}_load",
          bus=c,
          p_set=hourly_load.values)
    
    # 2. Import generation data and convert to generator units
    df_path = os.path.join(script_dir, f"{c}_Gene_d).csv")
    gene_df = pd.read_csv(df_path, index_col=0) 
    gene_df = clean_datetime_index(gene_df)
    
    for tech in country_techs[c]:
        cost = costs[tech]
        
        tech_df = gene_df[gene_df['Production Type'] == tech]
        
        if tech_df.empty:
            print(f"⚠️ Warning: No valid generation data found for {tech} in {c} within the CSV.")
            continue
            
        # Also force conversion to numeric format
        gen_series = tech_df['Generation (MW)'].astype(str).str.replace(',', '')
        gen_series = pd.to_numeric(gen_series, errors='coerce')

        tech_gen = gen_series.resample('1h').mean()
        tech_gen = tech_gen.reindex(n.snapshots).fillna(0)
        
        if tech_gen.max() == 0:
            print(f"⚠️ Warning: Annual generation data for {tech} in {c} is zero.")
            continue
            
        # A. Variable Renewable Energy Sources (VRES)
        if tech in vres_techs:
            # Create availability profile (p_max_pu)
            p_max_pu_profile = tech_gen / tech_gen.max()
            p_max_pu_profile = np.clip(p_max_pu_profile.values, 0, 1) 
            
            n.add("Generator", f"{c}_{tech}",
                  bus=c,
                  carrier=tech,
                  p_nom_extendable=True,
                  p_max_pu=p_max_pu_profile,
                  capital_cost=cost["capital_cost"],
                  marginal_cost=cost["marginal_cost"])
                  
        # B. Pumped Hydro Storage (modeled as StorageUnit)
        elif tech == "Hydro Pumped Storage":
            n.add("StorageUnit", f"{c}_{tech}",
                  bus=c,
                  carrier=tech,
                  p_nom_extendable=True,
                  capital_cost=cost["capital_cost"],
                  marginal_cost=cost["marginal_cost"],
                  efficiency_store=0.8,     
                  efficiency_dispatch=0.9,  
                  max_hours=6)              
                  
        # C. Conventional Dispatchable Generators
        else:
            n.add("Generator", f"{c}_{tech}",
                  bus=c,
                  carrier=tech,
                  p_nom_extendable=True,
                  capital_cost=cost["capital_cost"],
                  marginal_cost=cost["marginal_cost"])

# ==========================================
# 5. Run DC Optimal Power Flow (DC OPF)
# ==========================================
print("✅ Model construction complete, including the following components:")
print(n.components)
print("\nSystem ready. Starting joint optimization solver...")

# ==========================================
# Task g) Define CH4 Network
# ==========================================

# 1. Define carrier and buses
n.add("Carrier", "CH4")
for c in countries:
    n.add("Bus", f"{c} CH4", carrier="CH4")

# 2. Introduce natural gas benchmark price (17.3 €/MWh)
for c in countries:
    n.add("Generator", f"{c} Gas Market",
          bus=f"{c} CH4",
          carrier="CH4",
          p_nom_extendable=True,
          marginal_cost=17.3)

# 3. Add cross-border natural gas pipelines
for name, params in interconnectors.items():
    n.add("Link", f"{name} CH4 Pipeline",
          bus0=f"{params['bus0']} CH4",
          bus1=f"{params['bus1']} CH4",
          p_nom_extendable=True,
          p_min_pu=-1)

# 4. Establish sector coupling (Power-to-Gas and OCGT)
for c in countries:
    n.add("Link", f"{c} Power-to-Gas",
          bus0=c,              
          bus1=f"{c} CH4",     
          p_nom_extendable=True,
          efficiency=0.6,      
          capital_cost=75000)  
          
    n.add("Link", f"{c} OCGT",
          bus0=f"{c} CH4",     
          bus1=c,              
          p_nom_extendable=True,
          efficiency=0.4,     
          capital_cost=47000)  

# ==========================================
# Operational Optimization: Linear Power Flow (DC Approximation) based on Kirchhoff's Laws
# ==========================================
status, condition = n.optimize(solver_name="gurobi") # Change solver_name if using open-source solvers like glpk or cbc
print(f"Optimization Status: {status}")

if status == "ok":
    print("\n--- Optimized Interconnector Configuration and Loading Factors ---")
    # Calculate the average loading rate of the lines
    loading = (n.lines_t.p0.abs().mean() / n.lines.s_nom) * 100
    print(loading.round(2).astype(str) + " %")

# ==========================================
# 6. Data Extraction (Preparation for subsequent sections)
# ==========================================
if status == "ok":
    print("\n--- Overview of the total power flow of the interconnected lines ---")
    print(n.lines_t.p0.describe())
    
    print("\n--- Optimized generator capacity of each node (in MW) ---")
    print(n.generators.p_nom_opt)
    
    # Get the power flow at the first time step; this is the benchmark for manual PTDF verification in part e)
    print("\n--- Line power at the first time step (MW) ---")
    first_step_flows = n.lines_t.p0.iloc[0]
    print(first_step_flows)
    
    # Save nodal power imbalances (Generation - Demand) at the first time step for part e)
    first_step_imbalance = (n.generators_t.p.iloc[0].groupby(n.generators.bus).sum() 
                            - n.loads_t.p_set.iloc[0].groupby(n.loads.bus).sum())
    print("\n--- Nodal power injection/imbalance at the first time step (MW) ---")
    print(first_step_imbalance)

    # =========================================
    # Supplementary print: View the optimized capacities of Link components (pipelines and conversion facilities)
    # =========================================
    print("\n--- Optimized Link capacities (in MW) ---")
    # Filter out original power grid data, focusing only on the relevant pipelines, P2G, and OCGT
    gas_links = n.links[n.links.index.str.contains("Pipeline|Power-to-Gas|OCGT")]
    print(gas_links.p_nom_opt)

    # =========================================
    # Supplementary print: Comparison of energy transport required for Task g)
    # =========================================
    print("\n--- Task g) Energy Transport Comparison ---")
    # Extract total transport volume of AC transmission lines (MWh)
    total_electricity_transported = n.lines_t.p0.abs().sum().sum()

    # Extract total transport volume of cross-border natural gas pipelines (MWh)
    pipeline_links = n.links.index[n.links.index.str.contains("CH4 Pipeline")]
    total_gas_transported = n.links_t.p0[pipeline_links].abs().sum().sum()

    print(f"Total Electricity Transported: {total_electricity_transported / 1e6:.2f} TWh")
    print(f"Total Gas (CH4) Transported:   {total_gas_transported / 1e6:.2f} TWh")

# ==========================================
# 1. Set bus coordinates (Core trick: slightly offset gas network coordinates)
# ==========================================
countries = ["DE", "FR", "CH", "AT"]
coords = {"DE": [10.45, 50.2], "FR": [2.21, 46.22], "CH": [8.22, 46.81], "AT": [14.55, 47.51]}

# Set power grid bus coordinates
for c in countries:
    n.buses.loc[c, ["x", "y"]] = coords[c]

# Set natural gas bus coordinates (offset to the bottom right to avoid overlap)
offset_x, offset_y = 0.5, -0.4
for c in countries:
    if f"{c} CH4" in n.buses.index: 
        n.buses.loc[f"{c} CH4", ["x", "y"]] = [coords[c][0] + offset_x, coords[c][1] + offset_y]

# ==========================================
# 2. Extract transmission data and set visual parameters
# ==========================================
# Power grid data (Lines)
ac_mean_flow = n.lines_t.p0.mean().abs()

ac_loading = (ac_mean_flow / n.lines.s_nom_opt) * 100 

# Gas network data (Pipelines in Links)
pipeline_links = n.links.index[n.links.index.str.contains("Pipeline")]
gas_mean_flow = n.links_t.p0[pipeline_links].mean().abs()

# Set bus colors (Electricity: light blue, Gas: orange)
bus_colors = pd.Series("lightblue", index=n.buses.index)
bus_colors[n.buses.index.str.contains("CH4")] = "#FFA500" # Orange

# Set line widths 
scale_factor = 1000 
line_widths = ac_mean_flow / scale_factor

link_widths = pd.Series(0.0, index=n.links.index)
link_widths[pipeline_links] = gas_mean_flow / scale_factor

# Set pipeline colors (Natural gas pipelines set to red)
link_colors = pd.Series("lightgray", index=n.links.index)
link_colors[pipeline_links] = "#FF4500" # OrangeRed

# ==========================================
# 3. Plot the network
# ==========================================
fig, ax = plt.subplots(figsize=(12, 9), dpi=150) # 提高分辨率

n.plot(
    ax=ax,
    bus_sizes=0.04,                        
    bus_colors=bus_colors,                
    line_colors=ac_loading,                   
    line_cmap=plt.cm.Blues,            
    line_widths=line_widths,
    link_colors=link_colors,
    link_widths=link_widths,
    title="Comparison of Electricity (AC) vs. Natural Gas (CH4) Energy Transport"
)


plt.title("Comparison of Electricity vs. Gas Energy Transport\nThickness indicates Average Power Flow", 
          y=1.02, fontsize=16, fontweight='bold', pad=15)

# ==========================================
# 4. Add elegant text labels (annotate actual flows)
# ==========================================
# Add average transmission labels to the power grid (blue boxes)
for line_name, line in n.lines.iterrows():
    bus0, bus1 = n.buses.loc[line.bus0], n.buses.loc[line.bus1]
    x_pos, y_pos = (bus0.x + bus1.x) / 2, (bus0.y + bus1.y) / 2 + 0.1
    flow_gw = ac_mean_flow[line_name] / 1000 # 转换为 GW
    
    ax.text(x_pos, y_pos, f"AC: {flow_gw:.1f} GW", 
            fontsize=9, fontweight='bold', color='#003366', ha='center', va='bottom', 
            bbox=dict(facecolor='#E6F2FF', alpha=0.9, edgecolor='#66B2FF', boxstyle='round,pad=0.2'))

# Add average transmission labels to the gas network (orange boxes)
for link_name in pipeline_links:
    link = n.links.loc[link_name]
    bus0, bus1 = n.buses.loc[link.bus0], n.buses.loc[link.bus1]
    x_pos, y_pos = (bus0.x + bus1.x) / 2, (bus0.y + bus1.y) / 2 - 0.1
    flow_gw = gas_mean_flow[link_name] / 1000 # 转换为 GW
    
    ax.text(x_pos, y_pos, f"Gas: {flow_gw:.1f} GW", 
            fontsize=9, fontweight='bold', color='#802200', ha='center', va='top', 
            bbox=dict(facecolor='#FFF0E6', alpha=0.9, edgecolor='#FF9966', boxstyle='round,pad=0.2'))

# Add country labels
for bus_name, bus in n.buses.iterrows():
    if "CH4" not in bus_name: # 只在电网节点标国家名，避免重复
        ax.text(bus.x - 0.2, bus.y + 0.2, bus_name, fontsize=14, fontweight='bold', ha='right')

# ==========================================
# 5. Add custom legend
# ==========================================
legend_elements = [
    mpatches.Patch(facecolor='lightblue', edgecolor='gray', label='Electricity Bus'),
    mpatches.Patch(facecolor='#FFA500', edgecolor='gray', label='Natural Gas Bus'),
    plt.Line2D([0], [0], color='#66B2FF', lw=4, label='AC Transmission Line'),
    plt.Line2D([0], [0], color='#FF4500', lw=4, label='CH4 Pipeline')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11, frameon=True, shadow=True)

ax.axis('off')
plt.tight_layout()
plt.show()