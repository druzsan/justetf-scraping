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

<div>
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
      <td>5415</td>
      <td>14.835616</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.73</td>
      <td>18.00</td>
      <td>20.09</td>
      <td>0.67</td>
      <td>0.67</td>
      <td>0.88</td>
      <td>-33.71</td>
      <td>-13.39</td>
      <td>-15.92</td>
      <td>-17.11</td>
    </tr>
    <tr>
      <th>IE00B4L5Y983</th>
      <td>A0RPWH</td>
      <td>EUNL</td>
      <td>10608388</td>
      <td>iShares Core MSCI World UCITS ETF USD (Acc)</td>
      <td>2009-09-25</td>
      <td>5651</td>
      <td>15.482192</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>13.79</td>
      <td>15.27</td>
      <td>17.02</td>
      <td>0.73</td>
      <td>0.72</td>
      <td>0.97</td>
      <td>-33.91</td>
      <td>-11.24</td>
      <td>-15.01</td>
      <td>-16.88</td>
    </tr>
    <tr>
      <th>IE00B3XXRP09</th>
      <td>A1JX53</td>
      <td>VUSA</td>
      <td>18575508</td>
      <td>Vanguard S&amp;P 500 UCITS ETF (USD) Distributing</td>
      <td>2012-05-22</td>
      <td>4681</td>
      <td>12.824658</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.95</td>
      <td>18.20</td>
      <td>20.19</td>
      <td>0.66</td>
      <td>0.66</td>
      <td>0.87</td>
      <td>-33.70</td>
      <td>-13.43</td>
      <td>-16.10</td>
      <td>-17.28</td>
    </tr>
    <tr>
      <th>IE00B3YCGJ38</th>
      <td>A1CYW7</td>
      <td>P500</td>
      <td>11358996</td>
      <td>Invesco S&amp;P 500 UCITS ETF</td>
      <td>2010-05-20</td>
      <td>5414</td>
      <td>14.832877</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.87</td>
      <td>18.08</td>
      <td>20.16</td>
      <td>0.69</td>
      <td>0.68</td>
      <td>0.89</td>
      <td>-33.69</td>
      <td>-13.61</td>
      <td>-16.06</td>
      <td>-17.20</td>
    </tr>
    <tr>
      <th>IE00BKM4GZ66</th>
      <td>A111X9</td>
      <td>IS3N</td>
      <td>24209517</td>
      <td>iShares Core MSCI Emerging Markets IMI UCITS E...</td>
      <td>2014-05-30</td>
      <td>3943</td>
      <td>10.802740</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>14.27</td>
      <td>14.24</td>
      <td>15.79</td>
      <td>0.64</td>
      <td>0.36</td>
      <td>0.54</td>
      <td>-34.34</td>
      <td>-10.36</td>
      <td>-17.53</td>
      <td>-23.61</td>
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
      <th>IE00BF4TW453</th>
      <td>A2F4WK</td>
      <td>XMWH</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree Bund 30Y 3x Daily Short</td>
      <td>2017-12-08</td>
      <td>2655</td>
      <td>7.273973</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>43.83</td>
      <td>58.07</td>
      <td>NaN</td>
      <td>0.85</td>
      <td>0.65</td>
      <td>NaN</td>
      <td>-49.46</td>
      <td>-30.58</td>
      <td>-49.46</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2427363036</th>
      <td>A3GWVS</td>
      <td>2FLY</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree STOXX Europe Travel &amp; Leisure 2x Da...</td>
      <td>2022-03-02</td>
      <td>1110</td>
      <td>3.041096</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>33.07</td>
      <td>43.18</td>
      <td>NaN</td>
      <td>-0.46</td>
      <td>0.19</td>
      <td>NaN</td>
      <td>-42.03</td>
      <td>-36.10</td>
      <td>-42.03</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>JE00B24DKJ77</th>
      <td>A0V6Y0</td>
      <td>4RTE</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree Nickel 1x Daily Short</td>
      <td>2008-02-22</td>
      <td>6232</td>
      <td>17.073973</td>
      <td>Short &amp; Leveraged</td>
      <td>Jersey</td>
      <td>USD</td>
      <td>...</td>
      <td>25.45</td>
      <td>46.59</td>
      <td>49.48</td>
      <td>0.56</td>
      <td>0.51</td>
      <td>-0.51</td>
      <td>-96.99</td>
      <td>-23.84</td>
      <td>-47.83</td>
      <td>-89.44</td>
    </tr>
    <tr>
      <th>XS2842095759</th>
      <td>&lt;NA&gt;</td>
      <td>3SBB</td>
      <td>&lt;NA&gt;</td>
      <td>GraniteShares 3x Short Alibaba Daily ETP</td>
      <td>2022-02-02</td>
      <td>1138</td>
      <td>3.117808</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>130.77</td>
      <td>154.54</td>
      <td>NaN</td>
      <td>-0.73</td>
      <td>-0.58</td>
      <td>NaN</td>
      <td>-99.88</td>
      <td>-95.97</td>
      <td>-99.88</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2427474023</th>
      <td>A3GWVN</td>
      <td>O2IG</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree STOXX Europe Oil &amp; Gas 2x Daily Short</td>
      <td>2022-03-02</td>
      <td>1110</td>
      <td>3.041096</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>32.07</td>
      <td>41.70</td>
      <td>NaN</td>
      <td>-0.29</td>
      <td>-0.59</td>
      <td>NaN</td>
      <td>-63.42</td>
      <td>-23.03</td>
      <td>-61.78</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>3486 rows × 42 columns</p>
</div>

To reduce the number of requests, one particular ETF type can be loaded, e.g. long-only ETFs:

```python
df = justetf_scraping.load_overview(streategy="epg-longOnly")
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
      <th>2025-03-10</th>
      <td>74.54</td>
      <td>261.844660</td>
      <td>0.0</td>
      <td>10.22</td>
      <td>84.76</td>
      <td>311.456311</td>
      <td>24.032814</td>
      <td>98.572814</td>
      <td>378.508807</td>
    </tr>
    <tr>
      <th>2025-03-11</th>
      <td>73.96</td>
      <td>259.029126</td>
      <td>0.0</td>
      <td>10.22</td>
      <td>84.18</td>
      <td>308.640777</td>
      <td>23.845814</td>
      <td>97.805814</td>
      <td>374.785503</td>
    </tr>
    <tr>
      <th>2025-03-12</th>
      <td>74.37</td>
      <td>261.019417</td>
      <td>0.0</td>
      <td>10.22</td>
      <td>84.59</td>
      <td>310.631068</td>
      <td>23.978004</td>
      <td>98.348004</td>
      <td>377.417494</td>
    </tr>
    <tr>
      <th>2025-03-13</th>
      <td>70.64</td>
      <td>242.912621</td>
      <td>0.0</td>
      <td>10.22</td>
      <td>80.86</td>
      <td>292.524272</td>
      <td>22.775396</td>
      <td>93.415396</td>
      <td>353.472795</td>
    </tr>
    <tr>
      <th>2025-03-14</th>
      <td>71.49</td>
      <td>247.038835</td>
      <td>0.0</td>
      <td>10.22</td>
      <td>81.71</td>
      <td>296.650485</td>
      <td>23.049449</td>
      <td>94.539449</td>
      <td>358.929362</td>
    </tr>
  </tbody>
</table>
<p>7078 rows × 9 columns</p>

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
      <th>2025-03-10</th>
      <td>281.286550</td>
      <td>147.874825</td>
    </tr>
    <tr>
      <th>2025-03-11</th>
      <td>278.677463</td>
      <td>147.220925</td>
    </tr>
    <tr>
      <th>2025-03-12</th>
      <td>280.521817</td>
      <td>147.594582</td>
    </tr>
    <tr>
      <th>2025-03-13</th>
      <td>263.742690</td>
      <td>138.953760</td>
    </tr>
    <tr>
      <th>2025-03-14</th>
      <td>267.566352</td>
      <td>141.569360</td>
    </tr>
  </tbody>
</table>
<p>7057 rows × 2 columns</p>

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

#### Get real-time gettex quote only with `get_gettex_quote`

```python
quote = justetf_scraping.get_gettex_quote("IE00B3RBWM25")

print(f"Bid: {quote['bid']} EUR")
print(f"Ask: {quote['ask']} EUR")
print(f"Spread: {quote['spread_percent']}%")
print(f"Day Change: {quote['day_change_percent']}%")
print(f"Timestamp: {quote['timestamp']}")  # datetime object
```

#### Get raw gettex data with `get_gettex_quote_raw`

```python
raw_data = justetf_scraping.get_gettex_quote_raw("IE00B3RBWM25")
# Returns the raw JSON response from the WebSocket
```

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
