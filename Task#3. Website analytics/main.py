import csv

def open_file(path):
    users = {}
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = row["user_id"].strip()
            product = row["product_id"].strip()
            users.setdefault(user, set()).add(product)
    return users

def find_users(file1, file2):
    day1 = open_file(file1)
    day2 = open_file(file2)

    result = []
    for user in day1.keys() & day2.keys():
        new_products = day2[user] - day1[user]
        print(f"User {user}: new_product={new_products}")
        if new_products:
            result.append(user)

if __name__ == "__main__":
    find_users("day1.csv", "day2.csv") #names of csv can be changed
