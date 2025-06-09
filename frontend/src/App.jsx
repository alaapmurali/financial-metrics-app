import React from 'react';
import TickerForm from './components/AddNewTicker';
import DumpData from './components/DumpData';
// import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Great Companies at Bargain Prices</h1>
      </header>
      <main>
        <DumpData />
      </main>
    </div>
  );
};

export default App;