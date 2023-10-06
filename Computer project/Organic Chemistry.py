import requests


CACTUS = "https://cactus.nci.nih.gov/chemical/structure/{0}/{1}"


def smiles_to_iupac(smiles):
    rep = "iupac_name"
    url = CACTUS.format(smiles, rep)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


print(smiles_to_iupac('c1ccccc1'))
print(smiles_to_iupac('CC(=O)OC1=CC=CC=C1C(=O)O'))