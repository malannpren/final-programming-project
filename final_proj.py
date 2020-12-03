import geopandas as gpd
import pandas as pd
import random
import matplotlib
import matplotlib.pyplot as plt

# data set-up

datatable = {'county': [], 'AcresHarv2012': [], 'AcresHarv2017': []}

from csv import DictReader
Names = ["yuma", "weld", "phillips", "kitcarson", "adams"]

with open(r"C:\Users\catan\Desktop\programming final\AcresTotalsCounty20122017.csv", newline='') as csvfile:
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

cty2012prcp = pd.read_csv(r"C:\Users\catan\Desktop\programming final\cty2012prcp.csv")
cty2017prcp = pd.read_csv(r"C:\Users\catan\Desktop\programming final\cty2017prcp.csv")

prcp_join = cty2012prcp.merge(cty2017prcp, on='county')

# joining precipitation and harvest data

all_data = prcp_join.merge(HarvGdf, on='county')

# creating percent change columns

all_data['prcp_change'] = ((all_data['avg_prcp2017'] - all_data['avg_prcp2012']) / all_data['avg_prcp2012']) * 100
all_data['harv_change'] = ((all_data['AcresHarv2017'] - all_data['AcresHarv2012']) / all_data['AcresHarv2012']) * 100

# exporting final table to csv

all_data.to_csv(r"C:\Users\catan\Desktop\programming final\final_proj.csv", index = False)

# concluding print statement

print("The county with the largest precipitation change is Yuma. The county with the largest acres harvest change is Kit Carson.")

# map creation

fp = r"C:\Users\catan\Desktop\programming final\Colorado_County_Boundaries-shp\Colorado_County_Boundaries.shp"
map_df = gpd.read_file(fp)
map_df['COUNTY'] = map_df['COUNTY'].str.lower()
df = pd.read_csv(r"C:\Users\catan\Desktop\programming final\final_proj.csv", header=0)
merged = map_df.set_index('COUNTY').join(df.set_index('county'))
variable = merged['prcp_change']
vmin, vmax = 0, 100
fig, ax = plt.subplots(1, figsize = (10,6))
merged.plot(column = variable, cmap = 'Blues', linewidth = 0.8, ax = ax, edgecolor = '0.8')
merged
ax.axis('off')
ax.set_title('Colorado Counties Precipitation Change from 2012 to 2017', fontdict={'fontsize': '25', 'fontweight' : '3'})
ax.annotate('Data source: Colorado State University, Warner College; USDA', xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
ax.annotate('Created by Hannah Shook, Mallory Prentiss, and Rachel Tarbet', xy=(0.1, .12),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
plt.colorbar(sm,fraction=0.046, pad=0.0000001)

fig.savefig(r'C:\Users\catan\Desktop\programming final\map_export.png', dpi=300)