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

Load overviews for all available (over 3400 at the moment) ETFs. By default, it loads long-only, active, short & leveraged ETFs (3 requests), but without further enrichments:

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
      <th>...</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>IE00B5BMR087</th>
      <td>A0YEDG</td>
      <td>SXR8</td>
      <td>10737041</td>
      <td>iShares Core S&amp;P 500 UCITS ETF USD (Acc)</td>
      <td>2010-05-19</td>
      <td>5738</td>
      <td>15.720548</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>18.97</td>
      <td>15.85</td>
      <td>17.58</td>
      <td>0.04</td>
      <td>1.12</td>
      <td>0.86</td>
      <td>-33.71</td>
      <td>-22.60</td>
      <td>-22.60</td>
      <td>-22.60</td>
    </tr>
    <tr>
      <th>IE00B4L5Y983</th>
      <td>A0RPWH</td>
      <td>EUNL</td>
      <td>10608388</td>
      <td>iShares Core MSCI World UCITS ETF USD (Acc)</td>
      <td>2009-09-25</td>
      <td>5974</td>
      <td>16.367123</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.38</td>
      <td>13.20</td>
      <td>14.73</td>
      <td>0.26</td>
      <td>1.23</td>
      <td>0.91</td>
      <td>-33.91</td>
      <td>-20.45</td>
      <td>-20.45</td>
      <td>-20.45</td>
    </tr>
    <tr>
      <th>IE00B3XXRP09</th>
      <td>A1JX53</td>
      <td>VUSA</td>
      <td>18575508</td>
      <td>Vanguard S&amp;P 500 UCITS ETF (USD) Distributing</td>
      <td>2012-05-22</td>
      <td>5004</td>
      <td>13.709589</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>19.69</td>
      <td>16.20</td>
      <td>17.81</td>
      <td>0.04</td>
      <td>1.10</td>
      <td>0.85</td>
      <td>-33.70</td>
      <td>-23.74</td>
      <td>-23.74</td>
      <td>-23.74</td>
    </tr>
    <tr>
      <th>IE00B4ND3602</th>
      <td>A1KWPQ</td>
      <td>PPFB</td>
      <td>12881542</td>
      <td>iShares Physical Gold ETC</td>
      <td>2011-04-08</td>
      <td>5414</td>
      <td>14.832877</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>19.76</td>
      <td>16.04</td>
      <td>15.57</td>
      <td>2.90</td>
      <td>2.09</td>
      <td>1.43</td>
      <td>-37.20</td>
      <td>-7.86</td>
      <td>-7.86</td>
      <td>-11.73</td>
    </tr>
    <tr>
      <th>IE00B3YCGJ38</th>
      <td>A1CYW7</td>
      <td>P500</td>
      <td>11358996</td>
      <td>Invesco S&amp;P 500 UCITS ETF Acc</td>
      <td>2010-05-20</td>
      <td>5737</td>
      <td>15.717808</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>19.17</td>
      <td>15.99</td>
      <td>17.67</td>
      <td>0.05</td>
      <td>1.13</td>
      <td>0.87</td>
      <td>-33.62</td>
      <td>-22.61</td>
      <td>-22.61</td>
      <td>-22.61</td>
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
      <td>...</td>
      <td>...</td>
      <td>...</td>
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
      <th>XS2427474023</th>
      <td>A3GWVN</td>
      <td>O2IG</td>
      <td>NaN</td>
      <td>WisdomTree STOXX Europe Oil &amp; Gas 2x Daily Short</td>
      <td>2022-03-02</td>
      <td>1433</td>
      <td>3.926027</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>38.06</td>
      <td>36.21</td>
      <td>NaN</td>
      <td>-1.21</td>
      <td>-0.69</td>
      <td>NaN</td>
      <td>-77.65</td>
      <td>-59.72</td>
      <td>-62.49</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2437455608</th>
      <td>A3GXB6</td>
      <td>STR2</td>
      <td>NaN</td>
      <td>WisdomTree STOXX Europe Travel &amp; Leisure 2x Da...</td>
      <td>2022-03-02</td>
      <td>1433</td>
      <td>3.926027</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>39.58</td>
      <td>36.97</td>
      <td>NaN</td>
      <td>-0.25</td>
      <td>-0.49</td>
      <td>NaN</td>
      <td>-75.87</td>
      <td>-50.62</td>
      <td>-56.76</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS3037640110</th>
      <td>NaN</td>
      <td>SBA3</td>
      <td>NaN</td>
      <td>Leverage Shares -3x Short Alibaba (BABA) ETP S...</td>
      <td>2022-06-07</td>
      <td>1336</td>
      <td>3.660274</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>156.89</td>
      <td>129.87</td>
      <td>NaN</td>
      <td>-0.61</td>
      <td>-0.61</td>
      <td>NaN</td>
      <td>-99.93</td>
      <td>-96.88</td>
      <td>-99.66</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2531767767</th>
      <td>NaN</td>
      <td>5SIT</td>
      <td>NaN</td>
      <td>GraniteShares 5x Short MIB Daily ETF</td>
      <td>2023-06-09</td>
      <td>969</td>
      <td>2.654795</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>88.05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-0.93</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-97.70</td>
      <td>-87.80</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2842095759</th>
      <td>NaN</td>
      <td>3SBB</td>
      <td>NaN</td>
      <td>GraniteShares 3x Short Alibaba Daily ETP</td>
      <td>2022-02-02</td>
      <td>1461</td>
      <td>4.002740</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>150.08</td>
      <td>5696.15</td>
      <td>NaN</td>
      <td>-0.64</td>
      <td>-0.01</td>
      <td>NaN</td>
      <td>-99.99</td>
      <td>-96.79</td>
      <td>-99.99</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>4068 rows × 42 columns</p>

To reduce the number of requests, one particular ETF type can be loaded, e.g. long-only ETFs:

```python
df = justetf_scraping.load_overview(strategy="epg-longOnly")
```

To further enrich the data with additional information (asset class, region, exchanges and instrument, multiple requests for each combination required):

```python
df = justetf_scraping.load_overview(enrich=True)
```

Load ETFs for a single index, e.g. MSCI World:

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
      <th>2026-01-26</th>
      <td>81.57</td>
      <td>295.970874</td>
      <td>0.0</td>
      <td>10.98</td>
      <td>92.55</td>
      <td>349.271845</td>
      <td>27.130307</td>
      <td>108.700307</td>
      <td>427.671393</td>
    </tr>
    <tr>
      <th>2026-01-27</th>
      <td>81.40</td>
      <td>295.145631</td>
      <td>0.0</td>
      <td>10.98</td>
      <td>92.38</td>
      <td>348.446602</td>
      <td>27.073765</td>
      <td>108.473765</td>
      <td>426.571674</td>
    </tr>
    <tr>
      <th>2026-01-28</th>
      <td>80.95</td>
      <td>292.961165</td>
      <td>0.0</td>
      <td>10.98</td>
      <td>91.93</td>
      <td>346.262136</td>
      <td>26.924094</td>
      <td>107.874094</td>
      <td>423.660651</td>
    </tr>
    <tr>
      <th>2026-01-29</th>
      <td>80.88</td>
      <td>292.621359</td>
      <td>0.0</td>
      <td>10.98</td>
      <td>91.86</td>
      <td>345.922330</td>
      <td>26.900812</td>
      <td>107.780812</td>
      <td>423.207825</td>
    </tr>
    <tr>
      <th>2026-01-30</th>
      <td>80.88</td>
      <td>292.621359</td>
      <td>0.0</td>
      <td>10.98</td>
      <td>91.86</td>
      <td>345.922330</td>
      <td>26.900812</td>
      <td>107.780812</td>
      <td>423.207825</td>
    </tr>
  </tbody>
</table>
<p>7400 rows × 9 columns</p>

For accumulating ETFs, all dividends columns are zeros and all columns with dividends are equal to the ones without.

If you want to include quote from not yet closed day (today):

```python
df = justetf_scraping.load_chart("IE00B0M62Q58", unclosed=True)
```

Compare multiple charts. It will take the shortest time period and compare gain as percentage including payed out but not reinvested dividends:

```python
df = justetf_scraping.compare_charts(
    {
        "IE00B0M62Q58": justetf_scraping.load_chart("IE00B0M62Q58"),
        "IE00B0M63177": justetf_scraping.load_chart("IE00B0M63177"),
    },
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
      <th>2026-01-26</th>
      <td>316.329285</td>
      <td>190.191499</td>
    </tr>
    <tr>
      <th>2026-01-27</th>
      <td>315.564552</td>
      <td>191.359178</td>
    </tr>
    <tr>
      <th>2026-01-28</th>
      <td>313.540261</td>
      <td>194.722092</td>
    </tr>
    <tr>
      <th>2026-01-29</th>
      <td>313.225371</td>
      <td>194.581971</td>
    </tr>
    <tr>
      <th>2026-01-30</th>
      <td>313.225371</td>
      <td>191.452592</td>
    </tr>
  </tbody>
</table>
<p>7379 rows × 2 columns</p>

### 💗 Scrape Live Quote

Load the last quote of a chosen ETF by its ISIN:

```python
quote = justetf_scraping.load_live_quote("IE00B0M62Q58")
quote
```

```
Quote(isin='IE00B0M62Q58', timestamp=datetime.datetime(2026, 2, 2, 15, 43, 30, 201000, tzinfo=datetime.timezone.utc), exchange='gettex', currency='EUR', trend=None, ask=82.0, bid=81.98, mid=81.99, last=81.19, spread=0.02, spread_relative=0.0002, spread_percentage=0.02, day_to_day=0.8, day_to_day_relative=0.0099, day_to_day_percentage=0.99)
```

Currently, only Gettex exchange and Euro currency are supported.

Subscribe to live quote of a chosen ETF by its ISIN:

```python
for quote in justetf_scraping.iterate_live_quote("IE00B0M62Q58"):
    print(quote)  # Add your processing here
```

```
Quote(isin='IE00B0M62Q58', timestamp=datetime.datetime(2026, 2, 2, 15, 43, 30, 201000, tzinfo=datetime.timezone.utc), exchange='gettex', currency='EUR', trend=None, ask=82.0, bid=81.98, mid=81.99, last=81.19, spread=0.02, spread_relative=0.0002, spread_percentage=0.02, day_to_day=0.8, day_to_day_relative=0.0099, day_to_day_percentage=0.99)
Quote(isin='IE00B0M62Q58', timestamp=datetime.datetime(2026, 2, 2, 15, 43, 32, 270000, tzinfo=datetime.timezone.utc), exchange='gettex', currency='EUR', trend=None, ask=82.0, bid=81.98, mid=81.99, last=81.19, spread=0.02, spread_relative=0.0002, spread_percentage=0.02, day_to_day=0.8, day_to_day_relative=0.0099, day_to_day_percentage=0.99)
Quote(isin='IE00B0M62Q58', timestamp=datetime.datetime(2026, 2, 2, 15, 43, 34, 656000, tzinfo=datetime.timezone.utc), exchange='gettex', currency='EUR', trend=None, ask=82.0, bid=81.97, mid=81.99, last=81.19, spread=0.03, spread_relative=0.0004, spread_percentage=0.04, day_to_day=0.8, day_to_day_relative=0.0099, day_to_day_percentage=0.99)
...
```

So you can react to quote change. Again, only Gettex exchange and Euro currency are supported. The update frequency cannot be controlled. No updates besides the initial quote will be received outside of trade hours.

### 🔍 Scrape ETF Profile Data

Get comprehensive ETF profile data including description, holdings allocation by country and sector, and real-time quotes from gettex.

#### Get complete ETF overview with `get_etf_overview`

```python
overview = justetf_scraping.get_etf_overview("IE00B3RBWM25")

# Access basic info
print(f"Name: {overview['name']}")
print(f"TER: {overview['ter']}%")
print(f"Fund Size: EUR {overview['fund_size_eur']}m")
print(f"Description: {overview['description']}")

# Access country allocation (full list, not truncated)
for country in overview['countries']:
    print(f"  {country['name']}: {country['percentage']}%")

# Access sector allocation (full list)
for sector in overview['sectors']:
    print(f"  {sector['name']}: {sector['percentage']}%")

# Access top 10 holdings with their ISINs
for holding in overview['top_holdings']:
    print(f"  {holding['name']} ({holding['isin']}): {holding['percentage']}%")

# Access real-time gettex quote
quote = overview['gettex']
print(f"Bid: {quote['bid']} {quote['currency']}")
print(f"Ask: {quote['ask']} {quote['currency']}")
print(f"Day Change: {quote['day_change_percent']}%")
```

The `get_etf_overview` function returns a dictionary with:

| Field                 | Type  | Description                      |
|-----------------------|-------|----------------------------------|
| `isin`                | str   | ISIN code                        |
| `name`                | str   | ETF name                         |
| `description`         | str   | Short description                |
| `index`               | str   | Tracked index                    |
| `ter`                 | float | Total Expense Ratio (e.g., 0.19) |
| `fund_size_eur`       | float | Fund size in EUR millions        |
| `replication`         | str   | Replication method               |
| `fund_currency`       | str   | Fund currency                    |
| `distribution_policy` | str   | Distributing/Accumulating        |
| `inception_date`      | str   | Launch date                      |
| `fund_domicile`       | str   | Country of domicile              |
| `countries`           | list  | Full country allocation          |
| `sectors`             | list  | Full sector allocation           |
| `top_holdings`        | list  | Top 10 holdings with ISINs       |
| `gettex`              | dict  | Real-time quote data             |

For a complete example, see [test_scrape.py](notebooks/test_scrape.py)

For further exploration examples, see [Jupyter Notebooks](notebooks/)

## ⚒️ Development Setup

Prerequisites:
- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) for dependency management
- make (optional) for shortcut commands
- [direnv](https://direnv.net/) (optional) to automate enviroment setup
- [asdf](https://asdf-vm.com/) (optional) to manage direnv, Python and uv versions. For correct direnv setup, use [pre 0.16](https://asdf-vm.com/guide/getting-started-legacy.html) version.

Setup project using asdf, direnv and make
```shell
asdf add plugin python
asdf add plugin uv
asdf add plugin direnv
asdf direnv setup --shell bash --version latest
# Navigate to project folder
asdf install
direnv allow
uv sync --all-extras
```

Setup project using pip (Python should be preinstalled):

```shell
pip install uv
# Navigate to project folder
uv sync --all-extras
uv run pre-commit install
# To run any environment-related commands, use `uv run ...`, e.g.:
uv run notebook
```

Optionally, use make targets for predefined commands, e.g. `make sync` to install all dependencies. Run `make help` to see all commands.

## Similar Projects

- https://github.com/AshNL/justETF-overview-scraper
- https://github.com/SimonMandlik/etf_filter

## Thanks

This project was inspired by
[this](https://stackoverflow.com/questions/64813023/scraping-dynamic-datatable-of-many-pages-but-same-url)
Stack Overflow question.
