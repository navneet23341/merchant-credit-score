function CapitalRecommendation({ data }) {
  console.log("CAPITAL DATA:", data);
  const recommendation = data?.recommendation;

  if (!recommendation) {
    return null;
  }

  const {
    eligible,
    max_amount,
    interest_rate,
    tenure_months,
    tier,
  } = recommendation;

  return (
    <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">
          Working Capital Recommendation
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Recommended financing based on merchant profile
        </p>
      </div>

      {!eligible ? (
        <div className="rounded-xl border border-red-900/50 bg-red-950/20 p-5">
          <p className="text-sm font-medium text-red-400">
            Not currently eligible
          </p>

          <p className="mt-2 text-sm leading-6 text-zinc-500">
            The merchant does not currently meet the recommendation criteria.
          </p>
        </div>
      ) : (
        <>
          <div className="mb-5 rounded-xl bg-[#111111] p-5">
            <p className="text-sm text-zinc-500">
              Maximum recommended amount
            </p>

            <p className="mt-2 text-4xl font-light text-blue-400">
              ₹{(max_amount / 100000).toFixed(2)}L
            </p>

            <p className="mt-1 text-sm text-zinc-500">
              {tier} financing tier
            </p>
          </div>

          <div className="grid grid-cols-3 gap-3">

            <div className="rounded-xl bg-[#111111] p-4">
              <p className="text-xs text-zinc-500">
                Interest Rate
              </p>

              <p className="mt-2 text-lg font-medium text-zinc-200">
                {interest_rate}%
              </p>
            </div>

            <div className="rounded-xl bg-[#111111] p-4">
              <p className="text-xs text-zinc-500">
                Tenure
              </p>

              <p className="mt-2 text-lg font-medium text-zinc-200">
                {tenure_months} months
              </p>
            </div>

            <div className="rounded-xl bg-[#111111] p-4">
              <p className="text-xs text-zinc-500">
                Tier
              </p>

              <p className="mt-2 text-lg font-medium text-zinc-200">
                {tier}
              </p>
            </div>

          </div>
        </>
      )}
    </section>
  );
}

export default CapitalRecommendation;