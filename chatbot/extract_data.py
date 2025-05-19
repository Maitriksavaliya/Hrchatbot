
def _extract_single_field(user, field_name):
    """
    Helper function to extract a single field from a user object.
    
    Args:
        user (dict): The user object from the API response.
        field_name (str): The field to extract.
    
    Returns:
        The value of the field if found, None otherwise.
    """
    joining_detail_fields = [
        "employeeJoiningDetailId" , "employeeCode" , "AccountMasterId" , "dob" , "joiningDate" , "leavingDate","adharCard" , "esicNumber" , "pfNumber" , "uanNumber" , "pancard" , "bankMasterID" , "bankBranchID" , "bankIFSC"  , "bankAccountNo" , "retirementAge" , "retirementDate" , "noticePeriod" , "applicableDate" , "endDate" , "salarytype" , "biometricCode" , "biometricSerialNo"  , "salaryCalculationAct" , "employment" , "overtime"  , "esicEndMonth" , "adharName"  , "pfjoiningDate" , "pfbankMasterID" , "pfbankIFSC" , "pfbankAccountNo" , "esicjoiningDate" , "bloodgroup" , "nationality" , "attendanceFrom" , "fullMonthPresence" , "nameAsBank" , "employeeType" , "contractorId" , "payrollFrequency"
    ]

    company_details =["companyMasterID" , "companyName" , "companyAddress" , "companyWebsite" , "companyEmail" , "companyLogo" , "cpName" , "cpMobileNo" , "cpEmail" , "parentCompanyMasterID" , "subCompanyRequired" , "employeeCodePattern" , "expenseDatePicker" , "panNumber" , "tanNumber" , "companyDescription" , "employeeCodeType" , "authorizedSignature" ,  "customerListPreference" , "ownerName" , "ownerFatherName" , "tdsdeduction" , "uniqueEmpCode" , "cinNumber" , "setUpTime"]
    
    if field_name in ["displayName" , "displayNameWithNumber" , "userMasterID" , "firstName" , "middleName" , "lastName" , "userNumber" , "gender" , "maratialStatus" , "email" , "otherContactNumber" , "status"]:
        return user.get(field_name)
    
    elif field_name == "roleName":
        if (isinstance(user.get('userRoles'), list) and 
            len(user['userRoles']) > 0 and
            isinstance(user['userRoles'][0].get('roleMaster'), dict)):
            return user['userRoles'][0]['roleMaster'].get('roleName')
        else:
            return None
    
    elif field_name in company_details:
        print(field_name)
        if isinstance(user.get("companyMaster"), dict):
            return user["companyMaster"].get(field_name)
        else:
            return None

        
    elif field_name in joining_detail_fields:
        if isinstance(user.get('employeeJoiningDetails'), list) and len(user['employeeJoiningDetails']) > 0:
            return user['employeeJoiningDetails'][0].get(field_name)
        else:
            return None
        
    elif field_name == "createdBy_displayName":
        parent_key, child_key = field_name.split('_', 1)
        if isinstance(user.get(parent_key), dict):
            return user[parent_key].get(child_key)
        else:
            return None
        
    elif field_name == "updatedBy_displayName":
        parent_key, child_key = field_name.split('_', 1)
        if isinstance(user.get(parent_key), dict):
            return user[parent_key].get(child_key)
        else:
            return None
    
    elif field_name == "departmentName":
        if (isinstance(user.get('employeeDepartments'), list) and 
            len(user['employeeDepartments']) > 0 and
            isinstance(user['employeeDepartments'][0].get('department'), dict)):
            return user['employeeDepartments'][0]['department'].get('departmentName')
        else:
            return None
    
    elif field_name == "designationName":
        if (isinstance(user.get('employeeDesignations'), list) and 
            len(user['employeeDesignations']) > 0 and
            isinstance(user['employeeDesignations'][0].get('designation'), dict)):
            return user['employeeDesignations'][0]['designation'].get('designationName')
        else:
            return None
    
    elif field_name == "branchName":
        if (isinstance(user.get('employeeBranches'), list) and 
            len(user['employeeBranches']) > 0 and
            isinstance(user['employeeBranches'][0].get('branchMaster'), dict)):
            return user['employeeBranches'][0]['branchMaster'].get('branchName')
        else:
            return None
    
    else:
        # Try dot notation for nested fields
        field_parts = field_name.split('.')
        current = user
        for part in field_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

def extract_fields(api_response, field_names):
    """
    Extract the values of specified fields from the API response for the given fields.
    
    Args:
        api_response (dict): The JSON API response as a dictionary.
        field_names (list of str): The fields to extract (e.g., ['firstName', 'departmentName']).
    
    Returns:
        dict: A dictionary where keys are field names and values are lists of values 
              for that field across all users in the response. Each list contains 
              values for all users, with None if the field is not found for a user.
    
    Raises:
        ValueError: If api_response is not a dictionary or field_names is not a list of strings.
    """
    # Type checking
    if not isinstance(api_response, dict):
        raise ValueError("api_response must be a dictionary")
    if not isinstance(field_names, list) or not all(isinstance(field, str) for field in field_names):
        raise ValueError("field_names must be a list of strings")
    
    # Initialize result dictionary with empty lists for each field
    result_dict = {field: [] for field in field_names}
    
    # Check if 'data' key exists and is a list
    if 'data' not in api_response or not isinstance(api_response['data'], list):
        return result_dict
    
    # Iterate through each user and extract all requested fields
    for user in api_response['data']:
        for field in field_names:
            value = _extract_single_field(user, field)
            result_dict[field].append(value)

    
    return result_dict