import React, { useState, useEffect } from 'react';
import $ from 'jquery';


export default function Calendar({ calendarVisibility }) {
    const [monthNames] = useState(['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
                                    'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 
                                    'Listopad', 'Prosinec']);

    const [dayNames] = useState(['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']);
    
    const [month, setMonth] = useState(monthNames[new Date().getMonth()]);
    const [year, setYear] = useState(new Date().getFullYear());
    const [dayCounts, setDayCounts] = useState([31, (year % 4 === 0) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
    const [days, setDays] = useState([]);

    const nextMonthName = () => {
        var newMonth = (month !== 'Prosinec') ? monthNames[monthNames.indexOf(month) + 1] : 'Leden';
        
        if (month === 'Prosinec') {
            var febDays = ((year + 1) % 4 === 0) ? 29 : 28;
            setDayCounts([31, febDays, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
            setYear(year + 1);
        }

        setMonth(newMonth);
    };

    const prevMonthName = () => {
        var newMonth = (month !== 'Leden') ? monthNames[monthNames.indexOf(month) - 1] : 'Prosinec';

        if (month === 'Leden') {
            var febDays = ((year - 1) % 4 === 0) ? 29 : 28;
            setDayCounts([31, febDays, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
            setYear(year - 1);
        }

        setMonth(newMonth);
    };

    const createDays = (daysCount, first_day_index) => {
        var days = [];

        for (var i = 0; i < daysCount + first_day_index - 1; i++) {
            var value = "";
            var currDate = false;

            if (i >= first_day_index - 1) {
                value = i - first_day_index + 2;
            }

            var today = new Date();

            if ((year === today.getFullYear()) && (monthNames.indexOf(month) + 1 === today.getMonth() + 1) && (value === today.getDate())) {
                currDate = true;
            }

            days.push(<Day value={value} currDate={currDate}/>);
        }

        return days;
    };


    // generate calendar days
    useEffect(() => {
        var first_day_date = new Date(`${year}-${monthNames.indexOf(month) + 1}-1`);
        var first_day_index = first_day_date.getDay();
        setDays(createDays(dayCounts[monthNames.indexOf(month)], first_day_index));

    }, [year, month, dayCounts, dayNames, monthNames]);
    return (
        <div className="calendar" style={ {display: calendarVisibility ? 'block' : 'none'} }>
            <CalendarHeader />
            <CalendarBody days={days}/>
            <CalendarFooter />
        </div>
    );


    function CalendarHeader() {

        return (
            <div className="calendar-header">
                <span className="month-change" id="prev-month" onClick={prevMonthName}>
                    <pre>&#60;</pre>
                </span>
                <span className="mont-picker" id="month-picker">
                    {month}
                </span>
                <span className="month-change" id="next-month" onClick={nextMonthName}>
                    <pre>&#62;</pre>
                </span>
                <div className="year-picker">
                    <span id="year">
                        {year}
                    </span>
                </div>
            </div>
        );
    }


    function CalendarBody({ days }) {
        return (
            <div className="calendar-body">
                <div className="calendar-week-day">
                    <div>Po</div>
                    <div>Út</div>
                    <div>St</div>
                    <div>Čt</div>
                    <div>Pá</div>
                    <div>So</div>
                    <div>Ne</div>
                </div>
                <div className="calendar-days">
                    {days}
                </div>
            </div>
        );
    }


    function CalendarFooter() {
        return (
            <div className="calendar-footer">
                <div className="toggle">
                    <span>Dark Mode</span>
                    <ModeSwitcher />
                </div>
            </div>
        );
    }


    function ModeSwitcher() {
        const switchMode = () => {
            $('body').toggleClass('dark light');
        }

        return (
            <div onClick={switchMode} className="dark-mode-switch">
                <div className="dark-mode-switch-ident" />
            </div>
        );
    }

    function Day({ value, currDate }) {
        const dayClass = (currDate) ? "calendar-day-hover curr-date" : "calendar-day-hover";

        return (
            <div className={dayClass}>
                {value}
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        );
    }
}