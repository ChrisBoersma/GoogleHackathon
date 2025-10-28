# Healthcare Simulation Project

This project simulates a healthcare environment with different AI agents (Doctor, Nurse, Data Scientist) interacting to manage patient care and data.

## Project Setup

To get this project up and running, follow these steps:

### 1. Clone the Repository

```bash
git clone <repository_url>
cd GoogleHackathon
```

### 2. Python Environment

It is recommended to use a virtual environment for this project.

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Create `temp_pickle_data` Folder

This project requires a `temp_pickle_data` folder at the root level to store temporary data.

```bash
mkdir temp_pickle_data
```

### 5. Environment Variables

Create a `.env` file in the root directory of the project based on the provided `.env.example` file. This file will contain necessary API keys and configurations.

```bash
cp .env.example .env
```

Open the newly created `.env` file and fill in the required values (e.g., Google API Key).

## Agent flow
The agent, a doctor, will get the name of a patient from the user.
It will ask the Nurse to do a random measurement.
Then it will ask the data scientist to make a prediction.
The datascientist will make a prediction based on the measurements.
If the certainty is higher than 75% the doctor will say if the patient can be discharged, has to be kept, or has to go to the ICU.
If the certainty is too low, the doctor will ask for another random measurement from the Nurse.
After 5 measurements, if the certainty is still too low, the doctor will take the last prediction of the datascientist.
## Running the agent

You can start the agent by doing

```bash
adk run Doctor
```
Then type the name of a patient to evaluate.
For example "Christina Matinez"

## Project Structure

- `Doctor/`: Contains the Doctor agent and its sub-agents for patient communication and intake.
- `Nurse_agent/`: Contains the Nurse agent.
- `datascientist_agent/`: Contains the Data Scientist agent.
- `Data/`: Stores healthcare-related datasets.
- `temp_pickle_data/`: Temporary storage for pickled data (user-created).
- `.env.example`: Example file for environment variables.
- `requirements.txt`: Lists project dependencies.