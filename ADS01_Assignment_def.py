import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setting the style using Seaborn directly
sns.set_style("darkgrid")

# Load data
df = pd.read_csv('electricity_prod_source_stacked.csv')
print(df.head())

# Rename columns to more manageable names
df = df.rename(columns={
    'Other renewables excluding bioenergy - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'renewables_other_twh',
    'Electricity from bioenergy - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'bioenergy_twh',
    'Electricity from solar - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'solar_twh',
    'Electricity from wind - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'wind_twh',
    'Electricity from hydro - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'hydro_twh',
    'Electricity from nuclear - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'nuclear_twh',
    'Electricity from oil - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'oil_twh',
    'Electricity from gas - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'gas_twh',
    'Electricity from coal - TWh (adapted for visualization ' 
    'of chart electricity-prod-source-stacked)': 'coal_twh'
})
print(df.head())

# Drop 'Code' column
df = df.drop('Code', axis=1)
print(df.info())

# Filter data for 'World'
df_world = df[df['Entity'] == 'World']
print(df_world.head())

def plot_energy_production(data_frame, title, x_label, y_label, figsize=(8, 6),
                           start_col=2):
    """Plots energy production over time for different energy sources."""
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=figsize)
    for column in data_frame.columns[start_col:]:
        ax.plot(data_frame['Year'], data_frame[column], label=column)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(title='Energy Sources')
    plt.show()

plot_energy_production(
    df_world, 'World Energy Production by Source (1985-2022)', 'Year', 
    'Production in TWh'
)

def plot_pie_for_year(df, year, explode):
    """Plots a pie chart for energy sources in a given year."""
    year_data = df[df['Year'] == year].iloc[0, 2:]
    plt.figure(figsize=(8, 6))
    plt.pie(
        year_data.values, labels=year_data.index, autopct='%1.1f%%',
        startangle=140, explode=explode, pctdistance=0.85
    )
    plt.title(f'World Energy Production Sources in {year}')
    plt.show()

plot_pie_for_year(df_world, 2010, (0.1, 0.1, 0.2, 0.0, 0, 0.3, 0, 0, 0))
plot_pie_for_year(df_world, 2020, (0, 0, 0.1, 0.1, 0, 0.0, 0.3, 0, 0))

def plot_energy_subplots(data_frame, figsize=(15, 10), 
                         title='Distribution of World Energy Production by Source', 
                         grid=False):
    """Generates subplots of boxplots for each energy source."""
    numeric_df = data_frame.select_dtypes(include=[np.number])
    num_cols = numeric_df.shape[1]
    num_rows = int(np.ceil(num_cols / 3))
    
    fig, axes = plt.subplots(num_rows, 3, figsize=figsize, constrained_layout=True)
    fig.suptitle(title)
    axes = axes.flatten() if num_rows > 1 else [axes]
    
    for ax, (col_name, col_data) in zip(axes, numeric_df.items()):
        ax.boxplot(col_data.dropna())
        ax.set_title(col_name)
        ax.set_xlabel('World')
        ax.set_ylabel('Production in TWh')
        ax.grid(grid)
    
    for ax in axes[num_cols:]:
        ax.set_visible(False)

    plt.show()

plot_energy_subplots(df_world.drop('Year', axis=1))
