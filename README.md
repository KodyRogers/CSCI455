# CSCI455

This is the repo for voting database application for CSCI-455.

## Steps to run
1. Extract the Files into a folder, will not run properly in a zip folder.
2. This program was made on python 3.12.7 
3. Install required libraries from requirements.txt, `py -m pip install -r requirements.txt`
4. Create ssh.txt in the root directory, on the first line write your username, on the second line write your password. Make sure to never commit this file to github.
5. To run the program run `py src/main.py` from the `CSCI455` directory

## Commands - format | usage
admin_login.py - username password | Logs in as admin
voter_login.py - first_name, last_name, last four ssn digits | Logs in as a voter
voter_info.py - None | Gets the currently logged in voters information
logout.py - None | Logout any user
view_election.py - None | Views all ongoing elections
view_candidates.py - Election_name | Gets all candidates for an Election
run_in_election.py - Election_name | Requires user to be logged in as a voter and enroles them as a Candidate
vote.py - Election_Name, Candidate_ID | Votes for the candidate find the CandidateID in view_candidate.py
register_voter.py - first_name, middle_name, last_name, ssn (format XXX-XX-0000 [0 can be any number]), party
                    | Register_Voter is an Admin only command
end_election.py - Election_name | ends the election, this is an Admin only command