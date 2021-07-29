import csv


def parse_rckms_input():
    """Read tab delimited file from adjacent filesystem; return dict

    Using https://cste-my.sharepoint.com/:x:/r/personal/skrishan_cste_org/_layouts/15/Doc.aspx?sourcedoc=%7BF727CA70-1605-4E77-9C05-B9939A6C7190%7D&file=RCKMS%20Condition%20Codes.20210609.xlsx&action=default&mobileredirect=true
    as source data, scraped into tab delimited file `RCKMS_condition_codes.tdv

    The function parses the file and returns a list of dict rows based on the headers
    """
    results = []
    headers = []
    with open("pwd_check", 'w') as out:
        out.write("dummy file to help debug deployed path issues")

    with open("code_systems/RCKMS_condition_codes.tdv", 'r') as input:
        code_reader = csv.DictReader(input, delimiter='\t')
        for row in code_reader:
            results.append(dict(row))

    return results


def load_rckms_condition_codes():
    """Parse input and generate rows in the RCKMS lookup table"""
    from ..db import db
    from ..api.models import RckmsConditionCodes
    data = parse_rckms_input()
    for row in data:
        rcc = RckmsConditionCodes()
        rcc.condition = row['Condition']
        rcc.code = row['Code']
        rcc.code_system = row['Code System']
        db.session.add(rcc)
    db.session.commit()
