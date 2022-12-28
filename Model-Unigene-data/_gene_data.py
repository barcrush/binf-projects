"""
Example script:
Gene data extracted from `unigene_model.py` is written to ".unigene" files
"""
import json

from unigene_model import get_unigene_data_structure
gene = get_unigene_data_structure(file='Unigene')

'''
gene = {
      'CHROMOSOME': '14',
      'CYTOBAND': '14q11.2',
      'EXPRESS': [
             'adipose tissue',
             'bladder',
             'brain',
             'cervix',
             'embryonic tissue',
             'esophagus',
             'eye',
             'intestine',
             'kidney',
             'larynx',
             'lung',
             'mammary gland',
             'pancreatic tumor',
             'skin tumor',
             'uterine tumor',
             'embryoid body',
             'fetus',
             'neonate',
             'adult'],
      'GENE': 'TGM1',
      'ID': 'Hs.508950',
      'LOCUSLINK': '7051',
      'PROTSIM': [
             {'ALN': 816,
              'ORG': 9986,
              'PCT': 94.13,
              'PROTGI': 291403635,
              'PROTID': 'XP_002718148.1'
             },
             {'ALN': 815,
              'ORG': 9606,
              'PCT': 100.0,
              'PROTGI': 4507475,
              'PROTID': 'NP_000350.1'
             },
             {'ALN': 701,
              'ORG': 7719,
              'PCT': 47.51,
              'PROTGI': 198433080,
              'PROTID': 'XP_002119887.1'
             },
           ],
     'TITLE': 'Transglutaminase 1 (K polypeptide epidermal type I, protein-glutamine-gamma-glutamyltransferase)',
}
'''

with open("TGM1.unigene", "w") as write_file:
    json.dump(gene, write_file, sort_keys=True, indent=4)




