def strip_ingredients():
    """Clean up the data from the New York Times so it's just a list of ingredients"""

    contents = open("New_York_Times_ingredient_phrase_tagger.txt")
    output = open("ingredients_list.txt", "a+")

    for line in contents.xreadlines():

        line_as_list = line.split(",")
        output.write(line_as_list[2] + "\n")

    contents.close()
    output.close()


strip_ingredients()





# I think the way to do this is to strip out the number and the comma that come first,
# then see if the first character in the string is a comma and if it is, treat it differently,
# if it isn't, the method above works.
#  Remember to delete the contents of the file first or switch to w instead of a+
# w might be the better way, anyway.
