import React, { useEffect } from 'react'
import Card from './card.jsx'
import useRightClickMenu from "../../hooks/useRightClickMenu.jsx";
import '../../App.css'
import './card.css'

function App() {
   
    const { x, y, showMenu, cardRef, menuRef, handleContextMenu } = useRightClickMenu();
    
    useEffect(() => {
        if (cardRef.current) {
            console.log("cardRef is attached:", cardRef.current);
        }
        }, [cardRef]); 

    return (
        <div ref={cardRef} onContextMenu={handleContextMenu}>
            {showMenu && (
                <div ref={menuRef} 
                    className='contextMenu'
                    style={{
                        position: 'absolute',
                        top: `${y}px`,
                        left: `${x}px`,
                    }}
                >
                    <ul>
                        <li>Добавить в избранное</li>
                        <li>Заменить</li>
                        <li>Удалить</li>
                    </ul>
                </div>
            )}



            <div className="str">
                <Card />
                <Card/>
                <Card />
            </div>

            <div className="str">
                <Card />
                <Card />
                <Card />
            </div>
       
        </div>  
    )
}

export default App


