import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function ScoreTrajectory({ data }) {
  if (!data?.merchant) return null;

  const currentScore = Number(
    data.credit?.credit_score ?? 0
  );

  const trajectory = Array.isArray(
    data.merchant?.score_trajectory
  )
    ? data.merchant.score_trajectory
        .map(Number)
        .filter(Number.isFinite)
    : [];

  const projectedScore = Number(
    data.merchant?.projected_score_3months ??
      currentScore
  );

  const firstScore =
    trajectory[0] ?? currentScore;

  const latestScore =
    trajectory[trajectory.length - 1] ??
    currentScore;

  const trajectoryChange =
    latestScore - firstScore;

  const isPositive = trajectoryChange >= 0;

  // Convert the score array into chart data
  const chartData = trajectory.map(
    (score, index) => ({
      period: `P${index + 1}`,
      score,
    })
  );

  return (
    <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

      {/* Header */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">
          Score Trajectory
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Historical performance and projected credit score
        </p>
      </div>

      {/* Score Summary */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">

        {/* Current Score */}
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <p className="text-sm text-zinc-500">
            Current Score
          </p>

          <p className="mt-2 text-3xl font-semibold text-white">
            {currentScore.toFixed(2)}
          </p>
        </div>

        {/* Trajectory Change */}
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <p className="text-sm text-zinc-500">
            Score Trajectory
          </p>

          <p
            className={`mt-2 text-3xl font-semibold ${
              isPositive
                ? "text-emerald-400"
                : "text-red-400"
            }`}
          >
            {trajectoryChange >= 0 ? "+" : ""}
            {trajectoryChange.toFixed(2)}
          </p>

          <p className="mt-1 text-xs text-zinc-500">
            Historical change
          </p>
        </div>

        {/* Projected Score */}
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <p className="text-sm text-zinc-500">
            Projected Score
          </p>

          <p className="mt-2 text-3xl font-semibold text-blue-400">
            {projectedScore.toFixed(2)}
          </p>

          <p className="mt-1 text-xs text-zinc-500">
            Next 3 months
          </p>
        </div>

      </div>

      {/* Actual Line Chart */}
      <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-5">

        <div className="mb-5">
          <h3 className="text-sm font-medium text-white">
            Credit Score History
          </h3>

          <p className="mt-1 text-xs text-zinc-500">
            Score movement across recent periods
          </p>
        </div>

        <div className="h-64 w-full">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <LineChart
              data={chartData}
              margin={{
                top: 10,
                right: 10,
                left: 0,
                bottom: 5,
              }}
            >

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#27272a"
              />

              <XAxis
                dataKey="period"
                tick={{
                  fill: "#71717a",
                  fontSize: 12,
                }}
                axisLine={{
                  stroke: "#3f3f46",
                }}
                tickLine={false}
              />

              <YAxis
                domain={[
                  "dataMin - 20",
                  "dataMax + 20",
                ]}
                tick={{
                  fill: "#71717a",
                  fontSize: 12,
                }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#18181b",
                  border: "1px solid #3f3f46",
                  borderRadius: "10px",
                  color: "#ffffff",
                }}
                labelStyle={{
                  color: "#a1a1aa",
                }}
                formatter={(value) => [
                  Number(value).toFixed(2),
                  "Credit Score",
                ]}
              />

              <Line
                type="monotone"
                dataKey="score"
                stroke="#3b82f6"
                strokeWidth={3}
                dot={{
                  r: 4,
                  fill: "#3b82f6",
                  strokeWidth: 0,
                }}
                activeDot={{
                  r: 6,
                }}
              />

            </LineChart>
          </ResponsiveContainer>

        </div>

        {/* Start / End */}
        <div className="mt-3 flex justify-between text-xs text-zinc-500">
          <span>
            Start: {firstScore.toFixed(2)}
          </span>

          <span>
            Latest: {latestScore.toFixed(2)}
          </span>
        </div>

      </div>

    </section>
  );
}

export default ScoreTrajectory;