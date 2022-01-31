import './App.css';
import Calendar from './Calendar';
import MenuList from './Menu';
import 'bootstrap/dist/css/bootstrap.min.css';
import './calendar.css';
import { useState } from 'react';

function App() {
  const [menuVisibility, setMenuVisibility] = useState(false);
  console.log(menuVisibility);
  return ([
    <Calendar calendarVisibility={ menuVisibility ? false : true }/>,
    <MenuList menuVisibility={ menuVisibility }/>
  ]);
}

export default App;
