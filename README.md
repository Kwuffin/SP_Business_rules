# SP_Business_rules
I used the database made by Nick Roumimper to make these recommendations.

### Collaborative filitering rule
This rule looks at all the viewed products in a profile and selects a random product from that list.
We want it random, because otherwise the customer will get the same recommended products every time,
which gets really annoying.

After a product is chosen, it will look for other profiles that looked at the same product.
A random profile will be selected and the program is going to check if this
profile has viewed enough products to make new recommendations.

If a profile is accepted, it will look up all the products that this user has
viewed and there will be four recommendations chosen for the given user.

### Content filtering rule
This rule gets a product as input in order to make recommendations.

This rules is quite simple, it looks at the input product's attributes.

Once its subsubcategory is obtained, it will look for other products with the same
subsubcategory. It will pick four random products to recommend.

