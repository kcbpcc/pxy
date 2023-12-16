import csv

def update_reinvest_csv(key):
    reinvest_file = 'reinvest.csv'

    try:
        with open(reinvest_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            key_exists = any(row['key'] == key for row in rows)

            if not key_exists:
                with open(reinvest_file, 'a', newline='') as csvfile:
                    fieldnames = ['key']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({'key': key})
                return True
            else:
                return False

    except FileNotFoundError:
        with open(reinvest_file, 'w', newline='') as csvfile:
            fieldnames = ['key']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'key': key})
        return True
