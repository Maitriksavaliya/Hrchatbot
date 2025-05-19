def select_employee(employees):
    """
    Prompt the user to select an employee from a list of employees with the same name.
    
    Args:
        employees (list): A list of employee dictionaries from the API response.
    
    Returns:
        dict: The selected employee dictionary, or None if no valid selection is made.
    """
    if not employees:
        print("No employees found.")
        return None
    
    if len(employees) == 1:
        return employees[0]
    
    print(f"There are multiple employees with the same name:")
    for i, user in enumerate(employees, 1):
        print(f"{i}. {user['displayName']} with ID {user['userMasterID']}")
    
    try:
        choice = input("Please specify which one you want by entering the number: ")
        index = int(choice) - 1
        if 0 <= index < len(employees):
            return employees[index]
        else:
            print("Invalid choice. Please try again.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None