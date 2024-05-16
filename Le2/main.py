import time
import os
from util.user_manager import UserManager

def main():
    manager = UserManager()
    while True:
        try:
            os.system('cls')
            print("Welcome to Dice Roll Game!")
            option = int(input("1. Register\n2. Login\n3. Exit \n\nEnter number only: "))

            if option == 1:
                manager.register()
            elif option == 2:
                manager.login()
            elif option == 3:
                print(f"Thank you for using our program!")
                time.sleep(1)
                exit()
            else:
                raise ValueError("Enter number from list!")
            
        except ValueError as e:
            print("Error: ", e)
            time.sleep(1)

if __name__ == "__main__":
    main()

