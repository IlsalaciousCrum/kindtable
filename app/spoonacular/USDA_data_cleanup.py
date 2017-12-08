"""Clean up the USDA data from https://www.ars.usda.gov/ARSUserFiles/80400525/Data/SR27/asc/FOOD_DES.txt
   The data will be used to check ingredients to avoid against, when recipe searches come back blank."""


def trying():

    USDA = open("USDA.txt", "r")
    DATA = open("data.txt", "a")

    for a_line in USDA.readlines():
        b_line = a_line[16:]
        c_line = b_line.split("~^~")

        DATA.write(c_line[0] + "\n")

    USDA.close()
    DATA.close()

trying()
