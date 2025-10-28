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

## Running the model

You can start the model by doing

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