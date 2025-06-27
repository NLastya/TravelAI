import style from './ratingcard.module.css';


// eslint-disable-next-line react/prop-types
const RatingCard = ({ rating, ...props }) => {
  const color = rating >= 4.0 
                ? '#8DD3BB' 
                : (rating >= 2.7 ? 'yellow' : 'red');
  return (
    <div
      className={style.card}
      style={{ border: `2px solid ${color}` }}
      {...props}>
      <span> {rating}</span>
    </div>
  );
};

export default RatingCard;

