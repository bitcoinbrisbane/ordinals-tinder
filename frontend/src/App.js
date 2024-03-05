import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import WelcomeScreen from "./screens/welcome.js";
import SwipeScreen from "./screens/swipe.js";
import LeaderBoard from "./screens/leaderboard.js";
import AccountPage from "./screens/account.js";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<WelcomeScreen />} />
        <Route path="/swipe" element={<SwipeScreen />} />
        <Route path="/leaderboard" element={<LeaderBoard />} />
        <Route path="/account" element={<AccountPage />} />
      </Routes>
    </Router>
  );
}

export default App;
