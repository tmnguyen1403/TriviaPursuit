from category_selection import CategorySelection

cs = CategorySelection()
cs.run()
pair = cs.get_Selected_Categories()
for i in range(0, len(pair)):
    print(f"Category: {pair[i].name}, Color: {pair[i].color}")