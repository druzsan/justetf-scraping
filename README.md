# 💹 justETF Scraping

Scrape the [justETF](https://www.justetf.com).

## 🛠️ Installation

To use justETF scraping package in your project, install the actual version from GitHub:

```shell
pip install git+https://github.com/druzsan/justetf-scraping.git
```

If you are going to play [notebooks](./notebooks) through, use the following installation:

```shell
pip install justetf-scraping[all]@git+https://github.com/druzsan/justetf-scraping.git
```

## 🚀 Usage

### 📋 Scrape the [justETF Screener](https://www.justetf.com/en/find-etf.html)

Load overviews for all available (over 3400 at the moment) ETFs (requires a request for all ETF type: long-only, active, short & leveraged):

```python
import justetf_scraping

df = justetf_scraping.load_overview()
df
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>wkn</th>
      <th>ticker</th>
      <th>valor</th>
      <th>name</th>
      <th>inception_date</th>
      <th>age_in_days</th>
      <th>age_in_years</th>
      <th>strategy</th>
      <th>domicile_country</th>
      <th>currency</th>
      <th>hedged</th>
      <th>securities_lending</th>
      <th>dividends</th>
      <th>ter</th>
      <th>replication</th>
      <th>size</th>
      <th>is_sustainable</th>
      <th>number_of_holdings</th>
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
      <th>max_drawdown</th>
      <th>last_year_max_drawdown</th>
      <th>last_three_years_max_drawdown</th>
      <th>last_five_years_max_drawdown</th>
      <th>asset_class</th>
      <th>instrument</th>
      <th>region</th>
      <th>exchange</th>
    </tr>
    <tr>
      <th>isin</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>IE00B4L5Y983</th>
      <td>A0RPWH</td>
      <td>EUNL</td>
      <td>10608388</td>
      <td>iShares Core MSCI World UCITS ETF USD (Acc)</td>
      <td>2009-09-25</td>
      <td>5555</td>
      <td>15.219178</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>True</td>
      <td>Accumulating</td>
      <td>0.20</td>
      <td>Optimized sampling</td>
      <td>88335</td>
      <td>False</td>
      <td>1409</td>
      <td>28.62</td>
      <td>0.14</td>
      <td>3.48</td>
      <td>13.61</td>
      <td>14.62</td>
      <td>30.54</td>
      <td>36.24</td>
      <td>90.45</td>
      <td>19.55</td>
      <td>-12.96</td>
      <td>32.10</td>
      <td>6.13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>11.83</td>
      <td>15.29</td>
      <td>18.35</td>
      <td>2.57</td>
      <td>0.71</td>
      <td>0.75</td>
      <td>-33.91</td>
      <td>-8.75</td>
      <td>-16.88</td>
      <td>-33.91</td>
      <td>Equity</td>
      <td>ETF</td>
      <td>World</td>
      <td>gettex, XETRA, London, Stuttgart, SIX Swiss Exchange, Borsa Italiana, Euronext Amsterdam</td>
    </tr>
    <tr>
      <th>IE00B3XXRP09</th>
      <td>A1JX53</td>
      <td>VUSA</td>
      <td>18575508</td>
      <td>Vanguard S&amp;P 500 UCITS ETF (USD) Distributing</td>
      <td>2012-05-22</td>
      <td>4585</td>
      <td>12.561644</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>True</td>
      <td>Distributing</td>
      <td>0.07</td>
      <td>Full replication</td>
      <td>43952</td>
      <td>False</td>
      <td>487</td>
      <td>34.27</td>
      <td>-0.32</td>
      <td>3.16</td>
      <td>16.07</td>
      <td>17.53</td>
      <td>35.75</td>
      <td>44.35</td>
      <td>116.12</td>
      <td>21.54</td>
      <td>-13.29</td>
      <td>39.08</td>
      <td>8.05</td>
      <td>0.95</td>
      <td>1.27</td>
      <td>13.67</td>
      <td>18.25</td>
      <td>21.76</td>
      <td>2.61</td>
      <td>0.71</td>
      <td>0.76</td>
      <td>-33.70</td>
      <td>-9.09</td>
      <td>-17.28</td>
      <td>-33.70</td>
      <td>Equity</td>
      <td>ETF</td>
      <td></td>
      <td>gettex, XETRA, London, Euronext Paris, Stuttgart, SIX Swiss Exchange, Borsa Italiana, Euronext Amsterdam</td>
    </tr>
    <tr>
      <th>IE00B3YCGJ38</th>
      <td>A1CYW7</td>
      <td>P500</td>
      <td>11358996</td>
      <td>Invesco S&amp;P 500 UCITS ETF</td>
      <td>2010-05-20</td>
      <td>5318</td>
      <td>14.569863</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>0.05</td>
      <td>Swap based Unfunded</td>
      <td>27500</td>
      <td>False</td>
      <td>&lt;NA&gt;</td>
      <td>34.71</td>
      <td>-0.16</td>
      <td>3.34</td>
      <td>16.30</td>
      <td>17.82</td>
      <td>36.20</td>
      <td>45.49</td>
      <td>118.77</td>
      <td>21.80</td>
      <td>-13.10</td>
      <td>39.37</td>
      <td>8.31</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>13.66</td>
      <td>18.16</td>
      <td>21.75</td>
      <td>2.64</td>
      <td>0.73</td>
      <td>0.78</td>
      <td>-33.69</td>
      <td>-9.09</td>
      <td>-17.20</td>
      <td>-33.69</td>
      <td>Equity</td>
      <td>ETF</td>
      <td></td>
      <td>gettex, XETRA, London, SIX Swiss Exchange, Borsa Italiana, Euronext Amsterdam</td>
    </tr>
  </tbody>
</table>

Further enrich the data with additional information (asset class, region, exchanges and instrument, it requires further requests):

```python
df = justetf_scraping.load_overview(enrich=True)
```

Load long-only ETFs (only requires one single request):

```python
df = justetf_scraping.load_overview(strategy="epg-longOnly")
```

Load MSCI World ETFs:

```python
df = justetf_scraping.load_overview(strategy="epg-longOnly", index="MSCI World")
```

### 📈 Scrape ETF Chart Data from justETF ([e.g.](https://www.justetf.com/en/etf-profile.html?isin=IE00B0M62Q58#chart))

Load the whole history of a chosen ETF by its ISIN:

```python
df = justetf_scraping.load_chart("IE00B0M62Q58")
df
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>quote</th>
      <th>relative</th>
      <th>dividends</th>
      <th>cumulative_dividends</th>
      <th>quote_with_dividends</th>
      <th>relative_with_dividends</th>
      <th>reinvested_dividends</th>
      <th>quote_with_reinvested_dividends</th>
      <th>relative_with_reinvested_dividends</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2005-10-28</th>
      <td>20.60</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>20.60</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>20.600000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2005-10-29</th>
      <td>20.60</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>20.60</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>20.600000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2005-10-30</th>
      <td>20.60</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>20.60</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>20.600000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2005-10-31</th>
      <td>20.99</td>
      <td>1.893204</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>20.99</td>
      <td>1.893204</td>
      <td>0.000000</td>
      <td>20.990000</td>
      <td>1.893204</td>
    </tr>
    <tr>
      <th>2005-11-01</th>
      <td>21.03</td>
      <td>2.087379</td>
      <td>0.0</td>
      <td>0.00</td>
      <td>21.03</td>
      <td>2.087379</td>
      <td>0.000000</td>
      <td>21.030000</td>
      <td>2.087379</td>
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
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2024-12-05</th>
      <td>77.86</td>
      <td>277.961165</td>
      <td>0.0</td>
      <td>10.04</td>
      <td>87.90</td>
      <td>326.699029</td>
      <td>24.922629</td>
      <td>102.782629</td>
      <td>398.944801</td>
    </tr>
    <tr>
      <th>2024-12-06</th>
      <td>77.70</td>
      <td>277.184466</td>
      <td>0.0</td>
      <td>10.04</td>
      <td>87.74</td>
      <td>325.922330</td>
      <td>24.871414</td>
      <td>102.571414</td>
      <td>397.919484</td>
    </tr>
    <tr>
      <th>2024-12-07</th>
      <td>77.70</td>
      <td>277.184466</td>
      <td>0.0</td>
      <td>10.04</td>
      <td>87.74</td>
      <td>325.922330</td>
      <td>24.871414</td>
      <td>102.571414</td>
      <td>397.919484</td>
    </tr>
    <tr>
      <th>2024-12-08</th>
      <td>77.70</td>
      <td>277.184466</td>
      <td>0.0</td>
      <td>10.04</td>
      <td>87.74</td>
      <td>325.922330</td>
      <td>24.871414</td>
      <td>102.571414</td>
      <td>397.919484</td>
    </tr>
    <tr>
      <th>2024-12-09</th>
      <td>77.60</td>
      <td>276.699029</td>
      <td>0.0</td>
      <td>10.04</td>
      <td>87.64</td>
      <td>325.436893</td>
      <td>24.839404</td>
      <td>102.439404</td>
      <td>397.278661</td>
    </tr>
  </tbody>
</table>
<p>6983 rows × 9 columns</p>

Compare

```python
df = justetf_scraping.compare_charts(
    {
        "IE00B0M62Q58": justetf_scraping.load_chart("IE00B0M62Q58"),
        "IE00B0M63177": justetf_scraping.load_chart("IE00B0M63177"),
    },
    input_value="quote_with_dividends"
)
df
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>IE00B0M62Q58</th>
      <th>IE00B0M63177</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2005-11-18</th>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2005-11-19</th>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2005-11-20</th>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2005-11-21</th>
      <td>-0.539811</td>
      <td>-0.887436</td>
    </tr>
    <tr>
      <th>2005-11-22</th>
      <td>0.629780</td>
      <td>-0.934143</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2024-12-05</th>
      <td>295.411606</td>
      <td>143.390939</td>
    </tr>
    <tr>
      <th>2024-12-06</th>
      <td>294.691858</td>
      <td>143.110696</td>
    </tr>
    <tr>
      <th>2024-12-07</th>
      <td>294.691858</td>
      <td>143.110696</td>
    </tr>
    <tr>
      <th>2024-12-08</th>
      <td>294.691858</td>
      <td>143.110696</td>
    </tr>
    <tr>
      <th>2024-12-09</th>
      <td>294.242015</td>
      <td>146.987389</td>
    </tr>
  </tbody>
</table>
<p>6962 rows × 2 columns</p>

For further exploration examples, see [Jupyter Notebooks](notebooks/)

## ⚒️ Development Setup

To setup locally cloned project, first install [Poetry](https://python-poetry.org/):

```shell
pip install poetry
```

In the local project folder, install all dependencies and extras:

```shell
poetry install --all-extras
```

Activate local Poetry environment:

```shell
poetry shell
```

Setup [pre-commit hooks](https://pre-commit.com/):

```shell
pre-commit install
```

## Similar Projects

- https://github.com/AshNL/justETF-overview-scraper
- https://github.com/SimonMandlik/etf_filter

## Thanks

This project was inspired by
[this](https://stackoverflow.com/questions/64813023/scraping-dynamic-datatable-of-many-pages-but-same-url)
Stack Overflow question.
