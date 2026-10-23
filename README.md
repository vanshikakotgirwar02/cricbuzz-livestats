
# Cricbuzz LiveStats 🏏

Cricbuzz LiveStats is a cricket analytics dashboard built using Python, Streamlit, SQLite, Pandas, and the Cricbuzz API through RapidAPI.

The application provides cricket match information, player statistics, SQL analytics, and database management features through an interactive web interface.

## Features

- **Live Matches:** Fetch match details, team names, match formats, statuses, and innings scores using the Cricbuzz API.
- **Top Players:** Explore player statistics stored in the SQLite database.
- **SQL Analytics:** Analyze cricket data using SQL queries.
- **CRUD Operations:** Create, read, update, and delete supported database records.
- **SQLite Database:** Store teams, players, venues, matches, and player match statistics.
- **Interactive Dashboard:** User-friendly interface built with Streamlit.

**Note:** The Live Matches page fetches data from the Cricbuzz API. Other pages may use locally stored records or sample data. Sample database statistics are not verified live scores.

## Technologies Used

- Python
- Streamlit
- Pandas
- SQLite
- Requests
- python-dotenv
- Plotly
- Cricbuzz API via RapidAPI

## Project Structure

```text
cricbuzz_livestats/
├── app.py
├── config.py
├── api/
│   └── cricbuzz_client.py
├── pages/
│   ├── 1_Live_Matches.py
│   ├── 2_Top_Players.py
│   ├── 3_SQL_Analytics.py
│   └── 4_CRUD.py
├── services/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── utils/
├── data/
│   └── cricbuzz.db
├── requirements.txt
└── README.md
```

The exact structure may vary slightly depending on the files included in your project.

## Installation and Setup

### Prerequisites

- Python 3.11 recommended
- Internet connection
- RapidAPI account with access to the Cricbuzz API

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd cricbuzz_livestats
```

Alternatively, download and extract the project ZIP, then open the extracted folder in VS Code.

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
py -3.11 -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure the API

Create a `.env` file in the project root and add your own RapidAPI credentials:

```env
CRICBUZZ_API_KEY=your_rapidapi_key_here
CRICBUZZ_API_HOST=your_cricbuzz_api_host_here
```

Use the exact variable names expected by `config.py` and the API host shown in your RapidAPI dashboard.

**Security:** Never commit your real API key or `.env` file to a public GitHub repository.

### Step 5: Initialize the Database

If your project contains `database/init_db.py`, run:

```powershell
python database/init_db.py
```

If the database is already initialized, this step may not be necessary. Back up your database before making changes.

### Step 6: Run the Application

```powershell
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## API Connection Test

If `test_api.py` is included in the project, run:

```powershell
python test_api.py
```

A successful response confirms that the API request returned data at the time of testing. API availability depends on your credentials, subscription limits, and provider response.

## Troubleshooting

- **API request fails:** Check the API key, host, endpoint, internet connection, and RapidAPI quota.
- **Module not found:** Activate the virtual environment and install `requirements.txt`.
- **Database not found:** Check that `data/cricbuzz.db` exists.
- **Scores unavailable:** The API may not return score details for every match.
- **Streamlit does not start:** Check the terminal for errors and confirm that dependencies are installed.

## Future Improvements

- Automatic score refresh
- Improved match filtering
- Player performance visualizations
- Additional SQL analytics
- Enhanced dashboard design

## Author

Developed as a cricket data analytics project using Python, Streamlit, SQLite, and the Cricbuzz API.
