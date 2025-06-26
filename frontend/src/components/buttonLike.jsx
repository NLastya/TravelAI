import {useState} from 'react';

const ButtonLike = ({isLiked}, ...props) => {
    const [isFavorite, setIsFavorite] = useState(isLiked);

    return( <button className={"btn-like"}>
        <img src={isFavorite ? "/icons/like.svg" : '/icons/like-outline.svg'} />
      </button>)
}

export default ButtonLike;