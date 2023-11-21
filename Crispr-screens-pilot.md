# Pilot analysis of CRISPR-cas screen raw count


```python
# load required libraries
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr  
import seaborn as sns
import matplotlib.pyplot as plt
```


```python
df = pd.read_csv("DEM_rand1.readcounts")
```


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Gene</th>
      <th>CTRL Replicate 1</th>
      <th>CTRL Replicate 2</th>
      <th>TEST Replicate 1</th>
      <th>TEST Replicate 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None_001</td>
      <td>None</td>
      <td>230</td>
      <td>220</td>
      <td>253</td>
      <td>212</td>
    </tr>
    <tr>
      <th>1</th>
      <td>None_002</td>
      <td>None</td>
      <td>278</td>
      <td>288</td>
      <td>264</td>
      <td>309</td>
    </tr>
    <tr>
      <th>2</th>
      <td>None_003</td>
      <td>None</td>
      <td>80</td>
      <td>70</td>
      <td>57</td>
      <td>59</td>
    </tr>
    <tr>
      <th>3</th>
      <td>None_004</td>
      <td>None</td>
      <td>208</td>
      <td>200</td>
      <td>212</td>
      <td>192</td>
    </tr>
    <tr>
      <th>4</th>
      <td>None_005</td>
      <td>None</td>
      <td>107</td>
      <td>108</td>
      <td>106</td>
      <td>115</td>
    </tr>
  </tbody>
</table>
</div>




```python
# take a glimse on the data
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 12334 entries, 0 to 12333
    Data columns (total 6 columns):
     #   Column            Non-Null Count  Dtype 
    ---  ------            --------------  ----- 
     0   Name              12334 non-null  object
     1   Gene              12334 non-null  object
     2   CTRL Replicate 1  12334 non-null  int64 
     3   CTRL Replicate 2  12334 non-null  int64 
     4   TEST Replicate 1  12334 non-null  int64 
     5   TEST Replicate 2  12334 non-null  int64 
    dtypes: int64(4), object(2)
    memory usage: 578.3+ KB



```python
# check rows
len(df)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Input In [14], in <cell line: 2>()
          1 # check d
    ----> 2 dim(df)


    NameError: name 'dim' is not defined



```python
# unique genes in the library
unique_genes = np.unique(df[["Gene"]])
f'There are {len(unique_genes)} number of unqiue genes in the library'
```




    'There are 1095 number of unqiue genes in the library'



**Check correlation between replicates**


```python
# get column names
cols = df.columns

# control 
ctrl1 = np.array(df[cols[2]])
ctrl2 = np.array(df[cols[3]])
# correlation between control replicates
print(f'Correlation between control replicates is {pearsonr(ctrl1, ctrl2)[0]}')

# test
test1 = np.array(df[cols[4]])
test2 = np.array(df[cols[5]])
# correlation between test replicates
print(f'Correlation between test replicates is {pearsonr(test1, test2)[0]}')
```

    Correlation between control replicates is 0.9826003154957155
    Correlation between test replicates is 0.9594166762478604



```python
# visualizing the correlations altogether
corrMat = df.corr()
corrPlot = sns.heatmap(corrMat, linewidths=1, square=True, cmap='Blues')
plt.title('Correlation Matrix of Replicates')
plt.show()
```


    
![png](output_9_0.png)
    


**Normalization**


```python
# get individual sum of columns
colSums = list()
for i in range(2,6):
    cs = df[cols[i]].sum()
    colSums.append(cs)

colSums
```




    [1646338, 1648400, 1647911, 1642175]




```python
def cpm(counts):
    """Calculate read counts per 10 million reads given by,
    CPM = (C / S) * 10^7
    
    Where:
    C = read counts (values) 
    S = Column-sum 

    @param: counts, read counts for single replicate
    @return: n_counts, normalized counts
    """
    # sum each column to get total reads per sample
    S = counts.sum()
    C = counts
    # apply formula
    n_counts =  (C / S) * 1e7
    return(round(n_counts, 2))
```


```python
# apply the cpm function on each replicate
t_df = df
for i in range(2,6):
    t_df[cols[i]] = cpm(df[cols[i]])
```


```python
# check the transformed data
t_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Gene</th>
      <th>CTRL Replicate 1</th>
      <th>CTRL Replicate 2</th>
      <th>TEST Replicate 1</th>
      <th>TEST Replicate 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None_001</td>
      <td>None</td>
      <td>139.70</td>
      <td>133.46</td>
      <td>153.53</td>
      <td>129.10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>None_002</td>
      <td>None</td>
      <td>168.86</td>
      <td>174.71</td>
      <td>160.20</td>
      <td>188.17</td>
    </tr>
    <tr>
      <th>2</th>
      <td>None_003</td>
      <td>None</td>
      <td>48.59</td>
      <td>42.47</td>
      <td>34.59</td>
      <td>35.93</td>
    </tr>
    <tr>
      <th>3</th>
      <td>None_004</td>
      <td>None</td>
      <td>126.34</td>
      <td>121.33</td>
      <td>128.65</td>
      <td>116.92</td>
    </tr>
    <tr>
      <th>4</th>
      <td>None_005</td>
      <td>None</td>
      <td>64.99</td>
      <td>65.52</td>
      <td>64.32</td>
      <td>70.03</td>
    </tr>
  </tbody>
</table>
</div>



**The effect on the data**
The transformation generally helps the create a relative measure across all the genes. It scales on the data on a unified scale so that there is no biasness of technical or non-technical errors and it prevents skewness or one-sided variance. Furthermore, to understand the reproducibility of the values across the replicate samples we can draw a distribution curve to check any outliers as a starter for pre-processsing.

**Average log2FC**


```python
lfc_df = t_df
# get averages of each replicate group
# control
avg1 = (lfc_df[cols[2]] + lfc_df[cols[3]]) / 2
avg_ctrl = round(avg1, 2)
# test
avg2 = (lfc_df[cols[4]] + lfc_df[cols[5]]) / 2
avg_test = round(avg2, 2)

# calculate log2 fold-change between TEST and CTRL -- stored in "L2FC"
lfc_df["L2FC"] = np.log2(avg_test / avg_ctrl)

# check the log2 fold-change values
lfc_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Gene</th>
      <th>CTRL Replicate 1</th>
      <th>CTRL Replicate 2</th>
      <th>TEST Replicate 1</th>
      <th>TEST Replicate 2</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None_001</td>
      <td>None</td>
      <td>1397.04</td>
      <td>1334.63</td>
      <td>1535.28</td>
      <td>1290.97</td>
      <td>0.049095</td>
    </tr>
    <tr>
      <th>1</th>
      <td>None_002</td>
      <td>None</td>
      <td>1688.60</td>
      <td>1747.15</td>
      <td>1602.03</td>
      <td>1881.65</td>
      <td>0.019983</td>
    </tr>
    <tr>
      <th>2</th>
      <td>None_003</td>
      <td>None</td>
      <td>485.93</td>
      <td>424.65</td>
      <td>345.89</td>
      <td>359.28</td>
      <td>-0.368835</td>
    </tr>
    <tr>
      <th>3</th>
      <td>None_004</td>
      <td>None</td>
      <td>1263.41</td>
      <td>1213.30</td>
      <td>1286.48</td>
      <td>1169.18</td>
      <td>-0.012320</td>
    </tr>
    <tr>
      <th>4</th>
      <td>None_005</td>
      <td>None</td>
      <td>649.93</td>
      <td>655.18</td>
      <td>643.24</td>
      <td>700.29</td>
      <td>0.041857</td>
    </tr>
  </tbody>
</table>
</div>



**a. Plot a histogram of all log2 fold-change values**


```python
sns.set(style="darkgrid")
sns.histplot(lfc_df, x="L2FC")
plt.show()
```


    
![png](output_19_0.png)
    


**Devise a metric to compare the LFCs of all elements associated with a gene compared to the LFC of all 'Safe' elements**


```python
lfc_df.groupby("Gene")["Name"].count()
```




    Gene
    GENE0001     10
    GENE0002     10
    GENE0003     10
    GENE0004     10
    GENE0005     10
               ... 
    GENE1091     10
    GENE1092     10
    GENE1093     10
    None        750
    Safe        750
    Name: Name, Length: 1095, dtype: int64




```python
# get subset data for 'all' and 'safe' genes and sort them
x = lfc_df.loc[(lfc_df['Gene'] != 'None')]
y = x.loc[(x['Gene'] != 'Safe')]

# Sorting by column "Population"
all_genes = y.sort_values(by=['L2FC'], ascending=True)
all_genes
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Gene</th>
      <th>CTRL Replicate 1</th>
      <th>CTRL Replicate 2</th>
      <th>TEST Replicate 1</th>
      <th>TEST Replicate 2</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1834</th>
      <td>GENE0034_010</td>
      <td>GENE0034</td>
      <td>1524.60</td>
      <td>1637.95</td>
      <td>6.07</td>
      <td>140.06</td>
      <td>-4.435867</td>
    </tr>
    <tr>
      <th>8244</th>
      <td>GENE0681_008</td>
      <td>GENE0681</td>
      <td>109.33</td>
      <td>103.13</td>
      <td>6.07</td>
      <td>6.09</td>
      <td>-4.126976</td>
    </tr>
    <tr>
      <th>11706</th>
      <td>GENE1030_007</td>
      <td>GENE1030</td>
      <td>127.56</td>
      <td>181.99</td>
      <td>12.14</td>
      <td>6.09</td>
      <td>-4.085041</td>
    </tr>
    <tr>
      <th>2859</th>
      <td>GENE0137_008</td>
      <td>GENE0137</td>
      <td>273.33</td>
      <td>121.33</td>
      <td>6.07</td>
      <td>18.27</td>
      <td>-4.019209</td>
    </tr>
    <tr>
      <th>10435</th>
      <td>GENE0902_002</td>
      <td>GENE0902</td>
      <td>109.33</td>
      <td>139.53</td>
      <td>6.07</td>
      <td>12.18</td>
      <td>-3.770157</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>10567</th>
      <td>GENE0915_007</td>
      <td>GENE0915</td>
      <td>6.07</td>
      <td>6.07</td>
      <td>18.20</td>
      <td>24.36</td>
      <td>1.809730</td>
    </tr>
    <tr>
      <th>9642</th>
      <td>GENE0822_008</td>
      <td>GENE0822</td>
      <td>6.07</td>
      <td>6.07</td>
      <td>24.27</td>
      <td>24.36</td>
      <td>2.002375</td>
    </tr>
    <tr>
      <th>7177</th>
      <td>GENE0574_003</td>
      <td>GENE0574</td>
      <td>30.37</td>
      <td>6.07</td>
      <td>84.96</td>
      <td>85.25</td>
      <td>2.223636</td>
    </tr>
    <tr>
      <th>6562</th>
      <td>GENE0512_003</td>
      <td>GENE0512</td>
      <td>6.07</td>
      <td>6.07</td>
      <td>54.61</td>
      <td>60.89</td>
      <td>3.250053</td>
    </tr>
    <tr>
      <th>11908</th>
      <td>GENE1051_004</td>
      <td>GENE1051</td>
      <td>6.07</td>
      <td>6.07</td>
      <td>48.55</td>
      <td>127.88</td>
      <td>3.861337</td>
    </tr>
  </tbody>
</table>
<p>10834 rows × 7 columns</p>
</div>




```python
z = lfc_df.loc[lfc_df['Gene'] == 'Safe']
safe_genes = z.sort_values(by=['L2FC'], ascending=True)
safe_genes
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Gene</th>
      <th>CTRL Replicate 1</th>
      <th>CTRL Replicate 2</th>
      <th>TEST Replicate 1</th>
      <th>TEST Replicate 2</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1293</th>
      <td>Safe_544</td>
      <td>Safe</td>
      <td>1403.11</td>
      <td>1389.23</td>
      <td>673.58</td>
      <td>267.94</td>
      <td>-1.568411</td>
    </tr>
    <tr>
      <th>1180</th>
      <td>Safe_431</td>
      <td>Safe</td>
      <td>164.00</td>
      <td>133.46</td>
      <td>72.82</td>
      <td>42.63</td>
      <td>-1.365552</td>
    </tr>
    <tr>
      <th>1023</th>
      <td>Safe_274</td>
      <td>Safe</td>
      <td>741.04</td>
      <td>752.24</td>
      <td>151.71</td>
      <td>444.53</td>
      <td>-1.324520</td>
    </tr>
    <tr>
      <th>922</th>
      <td>Safe_173</td>
      <td>Safe</td>
      <td>230.82</td>
      <td>212.33</td>
      <td>84.96</td>
      <td>97.43</td>
      <td>-1.280722</td>
    </tr>
    <tr>
      <th>1249</th>
      <td>Safe_500</td>
      <td>Safe</td>
      <td>188.30</td>
      <td>145.60</td>
      <td>97.09</td>
      <td>54.81</td>
      <td>-1.136294</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>906</th>
      <td>Safe_157</td>
      <td>Safe</td>
      <td>212.59</td>
      <td>224.46</td>
      <td>382.30</td>
      <td>438.44</td>
      <td>0.909160</td>
    </tr>
    <tr>
      <th>1343</th>
      <td>Safe_594</td>
      <td>Safe</td>
      <td>18.22</td>
      <td>18.20</td>
      <td>36.41</td>
      <td>36.54</td>
      <td>1.001979</td>
    </tr>
    <tr>
      <th>861</th>
      <td>Safe_112</td>
      <td>Safe</td>
      <td>54.67</td>
      <td>72.80</td>
      <td>127.43</td>
      <td>127.88</td>
      <td>1.002036</td>
    </tr>
    <tr>
      <th>1246</th>
      <td>Safe_497</td>
      <td>Safe</td>
      <td>115.41</td>
      <td>139.53</td>
      <td>424.78</td>
      <td>97.43</td>
      <td>1.034445</td>
    </tr>
    <tr>
      <th>1282</th>
      <td>Safe_533</td>
      <td>Safe</td>
      <td>42.52</td>
      <td>78.86</td>
      <td>236.66</td>
      <td>182.68</td>
      <td>1.788590</td>
    </tr>
  </tbody>
</table>
<p>750 rows × 7 columns</p>
</div>



In order to compare these two unequal pair of samples for extrapolating key information regarding their association -- we can check whether they originate from the same distribution using Wilcoxon's Rank Sum test.


```python
# extracting the LFC values from both data
sample1 = all_genes['L2FC']
sample2 = safe_genes['L2FC']
# conducting wilcoxon rank-sum statistic using scipy
from scipy.stats import ranksums
ranksums(sample1, sample2)
```




    RanksumsResult(statistic=1.9738477048326595, pvalue=0.048399062591262344)



We can observe that the p-value is almost at the threshold (>=0.05). Hence, we accept the hypothesis that these two samples are potentially from the same distribution and therefore there is a significant association between them.


```python
# Comparing the top five genes with the most negative LFC compared to "Safe" 
most_neg1 = all_genes[['Name', 'L2FC']][:5]
most_neg1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1834</th>
      <td>GENE0034_010</td>
      <td>-4.435867</td>
    </tr>
    <tr>
      <th>8244</th>
      <td>GENE0681_008</td>
      <td>-4.126976</td>
    </tr>
    <tr>
      <th>11706</th>
      <td>GENE1030_007</td>
      <td>-4.085041</td>
    </tr>
    <tr>
      <th>2859</th>
      <td>GENE0137_008</td>
      <td>-4.019209</td>
    </tr>
    <tr>
      <th>10435</th>
      <td>GENE0902_002</td>
      <td>-3.770157</td>
    </tr>
  </tbody>
</table>
</div>




```python
most_neg2 = safe_genes[['Name', 'L2FC']][:5]
most_neg2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1293</th>
      <td>Safe_544</td>
      <td>-1.568411</td>
    </tr>
    <tr>
      <th>1180</th>
      <td>Safe_431</td>
      <td>-1.365552</td>
    </tr>
    <tr>
      <th>1023</th>
      <td>Safe_274</td>
      <td>-1.324520</td>
    </tr>
    <tr>
      <th>922</th>
      <td>Safe_173</td>
      <td>-1.280722</td>
    </tr>
    <tr>
      <th>1249</th>
      <td>Safe_500</td>
      <td>-1.136294</td>
    </tr>
  </tbody>
</table>
</div>




```python
# similarly, comparing the top five genes with the most positive LFC compared to "Safe"
most_pos1 = all_genes[['Name', 'L2FC']][len(all_genes)- 5:]
most_pos1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10567</th>
      <td>GENE0915_007</td>
      <td>1.809730</td>
    </tr>
    <tr>
      <th>9642</th>
      <td>GENE0822_008</td>
      <td>2.002375</td>
    </tr>
    <tr>
      <th>7177</th>
      <td>GENE0574_003</td>
      <td>2.223636</td>
    </tr>
    <tr>
      <th>6562</th>
      <td>GENE0512_003</td>
      <td>3.250053</td>
    </tr>
    <tr>
      <th>11908</th>
      <td>GENE1051_004</td>
      <td>3.861337</td>
    </tr>
  </tbody>
</table>
</div>




```python
most_pos2 = safe_genes[['Name', 'L2FC']][len(safe_genes)- 5:]
most_pos2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>L2FC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>906</th>
      <td>Safe_157</td>
      <td>0.909160</td>
    </tr>
    <tr>
      <th>1343</th>
      <td>Safe_594</td>
      <td>1.001979</td>
    </tr>
    <tr>
      <th>861</th>
      <td>Safe_112</td>
      <td>1.002036</td>
    </tr>
    <tr>
      <th>1246</th>
      <td>Safe_497</td>
      <td>1.034445</td>
    </tr>
    <tr>
      <th>1282</th>
      <td>Safe_533</td>
      <td>1.788590</td>
    </tr>
  </tbody>
</table>
</div>



**b. Verify your findings by plotting the LFCs of your selected genes against the same number of random "Safe" LFCs**


```python
# verifying our findings using regression plot
# for negative LFC values (All vs Safe)
az = sns.regplot(most_neg2['L2FC'], most_neg1['L2FC'])
az.set(xlabel='Safe',
       ylabel='All',
       title='Negative LFC values')
plt.show()
```

    /Users/yogeshmaithania/opt/anaconda3/lib/python3.9/site-packages/seaborn/_decorators.py:36: FutureWarning: Pass the following variables as keyword args: x, y. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      warnings.warn(



    
![png](output_32_1.png)
    



```python
# for positive LFC values (All vs Safe)
ab = sns.regplot(most_pos2['L2FC'], most_pos1['L2FC'])
ab.set(xlabel='Safe',
       ylabel='All',
       title='Positive LFC values')
```

    /Users/yogeshmaithania/opt/anaconda3/lib/python3.9/site-packages/seaborn/_decorators.py:36: FutureWarning: Pass the following variables as keyword args: x, y. From version 0.12, the only valid positional argument will be `data`, and passing other arguments without an explicit keyword will result in an error or misinterpretation.
      warnings.warn(





    [Text(0.5, 0, 'Safe'),
     Text(0, 0.5, 'All'),
     Text(0.5, 1.0, 'Positive LFC values')]




    
![png](output_33_2.png)
    


From the visualizations, we can infer that there was a decent linear regression trend when we mapped the negative LFC values, however, the positive plot gave an usual trend suggesting more reliable tests needed in the future to draw firm conclusions on our association hypothesis.
