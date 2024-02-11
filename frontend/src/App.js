import logo from './logo.svg';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';

import WelcomeScreen from './screens/welcome.js';
import SwipeScreen from './screens/swipe.js';

function App() {
  return (
    
    <Router>
      <Routes>

        <Route path="/" element={<WelcomeScreen />} />
        <Route path="/swipe" element={<SwipeScreen />} />
        
      </Routes>
  </Router>

  );
}

export default App;
