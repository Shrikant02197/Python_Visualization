import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)

soup = BeautifulSoup(html,'lxml')
type(soup)

title = soup.title
print(title)

text = soup.get_text()
#print(soup.text)
soup.find_all('a')

all_links = soup.find_all('a')
print(all_links)
for link in all_links:
    print(link.get('href'))

print("# Printing the first 10 rows for sanity check")
rows = soup.find_all('tr')
print(rows[:10])

for row in rows:
    row_td = row.find_all('td')
print("row_td")
print(row_td)
type(row_td)
str_cells = str(row_td)

cleantext = BeautifulSoup(str_cells,"lxml").get_text()
print("Clean text below: ")
print(cleantext)

import re
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean,"",str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)
df = pd.DataFrame(list_rows)
print(df.head(10))

df1 = df[0].str.split(",",expand=True)
print(df1.head(10))

df1 = df[0].str.split(",",expand=True)
print(df1.head(10))

col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str,"lxml").get_text()
all_header.append(cleantext2)
print(all_header)

df2 = pd.DataFrame(all_header)
print(df2.head())

df3 = df2[0].str.split(',',expand=True)
print(df3.head())

frames = [df3,df1]
df4 = pd.concat(frames)
print(df4.head(10))
df5 = df4.rename(columns=df4.iloc[0])
print(df5.head())
print(df5.info())
print(df5.shape)

df6 = df5.dropna(axis=0,how='any')
df7 = df6.drop(df6.index[0])
print(df7.head())
df7.rename(columns={'[Place':'Place'},inplace=True)
df7.rename(columns={' Team]':'Team'},inplace=True)
print(df7.head())

df7['Team'] = df7['Team'].str.strip(']')
print(df7.head())
df7['Place'] = df7['Place'].str.strip('[')
print(df7.head())
print(df7.shape)

time_list = df7[' Time'].tolist()
#You can use a for loop to convert 'Time' to minutes
time_mins = []
for i in time_list:
    if i.count(':')==1: #Check for : count
        m, s = i.split(':')
        math = ((int(m) * 60) + int(s))/60
    elif i.count(":")==2: #second also expected
        h, m, s = i.split(':')
        math = (int(h) * 3600 + int(m) * 60 + int(s))/60
    else:
        print("Error occured reading the data")
        math = 0
    time_mins.append(math)
print(time_mins)
df7['Runner_mins'] = time_mins
print(df7.head())

print(df7.describe(include=[np.number]))
from pylab import rcParams
rcParams['figure.figsize'] = 10, 5
df7.boxplot(column='Runner_mins')
plt.grid(True,axis='y')
plt.ylabel('Time')
plt.xticks([1],['Runners'])
plt.title("Time of all the Runners")
plt.show()

#Normal Distribution Graph
x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m',
                  bins=25, hist_kws={'edgecolor':'black'})
plt.show()

f_fuko = df7.loc[df7[' Gender'] == ' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender'] == ' M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False,
             hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko,hist=True, kde=True, rug=False,
             hist_kws={'edgecolor':'black'}, label='Male')
plt.legend()
plt.show()

g_stats = df7.groupby(' Gender', as_index=True).describe()
print(g_stats)

df7.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Time')
plt.suptitle("")
plt.show()