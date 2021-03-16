import hashlib
from datetime import date
# ---------------------------------------------------------------------->
# (Uploading to Google Sheets as represented Database)
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

spreadsheet_person = client.open('Sheets_database_copy').worksheet("individual_template")
spreadsheet_company = client.open('Sheets_database_copy').worksheet('company_template')
# ---------------------------------------------------------------------->


def user_validation(data):  # (Writing to a regular file)
    with open('database_users.txt', mode='a') as database_users:
        email = data["email"]
        file = database_users.write(f'''
        \n------------------------------------------>
        \nUser: {email} has been successfully saved to the database.
        \nPlease refer to query for password details.
        \n------------------------------------------>''')


def save_info_person_1(data):  # (Writing to a regular file)
    with open('database_info.txt', mode='a') as database_info:
        fiscal = data['fiscal']
        CURP = data['CURP']
        first_name = data['first_name']
        last_name = data['last_name']
        middle_name = data['middle_name']
        birthday = data['birthday']
        nationality = data['nationality']
        gender = data['gender']
        occupation = data['occupation']
        economic_sector = data['economic_sector']
        phone_number = data['phone_number']
        email = data['email']
        bank_name = data['bank_name']
        bank_number = data['bank_number']
        file = database_info.write(f'''
        
        \n++++++++++++++++++++++++++++++++++++++++++>
        \n++++++++++++++++++++++++++++++++++++++++++>
        THE FOLLOWING INFORMATION BELONGS TO THE USER
        WITH THE PROFILE OF: 
        {last_name}, {first_name}, {email}
        \n++++++++++++++++++++++++++++++++++++++++++>
        \n++++++++++++++++++++++++++++++++++++++++++>
        \n------------------------------------------>
        PERSONAL DETAILS:
        \n------------------------------------------>
        fiscal: {fiscal}
        CURP: {CURP}
        first_name: {first_name}
        last_name: {last_name}
        middle_name: {middle_name}
        birthday: {birthday}
        nationality: {nationality}
        gender: {gender}
        occupation: {occupation}
        economic_sector: {economic_sector}
        phone_number: {phone_number}
        email: {email}
        bank_name: {bank_name}
        bank_number: {bank_number}
        \n------------------------------------------>''')
    global new_sheet
    try:
        new_sheet = spreadsheet_person.duplicate(1, None, f'KYC_Fisicas - ({first_name}, {last_name}): ({email})')
        new_sheet = client.open('Sheets_database_copy').worksheet(
            f'KYC_Fisicas - ({first_name}, {last_name}): ({email})')
        new_sheet.update('A2', fiscal)
        new_sheet.update('B2', CURP)
        new_sheet.update('C2', first_name)
        new_sheet.update('D2', last_name)
        new_sheet.update('E2', middle_name)
        new_sheet.update('F2', birthday)
        new_sheet.update('G2', nationality)
        new_sheet.update('H2', gender)
        new_sheet.update('I2', occupation)
        new_sheet.update('J2', economic_sector)
        new_sheet.update('K2', phone_number)
        new_sheet.update('L2', email)
        new_sheet.update('M2', bank_name)
        new_sheet.update('N2', bank_number)
    except:
        new_sheet = client.open('Sheets_database_copy').worksheet(
            f'KYC_Fisicas - ({first_name}, {last_name}): ({email})')
        new_sheet.update('A2', fiscal)
        new_sheet.update('B2', CURP)
        new_sheet.update('C2', first_name)
        new_sheet.update('D2', last_name)
        new_sheet.update('E2', middle_name)
        new_sheet.update('F2', birthday)
        new_sheet.update('G2', nationality)
        new_sheet.update('H2', gender)
        new_sheet.update('I2', occupation)
        new_sheet.update('J2', economic_sector)
        new_sheet.update('K2', phone_number)
        new_sheet.update('L2', email)
        new_sheet.update('M2', bank_name)
        new_sheet.update('N2', bank_number)


def save_info_person_2(data):  # (Writing to a regular file)
    with open('database_info.txt', mode='a') as database_info:
        address = data['address']
        exterior_number = data['exterior_number']
        interior_number = data['interior_number']
        suburb = data['suburb']
        city = data['city']
        state = data['state']
        zip = data['zip']
        colony = data['colony']
        country = data['country']
        file = database_info.write(f'''
        ADDRESS DETAILS:
        \n------------------------------------------>
        address: {address}
        exterior_number: {exterior_number}
        interior_number: {interior_number}
        suburb: {suburb}
        city: {city}
        state: {state}
        zip: {zip}
        colony: {colony}
        country: {country}
        \n------------------------------------------>''')
    new_sheet_2 = new_sheet
    new_sheet.update('O2', address)
    new_sheet.update('P2', exterior_number)
    new_sheet.update('Q2', interior_number)
    new_sheet.update('R2', suburb)
    new_sheet.update('S2', city)
    new_sheet.update('T2', state)
    new_sheet.update('U2', zip)
    new_sheet.update('V2', colony)
    new_sheet.update('W2', country)


def save_info_person_3(data):  # (Writing to a regular file)
    with open('database_info.txt', mode='a') as database_info:
        average_position = data['average_position']
        operating_frequency = data['operating_frequency']
        beneficiaries = data['beneficiaries']
        who_1 = data['who_1']
        when_1 = data['when_1']
        what_position_1 = data['what_position_1']
        who_2 = data['who_2']
        when_2 = data['when_2']
        what_position_2 = data['what_position_2']
        who_3 = data['who_3']
        when_3 = data['when_3']
        file = database_info.write(f'''
        COMPLIANCE DETAILS:
        \n------------------------------------------>
        average_position: {average_position}
        operating_frequency: {operating_frequency}
        beneficiaries: {beneficiaries}
        who_1: {who_1}
        when_1: {when_1}
        what_position_1: {what_position_1}
        who_2: {who_2}
        when_2: {when_2}
        what_position_2: {what_position_2}
        who_3: {who_3}
        when_3: {when_3}
        \n------------------------------------------>''')
    time = str(date.today())
    new_sheet.update('X2', average_position)
    new_sheet.update('Y2', operating_frequency)
    new_sheet.update('Z2', beneficiaries)
    new_sheet.update('AA2', who_1)
    new_sheet.update('AB2', when_1)
    new_sheet.update('AC2', what_position_1)
    new_sheet.update('AD2', who_2)
    new_sheet.update('AE2', when_2)
    new_sheet.update('AF2', what_position_2)
    new_sheet.update('AG2', who_3)
    new_sheet.update('AH2', when_3)
    new_sheet.update('AI2', time)


def save_info_company_1(data):  # (Writing to a regular file)
    with open('database_info.txt', mode='a') as database_info:
        # (Page 1)
        company_legal_name = data['company_legal_name']
        date_of_incorporation = data['date_of_incorporation']
        nationality = data['nationality']
        fiscal = data['fiscal']
        CURP = data['CURP']
        business_purpose = data['business_purpose']
        phone_number = data['phone_number']
        email = data['email']
        legal_representative_name = data['legal_representative_name']
        nationality_of_legal = data['nationality_of_legal']
        bank_number = data['bank_number']
        file_data_company = database_info.write(f'''
        \n++++++++++++++++++++++++++++++++++++++++++>
        \n++++++++++++++++++++++++++++++++++++++++++>
        THE FOLLOWING INFORMATION BELONGS TO THE USER
        WITH THE PROFILE OF: {company_legal_name}, {email}
        \n++++++++++++++++++++++++++++++++++++++++++>
        \n++++++++++++++++++++++++++++++++++++++++++>
        \n------------------------------------------>
        COMPANY GENERAL DETAILS:
        \n------------------------------------------>
        company_legal_name: {company_legal_name}
        date_of_incorporation: {date_of_incorporation}
        nationality: {nationality}
        fiscal: {fiscal}
        CURP: {CURP}
        business_purpose: {business_purpose}
        phone_number: {phone_number}
        email: {email}
        legal_representative_name: {legal_representative_name}
        nationality_of_legal: {nationality_of_legal}
        bank_number: {bank_number}

        \n------------------------------------------>''')
    try:
        global new_sheet
        new_sheet = spreadsheet_company.duplicate(1, None, f'KYC_Morales - ({company_legal_name}): ({email})')
        new_sheet = client.open('Sheets_database_copy').worksheet(
            f'KYC_Morales - ({company_legal_name}): ({email})')
        new_sheet.update('A2', company_legal_name)
        new_sheet.update('B2', date_of_incorporation)
        new_sheet.update('C2', nationality)
        new_sheet.update('D2', fiscal)
        new_sheet.update('E2', CURP)
        new_sheet.update('F2', business_purpose)
        new_sheet.update('G2', phone_number)
        new_sheet.update('H2', email)
        new_sheet.update('I2', legal_representative_name)
        new_sheet.update('J2', nationality_of_legal)
        new_sheet.update('K2', bank_number)
    except:
        new_sheet = client.open('Sheets_database_copy').worksheet(
            f'KYC_Morales - ({company_legal_name}): ({email})')
        new_sheet.update('A2', company_legal_name)
        new_sheet.update('B2', date_of_incorporation)
        new_sheet.update('C2', nationality)
        new_sheet.update('D2', fiscal)
        new_sheet.update('E2', CURP)
        new_sheet.update('F2', business_purpose)
        new_sheet.update('G2', phone_number)
        new_sheet.update('H2', email)
        new_sheet.update('I2', legal_representative_name)
        new_sheet.update('J2', nationality_of_legal)
        new_sheet.update('K2', bank_number)


def save_info_company_2(data):  # (Writing to a regular file)
    with open('database_info.txt', mode='a') as database_info:
        address = data['address']
        exterior_number = data['exterior_number']
        interior_number = data['interior_number']
        suburb = data['suburb']
        city = data['city']
        state = data['state']
        zip = data['zip']
        colony = data['colony']
        country = data['country']
        file_data_company = database_info.write(f'''
        ADDRESS DETAILS:
        \n------------------------------------------>
        address: {address}
        exterior_number: {exterior_number}
        interior_number: {interior_number}
        suburb: {suburb}
        city: {city}
        state: {state}
        zip: {zip}
        colony: {colony}
        country: {country}
        \n------------------------------------------>''')
    new_sheet.update('L2', address)
    new_sheet.update('M2', exterior_number)
    new_sheet.update('N2', interior_number)
    new_sheet.update('O2', suburb)
    new_sheet.update('P2', city)
    new_sheet.update('Q2', state)
    new_sheet.update('R2', zip)
    new_sheet.update('S2', colony)
    new_sheet.update('T2', country)


def save_info_company_3(data):  # (Writing to a regular file)
    with open('database_info.txt', mode='a') as database_info:
        source_of_funding = data['source_of_funding']
        average_position = data['average_position']
        operating_frequency = data['operating_frequency']
        beneficiaries = data['beneficiaries']
        who_1 = data['who_1']
        when_1 = data['when_1']
        what_position_1 = data['what_position_1']
        who_2 = data['who_2']
        when_2 = data['when_2']
        what_position_2 = data['what_position_2']
        who_3 = data['who_3']
        when_3 = data['when_3']
        file_data_company = database_info.write(f'''
        COMPLIANCE AND OTHERS
        \n------------------------------------------>
        source_of_funding: {source_of_funding}
        average_position: {average_position}
        operating_frequency: {operating_frequency}
        beneficiaries: {beneficiaries}
        who_1: {who_1}
        when_1: {when_1}
        what_position_1: {what_position_1}
        who_2: {who_2}
        when_2: {when_2}
        what_position_2: {what_position_2}
        who_3: {who_3}
        when_3: {when_3}
        \n------------------------------------------>''')
    time = str(date.today())
    new_sheet.update('U2', source_of_funding)
    new_sheet.update('V2', average_position)
    new_sheet.update('W2', operating_frequency)
    new_sheet.update('X2', beneficiaries)
    new_sheet.update('Y2', who_1)
    new_sheet.update('Z2', when_1)
    new_sheet.update('AA2', what_position_1)
    new_sheet.update('AB2', who_2)
    new_sheet.update('AC2', when_2)
    new_sheet.update('AD2', what_position_2)
    new_sheet.update('AE2', who_3)
    new_sheet.update('AF2', when_3)
    new_sheet.update('AG2', time)
