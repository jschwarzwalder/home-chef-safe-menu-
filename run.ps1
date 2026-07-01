# If Powershell complains about running scripts, run this command in Powershell to allow scripts to run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Run the program
python main.py