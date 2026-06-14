class CommentaryEngine:

    def generate_market_commentary(
        self,
        regime_data: dict,
        top_sector: str,
    ):

        regime = regime_data["regime"]

        commentary = []

        # ==========================
        # MARKET REGIME
        # ==========================

        if regime == "bullish":

            commentary.append("Market remains in bullish regime.")

            commentary.append("Momentum and breadth remain strong.")

        elif regime == "cautious_bullish":

            commentary.append("Market trend improving cautiously.")

            commentary.append("Selective opportunities emerging.")

        elif regime == "sideways":

            commentary.append("Market currently moving sideways.")

            commentary.append("Swing opportunities remain selective.")

        elif regime == "bearish":

            commentary.append("Market remains under pressure.")

            commentary.append("Defensive positioning recommended.")

        elif regime == "panic":

            commentary.append("High risk market environment detected.")

            commentary.append("Capital preservation prioritized.")

        # ==========================
        # SECTOR ROTATION
        # ==========================

        commentary.append(f"Leading sector currently: {top_sector}.")

        # ==========================
        # AI INSIGHT
        # ==========================

        if regime in ["bullish", "cautious_bullish"]:

            commentary.append("AI suggests focusing on momentum leaders.")

        elif regime == "sideways":

            commentary.append("AI suggests shorter swing duration.")

        else:

            commentary.append("AI recommends reducing overall exposure.")

        return commentary
