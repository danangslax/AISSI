class PortfolioRiskEngine:

    def calculate_position_size(
        self,
        capital: float,
        risk_per_trade_pct: float,
        entry_price: float,
        stop_loss_price: float,
    ):

        risk_amount = (capital * risk_per_trade_pct) / 100

        risk_per_share = entry_price - stop_loss_price

        if risk_per_share <= 0:

            return {
                "shares": 0,
                "position_size": 0,
                "risk_amount": 0,
            }

        shares = risk_amount / risk_per_share

        position_size = shares * entry_price

        return {
            "shares": int(shares),
            "position_size": round(position_size, 2),
            "risk_amount": round(risk_amount, 2),
        }

    def calculate_risk_reward(
        self, entry_price: float, stop_loss_price: float, take_profit_price: float
    ):

        risk = entry_price - stop_loss_price

        reward = take_profit_price - entry_price

        if risk <= 0:
            return 0

        rr = reward / risk

        return round(rr, 2)

    def portfolio_exposure(self, open_positions: list[dict]):

        total_exposure = sum(pos["position_size"] for pos in open_positions)

        return round(total_exposure, 2)
