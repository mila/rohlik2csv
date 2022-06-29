
# rohlik2csv

Parse items from invoiced geneated by Rohlik.cz.


## Installation

* Make sure that Java is installed.
* Make sure that you have Python3 and pip installed.
  Installation into a vitualenv is recommended.
* `pip install tabula-py`


## Usage

At Rohlik.cz, go to "Můj účet" > "Minulé nákupy" and download an invoice "Daňový doklad" for each order.
Move all the downloaded invoices into the `faktury/` directory. 

```
./rohlik2csv.py faktury/ > faktury/data.csv 
```
