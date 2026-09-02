import { useEffect, useState } from "react";

function StressTester({
  merchantId,
  data,
}) {
  const currentScore = Number(
    data?.current_score ?? 0
  );

  const scenarios = data?.all_scenarios ?? [];

  const getInitialValue = (
    feature,
    fallback
  ) => {
    const scenario = scenarios.find(
      (item) => item.feature === feature
    );

    return Number(
      scenario?.current_value ?? fallback
    );
  };

  const [refundRate, setRefundRate] =
    useState(
      getInitialValue("refund_rate", 8)
    );

  const [repeatCustomers, setRepeatCustomers] =
    useState(
      getInitialValue(
        "customer_repeat_rate",
        36
      )
    );

  const [failedPayments, setFailedPayments] =
    useState(
      getInitialValue(
        "failed_payment_rate",
        1
      )
    );

  const [
    simulatedScore,
    setSimulatedScore,
  ] = useState(currentScore);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");

  useEffect(() => {
    setSimulatedScore(currentScore);
  }, [currentScore]);

  const runSimulation = async (
    changes
  ) => {
    if (!merchantId) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/merchant/${merchantId}/stress-test`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            changes,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Stress test failed"
        );
      }

      const result =
        await response.json();

      setSimulatedScore(
        Number(result.projected_score)
      );

    } catch (error) {
      console.error(error);
      setError(
        "Unable to calculate simulation."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRefundChange = (value) => {
    setRefundRate(value);

    runSimulation({
      refund_rate: value,
      customer_repeat_rate:
        repeatCustomers,
      failed_payment_rate:
        failedPayments,
    });
  };

  const handleRepeatChange = (value) => {
    setRepeatCustomers(value);

    runSimulation({
      refund_rate: refundRate,
      customer_repeat_rate: value,
      failed_payment_rate:
        failedPayments,
    });
  };

  const handleFailedPaymentChange = (
    value
  ) => {
    setFailedPayments(value);

    runSimulation({
      refund_rate: refundRate,
      customer_repeat_rate:
        repeatCustomers,
      failed_payment_rate: value,
    });
  };

  const scoreDifference =
    simulatedScore - currentScore;

  return (
    <section className="rounded-2xl border border-zinc-700 bg-[#181818] p-7">

      <div className="mb-7">
        <h2 className="text-xl font-medium text-zinc-200">
          What-if stress tester
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Adjust merchant metrics to see how
          the credit score could change
        </p>
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">

        {/* LEFT */}
        <div className="space-y-7">

          <Slider
            label="Refund rate"
            value={refundRate}
            min={0}
            max={20}
            unit="%"
            onChange={
              handleRefundChange
            }
          />

          <Slider
            label="Failed payments"
            value={failedPayments}
            min={0}
            max={20}
            unit="%"
            onChange={
              handleFailedPaymentChange
            }
          />

        </div>

        {/* RIGHT */}
        <div className="space-y-7">

          <Slider
            label="Repeat customers"
            value={repeatCustomers}
            min={0}
            max={100}
            unit="%"
            onChange={
              handleRepeatChange
            }
          />

          {/* RESULT */}
          <div className="flex min-h-36 flex-col items-center justify-center rounded-xl bg-[#111111]">

            <p className="text-sm text-zinc-500">
              Simulated score
            </p>

            {loading ? (
              <div className="mt-3 h-7 w-7 animate-spin rounded-full border-2 border-zinc-700 border-t-blue-400" />
            ) : (
              <>
                <p className="mt-2 text-4xl font-light text-blue-400">
                  {simulatedScore.toFixed(2)}
                </p>

                <p
                  className={`mt-1 text-sm ${
                    scoreDifference >= 0
                      ? "text-green-500"
                      : "text-red-400"
                  }`}
                >
                  {scoreDifference >= 0
                    ? "+"
                    : ""}
                  {scoreDifference.toFixed(2)}{" "}
                  points
                </p>
              </>
            )}

          </div>

          {error && (
            <p className="text-center text-sm text-red-400">
              {error}
            </p>
          )}

        </div>

      </div>
    </section>
  );
}

function Slider({
  label,
  value,
  min,
  max,
  unit,
  onChange,
}) {
  return (
    <div>

      <div className="mb-4 flex items-center justify-between">

        <span className="text-base text-zinc-400">
          {label}
        </span>

        <span className="text-base text-zinc-300">
          {value}
          {unit}
        </span>

      </div>

      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) =>
          onChange(
            Number(e.target.value)
          )
        }
        className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-zinc-700 accent-white"
      />

    </div>
  );
}

export default StressTester;