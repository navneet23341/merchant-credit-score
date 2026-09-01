import { useState } from "react";

function Header({ onAnalyse }) {
  const [merchantId, setMerchantId] = useState("");

  const handleAnalyse = () => {
    const id = merchantId.trim();

    if (!id) return;

    onAnalyse(id);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleAnalyse();
    }
  };

  return (
    <header className="w-full px-6 py-8">
      <div className="flex items-center justify-between gap-8">
        
        {/* Logo / Title */}
        <div>
          <p className="text-sm font-semibold text-gray-500">
            MerchantScore
          </p>

          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-white">
            Merchant credit intelligence
          </h1>
        </div>

        {/* Search */}
        <div className="flex items-center gap-3">
          <input
            type="text"
            value={merchantId}
            onChange={(e) => setMerchantId(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter merchant ID..."
            className="
              w-72
              rounded-lg
              border
              border-gray-700
              bg-[#181818]
              px-4
              py-3
              text-base
              text-white
              placeholder-gray-400
              outline-none
              transition
              focus:border-gray-500
            "
          />

          <button
            onClick={handleAnalyse}
            className="
              rounded-full
              border-2
              border-white
              px-6
              py-2
              text-sm
              font-semibold
              text-white
              transition
              hover:bg-white
              hover:text-black
            "
          >
            Analyse
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;