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

# Proof of Concept
We worked on two distinct approaches: one similar to the Office Ally POC algorithm, and our novel approach.

## Office Ally POC algorithm (Challenge 1 - Algorithm 1 code)
- This approach will:
1) Create a file called patient_matching.db, a local SQLite database
2) Load the original data into the "patients" table
3) Run POC-inspired patient matching algorithm
4) Generate output file "Post_Patient_Matching_Groups.csv" with the final matchings, and populate "matched_patients" table.
- Run patient matching algorithm from the Challenge 1 - Algorithm 1 folder. 
```
python3 run.py "Patient_Matching_Data.csv"
```

## Novel approach
- Run patient matching algorithm:
```
python evaluate.py --input <your input file here> --output <your output file here>
```

## Contact info
Helena: helenawu1998@gmail.com
