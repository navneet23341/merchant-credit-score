import { useState } from "react";

import Header from "./components/Header";
import StatCard from "./components/StatCard";
import ScoreBreakdown from "./components/ScoreBreakdown";
import ScoreTrajectory from "./components/ScoreTrajectory";
import HinglishExplanation from "./components/HinglishExplanation";
import StressTester from "./components/StressTester";
import CapitalRecommendation from "./components/CapitalRecommendation";

function App() {
  const [merchantData, setMerchantData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyse = async (merchantId) => {
    if (!merchantId) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/merchant/${merchantId}`
      );

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("Merchant not found");
        }

        throw new Error("Failed to fetch merchant data");
      }

      const data = await response.json();

      console.log("MERCHANT DATA:", data);

      setMerchantData(data);
    } catch (error) {
      console.error(error);
      setMerchantData(null);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <Header onAnalyse={handleAnalyse} />

      <main className="px-6 pb-10">
        {loading && (
          <div className="py-10 text-center text-gray-400">
            Loading merchant data...
          </div>
        )}

        {error && (
          <div className="py-10 text-center text-red-400">
            {error}
          </div>
        )}

        {merchantData && !loading && (
          <>
            {/* ========================= */}
            {/* TOP STAT CARDS */}
            {/* ========================= */}

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <StatCard
                label="Credit Score"
                value={merchantData.credit.credit_score}
                subtitle={
                  merchantData.credit.credit_tier
                }
                valueColor="text-blue-400"
              />

              <StatCard
                label="Credit Tier"
                value={
                  merchantData.credit.credit_tier
                }
                subtitle="Credit profile"
                valueColor="text-emerald-400"
              />

              <StatCard
                label="Monthly Revenue"
                value={`₹${(
                  merchantData.merchant.monthly_revenue / 100000
                ).toFixed(1)}L`}
                subtitle="Average"
              />

              <StatCard
                label="Working Capital"
                value="₹1.2L"
                subtitle="Recommended"
              />
            </div>

            {/* ========================= */}
            {/* SCORE BREAKDOWN */}
            {/* ========================= */}

            <ScoreBreakdown
              data={merchantData.explanation}
            />

            {/* ========================= */}
            {/* SCORE TRAJECTORY */}
            {/* ========================= */}

            <ScoreTrajectory
              data={merchantData}
            />

            {/* ========================= */}
            {/* HINGLISH EXPLANATION */}
            {/* ========================= */}

            <HinglishExplanation
              merchantId={
                merchantData.merchant.merchant_id
              }
            />

            {/* ========================= */}
            {/* STRESS TEST */}
            {/* ========================= */}

            <StressTester
              merchantId={
                merchantData.merchant.merchant_id
              }
              data={merchantData.stress_test}
            />

            {/* ========================= */}
            {/* CAPITAL RECOMMENDATION */}
            {/* ========================= */}

            <CapitalRecommendation
              data={merchantData}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;