"use client";

import { useEffect, useState } from "react";

import { useRouter } from "next/navigation";

import { api } from "@/services/api";

import DashboardCard from "@/components/DashboardCard";
import SectionTitle from "@/components/SectionTitle";
import RegimeBadge from "@/components/RegimeBadge";

import { useAuth } from "@/hooks/useAuth";

import { createClient } from "@/lib/supabase-browser";

import {
  getPortfolio,
} from "@/services/portfolio";

import {
  portfolioHealthScore,
} from "@/services/portfolio-analytics";

const supabase = createClient();

export default function Home() {

  const router = useRouter();

  const { user, loading } = useAuth();

  const [regime, setRegime] =
    useState<any>(null);

  const [screener, setScreener] =
    useState<any[]>([]);

  const [sectorRotation, setSectorRotation] =
    useState<any[]>([]);

  const [portfolio, setPortfolio] =
    useState<any[]>([]);

  const [portfolioHealth, setPortfolioHealth] =
    useState(0);

  const [aiSignals, setAiSignals] = useState<any[]>([]);

  // =========================================
  // AUTH CHECK
  // =========================================

  useEffect(() => {

    if (!loading && !user) {

      router.push("/login");
    }

  }, [user, loading, router]);

  // =========================================
  // FETCH DASHBOARD DATA
  // =========================================

  useEffect(() => {

    console.log(
      process.env.NEXT_PUBLIC_SUPABASE_URL
    );

    fetchData();

  }, []);

  async function fetchData() {

    try {

      // ====================================
      // FETCH API
      // ====================================

      const regimeRes = await api.get(
        "/market-regime"
      );

      const screenerRes = await api.get(
        "/screener"
      );

      const sectorRes = await api.get(
        "/sector-rotation"
      );

      const portfolioData =
        await getPortfolio();

      // ====================================
      // SET STATES
      // ====================================

      setRegime(regimeRes.data?.[0]);

      setScreener(
        screenerRes.data || []
      );

      setSectorRotation(
        sectorRes.data || []
      );

      setPortfolio(
        portfolioData || []
      );

      // ====================================
      // PORTFOLIO HEALTH ANALYTICS
      // ====================================

      if (portfolioData.length > 0) {

        const totalValue =
          portfolioData.reduce(
            (acc, item) =>
              acc +
              (
                item.quantity
                * item.average_price
              ),
            0
          );

        const largestPosition =
          Math.max(
            ...portfolioData.map(
              (item) =>
                (
                  item.quantity
                  * item.average_price
                )
            )
          );

        const concentration =
          (
            largestPosition
            / totalValue
          ) * 100;

        const health =
          portfolioHealthScore(
            concentration
          );

        const aiSignalRes = await api.get(
          "/ai-signals"
        );

        setAiSignals(
          aiSignalRes.data || []
        );

        setPortfolioHealth(
          health
        );
      }

    } catch (error) {

      console.error(error);
    }
  }

  // =========================================
  // LOGOUT
  // =========================================

  async function handleLogout() {

    await supabase.auth.signOut();

    router.push("/login");
  }

  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (

      <main
        className="
          min-h-screen
          bg-black
          text-white
          flex
          items-center
          justify-center
        "
      >

        <p>Loading...</p>

      </main>

    );
  }

  // =========================================
  // DASHBOARD
  // =========================================

  return (

    <main className="
      min-h-screen
      bg-black
      text-white
      p-8
    ">

      {/* HEADER */}

      <div className="
        flex
        justify-between
        items-center
        mb-8
      ">

        <SectionTitle
          title="AISSI Dashboard"
          subtitle="Institutional AI Trading Platform"
        />

        <button
          onClick={handleLogout}
          className="
            bg-red-500
            text-black
            px-4
            py-2
            rounded-lg
            font-bold
            h-fit
          "
        >
          Logout
        </button>

      </div>

      {/* GRID */}

      <div className="
        grid
        grid-cols-1
        lg:grid-cols-3
        gap-6
      ">

        {/* MARKET REGIME */}

        <DashboardCard title="Market Regime">

          {regime && (

            <div className="space-y-4">

              <RegimeBadge
                regime={regime.regime}
              />

              <div className="
                space-y-2
                text-zinc-300
              ">

                <p>
                  RSI : {regime.rsi}
                </p>

                <p>
                  Close : {regime.close}
                </p>

                <p>
                  EMA20 : {regime.ema20}
                </p>

                <p>
                  EMA50 : {regime.ema50}
                </p>

              </div>

            </div>

          )}

        </DashboardCard>

        {/* TOP PICKS */}

        <DashboardCard title="Top Picks">

          <div className="space-y-3">

            {screener.map(
              (stock, index) => (

                <div
                  key={index}
                  className="
                    flex
                    justify-between
                    items-center
                    border-b
                    border-zinc-800
                    pb-3
                  "
                >

                  <div>

                    <p className="
                      font-semibold
                    ">
                      {stock.symbol}
                    </p>

                    <p className="
                      text-sm
                      text-zinc-500
                    ">
                      RSI : {stock.rsi}
                    </p>

                  </div>

                  <div
                    className="
                      bg-emerald-500
                      text-black
                      px-3
                      py-1
                      rounded-lg
                      font-bold
                    "
                  >
                    {stock.score}
                  </div>

                </div>

              )
            )}

          </div>

        </DashboardCard>

        {/* SECTOR ROTATION */}

        <DashboardCard title="Sector Rotation">

          <div className="space-y-3">

            {sectorRotation.map(
              (sector, index) => (

                <div
                  key={index}
                  className="
                    flex
                    justify-between
                    items-center
                    border-b
                    border-zinc-800
                    pb-3
                  "
                >

                  <span className="
                    font-semibold
                  ">
                    {sector.sector}
                  </span>

                  <span
                    className="
                      bg-blue-500
                      text-black
                      px-3
                      py-1
                      rounded-lg
                      font-bold
                    "
                  >
                    {sector.score}
                  </span>

                </div>

              )
            )}

          </div>

        </DashboardCard>

        {/* PORTFOLIO */}

        <DashboardCard title="Portfolio">

          <div className="space-y-3">

            {portfolio.map(
              (position, index) => (

                <div
                  key={index}
                  className="
                    flex
                    justify-between
                    items-center
                    border-b
                    border-zinc-800
                    pb-3
                  "
                >

                  <div>

                    <p className="
                      font-semibold
                    ">
                      {position.symbol}
                    </p>

                    <p className="
                      text-sm
                      text-zinc-500
                    ">
                      Qty : {position.quantity}
                    </p>

                  </div>

                  <div
                    className="
                      bg-purple-500
                      text-black
                      px-3
                      py-1
                      rounded-lg
                      font-bold
                    "
                  >
                    {position.average_price}
                  </div>

                </div>

              )
            )}

          </div>

        </DashboardCard>

        {/* PORTFOLIO ANALYTICS */}

        <DashboardCard title="Portfolio Analytics">

          <div className="space-y-4">

            <div>

              <p className="
                text-zinc-400
              ">
                Health Score
              </p>

              <p
                className="
                  text-4xl
                  font-bold
                  text-emerald-400
                "
              >
                {portfolioHealth}/100
              </p>

            </div>

            <div className="
              space-y-2
              text-zinc-300
            ">

              {portfolioHealth < 50 && (

                <p>
                  ⚠ High concentration risk
                </p>

              )}

              {portfolioHealth >= 50 &&
                portfolioHealth < 80 && (

                <p>
                  Moderate portfolio health
                </p>

              )}

              {portfolioHealth >= 80 && (

                <p>
                  Portfolio well diversified
                </p>

              )}

            </div>

          </div>

        </DashboardCard>

        <DashboardCard title="AI Signals">

          <div className="space-y-4">

            {aiSignals.map((signal, index) => (

              <div
                key={index}
                className="
                  border-b
                  border-zinc-800
                  pb-4
                "
              >

                <div
                  className="
                    flex
                    justify-between
                    items-center
                    mb-2
                  "
                >

                  <p className="font-bold">
                    {signal.symbol}
                  </p>

                  <span
                    className="
                      bg-emerald-500
                      text-black
                      px-3
                      py-1
                      rounded-lg
                      font-bold
                    "
                  >
                    {signal.confidence}%
                  </span>

                </div>

                <p
                  className="
                    text-sm
                    text-zinc-400
                    mb-2
                  "
                >
                  {signal.signal}
                </p>

                <p
                  className="
                    text-xs
                    text-zinc-500
                  "
                >
                  {signal.reasons}
                </p>

              </div>

            ))}

          </div>

        </DashboardCard>

      </div>

    </main>

  );
}