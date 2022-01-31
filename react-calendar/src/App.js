import './App.css';
import Calendar from './Calendar';
import MenuList from './Menu';
import 'bootstrap/dist/css/bootstrap.min.css';
import './calendar.css';
import { useState } from 'react';

function App() {
  const [menuVisibility, setMenuVisibility] = useState(false);
  const [clickedDate, setClickedDate] = useState(null);

  const handleClick = (switchToMenuList, date) => {
    if (date) {
      setClickedDate(date);
      setMenuVisibility(switchToMenuList);
    } else {
      setMenuVisibility(switchToMenuList);
    }
  };

  return ([
    <Calendar calendarVisibility={ menuVisibility ? false : true } handleClick={handleClick}/>,
    <MenuList menuVisibility={ menuVisibility } handleClick={handleClick} clickedDate={clickedDate}/>
  ]);
}

export default App;
