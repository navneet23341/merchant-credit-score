function ScoreTrajectory({ data }) {
  if (!data?.merchant) return null;

  const currentScore = data.credit?.credit_score ?? 0;
  const trajectory = data.merchant.score_trajectory ?? 0;
  const projectedScore =
    data.merchant.projected_score_3months ?? currentScore;

  const isPositive = trajectory >= 0;

  return (
    <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">
          Score Trajectory
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Current performance and projected credit score
        </p>
      </div>

      {/* Scores */}
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

        {/* Trajectory */}
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
            {isPositive ? "+" : ""}
            {trajectory.toFixed(2)}
          </p>

          <p className="mt-1 text-xs text-zinc-500">
            Recent trend
          </p>
        </div>

        {/* Projection */}
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

      {/* Simple trajectory visualization */}
      <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-5">

        <div className="mb-3 flex items-center justify-between">
          <span className="text-sm text-zinc-500">
            Current
          </span>

          <span className="text-sm text-zinc-500">
            3 Months
          </span>
        </div>

        <div className="relative h-3 rounded-full bg-zinc-800">

          <div
            className="h-3 rounded-full bg-blue-500 transition-all"
            style={{
              width: `${Math.min(
                100,
                Math.max(
                  0,
                  (projectedScore / 1000) * 100
                )
              )}%`,
            }}
          />

        </div>

        <div className="mt-3 flex justify-between text-xs text-zinc-500">
          <span>{currentScore.toFixed(2)}</span>

          <span>{projectedScore.toFixed(2)}</span>
        </div>

      </div>
    </section>
  );
}

export default ScoreTrajectory;