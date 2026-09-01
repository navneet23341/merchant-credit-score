function HinglishExplanation({ explanation }) {
  return (
    <section className="rounded-2xl border border-blue-700 bg-[#062650] p-7">
      <h2 className="mb-3 text-xl font-medium text-zinc-200">
        Hinglish explanation
      </h2>

      <p className="text-base leading-7 text-zinc-300">
        {explanation ||
          "Aapka score analyse karne ke baad explanation yahan dikhega."}
      </p>
    </section>
  );
}

export default HinglishExplanation;