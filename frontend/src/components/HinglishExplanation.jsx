import { useEffect, useState } from "react";

function HinglishExplanation({ merchantId }) {
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!merchantId) return;

    const fetchExplanation = async () => {
      setLoading(true);
      setError("");
      setExplanation("");

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/merchant/${merchantId}/hinglish-explain`
        );

        if (!response.ok) {
          throw new Error("Failed to generate explanation");
        }

        const data = await response.json();

        console.log("HINGLISH EXPLANATION:", data);

        setExplanation(data.explanation || "");
      } catch (error) {
        console.error(error);
        setError("Unable to generate explanation right now.");
      } finally {
        setLoading(false);
      }
    };

    fetchExplanation();
  }, [merchantId]);

  return (
    <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

      {/* Header */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">
          AI Explanation
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Simple explanation of your credit profile
        </p>
      </div>

      {/* Loading */}
      {loading && (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <div className="flex items-center gap-3">

            <div className="h-4 w-4 animate-spin rounded-full border-2 border-zinc-700 border-t-blue-400" />

            <p className="text-sm text-zinc-400">
              Generating your explanation...
            </p>

          </div>
        </div>
      )}

      {/* Error */}
      {error && !loading && (
        <div className="rounded-xl border border-red-900/50 bg-red-950/20 p-5">
          <p className="text-sm text-red-400">
            {error}
          </p>
        </div>
      )}

      {/* Explanation */}
      {explanation && !loading && !error && (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">

          <div className="mb-4 flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500/10 text-lg">
              ✨
            </div>

            <div>
              <p className="text-sm font-medium text-white">
                Aapke liye simple explanation
              </p>

              <p className="text-xs text-zinc-500">
                AI-generated insight
              </p>
            </div>
          </div>

          <p className="text-sm leading-7 text-zinc-300">
            {explanation}
          </p>

        </div>
      )}

    </section>
  );
}

export default HinglishExplanation;