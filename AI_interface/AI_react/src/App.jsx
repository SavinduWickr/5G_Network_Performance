import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import BouncyButtons from './components/Team';
import Roadmap from './components/Roadmap';
import Data from './components/Data';

const App = () => {
  return (
    <div className="min-h-screen">
      <Header />
      <Hero />
      <div className="bg-pink-200">
        <BouncyButtons />
      </div>
      <Data />
      <Roadmap />
    </div>
  );
}

export default App;