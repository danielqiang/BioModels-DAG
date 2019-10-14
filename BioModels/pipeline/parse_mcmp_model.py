from typing import TextIO
from bs4 import BeautifulSoup


def parse_mcmp_model(file: TextIO):
    soup = BeautifulSoup(file, features='lxml')

    for compartment_tag in extract_compartments(soup):
        compartment = compartment_tag.attrs['id'] if 'id' in compartment_tag.attrs else compartment_tag.attrs['name']


def extract_compartments(soup: BeautifulSoup):
    for tag in soup.find_all("compartment"):
        yield tag


with open(r"C:\Users\danie\PythonProjects\BioModels\BioModels\curated\BIOMD0000000490.xml", "r", encoding='utf8') as f:
    parse_mcmp_model(f)
