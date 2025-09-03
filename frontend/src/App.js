import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import SystemsList from './pages/SystemsList';
import SystemDetail from './pages/SystemDetail';
import SystemForm from './pages/SystemForm';
import DataflowDiagram from './components/DataflowDiagram';
import SearchResults from './pages/SearchResults';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Container fluid className="mt-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/systems" element={<SystemsList />} />
            <Route path="/systems/:id" element={<SystemDetail />} />
            <Route path="/systems/new" element={<SystemForm />} />
            <Route path="/systems/edit/:id" element={<SystemForm />} />
            <Route path="/diagram" element={<DataflowDiagram />} />
            <Route path="/search" element={<SearchResults />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
}

export default App;
