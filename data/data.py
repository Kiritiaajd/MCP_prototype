import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Number of rows
n = 1000

def random_date(start, end):
    """Generate random date between start and end."""
    return start + timedelta(days=random.randint(0, (end - start).days))

# Columns and containers
data = {
    "Sr_No": list(range(1, n + 1)),
    "Cust_ID": [],
    "FCC_FCR_ID": [],
    "Application_No": [],
    "Cust_Name": [],
    "Segment": [],
    "Application_Status": [],
    "Type_of_Workflow": [],
    "Type_of_case": [],
    "Proj_Finance (Y/N)": [],
    "Zone": [],
    "RM_Name": [],
    "RM_ID": [],
    "Analyst_Name": [],
    "RBH_Name": [],
    "RCH_Name": [],
    "JD/Committee": [],
    "Final_Approval_Month": [],
    "#_Iterations": [],
    "Business_Supervisory_Review_(Y/N)": [],
    "Credit_Supervisory_Review_(Y/N)": [],
    "Date_of_Input": [],
    "Date_of_Login": [],
    "Date_of_Circulation": [],
    "Date_of_BH_Approval": [],
    "Date_of_CH_Approval": [],
    "Date_of_Final_Approval": [],
    "CAM_Creation_TAT": [],
    "Credit_Review_TAT": [],
    "Business_Review_TAT": [],
    "Total_Review_TAT": [],
    "Committee_TAT": [],
    "RM_TAT": [],
    "Final_TAT": [],
    "Overall_TAT": [],
    "Current_Exposure": [],
    "Proposed_Exposure": [],
    "CAM_Finalization_InDate": [],
    "CAM_Finalization_TAT": [],
}

segments = ['Manufacturing', 'Textiles', 'IT Services', 'Retail', 'Pharmaceuticals', 'Automobile', 'Construction', 'Education']
application_statuses = ['APPROVE', 'REJECT', 'PENDING']
workflow_types = ['APPWF_BGNBB', 'APPWF_RNWBB', 'APPWF_RSTBB']
case_types = ['Fresh', 'Renewal', 'Restructuring']
zones = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTRAL']
proj_finance_choices = ['Y', 'N']
yes_no = ['Y', 'N']
committees = ['ZCC', 'JDC', 'FRC', 'BOD']

# Generate RM, RBH, RCH, Analyst names pool
rm_names = [fake.name() for _ in range(20)]
analyst_names = [fake.name() for _ in range(20)]
rbh_names = [fake.name() for _ in range(5)]
rch_names = [fake.name() for _ in range(5)]
jd_committees = committees

start_date = datetime.strptime("2018-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-05-20", "%Y-%m-%d")

for i in range(n):
    cust_id = f"CTPT-{random.randint(1000,9999)}"
    data["Cust_ID"].append(cust_id)
    data["FCC_FCR_ID"].append("NA" if random.random() < 0.8 else f"FCR-{random.randint(100,999)}")
    data["Application_No"].append(f"APP-{1000+i}")
    data["Cust_Name"].append(fake.company())
    data["Segment"].append(random.choice(segments))
    data["Application_Status"].append(random.choices(application_statuses, weights=[0.5, 0.2, 0.3])[0])
    data["Type_of_Workflow"].append(random.choice(workflow_types))
    data["Type_of_case"].append(random.choice(case_types))
    data["Proj_Finance (Y/N)"].append(random.choice(proj_finance_choices))
    data["Zone"].append(random.choice(zones))
    rm = random.choice(rm_names)
    data["RM_Name"].append(rm)
    data["RM_ID"].append(f"RM{random.randint(1000,9999)}")
    data["Analyst_Name"].append(random.choice(analyst_names))
    data["RBH_Name"].append(random.choice(rbh_names))
    data["RCH_Name"].append(random.choice(rch_names))
    data["JD/Committee"].append(random.choice(jd_committees))
    final_approval_month = random.choice(['January', 'February', 'March', 'April', 'May', 'June',
                                         'July', 'August', 'September', 'October', 'November', 'December'])
    data["Final_Approval_Month"].append(final_approval_month)
    data["#_Iterations"].append(random.randint(1, 10))
    data["Business_Supervisory_Review_(Y/N)"].append(random.choice(yes_no))
    data["Credit_Supervisory_Review_(Y/N)"].append(random.choice(yes_no))

    date_input = random_date(start_date, end_date)
    data["Date_of_Input"].append(date_input.strftime("%d-%m-%Y"))

    date_login = date_input + timedelta(days=random.randint(0,2))
    data["Date_of_Login"].append(date_login.strftime("%d-%m-%Y"))

    date_circulation = date_login + timedelta(days=random.randint(0,3))
    data["Date_of_Circulation"].append(date_circulation.strftime("%d-%m-%Y"))

    date_bh_approval = date_circulation + timedelta(days=random.randint(0,5))
    data["Date_of_BH_Approval"].append(date_bh_approval.strftime("%d-%m-%Y"))

    # Sometimes CH approval missing for rejected or pending apps
    if data["Application_Status"][-1] == 'APPROVE':
        date_ch_approval = date_bh_approval + timedelta(days=random.randint(0,3))
        data["Date_of_CH_Approval"].append(date_ch_approval.strftime("%d-%m-%Y"))

        date_final_approval = date_ch_approval + timedelta(days=random.randint(0,5))
        data["Date_of_Final_Approval"].append(date_final_approval.strftime("%d-%m-%Y"))
    else:
        data["Date_of_CH_Approval"].append("NA")
        data["Date_of_Final_Approval"].append("NA")

    # Generate TATs (Turnaround times in days)
    cam_creation_tat = random.randint(1,10)
    credit_review_tat = random.randint(1,10)
    business_review_tat = random.randint(1,10)
    total_review_tat = cam_creation_tat + credit_review_tat + business_review_tat
    committee_tat = random.randint(1,5)
    rm_tat = random.randint(1,5)
    final_tat = total_review_tat + committee_tat + rm_tat
    overall_tat = final_tat + random.randint(0,3)

    data["CAM_Creation_TAT"].append(cam_creation_tat)
    data["Credit_Review_TAT"].append(credit_review_tat)
    data["Business_Review_TAT"].append(business_review_tat)
    data["Total_Review_TAT"].append(total_review_tat)
    data["Committee_TAT"].append(committee_tat)
    data["RM_TAT"].append(rm_tat)
    data["Final_TAT"].append(final_tat)
    data["Overall_TAT"].append(overall_tat)

    # Exposure values (in lakhs or crores)
    current_exposure = random.randint(1_000_000, 100_000_000)
    proposed_exposure = current_exposure + random.randint(-500_000, 5_000_000)
    data["Current_Exposure"].append(current_exposure)
    data["Proposed_Exposure"].append(proposed_exposure if proposed_exposure > 0 else current_exposure)

    if data["Application_Status"][-1] == 'APPROVE':
        cam_finalization_indate = date_final_approval + timedelta(days=random.randint(0, 3))
        cam_finalization_tat = (cam_finalization_indate - date_final_approval).days
        data["CAM_Finalization_InDate"].append(cam_finalization_indate.strftime("%d-%m-%Y"))
        data["CAM_Finalization_TAT"].append(cam_finalization_tat)
    else:
        data["CAM_Finalization_InDate"].append("NA")
        data["CAM_Finalization_TAT"].append("NA")

# Create DataFrame
df = pd.DataFrame(data)

# Fix columns to match exact names requested
df.rename(columns={
    "CAM_Creation_TAT": "CAM_Creation_TAT",
    "Credit_Review_TAT": "Credit_Review_TAT",
    "Business_Review_TAT": "Business_Review_TAT",
    "Total_Review_TAT": "Total_Review_TAT",
    "Committee_TAT": "Committee_TAT",
    "RM_TAT": "RM_TAT",
    "Final_TAT": "Final_TAT",
    "Overall_TAT": "Overall_TAT",
}, inplace=True)

# Save CSV
df.to_csv("loan_application_demo_dataset.csv", index=False)

print("Dataset created with 1000 rows and saved as loan_application_demo_dataset.csv")
