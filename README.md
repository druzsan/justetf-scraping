# justETF Scraping
Scraping the justETF [ETF Screener](https://www.justetf.com/en/find-etf.html).

The most part of the project is implemented as
[Notebook](justetf_scraping/justetf-scraping.ipynb),
but you can easily refactor this to a script.

## Usage

After [loading](justetf_scraping/justetf-scraping.ipynb#request),
[cleanup](justetf_scraping/justetf-scraping.ipynb#cleanup) and
[enrichment](justetf_scraping/justetf-scraping.ipynb#enrich)
you get `pandas.DataFrame` with over 2670 rows and following structure:

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
      <td>2.653215</td>
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
      <td>-38.90</td>
      <td>-5.35</td>
      <td>-28.91</td>
      <td>-22.74</td>
      <td>-46.65</td>
      <td>-19.87</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>129.88</td>
      <td>252.92</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>72.54</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-0.27</td>
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
      <td>3.521708</td>
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
      <td>-50.78</td>
      <td>-6.49</td>
      <td>-37.14</td>
      <td>-32.25</td>
      <td>-57.58</td>
      <td>-33.83</td>
      <td>200.00</td>
      <td>NaN</td>
      <td>166.39</td>
      <td>241.24</td>
      <td>20.41</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>77.30</td>
      <td>78.17</td>
      <td>NaN</td>
      <td>-0.44</td>
      <td>0.57</td>
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
      <td>16.538147</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>False</td>
      <td>True</td>
      <td>Distributing</td>
      <td>0.3</td>
      <td>Full replication</td>
      <td>471</td>
      <td>Equity</td>
      <td>ETF</td>
      <td>NaN</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>-11.57</td>
      <td>2.73</td>
      <td>1.06</td>
      <td>-3.27</td>
      <td>-9.75</td>
      <td>-0.02</td>
      <td>34.98</td>
      <td>47.69</td>
      <td>29.89</td>
      <td>5.14</td>
      <td>27.55</td>
      <td>-8.05</td>
      <td>1.81</td>
      <td>1.78</td>
      <td>18.44</td>
      <td>20.68</td>
      <td>17.65</td>
      <td>0.00</td>
      <td>0.51</td>
      <td>0.46</td>
    </tr>
  </tbody>
</table>

For further usage, see [Notebook](justetf_scraping/justetf-scraping.ipynb).

## Similar Projects
- https://github.com/AshNL/justETF-overview-scraper
- https://github.com/SimonMandlik/etf_filter

## Thanks
This project was inspired by
[this](https://stackoverflow.com/questions/64813023/scraping-dynamic-datatable-of-many-pages-but-same-url)
Stack Overflow question.
