import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import GlowyButton from './GlowyButton';
import GlowyBackground from './GlowyBackground';

const Hero = () => {
  const numberRef = useRef(null);

  useEffect(() => {
    const numbers = [1, 4, 2, 3, 5];
    let index = 0;

    const scrambleAnimation = gsap.to({}, {
      duration: 0.09,
      repeat: numbers.length * 3 - 1,
      repeatDelay: 0.01,
      onRepeat: () => {
        numberRef.current.textContent = numbers[index++ % numbers.length];
      },
      onComplete: () => {
        numberRef.current.textContent = '5';
      },
    });

    return () => scrambleAnimation.kill();
  }, []);

  return (
    <>
      <div className="fixed inset-0 z-0 pointer-events-none">
        <GlowyBackground />
      </div>

      <section className="relative h-[100vh] text-white overflow-hidden z-10">
        <div className="relative z-30 flex flex-col justify-center h-full pl-12 pr-4 md:pl-24 md:pr-10">
          <div className="max-w-xl">
            <h1 className="text-5xl md:text-8xl font-bold text-purple-300 leading-tight">
              <span ref={numberRef}>5</span>G Network
            </h1>
            <div className="pl-4 md:pl-6">
              <p className="mt-4 text-sm md:text-lg text-gray-300">
                Using 5G network performance data (such as throughput and latency), identify
                geographical zones (from longitude and latitude) with different performance levels.
                Also, the network performance of the zone can be predicted using time-series data.
              </p>
              <GlowyButton text="Dashboard" className="mt-6" />
            </div>
          </div>
        </div>
      </section>

      <section className="relative z-10 bg-transparent max-w-[160vh] min-h-[80vh] rounded-3xl ml-12 md:ml-24 mr-4 md:mr-10 -mt-32 mb-20 overflow-hidden shadow-[0_0_80px_20px_rgba(99,102,241,0.6)] border border-white">
        <img
          src="/Dashboard2.png"
          alt="5G Network Dashboard"
          className="w-full h-full object-cover rounded-3xl"
        />
      </section>
    </>
  );
};

export default Hero;
