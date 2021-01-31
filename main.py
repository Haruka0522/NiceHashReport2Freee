import argparse
import csv
from models import NicehashReport, FreeeReport


def parse_augment():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, help="path to nicehash report csv file")
    parser.add_argument("--output_name", type=str, help="output csv file name")
    args = parser.parse_args()

    return args


def load_input(filename):
    transaction_list = []
    with open(filename) as f:
        reader = [row for row in csv.reader(f)]
        for data in reader[1:-6]:
            transaction = NicehashReport(**{
                "datetime": data[0],
                "local_datetime": data[1],
                "purpose": data[2],
                "amount_btc": float(data[3]),
                "exchange_rate": float(data[4]),
                "amount_jpy": float(data[5])
            })
            transaction_list.append(transaction)

    return transaction_list


def convert_to_freee_category(transaction_list):
    out = []
    for transaction in transaction_list:
        if transaction.purpose == "Hashpower mining":
            out.append(FreeeReport(**{
                "収支区分": "収入",
                "発生日": transaction.local_datetime.split()[0],
                "勘定科目": "売上高",
                "税区分": "対象外",
                "金額": transaction.amount_jpy,
                "備考": "マイニング",
                "品名": "BTC"
            }))

        elif transaction.purpose == "Hashpower mining fee":
            out.append(FreeeReport(**{
                "収支区分": "支出",
                "発生日": transaction.local_datetime.split()[0],
                "勘定科目": "支払手数料",
                "税区分": "対象外",
                "金額": abs(transaction.amount_jpy),
                "備考": "マイニング手数料",
                "品名": ""
            }))

        # elif transaction.purpose == "Exchange trade":
        #    #交換の収支の計算を実装する
        #    out.append(FreeeReport(**{
        #        "収支区分": "収入",
        #        "発生日": transaction.local_datetime.split()[0],
        #        "勘定科目": "売上高",
        #        "税区分": "対象外",
        #        "金額":,
        #        "備考": "通貨交換収入",
        #        "品名": ""
        #    }))

        else:
            print(f"{transaction.purpose} is not supported in this version.")
    return out


def generate_freee_csv(output_filename, data):
    field_names = data[0].dict().keys()
    with open(output_filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for i in data:
            writer.writerow(i.dict())


if __name__ == "__main__":
    args = parse_augment()
    transaction_list = load_input(args.input_csv)
    generate_freee_csv(args.output_name, convert_to_freee_category(transaction_list))
