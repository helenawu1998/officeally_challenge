# officeally_challenge (Office Ally's Challenge #1 at LA Hacks)
Python application built to address the patient matching problem. 


# Team Name: Patiently. Challenge: Patient Matching
Members:
- Helena Wu
- Victor Chen
- Ziyan Mo

# Set up instructions
- Clone this repository. 
- Create a python virtualenv
```
python3 -m venv <your env name>
source <your env name>/bin/activate
```
- Install requirements.txt
```
pip install -r requirements.txt
```
- Set up database
```
python3 set_up.py
```
This should create a local file called patient_matching.db that will serve as your SQLite (development) database. Do not add this file to the repository.


# Testing
We worked on two distinct approaches: one to replicate the Office Ally POC, and our novel approach.

## Replicated Office Ally POC
- Run patient matching algorithm:
```
python3 run.py
```

## Novel approach
- Run patient matching algorithm:
```
python evaluate.py --input <your input file here> --output <your output file here>
```

## Contact info
TODO
