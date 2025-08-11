import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [team1, setTeam1] = useState('');
  const [team2, setTeam2] = useState('');
  const [advice, setAdvice] = useState('');
  const [error, setError] = useState('');
  const nbaTeams = [
    "Warriors", "Nuggets", "Lakers", "Celtics", "Bucks", "Suns",
    "Heat", "Clippers", "76ers", "Mavericks", "Grizzlies", "Kings",
    "Knicks", "Raptors", "Pelicans", "Timberwolves", "Hawks", "Bulls",
    "Pacers", "Nets", "Magic", "Thunder", "Jazz", "Hornets", "Spurs",
    "Wizards", "Trail Blazers", "Cavaliers", "Pistons", "Rockets"
  ];

  const getAdvice = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/advise?team1=${team1}&team2=${team2}`);
      const data = await response.json();

      if (response.ok) {
        setAdvice(data.gpt_explanation);
        setError('');
      } else {
        setAdvice('');
        setError('Error: ' + (data.detail || 'Failed to fetch advice'));
      }
    } catch (err) {
      setAdvice('');
      setError('Server not responding');
    }
  };

const [userId, setUserId] = useState('');
const [favoriteTeams, setFavoriteTeams] = useState([]);
const [favoriteAdvice, setFavoriteAdvice] = useState('');

const handleTeamInput = (index, value) => {
  const newTeams = [...favoriteTeams];
  newTeams[index] = value;
  setFavoriteTeams(newTeams);
};

const saveFavorites = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/set_teams', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, teams: favoriteTeams }),
    });

    const data = await response.json();
    if (response.ok) {
      alert('Favorites saved successfully!');
    } else {
      alert('Failed to save favorites: ' + data.detail);
    }
  } catch (err) {
    alert('Server error while saving favorites');
  }
};

const getFavoriteAdvice = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/get_advice?user_id=${userId}`);
    const data = await response.json();

    if (response.ok) {
      setFavoriteAdvice(data.gpt_betting_tip);
    } else {
      setFavoriteAdvice('');
      alert('Error: ' + (data.error || 'Unable to get advice'));
    }
  } catch (err) {
    alert('Server not responding for favorite advice');
  }
};


return (
  <div className="app-wrapper text-white">
    <div className="container mt-5 p-4 rounded" style={{ backgroundColor: "rgba(255, 255, 255, 0.9)" }}>
      <h1 className="text-center mb-5 display-4 fw-bold text-shadow">🏀 NBA Betting Advisor</h1>

      {/* Team Selection */}
      <div className="row mb-4">
        <div className="col-md-5 mb-3">
          <select
            className="form-select bg-dark text-white border-info"
            value={team1}
            onChange={(e) => setTeam1(e.target.value)}
          >
            <option value="">Select Team 1</option>
            {nbaTeams.map((team) => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>
        <div className="col-md-5 mb-3">
          <select
            className="form-select bg-dark text-white border-info"
            value={team2}
            onChange={(e) => setTeam2(e.target.value)}
          >
            <option value="">Select Team 2</option>
            {nbaTeams.map((team) => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>
        <div className="col-md-2 mb-3">
          <button className="btn btn-info w-100 fw-bold shadow" onClick={getAdvice}>
            🔮 Get Advice
          </button>
        </div>
      </div>

      {/* GPT Advice */}
      {advice && (
        <div className="card bg-success bg-gradient text-white shadow-sm mb-4">
          <div className="card-body">
            <h5 className="card-title">📊 GPT Betting Advice:</h5>
            <p className="card-text">{advice}</p>
          </div>
        </div>
      )}

      {error && (
        <div className="alert alert-danger shadow-sm">
          <h5>❌ Error:</h5>
          <p>{error}</p>
        </div>
      )}

      <hr className="my-5 border-light" />

      <h2 className="mb-4">⭐ Your Favorite Teams</h2>

      <div className="mb-3">
        <input
          type="text"
          className="form-control bg-dark text-white border-warning"
          placeholder="Enter your user ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
      </div>

      <div className="row mb-4">
        {[0, 1].map((index) => (
          <div className="col-md-6 mb-3" key={index}>
            <select
              className="form-select bg-dark text-white border-warning"
              value={favoriteTeams[index] || ''}
              onChange={(e) => handleTeamInput(index, e.target.value)}
            >
              <option value="">Favorite Team {index + 1}</option>
              {nbaTeams.map((team) => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>
        ))}
      </div>

      <div className="d-flex gap-3 mb-4">
        <button className="btn btn-success fw-bold shadow" onClick={saveFavorites}>💾 Save Favorites</button>
        <button className="btn btn-secondary fw-bold shadow" onClick={getFavoriteAdvice}>💡 Get Advice</button>
      </div>

      {favoriteAdvice && (
        <div className="card bg-primary text-white shadow-sm">
          <div className="card-body">
            <h5 className="card-title">🏆 GPT Advice for Your Teams:</h5>
            <p className="card-text">{favoriteAdvice}</p>
          </div>
        </div>
      )}
    </div>
  </div>
);
}

export default App;
