const getYearMonth = date => date.year() * 12 + date.month();
// FIX: bag width previous 7 days are opened
export const disabled7DaysDate = (current, { from, type }) => {
  if (from) {
    const minDate = from.add(0, 'days');
    const maxDate = from.add(6, 'days');
    switch (type) {
      case 'year':
        return current.year() < minDate.year() || current.year() > maxDate.year();
      case 'month':
        return (
          getYearMonth(current) < getYearMonth(minDate) ||
          getYearMonth(current) > getYearMonth(maxDate)
        );
      default:
        return Math.abs(current.diff(from, 'days')) >= 5;
    }
  }
  return false;
};


