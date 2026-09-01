import { useState } from "react";

function StressTester({
  currentScore = 724,
  initialRefundRate = 8,
  initialRepeatCustomers = 36,
  initialFailedPayments = 1,
}) {
  const [refundRate, setRefundRate] = useState(initialRefundRate);
  const [repeatCustomers, setRepeatCustomers] =
    useState(initialRepeatCustomers);
  const [failedPayments, setFailedPayments] =
    useState(initialFailedPayments);

  const calculateScore = () => {
    const refundImpact =
      (initialRefundRate - refundRate) * 2;

    const repeatImpact =
      (repeatCustomers - initialRepeatCustomers) * 0.4;

    const paymentImpact =
      (initialFailedPayments - failedPayments) * 3;

    return Math.round(
      currentScore +
        refundImpact +
        repeatImpact +
        paymentImpact
    );
  };

  const simulatedScore = calculateScore();
  const scoreDifference = simulatedScore - currentScore;

  return (
    <section className="rounded-2xl border border-zinc-700 bg-[#181818] p-7">
      <h2 className="mb-7 text-xl font-medium text-zinc-200">
        What-if stress tester
      </h2>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">

        {/* Left */}
        <div className="space-y-7">

          <Slider
            label="Refund rate"
            value={refundRate}
            min={0}
            max={20}
            unit="%"
            onChange={setRefundRate}
          />

          <Slider
            label="Failed payments"
            value={failedPayments}
            min={0}
            max={20}
            unit="%"
            onChange={setFailedPayments}
          />

        </div>

        {/* Right */}
        <div className="space-y-7">

          <Slider
            label="Repeat customers"
            value={repeatCustomers}
            min={0}
            max={100}
            unit="%"
            onChange={setRepeatCustomers}
          />

          <div className="flex min-h-36 flex-col items-center justify-center rounded-xl bg-[#111111]">
            <p className="text-sm text-zinc-500">
              Simulated score
            </p>

            <p className="mt-2 text-4xl font-light text-blue-400">
              {simulatedScore}
            </p>

            <p
              className={`mt-1 text-sm ${
                scoreDifference >= 0
                  ? "text-green-500"
                  : "text-red-400"
              }`}
            >
              {scoreDifference >= 0 ? "+" : ""}
              {scoreDifference} points
            </p>
          </div>

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
          onChange(Number(e.target.value))
        }
        className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-zinc-700 accent-white"
      />
    </div>
  );
}

export default StressTester;