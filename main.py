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
async def update_patient(first_name: None | str = None, last_name: None | str = None, updated_patient: Patient = None):
    
    for patient in patient_list:
        if patient['first_name'] == first_name and patient['last_name'] == last_name:
            patient.update(updated_patient)
            return 'Updated successfully'
        
        else:
            patient_list.append(updated_patient)
            return updated_patient
        
    
@app.delete('/patients/{first_name}/{last_name}')
async def delete_patient(first_name: str, last_name: str):
    
    for patient in patient_list:
        if patient['first_name'] == first_name and patient['last_name'] == last_name:
            patient_list.remove(patient)
            return f'{first_name} {last_name} deleted successfully'
        
    raise HTTPException(status_code=404, detail='Patient not found')
            
    
    