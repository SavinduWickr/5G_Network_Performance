import React, { useRef } from 'react';
import gsap from 'gsap';

const GlowyButton = ({ text = "Dashboard", className = "" }) => {
  const glowRef = useRef(null);

  const handleMouseMove = (e) => {
    const btn = e.currentTarget;
    const glow = glowRef.current;
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    gsap.to(glow, {
      x: x - glow.offsetWidth / 2,
      y: y - glow.offsetHeight / 2,
      duration: 0.3,
      ease: 'power2.out',
    });
  };

  const handleClick = () => {
    window.open('http://localhost:8501', '_blank');
  };

  return (
    <button
      onMouseMove={handleMouseMove}
      onClick={handleClick}
      className={`relative px-10 py-1.5 rounded-full font-medium text-sm bg-[#d9d9d9] text-zinc-800 overflow-hidden border border-zinc-300 transition-transform duration-200 hover:scale-[1.03] ${className}`}
    >
      <span className="relative z-10 flex items-center gap-2">
        {text} <span className="text-lg">→</span>
      </span>
      <div
        ref={glowRef}
        className="absolute w-40 h-40 rounded-full bg-amber-600 opacity-90 blur-[20px] pointer-events-none z-0"
        style={{
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
        }}
      />
    </button>
  );
};

export default GlowyButton;
