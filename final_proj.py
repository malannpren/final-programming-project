import geopandas as gpd
import pandas as pd
import random
import fiona
import matplotlib
import matplotlib.pyplot as plt

def join_func(left, right, variable):
    "This function performs a join between two tables or variables."

    join = left.merge(right, on=variable)

    return join

# data set-up

datatable = {'county': [], 'AcresHarv2012': [], 'AcresHarv2017': []}

from csv import DictReader
Names = ["yuma", "weld", "phillips", "kit carson", "adams"]

with open(r"C:\Users\catan\Documents\GitHub\final-programming-project\AcresTotalsCounty20122017.csv", newline='') as csvfile:
    reader = DictReader(csvfile)
    
    for row in reader:
        if row['county'] in Names:
            county = row['county']
            AcresHarv2012 = int(row['AcresHarv2012'])
            AcresHarv2017 = int(row['AcresHarv2017'])
            
            datatable['county'].append(county)
            datatable['AcresHarv2012'].append(AcresHarv2012)
            datatable['AcresHarv2017'].append(AcresHarv2017)
    
HarvGdf = gpd.GeoDataFrame(datatable)

# precipitation join

cty2012prcp = pd.read_csv(r"C:\Users\catan\Documents\GitHub\final-programming-project\cty2012prcp.csv")
cty2017prcp = pd.read_csv(r"C:\Users\catan\Documents\GitHub\final-programming-project\cty2017prcp.csv")

prcp_join = join_func(cty2012prcp, cty2017prcp, 'county')

# joining precipitation and harvest data

all_data = join_func(prcp_join, HarvGdf, 'county')

# creating percent change columns

all_data['prcp_change'] = ((all_data['avg_prcp2017'] - all_data['avg_prcp2012']) / all_data['avg_prcp2012']) * 100
all_data['harv_change'] = ((all_data['AcresHarv2017'] - all_data['AcresHarv2012']) / all_data['AcresHarv2012']) * 100

# exporting final table to csv

all_data.to_csv(r"C:\Users\catan\Documents\GitHub\final-programming-project\final_proj.csv", index = False)

# concluding print statement

print("The county with the largest precipitation change is Yuma. The county with the largest acres harvest change is Kit Carson.")

# map creation

fp = r"C:\Users\catan\Documents\GitHub\final-programming-project\Colorado_County_Boundaries.shp"
map_df = gpd.read_file(fp)
map_df['COUNTY'] = map_df['COUNTY'].str.lower()
df = pd.read_csv(r"C:\Users\catan\Documents\GitHub\final-programming-project\final_proj.csv", header=0)
merged = map_df.set_index('COUNTY').join(df.set_index('county'))
merged = map_df.merge(df, left_on='COUNTY', right_on='county')

#prcp change map
variable = merged['prcp_change']
vmin, vmax = 0, 100
fig, ax = plt.subplots(1, figsize = (10,6))
merged.plot(column = variable, cmap = 'Blues', linewidth = 0.8, ax = ax, edgecolor = '0.8')
print(merged)
ax.axis('off')
ax.set_title('Colorado Counties Precipitation Change from 2012 to 2017', fontdict={'fontsize': '16', 'fontweight' : '3'})
ax.annotate('Data source: Colorado State University, Warner College; USDA', xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
ax.annotate('Created by Hannah Shook, Mallory Prentiss, and Rachel Tarbet', xy=(0.1, .12),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
plt.colorbar(sm,fraction=0.046, pad=0.0000001)

fig.savefig(r'C:\Users\catan\Documents\GitHub\final-programming-project\prcp_map.png', dpi=300)

#acres harv map
variable = merged['harv_change']
vmin, vmax = 0, 100
fig, ax = plt.subplots(1, figsize = (10,6))
merged.plot(column = variable, cmap = 'Greens', linewidth = 0.8, ax = ax, edgecolor = '0.8')
print(merged)
ax.axis('off')
ax.set_title('Colorado Counties Acres Harvested Change from 2012 to 2017', fontdict={'fontsize': '16', 'fontweight' : '3'})
ax.annotate('Data source: Colorado State University, Warner College; USDA', xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
ax.annotate('Created by Hannah Shook, Mallory Prentiss, and Rachel Tarbet', xy=(0.1, .12),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

sm = plt.cm.ScalarMappable(cmap='Greens', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
plt.colorbar(sm,fraction=0.046, pad=0.0000001)

fig.savefig(r'C:\Users\catan\Documents\GitHub\final-programming-project\harv_map.png', dpi=300)