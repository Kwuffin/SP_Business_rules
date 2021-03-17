import psycopg2
from random import randint  # Used to get a bit of randomization in reccomendations

# Connect to database
c = psycopg2.connect("dbname=test user=postgres password=pass")  # TODO: edit this according to your database
cur = c.cursor()


def collaborative_filtering(profile_id):
    """
    Given the profile_id, gets the previously viewed product(s).
    Then looks at the profiles that also viewed that product
    :param profile_id:
    :return:
    """

    # Check if profile id exists in records
    cur.execute(f"SELECT prodid FROM profiles_previously_viewed WHERE profid = '{profile_id}';")
    valid = cur.fetchall()
    if not valid:
        print("Geen geldig profiel id")
        exit()

    # Check if any other profiles viewed the same product:
    profid_valid = ()
    count = 0
    while not profid_valid:
        count += 1
        # Get a random product from all viewed products
        viewed_prod = valid[randint(0, len(valid)-1)][0]

        # Get profiles that viewed the same product
        cur.execute(f"SELECT profid FROM profiles_previously_viewed WHERE prodid = '{viewed_prod}';")
        profid_valid = cur.fetchall()

        # If there are obviously no profiles that viewed the same product(s), resort to content filtering.
        if count == 300:
            recommendations = content_filtering(viewed_prod)
            return recommendations

    rand_profid = profid_valid[randint(0, len(profid_valid)-1)][0]
    cur.execute(f"SELECT prodid FROM profiles_previously_viewed WHERE profid = '{rand_profid}'")
    products_viewed = cur.fetchall()

    # If there are enough products to be recommended
    if len(products_viewed) >= 4:
        recommendations = [products_viewed[randint(0, len(products_viewed)-1)][0] for _ in range(4)]
        return recommendations
    else:
        return content_filtering(products_viewed[randint(0, len(products_viewed)-1)][0])


def content_filtering(product_id):
    """
    Gathers all products with a similar category, subcategory and subsubcategory
    and picks four recommendations based on the product given as input
    :param product_id: Input product
    :return:
    """

    # Check if product id exists in records
    cur.execute(f"SELECT * FROM products WHERE id = '{product_id}';")
    valid = cur.fetchall()
    if not valid:
        print("Geen geldig product id")
        exit()

    # Get attributes of input product
    subsubcategory = get_prod_attributes(product_id)

    # Get products with same subsubcategory:
    cur.execute(f"SELECT id FROM products WHERE subsubcategory = '{subsubcategory[0]}'")
    subsub_products = cur.fetchall()

    # Select four random recommendations in the same subsubcategory
    recommendations = [subsub_products[randint(0, len(subsub_products)-1)][0] for _ in range(4)]
    print(recommendations)
    return recommendations


def get_prod_attributes(product_id):
    cur.execute(f"SELECT subsubcategory FROM products WHERE id = '{product_id}';")
    return cur.fetchone()


def get_products(recommendations):
    for i, recommendation in enumerate(recommendations):
        cur.execute(f"SELECT * FROM products WHERE id = '{recommendation}'")
        print(f"Recommendation {i+1}:\n"
              f"{cur.fetchall()}\n")


def main():
    rec_option = input("Wat voor recommendation wil je?   (Vul '1' of '2' in)\n"
                       "1. Collaborative\n"
                       "2. Content-based\n> ")
    if rec_option == "1":
        prof_id_in = input("Geef een profiel id waar je recommendations voor wil:\n> ")
        rec = collaborative_filtering(prof_id_in)
    elif rec_option == "2":
        prod_id_in = input("Geef een product id waar je recommendations voor wil:\n> ")
        rec = content_filtering(prod_id_in)
    else:
        print("Geen geldige invoer.")
        exit()

    get_products(rec)


if __name__ == '__main__':
    main()
