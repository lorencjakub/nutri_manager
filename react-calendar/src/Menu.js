import React from 'react';


export default function MenuList({ menuVisibility }) {

    return (
        <div className="menu-list" style={ {display: menuVisibility ? 'block' : 'none'} }>
            <h1>THIS IS A MENU LIST</h1>
        </div>
    );
}