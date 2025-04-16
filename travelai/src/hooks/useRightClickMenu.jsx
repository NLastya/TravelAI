import { useState, useEffect, useRef } from "react";

export default function useRightClickMenu() {
    const [x, setX] = useState(0)
    const [y, setY] = useState(0)
    const [showMenu, setShowMenu] = useState(false)
    const cardRef = useRef(null); 
    const menuRef = useRef(null);
    
    const handleContextMenu = (e) => {
        if (!cardRef.current?.contains(e.target)) {
           return; 
        }
         e.preventDefault()
        setX(e.pageX + 175 > window.innerWidth ? window.innerWidth - 175 : e.pageX);
        setY(e.pageY + 94 > window.innerHeight ? window.innerHeight - 94 : e.pageY);
        setShowMenu(true)
    }
       
    const handleClick = (e) => {
        if (menuRef.current && !menuRef.current.contains(e.target) && showMenu) {
            setShowMenu(false);
        }
    }


    useEffect(() => {
        document.addEventListener('click', handleClick);
        document.addEventListener('contextmenu', handleContextMenu);
        return () => {
            document.removeEventListener('click', handleClick);
            document.removeEventListener('contextmenu', handleContextMenu);
        };
    }, [showMenu]);

    return {x, y, showMenu, cardRef, menuRef, handleContextMenu};
}