# justETF Scraping
Scraping the justETF [ETF Screener](https://www.justetf.com/en/find-etf.html).

The most part of the project is implemented as
[Notebook](justetf_scraping/justetf-scraping.ipynb),
but you can easily refactor this to script.

## Examples

### Overview

After [loading](justetf_scraping/justetf-scraping.ipynb#request),
[cleanup](justetf_scraping/justetf-scraping.ipynb#cleanup) and
[enrichment](justetf_scraping/justetf-scraping.ipynb#enrich)
you get `pandas.DataFrame` with over 2670 rows and following structure:

```python
etf_df.head(3)
```

<table>
  <thead>
    <tr>
      <th></th>
      <th>isin</th>
      <th>wkn</th>
      <th>ticker</th>
      <th>valor</th>
      <th>name</th>
      <th>index</th>
      <th>date</th>
      <th>age</th>
      <th>strategy</th>
      <th>domicile_country</th>
      <th>currency</th>
      <th>hedged</th>
      <th>securities_lending</th>
      <th>dividends</th>
      <th>ter</th>
      <th>replication</th>
      <th>size</th>
      <th>asset</th>
      <th>instrument</th>
      <th>region</th>
      <th>at_gettex</th>
      <th>at_xetra</th>
      <th>at_london</th>
      <th>at_euronext</th>
      <th>at_stuttgart</th>
      <th>at_six</th>
      <th>yesterday</th>
      <th>last_week</th>
      <th>last_month</th>
      <th>last_three_months</th>
      <th>last_six_months</th>
      <th>last_year</th>
      <th>last_three_years</th>
      <th>last_five_years</th>
      <th>2021</th>
      <th>2020</th>
      <th>2019</th>
      <th>2018</th>
      <th>last_dividends</th>
      <th>last_year_dividends</th>
      <th>last_year_volatility</th>
      <th>last_three_years_volatility</th>
      <th>last_five_years_volatility</th>
      <th>last_year_return_per_risk</th>
      <th>last_three_years_return_per_risk</th>
      <th>last_five_years_return_per_risk</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CH0496484640</td>
      <td>A22FMC</td>
      <td>21XA</td>
      <td>49648464</td>
      <td>21Shares Bitcoin Suisse Index ETP</td>
      <td>21Shares Bitcoin Suisse</td>
      <td>2019-10-04</td>
      <td>2.645902</td>
      <td>Long-only</td>
      <td>Switzerland</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>2.5</td>
      <td>Physically backed</td>
      <td>28</td>
      <td>Cryptocurrencies</td>
      <td>ETN</td>
      <td>NaN</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>True</td>
      <td>-36.98</td>
      <td>0.00</td>
      <td>-26.43</td>
      <td>-20.32</td>
      <td>-50.02</td>
      <td>-13.95</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>129.88</td>
      <td>252.92</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>72.57</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-0.19</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CH0445689208</td>
      <td>A2TT3D</td>
      <td>21XH</td>
      <td>44568920</td>
      <td>21Shares Crypto Basket Index ETP</td>
      <td>21Shares Crypto Basket</td>
      <td>2018-11-21</td>
      <td>3.514395</td>
      <td>Long-only</td>
      <td>Switzerland</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>2.5</td>
      <td>Physically backed</td>
      <td>111</td>
      <td>Cryptocurrencies</td>
      <td>ETN</td>
      <td>NaN</td>
      <td>True</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>-48.79</td>
      <td>-5.50</td>
      <td>-34.55</td>
      <td>-29.51</td>
      <td>-60.54</td>
      <td>-28.84</td>
      <td>212.12</td>
      <td>NaN</td>
      <td>166.39</td>
      <td>241.24</td>
      <td>20.41</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>77.33</td>
      <td>78.22</td>
      <td>NaN</td>
      <td>-0.37</td>
      <td>0.59</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>IE00B0M62Y33</td>
      <td>A0HGWF</td>
      <td>IUSJ</td>
      <td>2308837</td>
      <td>iShares AEX UCITS ETF</td>
      <td>AEX®</td>
      <td>2005-11-18</td>
      <td>16.530833</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>False</td>
      <td>True</td>
      <td>Distributing</td>
      <td>0.3</td>
      <td>Full replication</td>
      <td>468</td>
      <td>Equity</td>
      <td>ETF</td>
      <td>NaN</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>-13.58</td>
      <td>-1.41</td>
      <td>-1.72</td>
      <td>-5.48</td>
      <td>-14.64</td>
      <td>-2.44</td>
      <td>31.91</td>
      <td>44.49</td>
      <td>29.89</td>
      <td>5.14</td>
      <td>27.55</td>
      <td>-8.05</td>
      <td>1.85</td>
      <td>1.78</td>
      <td>18.34</td>
      <td>20.68</td>
      <td>17.63</td>
      <td>-0.13</td>
      <td>0.47</td>
      <td>0.43</td>
    </tr>
  </tbody>
</table>

### Statistics

For example, visualize the most frequent indices:

```python
index_counts = etf_df["index"].value_counts()
```

```python
sns.histplot(
    etf_df[etf_df["index"].isin(index_counts[index_counts > 7].index)],
    y="index",
    discrete=True,
)
```

![png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAhMAAAEGCAYAAADfUBeRAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8qNh9FAAAACXBIWXMAAAsTAAALEwEAmpwYAAA1LUlEQVR4nO3dd7hcVbnH8e8vhY4CggiCBpBiaCEJxRhKEBEVBSEKiEq4V0F6uSioXIkFC6IgXUCqgkFqFAQiEClSkpCQAqFIwhVEMJRIpCZ57x9rTbIzmTltzsycnPl9nuc8Z2bttvbOPJn3rL32+yoiMDMzM+uqPs3ugJmZmS3bHEyYmZlZTRxMmJmZWU0cTJiZmVlNHEyYmZlZTfo1uwNmjbbmmmvGgAEDmt0NM7NlyqRJk+ZExFqVljmYsJYzYMAAJk6c2OxumJktUyQ9U22Zb3OYmZlZTRxMmJmZWU0cTJiZmVlNHEyYmZlZTRxMmJmZWU0cTJiZmVlNHEyYmZlZTRxMmJmZWU2ctMpaztSpU5HU7G5YA6273vo89/f/a3Y3zHotBxPWct555x32+9Vfm90Na6Axhw5rdhfMejXf5jAzM7OaOJiwbidpgaQpkh6R9LCkYbl9XUnX5teDJH2qhmPcImm1buqymZnVwLc5rB7eiIhBAJI+AfwY2Dki/gGMzOsMAoYCt3TlABHR5UDEzMy6l0cmrN7eBbwCIGmApOmSlgO+D+yXRzD2k7SKpEslTZM0VdK+eZsDctt0ST8t7VTSbElr5n0+JukiSTMk3S5pxaacqZlZi/LIhNXDipKmACsA6wC7FhdGxNuSvgsMjYgjAXKgMDcitszvV5e0LvBTYAgpILld0t4RcWPZ8TYGDoiIr0m6BtgX+E1xBUmHAId072mamRl4ZMLq442IGBQRmwF7AFeo/WcxdwPOLb2JiFeAbYHxEfGviJgP/BbYqcK2syJiSn49CRhQvkJEXBgRQyNiaKfPxszM2uRgwuoqIu4H1gTWquNh3iq8XoBH3MzMGsrBhNWVpM2AvsBLZYteA1YtvB8HHFHYbnXgIWDnPDeiL3AA8Jf69tjMzDrLwYTVw4p5YuUUYAxwUEQsKFvnLmBgaQIm8ENg9TzR8hFgREQ8D5yU130EmBQRNzXuNMzMrCMUEc3ug1lDSQpnwGwtYw4dhv+vM6uNpEnV5p05mLCWoz59An/ul019+sHC+Z3ezLU5zGrXVjDh*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)

## Similar Projects
- https://github.com/AshNL/justETF-overview-scraper
- https://github.com/SimonMandlik/etf_filter

## Thanks
This project was inspired by
[this](https://stackoverflow.com/questions/64813023/scraping-dynamic-datatable-of-many-pages-but-same-url)
Stack Overflow question.
