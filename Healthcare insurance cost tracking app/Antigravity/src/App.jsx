import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import InsuranceProfile from './pages/InsuranceProfile';
import SymptomChecker from './pages/SymptomChecker';

import InsuranceUpload from './pages/InsuranceUpload';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<InsuranceUpload />} />
          <Route path="/profile-setup" element={<InsuranceProfile />} />
          <Route path="/symptom-checker" element={<SymptomChecker />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
