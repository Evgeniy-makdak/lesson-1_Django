import csv
import json

def csvs_v_jsons():
    files = ('ads','categories')
    for file in files:
        with open(f'datasets/{file}.csv',encoding="utf-8") as csvfile:
            with open(f'datasets/{file}.json', "w", encoding="utf-8") as jsonfile:
                json.dump(list(csv.DictReader(csvfile)),jsonfile)


def load_data_ads(Ad):
    with open(f'datasets/ads.csv', encoding="utf-8") as csvfile:
        rows_data = list(csv.DictReader(csvfile))
    print(rows_data)
    for row_data in rows_data:
        ad = Ad(
            name = row_data["name"],
            author = row_data["author"],
            price = int(row_data["price"]),
            description = row_data["description"],
            address = row_data["address"],
            is_published = bool(row_data["is_published"]))
        try:
            ad.save()
        except:
            return False
    return True

def load_data_cat(Category):
    with open(f'datasets/categories.csv', encoding="utf-8") as csvfile:
        rows_data = list(csv.DictReader(csvfile))
    for row_data in rows_data:
        cat = Category(
            name = row_data["name"])
        try:
            cat.save()
        except:
            return False
    return True

