import React, { useState, useEffect } from 'react';

const GlowyBackground = () => {
  const [mousePos, setMousePos] = useState({ x: -9999, y: -9999 });

  useEffect(() => {
    const moveSpotlight = (e) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("mousemove", moveSpotlight);
    return () => {
      window.removeEventListener("mousemove", moveSpotlight);
    };
  }, []);

  const maskStyle = {
    WebkitMaskImage: `radial-gradient(circle 150px at ${mousePos.x}px ${mousePos.y}px, white 0%, transparent 100%)`,
    maskImage: `radial-gradient(circle 150px at ${mousePos.x}px ${mousePos.y}px, white 0%, transparent 100%)`,
    WebkitMaskRepeat: "no-repeat",
    maskRepeat: "no-repeat",
    WebkitMaskSize: "100% 100%",
    maskSize: "100% 100%",
    transition: "mask-image 0.2s ease, -webkit-mask-image 0.2s ease",
  };

  return (
    <div className="absolute inset-0 z-0 overflow-hidden">
      <video
        className="absolute inset-0 w-full h-full object-cover"
        autoPlay
        loop
        muted
        playsInline
        src="/video.mp4"
      />
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: "url('/background.png')",
          ...maskStyle,
        }}
      />
    </div>
  );
};

const AnimatedCounter = ({ end, duration = 2000, suffix = "" }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime;
    const animate = (currentTime) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      setCount(Math.floor(easeOutQuart * end));
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [end, duration]);

  return <span>{count.toLocaleString()}{suffix}</span>;
};

export default function DataSection() {
  return (
    <div className="relative py-32 min-h-screen bg-slate-900">
      {/* Glowy Background */}
      <GlowyBackground />

      <div className="relative z-10 container mx-auto px-6">
        {/* Section Title */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-light text-white mb-4">
            Network <span className="text-orange-400">Data</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Real-time insights from our comprehensive 5G network analysis
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-sm border border-purple-500/20 rounded-xl p-6 text-center hover:border-orange-400/40 transition-colors">
            <div className="text-3xl font-bold text-white mb-2">
              <AnimatedCounter end={150} suffix="K" />
            </div>
            <div className="text-orange-400 font-semibold text-sm mb-1">Data Points</div>
            <div className="text-gray-400 text-xs">Network Records</div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-sm border border-purple-500/20 rounded-xl p-6 text-center hover:border-orange-400/40 transition-colors">
            <div className="text-3xl font-bold text-white mb-2">
              <AnimatedCounter end={32} />
            </div>
            <div className="text-orange-400 font-semibold text-sm mb-1">Columns</div>
            <div className="text-gray-400 text-xs">Data Features</div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-sm border border-purple-500/20 rounded-xl p-6 text-center hover:border-orange-400/40 transition-colors">
            <div className="text-3xl font-bold text-white mb-2">
              99.2<span className="text-xl">%</span>
            </div>
            <div className="text-orange-400 font-semibold text-sm mb-1">SVR Correlation Found</div>
            <div className="text-gray-400 text-xs">Network Reliability</div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-sm border border-purple-500/20 rounded-xl p-6 text-center hover:border-orange-400/40 transition-colors">
            <div className="text-3xl font-bold text-white mb-2">
              &lt;1<span className="text-xl">ms</span>
            </div>
            <div className="text-orange-400 font-semibold text-sm mb-1">Latency</div>
            <div className="text-gray-400 text-xs">Response Time</div>
          </div>
        </div>
      </div>
    </div>
  );
}