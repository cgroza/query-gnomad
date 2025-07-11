
# query-gnomad
Script to query allele frequencies from gnomAD

# Install GQL library
This script requires the GQL to run:
```
pip install "gql[all]"
```

# Usage:
To retrieve population frequencies of a list of SNPs use:
```
gnomad.py snpslist > snpfreqs.tsv
```

## Input
The list of SNPs is a file with one SNP per line.
For example:

```
chr19:712680:G:T
chr1:10974575:G:A
chr1:203144840:C:T
chr2:40463012:GA:G
chr17:16456743:A:G
```
