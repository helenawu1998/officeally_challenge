# officeally_challenge (Office Ally's Patient Matching Challenge)
Python solutions to the patient matching problem presented by Office Ally at LA Hacks 2020. Patient matching is an important unsolved problem, and accurate matching of patient records can save lives. Patiently presents an accurate and novel solution with a clean interface.


# Team Name: Patiently
Challenge: Patient Matching
Team Members:
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

# Proof of Concept Steps
We worked on two distinct approaches: one similar to the Office Ally POC algorithm, and our novel approach.

## Office Ally POC algorithm (Challenge 1 - Algorithm 1 code)
- Run program with "Patient_Matching_Data.csv" or similarly formatted data file.
- This approach will:
1) Create a file called patient_matching.db, a local SQLite database
2) Load the input data into the "patients" table
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
Ziyan: moziyan@yahoo.com
Victor: vlchen888@gmail.com

## Devpost link
https://devpost.com/software/pa-iently
