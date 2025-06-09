# Counts the items in a user-given list
from icecream import ic


user_list = []
while True:
    user_input = input("please input your next item: ")
    if user_input == 'q' or 'quit' in user_input:
        ic(user_list)
        ic(len(user_list))
        quit()
    ic(f"You have entered {user_input}, adding it to the list.")
    user_list.append(user_input)
    ic(f"{user_input} was added to the list, the current list is: {user_list} with a length of {len(user_list)} entries.")

