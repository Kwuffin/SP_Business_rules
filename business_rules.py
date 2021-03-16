import psycopg2
from random import randint  # Used to get a bit of randomization in reccomendations

# Connect to database
c = psycopg2.connect("dbname=test user=postgres password=pass")  # TODO: edit this according to your database
cur = c.cursor()


def content_filtering(product_id):
    """
    Gathers all products with a similar category, subcategory and subsubcategory
    and picks four recommendations based on the product given as input
    :param product_id: Input product
    :return:
    """

    # Get attributes of input product
    subsubcategory = get_prod_attributes(product_id)

    # Get products with same subsubcategory:
    cur.execute(f"SELECT id FROM products WHERE subsubcategory = '{subsubcategory[0]}'")
    subsub_products = cur.fetchall()

    # Select four random recommendations in the same subsubcategory
    recommendations = [subsub_products[randint(0, len(subsub_products))][0] for _ in range(4)]
    print(recommendations)
    return recommendations


def get_prod_attributes(product_id):
    cur.execute(f"SELECT subsubcategory FROM products WHERE id = '{product_id}';")
    return cur.fetchone()


def main():
    rec_option = input("Wat voor recommendation wil je?   (Vul '1' of '2' in)\n"
                       "1. Collaborative\n"
                       "2. Content-based\n> ")
    if rec_option == "1":
        pass
    elif rec_option == "2":
        prod_id_in = input("Geef een product id waar je recommendations voor wil:\n> ")
        content_filtering(prod_id_in)
    else:
        print("Geen geldige invoer.")


if __name__ == '__main__':
    main()
