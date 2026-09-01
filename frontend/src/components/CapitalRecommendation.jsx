function CapitalRecommendation({
  maxAmount = "₹10,00,000",
  interestRate = "15% p.a.",
  tenure = "18 months",
  actions = [
    "Reduce refund rate below 8%",
    "Increase repeat customer rate to 50%",
    "Reduce failed payments below 5%",
  ],
}) {
  return (
    <section className="rounded-2xl border border-zinc-700 bg-[#181818] p-7">
      <h2 className="mb-7 text-xl font-medium text-zinc-200">
        Working capital recommendation
      </h2>

      <div className="grid grid-cols-1 gap-6 text-center md:grid-cols-3">

        <div>
          <p className="text-sm text-zinc-500">
            Max amount
          </p>

          <p className="mt-1 text-2xl text-zinc-200">
            {maxAmount}
          </p>
        </div>

        <div>
          <p className="text-sm text-zinc-500">
            Interest rate
          </p>

          <p className="mt-1 text-2xl text-zinc-200">
            {interestRate}
          </p>
        </div>

        <div>
          <p className="text-sm text-zinc-500">
            Tenure
          </p>

          <p className="mt-1 text-2xl text-zinc-200">
            {tenure}
          </p>
        </div>

      </div>

      <div className="mt-7 rounded-xl bg-[#0b2b0d] px-5 py-4">
        <p className="text-sm leading-6 text-green-500">
          <span className="font-semibold">
            Top 3 actions to improve your score:
          </span>{" "}
          {actions.join(", ")}.
        </p>
      </div>
    </section>
  );
}

export default CapitalRecommendation;