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
      <th>index</th>
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
      <th>asset</th>
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
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>GB00BM9JYH62</th>
      <td>A3GZKD</td>
      <td>AVMX</td>
      <td>&lt;NA&gt;</td>
      <td>Global X Aave ETP</td>
      <td>Aave</td>
      <td>2023-03-13</td>
      <td>311</td>
      <td>0.852055</td>
      <td>Long-only</td>
      <td>Jersey</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>0.99</td>
      <td>Physically backed</td>
      <td>0</td>
      <td>False</td>
      <td>&lt;NA&gt;</td>
      <td>-9.48</td>
      <td>1.09</td>
      <td>-6.73</td>
      <td>56.94</td>
      <td>38.15</td>
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
      <td>-40.18</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Cryptocurrencies</td>
      <td>ETN</td>
      <td></td>
      <td>gettex, XETRA</td>
    </tr>
    <tr>
      <th>IE000GGQK173</th>
      <td>A3D4VW</td>
      <td>R8T</td>
      <td>125589092</td>
      <td>abrdn Global Real Estate Active Thematics UCITS ETF USD Accumulating ETF</td>
      <td>abrdn Global Real Estate Active Thematics</td>
      <td>2023-02-22</td>
      <td>330</td>
      <td>0.904110</td>
      <td>Long-only, Active</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>False</td>
      <td>False</td>
      <td>Accumulating</td>
      <td>0.40</td>
      <td>Full replication</td>
      <td>10</td>
      <td>True</td>
      <td>&lt;NA&gt;</td>
      <td>-2.14</td>
      <td>-1.93</td>
      <td>-1.82</td>
      <td>8.67</td>
      <td>4.21</td>
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
      <td>-15.23</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Real Estate</td>
      <td>ETF</td>
      <td>World</td>
      <td>gettex, XETRA</td>
    </tr>
    <tr>
      <th>IE00B0M62Y33</th>
      <td>A0HGWF</td>
      <td>IUSJ</td>
      <td>2308837</td>
      <td>iShares AEX UCITS ETF</td>
      <td>AEX®</td>
      <td>2005-11-18</td>
      <td>6635</td>
      <td>18.178082</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>False</td>
      <td>True</td>
      <td>Distributing</td>
      <td>0.30</td>
      <td>Full replication</td>
      <td>573</td>
      <td>False</td>
      <td>26</td>
      <td>-2.49</td>
      <td>-0.98</td>
      <td>-3.28</td>
      <td>4.46</td>
      <td>0.15</td>
      <td>4.79</td>
      <td>25.08</td>
      <td>70.81</td>
      <td>16.77</td>
      <td>-11.78</td>
      <td>29.89</td>
      <td>5.14</td>
      <td>2.18</td>
      <td>2.23</td>
      <td>12.06</td>
      <td>16.27</td>
      <td>18.5</td>
      <td>0.4</td>
      <td>0.48</td>
      <td>0.61</td>
      <td>-62.93</td>
      <td>-9.52</td>
      <td>-22.39</td>
      <td>-35.73</td>
      <td>Equity</td>
      <td>ETF</td>
      <td></td>
      <td>gettex, London, SIX Swiss Exchange, Euronext Amsterdam</td>
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
      <th>2024-01-13</th>
      <td>61.60</td>
      <td>199.029126</td>
      <td>0.0</td>
      <td>9.43</td>
      <td>71.03</td>
      <td>244.805825</td>
      <td>19.169742</td>
      <td>80.769742</td>
      <td>292.086128</td>
    </tr>
    <tr>
      <th>2024-01-14</th>
      <td>61.60</td>
      <td>199.029126</td>
      <td>0.0</td>
      <td>9.43</td>
      <td>71.03</td>
      <td>244.805825</td>
      <td>19.169742</td>
      <td>80.769742</td>
      <td>292.086128</td>
    </tr>
    <tr>
      <th>2024-01-15</th>
      <td>61.48</td>
      <td>198.446602</td>
      <td>0.0</td>
      <td>9.43</td>
      <td>70.91</td>
      <td>244.223301</td>
      <td>19.132399</td>
      <td>80.612399</td>
      <td>291.322324</td>
    </tr>
    <tr>
      <th>2024-01-16</th>
      <td>61.51</td>
      <td>198.592233</td>
      <td>0.0</td>
      <td>9.43</td>
      <td>70.94</td>
      <td>244.368932</td>
      <td>19.141735</td>
      <td>80.651735</td>
      <td>291.513275</td>
    </tr>
    <tr>
      <th>2024-01-17</th>
      <td>61.19</td>
      <td>197.038835</td>
      <td>0.0</td>
      <td>9.43</td>
      <td>70.62</td>
      <td>242.815534</td>
      <td>19.042151</td>
      <td>80.232151</td>
      <td>289.476464</td>
    </tr>
  </tbody>
</table>
<p>6656 rows × 9 columns</p>

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
      <th>2024-01-13</th>
      <td>219.523167</td>
      <td>114.806165</td>
    </tr>
    <tr>
      <th>2024-01-14</th>
      <td>219.523167</td>
      <td>114.806165</td>
    </tr>
    <tr>
      <th>2024-01-15</th>
      <td>218.983356</td>
      <td>114.572630</td>
    </tr>
    <tr>
      <th>2024-01-16</th>
      <td>219.118309</td>
      <td>112.937879</td>
    </tr>
    <tr>
      <th>2024-01-17</th>
      <td>217.678812</td>
      <td>108.967772</td>
    </tr>
  </tbody>
</table>
<p>6635 rows × 2 columns</p>

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
