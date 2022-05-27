# justETF Scraping
Scraping the justETF [ETF Screener](https://www.justetf.com/en/find-etf.html).

The most part of the project is implemented as
[Notebook](justetf_scraping/justetf-scraping.ipynb),
but you can easily refactor this to script.

## Examples

After [loading](justetf_scraping/justetf-scraping.ipynb#request),
[cleanup](justetf_scraping/justetf-scraping.ipynb#cleanup) and
[enrichment](justetf_scraping/justetf-scraping.ipynb#enrich)
the data you get `pandas.DataFrame` with over 2670 rows and following structure:

```python
etf_df.head(3)
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
      <th>isin</th>
      <th>wkn</th>
      <th>ticker</th>
      <th>valor</th>
      <th>name</th>
      <th>index</th>
      <th>date</th>
      <th>strategy</th>
      <th>domicile_country</th>
      <th>currency</th>
      <th>securities_lending</th>
      <th>dividends</th>
      <th>ter</th>
      <th>replication</th>
      <th>size</th>
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
      <td>04.10.19</td>
      <td>Long-only</td>
      <td>Switzerland</td>
      <td>USD</td>
      <td>No</td>
      <td>Accumulating</td>
      <td>2.50%</td>
      <td>Physically&lt;br /&gt;backed</td>
      <td>28</td>
      <td>-36.98%</td>
      <td>0.00%</td>
      <td>-26.43%</td>
      <td>-20.32%</td>
      <td>-50.02%</td>
      <td>-13.95%</td>
      <td>-</td>
      <td>-</td>
      <td>129.88%</td>
      <td>252.92%</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>72.57%</td>
      <td>-</td>
      <td>-</td>
      <td>-0.19</td>
      <td>-</td>
      <td>-</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CH0445689208</td>
      <td>A2TT3D</td>
      <td>21XH</td>
      <td>44568920</td>
      <td>21Shares Crypto Basket Index ETP</td>
      <td>21Shares Crypto Basket</td>
      <td>21.11.18</td>
      <td>Long-only</td>
      <td>Switzerland</td>
      <td>USD</td>
      <td>No</td>
      <td>Accumulating</td>
      <td>2.50%</td>
      <td>Physically&lt;br /&gt;backed</td>
      <td>111</td>
      <td>-48.79%</td>
      <td>-5.50%</td>
      <td>-34.55%</td>
      <td>-29.51%</td>
      <td>-60.54%</td>
      <td>-28.84%</td>
      <td>212.12%</td>
      <td>-</td>
      <td>166.39%</td>
      <td>241.24%</td>
      <td>20.41%</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>77.33%</td>
      <td>78.22%</td>
      <td>-</td>
      <td>-0.37</td>
      <td>0.59</td>
      <td>-</td>
    </tr>
    <tr>
      <th>2</th>
      <td>IE00B0M62Y33</td>
      <td>A0HGWF</td>
      <td>IUSJ</td>
      <td>2308837</td>
      <td>iShares AEX UCITS ETF</td>
      <td>AEX®</td>
      <td>18.11.05</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>Yes</td>
      <td>Distributing</td>
      <td>0.30%</td>
      <td>Full replication</td>
      <td>468</td>
      <td>-13.58%</td>
      <td>-1.41%</td>
      <td>-1.72%</td>
      <td>-5.48%</td>
      <td>-14.64%</td>
      <td>-2.44%</td>
      <td>31.91%</td>
      <td>44.49%</td>
      <td>29.89%</td>
      <td>5.14%</td>
      <td>27.55%</td>
      <td>-8.05%</td>
      <td>1.85%</td>
      <td>1.78%</td>
      <td>18.34%</td>
      <td>20.68%</td>
      <td>17.63%</td>
      <td>-0.13</td>
      <td>0.47</td>
      <td>0.43</td>
    </tr>
  </tbody>
</table>
</div>


## Similar Projects
- https://github.com/AshNL/justETF-overview-scraper
- https://github.com/SimonMandlik/etf_filter

## Thanks
This project was inspired by
[this](https://stackoverflow.com/questions/64813023/scraping-dynamic-datatable-of-many-pages-but-same-url)
Stack Overflow question.
