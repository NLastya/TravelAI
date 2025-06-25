const getDateText = (date) => {
    const day = date.split(':')[0]
    const len = day.length()

    if( day[len-1] === '1')
        return date + 'день'
    else if ([2, 3, 4].include(day[len-1]))
        return date + 'день'
    else if ([5, 6, 7, 8, 9, 0].include(day[len-1]))
        return date + 'дней'
    else
        return date + 'erro'
}

export default getDateText;