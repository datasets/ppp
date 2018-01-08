Purchasing power parity (PPP). Data are sourced from the World Bank, International Comparison Program database. One dataset is provided: PPP conversion factor, GDP (LCU per international $).

## Data

### Description

> Purchasing power parity conversion factor is the number of units of a country's currency required to buy the same amounts of goods and services in the domestic market as U.S. dollar would buy in the United States.[*][pa-nus-ppp]

### Citations

1. *PPP conversion factor, GDP (LCU per international $).* World Bank, International Comparison Program database.

### Sources

1. 
    * Name: PPP conversion factor, GDP (LCU per international $). World Bank, International Comparison Program database.
    * Web: http://data.worldbank.org/indicator/PA.NUS.PPP

## Preparation

### Requirements

Data preparation requires Python 2. Required external Python modules are listed in the `requirements.txt` file in this directory.

### Processing

Run the following script from this directory to download and process the data:

```bash
make data
```

### Resources

The raw data are output to `./tmp`. The processed data are output to `./data`.

## License

### ODC-PDDL-1.0

This Data Package is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/

### Notes

Refer to the [terms of use][worldbank] of the source dataset for any specific restrictions on using these data in a public or commercial product.

[pa-nus-ppp]: http://data.worldbank.org/indicator/PA.NUS.PPP 
[worldbank]: http://web.worldbank.org/WBSITE/EXTERNAL/0,,contentMDK:22547097~pagePK:50016803~piPK:50016805~theSitePK:13,00.html
