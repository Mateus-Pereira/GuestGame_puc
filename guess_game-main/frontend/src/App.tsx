import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Maker from './components/Maker';
import Breaker from './components/Breaker';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import GamesList from './components/GamesList';
import ProtectedRoute from './components/ProtectedRoute';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route 
                path="/login" 
                element={
                  <ProtectedRoute requireAuth={false}>
                    <Login />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/register" 
                element={
                  <ProtectedRoute requireAuth={false}>
                    <Register />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/maker" 
                element={
                  <ProtectedRoute>
                    <Maker />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/breaker" 
                element={
                  <ProtectedRoute>
                    <Breaker />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/games" 
                element={
                  <ProtectedRoute>
                    <GamesList />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
