import React from 'react';

import MyRouter from './router/index';
import Navbar from './components/Navbar';

const App = () => {
  return (
    <div>
      <Navbar />
      <MyRouter />
    </div>
  );
};

export default App;
