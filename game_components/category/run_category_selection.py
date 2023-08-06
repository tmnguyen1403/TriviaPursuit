from category_selection import CategorySelectionScreen

cs = CategorySelectionScreen()
cs.run()
pair = cs.get_Selected_Categories()
for i in range(0, len(pair)):
    print(f"Category: {pair[i].name}, Color: {pair[i].color}")