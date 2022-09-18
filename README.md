# Generating (divergent) bar plots of attitudes towards transport policy
Generating (divergent) bar plots using the data on attitudes towards transport policy in Switzerland (also known as "module 3") from the Mobility and Transport Microcensus (MTMC). This code does not estimate choice models for the stated ranking or stated choice data. It only generates descriptive statistics as bar plots and divergent bar plots. To know more about this module, check our paper published at the 22nd Swiss Transport Research Conference, "<a href="http://strc.ch/2022/Danalet_EtAl.pdf">Attitudes towards transportation policy in Switzerland: A new choice experiment</a>".

The code runs with python 3.9 and needs the following packages:
- pandas with openpyxl
- seaborn
- pyreadstat
- pathlib
- matplotlib