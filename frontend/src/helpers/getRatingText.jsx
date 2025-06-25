const getTourText = (rating) => {
    const ratingInt = Number(rating)

    if ([1].include(ratingInt))
        return ratingInt + 'звезда'
    else if ([2, 3, 4].include(ratingInt))
        return ratingInt + 'звезды'
    else
        return ratingInt + 'звёзд'
}

export default getTourText;