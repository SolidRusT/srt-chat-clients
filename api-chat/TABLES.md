# Query availabe tables in BEA datasets

Use the `get-datasets.py` script and corresponding [document](./DATASETS.md), then run the `get-tables.py` python script to list the available tables for a given dataset, ensuring that you have exported the BEA_API_KEY.

Not all datasets have tables available.

```bash
python get-tables.py <dataset_name>
```

Example output:

```plaintext
❯ python get-tables.py
Enter the dataset name: Regional
Available Tables in Regional:
- CAEMP25N: Total full-time and part-time employment by NAICS industry
- CAEMP25S: Total full-time and part-time employment by SIC industry
- CAGDP1: County and MSA gross domestic product (GDP) summary
- CAGDP11: Contributions to percent change in real GDP
```
