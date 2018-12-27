#!/usr/bin/env python3

import argparse
import json
import uuid

import pandas as pd
import sys
import time
import yaml


def generate_payload(patients, metadata):
    return {
        'id': str(uuid.uuid4()),
        'timestamp': str(time.time()),
        'subjects': patients,
        'metadata': metadata,
        'flags': {
            'source': 'EMR',
            'mailing_type': 'EMR',
            'research_project': True,
            'site': 1
        }
    }


def load_patients(filename):
    pts = pd.read_table(filename, header=None)
    return pts[0].tolist()


def load_metadata(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


def write_payload(file, payload):
    file.write(json.dumps(payload))


def run_program(args):
    patients = load_patients(args.patients)
    metadata = load_metadata(args.metadata)

    payload = generate_payload(patients, metadata)

    write_payload(args.output, payload)


def parse_arguments(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--patients', required=True)
    parser.add_argument('-m', '--metadata', required=True)
    parser.add_argument('-o', '--output', default=sys.stdout, type=argparse.FileType('w'))

    return parser.parse_args(args)


def main(args=None):
    args = parse_arguments(args)
    run_program(args)


if __name__ == '__main__':
    main()
