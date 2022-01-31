import React, { useState, useEffect } from 'react';


export default function MenuList(props) {
    const [menuForThisDay, setMenuForThisDay] = useState({"breakfast": "", "lunch": "", "snack": "", "dinner": ""});

    useEffect(() => {
        if (!props.menuVisibility) {
            generateMenu(false);
        }
    }, [props.menuVisibility]);

    const generateMenu = (generator) => {
        var breakfast = generator ? "Test Breakfast" : "";
        var lunch = generator ? "Test Lunch" : "";
        var snack = generator ? "Test Snack" : "";
        var dinner = generator ? "Test Dinner" : "";

        var meals = {
            "breakfast": breakfast,
            "lunch": lunch,
            "snack": snack,
            "dinner": dinner
        };
        setMenuForThisDay(meals);
    }

    return (
        <div className="menu-list" style={ {display: props.menuVisibility ? 'block' : 'none'} }>
            <div className="row text-center">
                <h1>{props.clickedDate ? `${props.clickedDate.getDate()}. 
                ${props.clickedDate.getMonth() + 1}. ${props.clickedDate.getFullYear()}` : ""}</h1>
            </div>

            <div className="row m-3">
                <div className="col-6">
                    <p>{"Snídaně:"}</p>
                </div>
                <div className="col-6">
                    <p>{menuForThisDay["breakfast"]}</p>
                </div>
            </div>
            <div className="row m-3">
                <div className="col-6">
                    <p>{"Oběd:"}</p>
                </div>
                <div className="col-6">
                    <p>{menuForThisDay["lunch"]}</p>
                </div>
            </div>
            <div className="row m-3">
                <div className="col-6">
                    <p>{"Svačina:"}</p>
                </div>
                <div className="col-6">
                    <p>{menuForThisDay["snack"]}</p>
                </div>
            </div>
            <div className="row m-3">
                <div className="col-6">
                    <p>{"Večeře:"}</p>
                </div>
                <div className="col-6">
                    <p>{menuForThisDay["dinner"]}</p>
                </div>
            </div>

            <div className="row m-3">
                <button className="btn btn-primary my-3" onClick={() => generateMenu(true)}>Chci menu!</button>
                <button className="btn btn-primary my-3" onClick={() => props.handleClick(false, null)}>Zavřít</button>
            </div>
        </div>
    );
}