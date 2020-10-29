"""
Class: CS230--Section 2
Name: Lacey Griffin
Description: (Give a brief description for Exercise name--See below)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source. 
I have not given my code to any student.
"""
import streamlit as st
import pandas as pd
df = pd.read_csv('baseball-salaries-simplified.csv')
st.sidebar.markdown('''Here, you have the option to select the beginning year which will be considered in your baseball data''')
first_year = st.sidebar.slider("Select the First Year", 1988, 2009)
st.sidebar.markdown('''Here, you have the option to select the final year which will be considered in your baseball data''')
last_year = st.sidebar.slider("Select the Last Year", first_year, 2009)
st.sidebar.markdown('''Here, you have the option to select the position which will be considered in your baseball data''')
position = st.sidebar.selectbox("Select a Position", ("OF", "1B", "2B", "3B", "P", "C", "SS", "DH"))
st.title(f'Salary Percentiles for {position} Between {first_year} and {last_year}')
just_2000s = (df.year >= first_year) & (df.year <= last_year)
just_third_base = df.pos == position
focus = df[just_2000s & just_third_base]

# Which years do we care about?
years = range( first_year, last_year )

# We'll store the results in a new DataFrame.
df_pcts = pd.DataFrame( { "year" : years } )

# How to compute a percentile in a given year:
def percentile_in_year ( year, percent ):
    return focus[focus.year == year].salary.quantile( percent/100 )

# Fill the DataFrame using that function.
for percent in range( 0, 110, 10 ):
    df_pcts[percent] = [ percentile_in_year( year, percent ) for year in years ]

# Make years the index.
df_pcts.index = df_pcts.year
del df_pcts['year']

# Change units to millions of dollars.
df_pcts /= 1000000

# See result.
import matplotlib.pyplot as plt
df_pcts.plot( legend='upper left' )
plt.gcf().set_size_inches(8,10)
plt.title( f'Salaries for {position} only, {len(focus)} players', fontsize=20 )
plt.xticks( df_pcts.index, rotation=90 )
plt.ylabel( 'Salary percentiles in $1M', fontsize=14 )
plt.xlabel( None )
st.pyplot()
st.write(f'These are the top 10 salaried {position} players between {first_year} and {last_year}')
st.write(focus.nlargest( 10, 'salary' ).reset_index( drop=True ))

