import React from 'react';

const Header = () => {
  return (
    <header className="w-full absolute top-0 z-50 flex items-center justify-between px-24 py-4 bg-transparent text-white">
      
      <div className="flex items-center space-x-12">
        <img
          src="/logo_cropped.png"
          alt="5G Logo"
          className="h-20 w-auto object-contain"
        />
        <nav className="flex space-x-12 font-semibold">
          <a
            href="#"
            className="px-4 py-2 rounded border-2 border-[#333] text-white no-underline transition-all duration-300 hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:border-white active:shadow-[0_0_30px_rgba(255,255,255,0.7)]"
          >
            Home
          </a>
          <a
            href="#teams"
            className="px-4 py-2 rounded border-2 border-[#333] text-white no-underline transition-all duration-300 hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:border-white active:shadow-[0_0_30px_rgba(255,255,255,0.7)]"
          >
            Teams
          </a>
          <a
            href="#data"
            className="px-4 py-2 rounded border-2 border-[#333] text-white no-underline transition-all duration-300 hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:border-white active:shadow-[0_0_30px_rgba(255,255,255,0.7)]"
          >
            Data
          </a>
          <a
            href="#models"
            className="px-4 py-2 rounded border-2 border-[#333] text-white no-underline transition-all duration-300 hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:border-white active:shadow-[0_0_30px_rgba(255,255,255,0.7)]"
          >
            Models
          </a>
        </nav>
      </div>

      <div className="flex items-center space-x-12">
        <a
          href="#insight"
          className="font-semibold px-4 py-2 rounded border-2 border-[#333] text-white no-underline transition-all duration-300 hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:border-white active:shadow-[0_0_30px_rgba(255,255,255,0.7)]"
        >
          Insight
        </a>

        <a
          href="https://github.com/SavinduWickr/5G_Network_Performance.git"
          className="flex items-center gap-2 font-semibold text-white px-4 py-2 rounded border-2 border-[#333] bg-[#1a1a1a] transition-all duration-300 hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] hover:border-white active:shadow-[0_0_30px_rgba(255,255,255,0.7)]"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 .5C5.73.5.5 5.73.5 12c0 5.08 3.29 9.39 7.86 10.92.58.11.79-.25.79-.56 0-.28-.01-1.02-.01-2-3.2.7-3.88-1.4-3.88-1.4-.53-1.34-1.3-1.7-1.3-1.7-1.06-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.77 2.74 1.26 3.41.96.11-.76.41-1.26.74-1.55-2.56-.29-5.25-1.28-5.25-5.7 0-1.26.45-2.3 1.19-3.11-.12-.3-.52-1.52.11-3.17 0 0 .97-.31 3.18 1.18A11.1 11.1 0 0112 6.8c.98.01 1.97.13 2.9.39 2.2-1.49 3.17-1.18 3.17-1.18.63 1.65.23 2.87.11 3.17.74.81 1.19 1.85 1.19 3.11 0 4.43-2.69 5.41-5.25 5.69.43.38.81 1.1.81 2.21 0 1.6-.01 2.89-.01 3.28 0 .31.21.68.8.56A10.52 10.52 0 0023.5 12C23.5 5.73 18.27.5 12 .5z" />
          </svg>
          Code
        </a>
      </div>

    </header>
  );
};

export default Header;

