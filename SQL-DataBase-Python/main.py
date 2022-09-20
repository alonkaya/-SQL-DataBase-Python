import sys

from Hat import Hat
from Order import Order
from Repository import repo
from Supplier import Supplier


def main(args):
    with open(sys.argv[1], 'r') as f:
        input_lines = f.readlines()  ##stringLines is list of strings

    list_of_lists = []  ##this will hold list of lists of the details as strings
    for line in input_lines:
        line_as_list = line.split(',')
        ##Remove the \n at the end:
        last_string_in_line = line_as_list[len(line_as_list) - 1]
        if last_string_in_line[len(last_string_in_line) - 1] == '\n':
            line_as_list[len(line_as_list) - 1] = last_string_in_line[:len(last_string_in_line) - 1]
        list_of_lists.append(line_as_list)

    repo.create_tables()

    i = 1
    while i < int(list_of_lists[0][0]) + 1:  ##parsing through hats and inserting given rows into table
        repo.hats.insert(Hat(*list_of_lists[i]))
        i = i + 1

    while i < len(list_of_lists):
        repo.suppliers.insert(Supplier(*list_of_lists[i]))  ##parsing through suppliers and inserting given rows
        i = i + 1

    ################################### Orders #################################

    with open(sys.argv[2], 'r') as f:
        input_lines = f.readlines()  ##stringLines is list of strings

    list_of_lists = []  ##this will hold list of lists of the details as strings
    for line in input_lines:
        line_as_list = line.split(',')
        ##Remove the \n at the end:
        last_string_in_line = line_as_list[len(line_as_list) - 1]
        if last_string_in_line[len(last_string_in_line) - 1] == '\n':
            line_as_list[len(line_as_list) - 1] = last_string_in_line[:len(last_string_in_line) - 1]
        list_of_lists.append(line_as_list)

    i = 0
    output = []
    while i < len(list_of_lists):
        location = list_of_lists[i][0]
        topping = list_of_lists[i][1]

        hat_of_topping = repo.hats.find_first_supplier_of_topping(topping)
        supplier_of_topping_name = repo.suppliers.find(hat_of_topping.supplier_id).name


        repo.orders.insert(Order(i + 1, location, hat_of_topping.id))  ##inserting order into database
        i = i + 1

        line = topping + "," + supplier_of_topping_name + "," + location
        output.append(line)

        ##decrement quantity of hat and delete row if quantity = 0
        repo.hats.decrement_quantity(hat_of_topping)
        quantity = hat_of_topping.quantity - 1
        if quantity == 0:
            repo.hats.remove(hat_of_topping.id)






    with open(sys.argv[3], 'w') as f:
        for line in output:
            f.write(line + '\n')


if __name__ == '__main__':  ##name is the class's name (in this case configMain)
    main(sys.argv)
