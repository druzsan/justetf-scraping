# justETF Scraping
Scraping the justETF [ETF Screener](https://www.justetf.com/en/find-etf.html).

The most part of the project is implemented as
[Notebook](justetf_scraping/justetf-scraping.ipynb),
but you can easily refactor this to a script.

## Usage

After [loading](justetf_scraping/justetf-scraping.ipynb#request),
[cleanup](justetf_scraping/justetf-scraping.ipynb#cleanup) and
[enrichment](justetf_scraping/justetf-scraping.ipynb#enrich)
you get `pandas.DataFrame` with over 3200 rows and following structure:


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
      <th>at_XETRA</th>
      <th>at_London</th>
      <th>at_Euronext Paris</th>
      <th>at_Stuttgart</th>
      <th>at_SIX Swiss Exchange</th>
      <th>at_Borsa Italiana</th>
      <th>at_Euronext Amsterdam</th>
      <th>at_Euronext Brussels</th>
      <th>yesterday</th>
      <th>last_week</th>
      <th>last_month</th>
      <th>last_three_months</th>
      <th>last_six_months</th>
      <th>last_year</th>
      <th>last_three_years</th>
      <th>last_five_years</th>
      <th>2023</th>
      <th>2022</th>
      <th>2021</th>
      <th>2020</th>
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
      <td>GB00BM9JYH62</td>
      <td>A3GZKD</td>
      <td>AVMX</td>
      <td>&lt;NA&gt;</td>
      <td>Global X Aave ETP</td>
      <td>Aave</td>
      <td>2023-03-13</td>
      <td>0.838232</td>
      <td>Long-only</td>
      <td>Jersey</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>0.99</td>
      <td>Physically backed</td>
      <td>0</td>
      <td>Cryptocurrencies</td>
      <td>ETN</td>
      <td>NaN</td>
      <td>True</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>-4.25</td>
      <td>3.72</td>
      <td>16.50</td>
      <td>65.07</td>
      <td>46.13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>IE000GGQK173</td>
      <td>A3D4VW</td>
      <td>R8T</td>
      <td>125589092</td>
      <td>abrdn Global Real Estate Active Thematics UCIT...</td>
      <td>abrdn Global Real Estate Active Thematics</td>
      <td>2023-02-22</td>
      <td>0.890286</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>0.40</td>
      <td>Full replication</td>
      <td>10</td>
      <td>Real Estate</td>
      <td>ETF</td>
      <td>World</td>
      <td>True</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>-0.96</td>
      <td>0.11</td>
      <td>2.66</td>
      <td>8.94</td>
      <td>5.23</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
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
      <td>18.164259</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>False</td>
      <td>True</td>
      <td>Distributing</td>
      <td>0.30</td>
      <td>Full replication</td>
      <td>571</td>
      <td>Equity</td>
      <td>ETF</td>
      <td>NaN</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>-1.56</td>
      <td>-0.73</td>
      <td>-1.52</td>
      <td>5.31</td>
      <td>3.47</td>
      <td>7.22</td>
      <td>28.09</td>
      <td>72.86</td>
      <td>16.77</td>
      <td>-11.78</td>
      <td>29.89</td>
      <td>5.14</td>
      <td>2.16</td>
      <td>2.26</td>
      <td>11.99</td>
      <td>16.28</td>
      <td>18.48</td>
      <td>0.6</td>
      <td>0.53</td>
      <td>0.63</td>
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
