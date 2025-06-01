import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import Spline from '@splinetool/react-spline';

const pieces = [
  { name: 'Data Ingestion', position: 'top-[10%] left-[16%]' },
  { name: 'Processing', position: 'top-[16%] right-[20%]' },
  { name: 'Clustering', position: 'bottom-[35%] left-[5%]' },
  { name: 'UI Dashboard', position: 'bottom-[8%] left-[23%]' },
  { name: 'Forecasting', position: 'bottom-[18%] right-[10%]' },
];

export default function App() {
  const textRef = useRef(null);
  const text = 'ROAD MAP';

  useEffect(() => {
    const chars = textRef.current.querySelectorAll('.char');
    gsap.set(chars, { opacity: 0 });

    const timeline = gsap.timeline({ repeat: -1, repeatDelay: 1 });

    timeline.to(chars, {
      opacity: 1,
      duration: 0.1,
      stagger: 0.15,
      ease: 'power1.inOut',
    });

    timeline.to(chars, {
      opacity: 0,
      duration: 0.1,
      stagger: 0.1,
      delay: 1,
      ease: 'power1.inOut',
    });
  }, []);

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-black to-[#1c1329] text-white font-sans overflow-hidden">
      {/* Animated Title */}
      <h1 ref={textRef} className="text-center text-4xl font-bold underline pt-10 z-30 relative">
        {text.split('').map((char, i) => (
          <span key={i} className="char inline-block">
            {char === ' ' ? '\u00A0' : char}
          </span>
        ))}
      </h1>

      {/* Arrowed Sequential Path */}
      <svg className="absolute inset-0 w-full h-full z-20 pointer-events-none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto-start-reverse" markerUnits="strokeWidth">
            <path d="M0,0 L10,5 L0,10 z" fill="white" />
          </marker>
        </defs>
        <line x1="28%" y1="17%" x2="69%" y2="23%" stroke="white" strokeWidth="2" markerEnd="url(#arrow)" />
        <line x1="68%" y1="27%" x2="17%" y2="50%" stroke="white" strokeWidth="2" markerEnd="url(#arrow)" />
        <line x1="18%" y1="54%" x2="79%" y2="68.5%" stroke="white" strokeWidth="2" markerEnd="url(#arrow)" />
        <line x1="78%" y1="74%" x2="35%" y2="86%" stroke="white" strokeWidth="2" markerEnd="url(#arrow)" />
      </svg>

      {/* 3D Spline Robot Centered */}
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <Spline scene="https://prod.spline.design/1EL3hGXqzN0kzmyG/scene.splinecode" className="w-full h-full pt-70" />
      </div>

      {/* Hide Spline Logo */}
      <div className="absolute bottom-1 right-1 w-[300px] h-[60px] bg-[#1c1329] z-30"></div>

      {/* Puzzle Nodes with External Labels */}
      {pieces.map(({ name, position }) => (
        <div
          key={name}
          className={`absolute ${position} z-40 flex flex-col items-center`}
        >
          <motion.div
            whileHover={{ scale: 1.1, boxShadow: '0 0 30px rgba(168,85,247,0.8)' }}
            className="transition-all duration-300 drop-shadow-[0_4px_8px_rgba(168,85,247,0.35)]"
          >
            <img
              src="/puzzle.png"
              alt="Puzzle Piece"
              className="w-36 h-36 object-contain transition-transform duration-300"
              style={{ transform: `rotate(${Math.floor(Math.random() * 360)}deg)` }}
            />
          </motion.div>
          <div className="mt-2 text-center text-lg font-bold text-white">
            {name}
          </div>
        </div>
      ))}
    </div>
  );
}