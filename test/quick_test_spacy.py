from argparse import Namespace
from main import main

opts = Namespace()
opts.config = f'./configs/config_localhost_test_spacy.yml'
main(opts)