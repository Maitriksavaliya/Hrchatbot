import requests
import json

GROQ_API_KEY = "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"  # Replace with your real key

def extract_intent_entity_field_groq(user_query: str) -> dict:
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an intelligent HR assistant.

Below is a list of valid fields related to employee and company information:
["displayName" , "displayNameWithNumber" , "userMasterID" , "firstName" , "middleName" , "lastName" , "userNumber" , "gender" , "maratialStatus" , "email" , "otherContactNumber" , "status" , "roleName" , "companyMasterID" , "companyName" , "companyAddress" , "companyWebsite" , "companyEmail" , "companyLogo" , "cpName" , "cpMobileNo" , "cpEmail" , "parentCompanyMasterID" , "subCompanyRequired" , "employeeCodePattern" , "expenseDatePicker" , "panNumber" , "tanNumber" , "companyDescription" , "employeeCodeType" , "authorizedSignature" ,  "customerListPreference" , "ownerName" , "ownerFatherName" , "tdsdeduction" , "uniqueEmpCode" , "cinNumber" , "setUpTime" , "employeeJoiningDetailId" , "employeeCode" , "AccountMasterId" , "dob" , "joiningDate" , "leavingDate","adharCard" , "esicNumber" , "pfNumber" , "uanNumber" , "pancard" , "bankMasterID" , "bankBranchID" , "bankIFSC"  , "bankAccountNo" , "retirementAge" , "retirementDate" , "noticePeriod" , "applicableDate" , "endDate" , "salarytype" , "biometricCode" , "biometricSerialNo"  , "salaryCalculationAct" , "employment" , "overtime"  , "esicEndMonth" , "adharName"  , "pfjoiningDate" , "pfbankMasterID" , "pfbankIFSC" , "pfbankAccountNo" , "esicjoiningDate" , "bloodgroup" , "nationality" , "attendanceFrom" , "fullMonthPresence" , "nameAsBank" , "employeeType" , "contractorId" , "payrollFrequency" , "createdBy_displayName" , "updatedBy_displayName" , "designationName" , "departmentName" , "branchName" ]

Your task is to extract the following from the user’s query:

1. Intent: Set to "get_personal_info" if the query requests information that is closely related to any of the valid fields listed above. For all other queries, set to null.
2. Entity: The full name of the employee mentioned in the query. If no employee name is provided, set to null.
3. Field: Identify all fields from the query that match or are closely related to the valid fields list. Return them as a list. If no fields in the query are related to the list, set to null.


Important Rules:

-Do NOT invent new field names. Only use fields from the provided list.
-Match the meaning of the query with the closest valid field(s).
-If the query contains multiple fields, return them as a list under the 'field' key.
-If the query does not relate to any fields in the list, set both 'intent' and 'field' to null.
-If no employee name is provided, set 'entity' to null.

Return the output in valid JSON format like this:
{{
  "intent": "<intent_name>",
  "entity": "<employee_full_name>",
  "field": ["<field_requested_1>", "<field_requested_2>", ...] or null
}}

Do not give the explanation.

User query: "{user_query}"
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 1,
        "max_tokens": 200,
        "top_p": 0.9
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            result = json.loads(content)
            intent = result.get("intent", None)
            entity = result.get("entity", None)
            field = result.get("field", None)
            return intent,entity,field
            
        else:
            print("Request failed:", response.status_code, response.text)
            intent = None
            entity = None
            field = None
            return intent,entity,field
        
    except Exception as e:
        print("Error:", e)
        intent = None
        entity = None
        field = None
        return intent,entity,field
    
if __name__ == "__main__":
        
        while True:
            query = input("enter your query:")
        
            if query =="exit":
                break
            intent,entity,field = extract_intent_entity_field_groq(query)
            print(intent,entity,field)
