import csv
import pathlib

import numpy as np
from lxml import objectify


def parse(xml_file_path):
    with xml_file_path.open('r', encoding='utf-8') as f:
        root = objectify.fromstring(f.read())
        dice_value = root.metrics.DICE.attrib['value']

    return (xml_file_path.parent.stem, float(dice_value))


def parse_and_save(main_path, cvs_file_path):
    # specifying the fields for csv file
    fields = ['id', 'name', 'dice']

    all_values = []
    for idx, p_path in enumerate(main_path.iterdir()):
        xml_file_path = p_path.joinpath('out.xml')
        parse_item = parse(xml_file_path)
        all_values.append({fields[0]: idx,
                           fields[1]: parse_item[0],
                           fields[2]: parse_item[1]})

    # calc mean and std value
    value_list = [item[fields[2]] for item in all_values]
    mean = np.mean(value_list)
    std = np.std(value_list)
    all_values.append({
        fields[0]: -2,
        fields[1]: 'mean',
        fields[2]: round(mean, 5)
    })
    all_values.append({
        fields[0]: -1,
        fields[1]: 'std',
        fields[2]: round(std, 5)
    })

    with cvs_file_path.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(all_values)


if __name__ == "__main__":
    main_path = pathlib.Path('./data')
    cvs_file_path = main_path.joinpath('all_out.csv')
    parse_and_save(main_path, cvs_file_path)
