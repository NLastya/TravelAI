import {useEffect, useState} from 'react';
import { addFavorite, removeFavorite } from '../helpers/fetchRoute';

const ButtonLike = ({isLiked, user_id, tour_id}, ...props) => {
    // useEffect(() => {
    //     addFavorite(user_id, tour_id, setIsFavorite)
    // }, [user_id, tour_id])

    const [isFavorite, setIsFavorite] = useState(isLiked);

    return( <button className={"btn-like"}
     onClick={(e) => {
        isFavorite ? removeFavorite(user_id, tour_id,  setIsFavorite) : addFavorite(user_id, tour_id,  setIsFavorite)
        // if(!isError1 && !isError2)
        //       setIsFavorite(prev => !prev)
     }}
    >
        <img src={isFavorite ? "/icons/like.svg" : '/icons/like-outline.svg'} />
      </button>)
}

export default ButtonLike;
