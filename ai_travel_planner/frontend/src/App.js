import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import HomePage from './pages/Home';
import PlannerPage from './pages/Planner';
import ChatPage from './pages/Chat';

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/planner" element={<PlannerPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Box>
  );
}

export default App;
