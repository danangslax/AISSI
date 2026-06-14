export function calculatePnL(
  averagePrice: number,
  currentPrice: number,
  quantity: number
) {

  const pnl =
    (currentPrice - averagePrice)
    * quantity;

  const pnlPct =
    (
      (currentPrice - averagePrice)
      / averagePrice
    ) * 100;

  return {
    pnl,
    pnlPct,
  };
}

export function calculateAllocation(
  positionValue: number,
  totalPortfolio: number
) {

  if (totalPortfolio <= 0)
    return 0;

  return (
    (positionValue / totalPortfolio)
    * 100
  );
}

export function portfolioHealthScore(
  concentrationPct: number
) {

  if (concentrationPct > 50)
    return 40;

  if (concentrationPct > 35)
    return 60;

  if (concentrationPct > 25)
    return 75;

  return 90;
}