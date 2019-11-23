import csv
import pathlib
from typing import Dict, List


def construct_rows(header: list, rows: list) -> List[Dict]:
    """Construct a list of csv row dicts.\n

    Arguments:
        header {list} -- csv header\n
        rows {list} -- csv contents\n
                        to warp if there is only a single row, e.g. [row]\n

    Returns:
        List[Dict] -- a list of csv rows\n
    """
    row_dicts = [{k: v for k, v in zip(header, row)} for row in rows]

    return row_dicts


def wirte_csv(csv_file: pathlib.Path, mode: str, header: list, contents: list) -> None:
    """write or append rows to csv file.\n

    Arguments:
        csv_file {pathlib.Path} -- csv file path\n
        mode {str} -- 'w' for write, 'a' for append\n
        header {list} -- csv header\n
        contents {list} -- csv contents\n
                        Use list to warp if there is only one row, e.g. [row].\n
                        Use `construct_rows()` if has header and contents is not dicts.\n
    """
    assert mode == 'w' or mode == 'a', f"mode must be one of 'w' or 'r', not {mode}"

    with csv_file.open(mode=mode, encoding='utf-8', newline='') as fw_csv:
        if header:
            writer = csv.DictWriter(fw_csv, fieldnames=header)

            # write csv header if file is not exists
            if not csv_file.exists() or mode == 'w':
                writer.writeheader()
        else:
            writer = csv.writer(fw_csv)

        writer.writerows(contents)


def read_csv(csv_file: pathlib.Path, has_header: bool=True):
    """read csv file\n

    Arguments:
        csv_file {pathlib.Path} -- csv file path\n

    Keyword Arguments:
        has_header {bool} -- whether to read with header (default: {True})\n

    Yields:
        [dict | List[str]] -- csv contents\n
                        yield a dict if `has_header` is `True`\n
                        yield a list of strings if `has_header` is `False`\n
    """
    with csv_file.open('r', encoding='utf-8', newline='') as fr_csv:
        if has_header:
            reader = csv.DictReader(fr_csv)
        else:
            reader = csv.reader(fr_csv)

        for row in reader:
            yield row


if __name__ == '__main__':
    csv_file = pathlib.Path('./w.csv')

    header = ['id', 'key', 'value']
    row1 = [1, 'a', '0.1']
    row2 = [2, 'b', '0.2']
    row3 = [3, 'c', '0.3']
    rows = [row1, row2, row3]

    rows = construct_rows(header, [row1])
    wirte_csv(csv_file=csv_file, mode='w', header=header, contents=rows)

    for row in read_csv(csv_file):
        print(row)
