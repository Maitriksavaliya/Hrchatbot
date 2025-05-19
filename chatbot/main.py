
# import time
# import logging
# from query_class import extract_intent_entity_field_groq
# from api_call import get_users_by_search_query
# from extract_data import extract_fields
# from reponse import generate_natural_response

# # Set up logging
# logging.basicConfig(filename='hr_assistant.log', level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# if __name__ == "__main__":
#     # Hardcoded token and companyID for simplicity
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6eyJ1c2VybWFzdGVyaWQiOjMyOTMsInVzZXJUeXBlIjoiMCJ9LCJpYXQiOjE3NDc2MzM3NjMsImV4cCI6MTc0NzcyMDE2M30.VaiqLrGlzjMORYomZ3BQP6STl7cQhb2Y9HenoE_XX1A'
#     companyID = 68
#     last_entity = None  # To maintain context across queries

#     while True:
#         query = input("Enter your query: ")
#         if query.lower() == "exit":
#             logging.info("User exited the session.")
#             break

#         try:
#             logging.info(f"Query: {query}")
#             start_time = time.perf_counter()

#             # Extract intent, entity, and field from the query
#             intent, entity, field = extract_intent_entity_field_groq(query)

#             # Maintain context: use last_entity if entity is not provided
#             if entity is not None:
#                 last_entity = entity
#             elif last_entity is not None:
#                 entity = last_entity

#             logging.info(f"Extracted: intent={intent}, entity={entity}, field={field}")

#             # Fetch data from the API
#             api_res = get_users_by_search_query(token, companyID, intent, entity)

#             if api_res:
#                 logging.info("API call successful")
#                 result = extract_fields(api_res, field)
#             else:
#                 logging.info("API call failed or no data returned")
#                 result = None

#             # Generate natural language response
#             response = generate_natural_response(intent, entity, result)
#             logging.info(f"Response: {response}")

#             # Calculate and log response time
#             end_time = time.perf_counter()
#             duration = end_time - start_time
#             logging.info(f"Query processed in {duration:.2f} seconds")

#             print(response)

#         except Exception as e:
#             logging.error(f"Error processing query '{query}': {e}")
#             print("An error occurred. Please try again.")



# import time
# import logging
# from query_class import extract_intent_entity_field_groq
# from api_call import get_users_by_search_query
# from extract_data import extract_fields
# from reponse import generate_natural_response

# # Set up logging
# logging.basicConfig(filename='hr_assistant.log', level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# if __name__ == "__main__":
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6eyJ1c2VybWFzdGVyaWQiOjMyOTMsInVzZXJUeXBlIjoiMCJ9LCJpYXQiOjE3NDc2MzM3NjMsImV4cCI6MTc0NzcyMDE2M30.VaiqLrGlzjMORYomZ3BQP6STl7cQhb2Y9HenoE_XX1A'  # Replace with your actual token
#     companyID = 68
#     selected_user = None  # To maintain context across queries

#     while True:
#         query = input("Enter your query: ")
#         if query.lower() == "exit":
#             logging.info("User exited the session.")
#             break

#         try:
#             logging.info(f"Query: {query}")
#             start_time = time.perf_counter()

#             # Extract intent, entity, and field from the query
#             intent, entity, field = extract_intent_entity_field_groq(query)
#             logging.info(f"Extracted: intent={intent}, entity={entity}, field={field}")

#             # Handle case where an entity is provided
#             if entity is not None:
#                 api_res = get_users_by_search_query(token, companyID, intent, entity)
#                 if api_res and api_res.get('data'):
#                     data = api_res['data']
#                     if len(data) == 1:
#                         # Single employee found
#                         selected_user = data[0]
#                         logging.info("Single employee found.")
#                     else:
#                         # Multiple employees found
#                         print(f"There are multiple employees with the name {entity}:")
#                         for i, user in enumerate(data, 1):
#                             print(f"{i}. {user['displayName']} with ID {user['userMasterID']}")
#                         choice = input("Please specify which one you want by entering the number: ")
#                         try:
#                             index = int(choice) - 1
#                             if 0 <= index < len(data):
#                                 selected_user = data[index]
#                                 logging.info(f"User selected employee ID: {selected_user['userMasterID']}")
#                             else:
#                                 print("Invalid choice. Please try again.")
#                                 continue
#                         except ValueError:
#                             print("Invalid input. Please enter a number.")
#                             continue
#                 else:
#                     print("No employees found with that name.")
#                     selected_user = None
#                     continue
#             else:
#                 # No entity provided; use previously selected user if available
#                 if selected_user is None:
#                     print("Please specify an employee name.")
#                     continue

#             # Process the selected user
#             if selected_user is not None:
#                 selected_api_res = {'data': [selected_user]}
#                 result = extract_fields(selected_api_res, field)
#                 employee_name = selected_user['displayName']
#                 response = generate_natural_response(intent, employee_name, result)
#                 logging.info(f"Response: {response}")
#                 print(response)

#             end_time = time.perf_counter()
#             duration = end_time - start_time
#             logging.info(f"Query processed in {duration:.2f} seconds")

#         except Exception as e:
#             logging.error(f"Error processing query '{query}': {e}")
#             print("An error occurred. Please try again.")


import time
import logging
from query_class import extract_intent_entity_field_groq
from api_call import get_users_by_search_query
from extract_data import extract_fields
from reponse import generate_natural_response
from employee_selector import select_employee

# Set up logging
logging.basicConfig(filename='hr_assistant.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Hardcoded token and companyID (replace with actual values)
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6eyJ1c2VybWFzdGVyaWQiOjMyOTMsInVzZXJUeXBlIjoiMCJ9LCJpYXQiOjE3NDc2MzM3NjMsImV4cCI6MTc0NzcyMDE2M30.VaiqLrGlzjMORYomZ3BQP6STl7cQhb2Y9HenoE_XX1A'
    companyID = 68
    selected_user = None  # To maintain context across queries

    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            logging.info("User exited the session.")
            break

        try:
            logging.info(f"Query: {query}")
            start_time = time.perf_counter()

            # Extract intent, entity, and field from the query
            intent, entity, field = extract_intent_entity_field_groq(query)
            logging.info(f"Extracted: intent={intent}, entity={entity}, field={field}")

            # Handle case where an entity is provided
            if entity is not None:
                api_res = get_users_by_search_query(token, companyID, intent, entity)
                if api_res and api_res.get('data'):
                    employees = api_res['data']
                    selected_user = select_employee(employees)  # Handle multiple employees
                    if selected_user is None:
                        continue  # Invalid selection, prompt again
                else:
                    print("No employees found with that name.")
                    selected_user = None
                    continue
            else:
                # No entity provided; use previously selected user if available
                if selected_user is None:
                    print("Please specify an employee name.")
                    continue

            # Process the selected user
            if selected_user is not None:
                selected_api_res = {'data': [selected_user]}
                result = extract_fields(selected_api_res, field)
                employee_name = selected_user['displayName']
                response = generate_natural_response(intent, employee_name, result)
                logging.info(f"Response: {response}")
                print(response)

            end_time = time.perf_counter()
            duration = end_time - start_time
            logging.info(f"Query processed in {duration:.2f} seconds")

        except Exception as e:
            logging.error(f"Error processing query '{query}': {e}")
            print("An error occurred. Please try again.")