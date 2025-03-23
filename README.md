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

Load overviews for all available (over 3500 at the moment) ETFs (requires a request for all ETF type: long-only, active, short & leveraged):

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
      <td>5422</td>
      <td>14.854795</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.43</td>
      <td>17.83</td>
      <td>18.80</td>
      <td>0.64</td>
      <td>0.58</td>
      <td>1.11</td>
      <td>-33.71</td>
      <td>-13.35</td>
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
      <td>5658</td>
      <td>15.501370</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>13.34</td>
      <td>15.05</td>
      <td>16.01</td>
      <td>0.72</td>
      <td>0.63</td>
      <td>1.19</td>
      <td>-33.91</td>
      <td>-11.29</td>
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
      <td>4688</td>
      <td>12.843836</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.63</td>
      <td>18.04</td>
      <td>18.91</td>
      <td>0.61</td>
      <td>0.56</td>
      <td>1.10</td>
      <td>-33.70</td>
      <td>-13.35</td>
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
      <td>5421</td>
      <td>14.852055</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>15.45</td>
      <td>17.88</td>
      <td>18.85</td>
      <td>0.62</td>
      <td>0.58</td>
      <td>1.12</td>
      <td>-33.69</td>
      <td>-13.34</td>
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
      <td>3950</td>
      <td>10.821918</td>
      <td>Long-only</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>13.51</td>
      <td>13.46</td>
      <td>14.97</td>
      <td>0.75</td>
      <td>0.29</td>
      <td>0.70</td>
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
      <th>XS2427363036</th>
      <td>A3GWVS</td>
      <td>2FLY</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree STOXX Europe Travel &amp; Leisure 2x Da...</td>
      <td>2022-03-02</td>
      <td>1117</td>
      <td>3.060274</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>33.31</td>
      <td>42.83</td>
      <td>NaN</td>
      <td>-0.53</td>
      <td>0.08</td>
      <td>NaN</td>
      <td>-42.03</td>
      <td>-36.10</td>
      <td>-41.91</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>JE00B24DKJ77</th>
      <td>A0V6Y0</td>
      <td>4RTE</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree Nickel 1x Daily Short</td>
      <td>2008-02-22</td>
      <td>6239</td>
      <td>17.093151</td>
      <td>Short &amp; Leveraged</td>
      <td>Jersey</td>
      <td>USD</td>
      <td>...</td>
      <td>25.36</td>
      <td>46.61</td>
      <td>49.42</td>
      <td>0.54</td>
      <td>0.54</td>
      <td>-0.54</td>
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
      <td>1145</td>
      <td>3.136986</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>USD</td>
      <td>...</td>
      <td>132.24</td>
      <td>147.11</td>
      <td>NaN</td>
      <td>-0.72</td>
      <td>-0.56</td>
      <td>NaN</td>
      <td>-99.90</td>
      <td>-96.62</td>
      <td>-99.72</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2437455608</th>
      <td>A3GXB6</td>
      <td>STR2</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree STOXX Europe Travel &amp; Leisure 2x Da...</td>
      <td>2022-03-02</td>
      <td>1117</td>
      <td>3.060274</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>33.19</td>
      <td>42.81</td>
      <td>NaN</td>
      <td>0.26</td>
      <td>-0.48</td>
      <td>NaN</td>
      <td>-71.68</td>
      <td>-42.95</td>
      <td>-71.27</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>XS2427474023</th>
      <td>A3GWVN</td>
      <td>O2IG</td>
      <td>&lt;NA&gt;</td>
      <td>WisdomTree STOXX Europe Oil &amp; Gas 2x Daily Short</td>
      <td>2022-03-02</td>
      <td>1117</td>
      <td>3.060274</td>
      <td>Short &amp; Leveraged</td>
      <td>Ireland</td>
      <td>EUR</td>
      <td>...</td>
      <td>32.28</td>
      <td>41.67</td>
      <td>NaN</td>
      <td>-0.40</td>
      <td>-0.59</td>
      <td>NaN</td>
      <td>-63.42</td>
      <td>-25.16</td>
      <td>-58.53</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>3503 rows × 42 columns</p>

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

### 📈 Scrape ETF Chart Data from justETF ([e.g.](https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983#chart))

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
      <th>2025-03-17</th>
      <td>72.19</td>
      <td>250.436893</td>
      <td>0.0</td>
      <td>10.34</td>
      <td>82.53</td>
      <td>300.631068</td>
      <td>23.397581</td>
      <td>95.587581</td>
      <td>364.017386</td>
    </tr>
    <tr>
      <th>2025-03-18</th>
      <td>71.61</td>
      <td>247.621359</td>
      <td>0.0</td>
      <td>10.34</td>
      <td>81.95</td>
      <td>297.815534</td>
      <td>23.209597</td>
      <td>94.819597</td>
      <td>360.289306</td>
    </tr>
    <tr>
      <th>2025-03-19</th>
      <td>72.32</td>
      <td>251.067961</td>
      <td>0.0</td>
      <td>10.34</td>
      <td>82.66</td>
      <td>301.262136</td>
      <td>23.439716</td>
      <td>95.759716</td>
      <td>364.852990</td>
    </tr>
    <tr>
      <th>2025-03-20</th>
      <td>72.52</td>
      <td>252.038835</td>
      <td>0.0</td>
      <td>10.34</td>
      <td>82.86</td>
      <td>302.233010</td>
      <td>23.504538</td>
      <td>96.024538</td>
      <td>366.138534</td>
    </tr>
    <tr>
      <th>2025-03-21</th>
      <td>72.42</td>
      <td>251.553398</td>
      <td>0.0</td>
      <td>10.34</td>
      <td>82.76</td>
      <td>301.747573</td>
      <td>23.472127</td>
      <td>95.892127</td>
      <td>365.495762</td>
    </tr>
  </tbody>
</table>
<p>7085 rows × 9 columns</p>

Compare multiple charts based on some value:

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
      <th>2025-03-17</th>
      <td>271.255061</td>
      <td>142.830453</td>
    </tr>
    <tr>
      <th>2025-03-18</th>
      <td>268.645974</td>
      <td>144.932275</td>
    </tr>
    <tr>
      <th>2025-03-19</th>
      <td>271.839856</td>
      <td>145.025689</td>
    </tr>
    <tr>
      <th>2025-03-20</th>
      <td>272.739541</td>
      <td>144.231667</td>
    </tr>
    <tr>
      <th>2025-03-21</th>
      <td>272.289699</td>
      <td>144.231667</td>
    </tr>
  </tbody>
</table>
<p>7064 rows × 2 columns</p>

### 📋 Scrape ETF stock exchange listings from justETF ([e.g.](https://www.justetf.com/en/etf-profile.html?isin=IE00B4L5Y983#stock-exchange))

Load stock exchange listings of a chosen ETF by its ISIN:

```python
df = justetf_scraping.load_listings("IE00B4L5Y983")
df
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Listing</th>
      <th>Trade Currency</th>
      <th>Ticker</th>
      <th>Bloomberg /  iNAV Bloomberg Code</th>
      <th>Reuters RIC /  iNAV Reuters</th>
      <th>Market Maker</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>London Stock Exchange</td>
      <td>GBX</td>
      <td>SWDA</td>
      <td>- -</td>
      <td>- -</td>
      <td>-</td>
    </tr>
    <tr>
      <th>1</th>
      <td>gettex</td>
      <td>EUR</td>
      <td>EUNL</td>
      <td>- -</td>
      <td>- -</td>
      <td>-</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Stuttgart Stock Exchange</td>
      <td>EUR</td>
      <td>EUNL</td>
      <td>- -</td>
      <td>- -</td>
      <td>-</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Bolsa Mexicana de Valores</td>
      <td>MXN</td>
      <td>-</td>
      <td>IWDAN MM</td>
      <td>IWDAN.MX</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Borsa Italiana</td>
      <td>EUR</td>
      <td>SWDA</td>
      <td>SWDA IM INAVIWDE</td>
      <td>SWDA.MI IWDAEUR.DE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Euronext Amsterdam</td>
      <td>EUR</td>
      <td>IWDA</td>
      <td>IWDA NA INAVIWDE</td>
      <td>IWDA.AS IWDAEUR.DE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>London Stock Exchange</td>
      <td>USD</td>
      <td>IWDA</td>
      <td>IWDA LN INAVIWDU</td>
      <td>IWAD.L IWDAUSD.DE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>London Stock Exchange</td>
      <td>GBP</td>
      <td>SWDA</td>
      <td>SWDA LN INAVIWDG</td>
      <td>SWDA.L 0TV6INAV.DE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SIX Swiss Exchange</td>
      <td>USD</td>
      <td>SWDA</td>
      <td>SWDA SE INAVIWDU</td>
      <td>SWDA.S FX0AINAV.DE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>XETRA</td>
      <td>EUR</td>
      <td>EUNL</td>
      <td>EUNL GY INAVIWDE</td>
      <td>EUNL.DE IWDAEUR.DE</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

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
