function StatCard({ label, value, subtitle, valueColor = "text-white" }) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-5">
      <p className="text-sm font-medium text-zinc-500">
        {label}
      </p>

      <p className={`mt-2 text-3xl font-semibold tracking-tight ${valueColor}`}>
        {value}
      </p>

      {subtitle && (
        <p className="mt-1 text-sm text-zinc-500">
          {subtitle}
        </p>
      )}
    </div>
  );
}

export default StatCard;