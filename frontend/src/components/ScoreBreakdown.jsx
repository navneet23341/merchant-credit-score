function ScoreBreakdown({ data }) {
  if (!data) return null;

  const positiveFactors = data.positive_factors || [];
  const negativeFactors = data.negative_factors || [];

  return (
    <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">
          Score Breakdown
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Factors influencing the merchant's credit score
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">

        {/* Positive Factors */}

        <div>
          <h3 className="mb-3 text-sm font-medium text-emerald-400">
            Positive Factors
          </h3>

          <div className="space-y-3">
            {positiveFactors.length > 0 ? (
              positiveFactors.slice(0, 3).map((factor) => (
                <div
                  key={factor.feature}
                  className="flex items-center justify-between rounded-xl border border-zinc-800 bg-zinc-900 p-4"
                >
                  <div>
                    <p className="text-sm text-white">
                      {factor.feature}
                    </p>

                    <p className="mt-1 text-xs text-zinc-500">
                      Value: {factor.value}
                    </p>
                  </div>

                  <span className="text-sm font-semibold text-emerald-400">
                    +{factor.impact}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-sm text-zinc-500">
                No positive factors identified.
              </p>
            )}
          </div>
        </div>

        {/* Negative Factors */}

        <div>
          <h3 className="mb-3 text-sm font-medium text-red-400">
            Negative Factors
          </h3>

          <div className="space-y-3">
            {negativeFactors.length > 0 ? (
              negativeFactors.slice(0, 3).map((factor) => (
                <div
                  key={factor.feature}
                  className="flex items-center justify-between rounded-xl border border-zinc-800 bg-zinc-900 p-4"
                >
                  <div>
                    <p className="text-sm text-white">
                      {factor.feature}
                    </p>

                    <p className="mt-1 text-xs text-zinc-500">
                      Value: {factor.value}
                    </p>
                  </div>

                  <span className="text-sm font-semibold text-red-400">
                    {factor.impact}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-sm text-zinc-500">
                No negative factors identified.
              </p>
            )}
          </div>
        </div>

      </div>
    </section>
  );
}

export default ScoreBreakdown;