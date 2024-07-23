from fastapi import FastAPI, HTTPException
from schemas import Patient

import json

app = FastAPI()

with open('patients.json', 'r') as f:
    patient_data = json.load(f)
    

patient_list = []
for patient in patient_data:
    patient_list.append(patient)


@app.get('/patients')
async def get_patients() -> list[Patient]:
    
    return patient_list

@app.post('/patients')
async def create_patient(patient: Patient) -> Patient:
    
    patient_list.append(patient)
    return patient
    
@app.put('/patients')
async def update_patient(first_name: str, last_name: str, updated_patient: Patient):
    
    for patient in patient_list:
        if patient['first_name'] == first_name and patient['last_name'] == last_name:
            patient.update(updated_patient)
            return updated_patient
        
    new_patient = Patient(first_name=updated_patient.first_name, last_name=updated_patient.last_name, address=updated_patient.address, age=updated_patient.age)
    
    patient_list.append(new_patient)
    return new_patient
        
    
@app.delete('/patients/{first_name}/{last_name}')
async def delete_patient(first_name: str, last_name: str):
    
    global patient_list
    
    patient_in_list = any(patient["first_name"] == first_name and patient["last_name"] == last_name for patient in patient_list)
    if not patient_in_list:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_list = [patient for patient in patient_list if patient['first_name'] != first_name or patient['last_name'] != last_name]
    
    return patient_list
    