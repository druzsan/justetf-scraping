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

Load overviews for all available (over 3300 at the moment) ETFs (requires a request for all ETF type: long-only, active, short & leveraged):

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
      <th>IE00B5BMR087</th>
      <td>A0YEDG</td>
      <td>SXR8</td>
      <td>10737041</td>
      <td>iShares Core S&amp;P 500 UCITS ETF (Acc)</td>
      <td>2010-05-19</td>
      <td>5198</td>
      <td>14.241096</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>True</td>
      <td>Accumulating</td>
      <td>0.07</td>
      <td>Full replication</td>
      <td>78449</td>
      <td>False</td>
      <td>503</td>
      <td>13.67</td>
      <td>-1.20</td>
      <td>-5.42</td>
      <td>0.61</td>
      <td>5.04</td>
      <td>21.13</td>
      <td>34.36</td>
      <td>99.91</td>
      <td>21.54</td>
      <td>-13.30</td>
      <td>39.07</td>
      <td>8.04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>12.86</td>
      <td>17.99</td>
      <td>21.63</td>
      <td>1.64</td>
      <td>0.57</td>
      <td>0.69</td>
      <td>-33.71</td>
      <td>-9.09</td>
      <td>-17.11</td>
      <td>-33.71</td>
      <td>Equity</td>
      <td>ETF</td>
      <td></td>
      <td>gettex, XETRA, London, Stuttgart, SIX Swiss Exchange, Borsa Italiana, Euronext Amsterdam</td>
    </tr>
    <tr>
      <th>IE00B4L5Y983</th>
      <td>A0RPWH</td>
      <td>EUNL</td>
      <td>10608388</td>
      <td>iShares Core MSCI World UCITS ETF USD (Acc)</td>
      <td>2009-09-25</td>
      <td>5434</td>
      <td>14.887671</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>True</td>
      <td>Accumulating</td>
      <td>0.20</td>
      <td>Optimized sampling</td>
      <td>67967</td>
      <td>False</td>
      <td>1429</td>
      <td>10.85</td>
      <td>-1.06</td>
      <td>-4.81</td>
      <td>-0.59</td>
      <td>4.28</td>
      <td>17.87</td>
      <td>25.66</td>
      <td>79.25</td>
      <td>19.55</td>
      <td>-12.96</td>
      <td>32.10</td>
      <td>6.13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>11.17</td>
      <td>15.25</td>
      <td>18.27</td>
      <td>1.59</td>
      <td>0.52</td>
      <td>0.68</td>
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
      <td>Vanguard S&amp;P 500 UCITS ETF</td>
      <td>2012-05-22</td>
      <td>4464</td>
      <td>12.230137</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Distributing</td>
      <td>0.07</td>
      <td>Full replication</td>
      <td>35981</td>
      <td>False</td>
      <td>498</td>
      <td>13.63</td>
      <td>-1.23</td>
      <td>-5.45</td>
      <td>0.57</td>
      <td>5.01</td>
      <td>21.08</td>
      <td>34.31</td>
      <td>99.85</td>
      <td>21.54</td>
      <td>-13.29</td>
      <td>39.08</td>
      <td>8.05</td>
      <td>1.11</td>
      <td>1.33</td>
      <td>12.89</td>
      <td>18.13</td>
      <td>21.70</td>
      <td>1.63</td>
      <td>0.57</td>
      <td>0.68</td>
      <td>-33.70</td>
      <td>-9.09</td>
      <td>-17.28</td>
      <td>-33.70</td>
      <td>Equity</td>
      <td>ETF</td>
      <td></td>
      <td>gettex, XETRA, London, Euronext Paris, Stuttgart, SIX Swiss Exchange, Borsa Italiana, Euronext Amsterdam</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <td>0.0</td>
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
      <th>2024-08-05</th>
      <td>64.90</td>
      <td>215.048544</td>
      <td>0.0</td>
      <td>9.9</td>
      <td>74.80</td>
      <td>263.106796</td>
      <td>20.643909</td>
      <td>85.543909</td>
      <td>315.261692</td>
    </tr>
    <tr>
      <th>2024-08-06</th>
      <td>65.95</td>
      <td>220.145631</td>
      <td>0.0</td>
      <td>9.9</td>
      <td>75.85</td>
      <td>268.203883</td>
      <td>20.977901</td>
      <td>86.927901</td>
      <td>321.980101</td>
    </tr>
    <tr>
      <th>2024-08-07</th>
      <td>65.74</td>
      <td>219.126214</td>
      <td>0.0</td>
      <td>9.9</td>
      <td>75.64</td>
      <td>267.184466</td>
      <td>20.911102</td>
      <td>86.651102</td>
      <td>320.636419</td>
    </tr>
    <tr>
      <th>2024-08-08</th>
      <td>66.80</td>
      <td>224.271845</td>
      <td>0.0</td>
      <td>9.9</td>
      <td>76.70</td>
      <td>272.330097</td>
      <td>21.248276</td>
      <td>88.048276</td>
      <td>327.418814</td>
    </tr>
    <tr>
      <th>2024-08-09</th>
      <td>67.05</td>
      <td>225.485437</td>
      <td>0.0</td>
      <td>9.9</td>
      <td>76.95</td>
      <td>273.543689</td>
      <td>21.327798</td>
      <td>88.377798</td>
      <td>329.018435</td>
    </tr>
  </tbody>
</table>
<p>6861 rows × 9 columns</p>

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
      <th>2024-08-05</th>
      <td>236.482231</td>
      <td>120.784680</td>
    </tr>
    <tr>
      <th>2024-08-06</th>
      <td>241.205578</td>
      <td>123.960766</td>
    </tr>
    <tr>
      <th>2024-08-07</th>
      <td>240.260909</td>
      <td>127.136852</td>
    </tr>
    <tr>
      <th>2024-08-08</th>
      <td>245.029240</td>
      <td>127.697338</td>
    </tr>
    <tr>
      <th>2024-08-09</th>
      <td>246.153846</td>
      <td>128.304531</td>
    </tr>
  </tbody>
</table>
<p>6840 rows × 2 columns</p>

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
