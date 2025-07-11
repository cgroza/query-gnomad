from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import asyncio
import json
import sys
import time

transport = AIOHTTPTransport(url="https://gnomad.broadinstitute.org/api", ssl=False)
client = Client(transport=transport, fetch_schema_from_transport=True)

def fetch_gnomad(snp):
    query = gql("""
    query VariantSet {{
    variant(dataset: gnomad_r4, variantId: "{snp}") {{
        variantId
        genome {{
        populations {{
            id
            ac
            an
        }}
        }}
    }}
    }}
    """.format(snp = snp))
    return client.execute(query, parse_result = True)

def query_snps(snps):
    # snps = ["chr1:14038951:G:A"]
    for snp in snps:
        try:
            yield fetch_gnomad(snp)
        except:
            print(snp, "FAILED")
        time.sleep(6)


snps_file = open(sys.argv[1])

done_snps = []
if len(sys.argv) == 3:
    done_file = open(sys.argv[2])
    done_snps = ["chr" + line.split()[0].replace("-", ":") for line in done_file.readlines() if line.split()[1] != "FAILED"]

snps = []
for snp in snps_file.read().splitlines():
    if snp not in done_snps:
        snps.append(snp)

print("SNP", "POP", "AC", "AN", "AF")
for result in query_snps(snps):
    if result is None:
        continue
    if result['variant']['genome'] is None:
        continue
    pops = result['variant']['genome']['populations']
    for pop in pops:
        if pop["id"] in ["afr", "nfe"]:
            if pop['an'] == 0:
                continue
            print(result['variant']['variantId'], pop['id'], pop['ac'], pop['an'],
                  round(float(pop['ac'])/float(pop['an']), 6)
                  )
