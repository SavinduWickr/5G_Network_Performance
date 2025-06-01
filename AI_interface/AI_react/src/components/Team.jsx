import React, { useEffect, useRef, useState } from 'react';
import Matter from 'matter-js';

const buttonsData = [
  { text: "Maisha", color: '#e7ebee', textColor: '#171614' },
  { text: 'Chung', color: '#8089d2', textColor: '#100C0B' },
  { text: 'Alvin', color: '#fd6d05', textColor: '#1C1B17' },
  { text: 'Tom', color: '#e7ebee', textColor: '#171614' },
  { text: 'Savindu', color: '#fd6d05', textColor: '#100C0B' },
];

export default function BouncyButtons() {
  const containerRef = useRef(null);
  const boxRef = useRef(null);
  const buttonRefs = useRef([]);
  const headingRef = useRef(null);

  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState('');
  const mouseDownIndex = useRef(null);
  const mouseDownTime = useRef(null);

  useEffect(() => {
    const { Engine, Runner, Bodies, World, Mouse, MouseConstraint } = Matter;
    const engine = Engine.create();
    const world = engine.world;
    engine.gravity.y = 1.2; // stronger gravity to make buttons settle tightly

    const box = boxRef.current;
    if (!box) return;

    const width = box.clientWidth;
    const height = box.clientHeight;

    const walls = [
      Bodies.rectangle(width / 2, -5, width, 10, { isStatic: true }), // top
      Bodies.rectangle(width / 2, height + 5, width, 100, { isStatic: true }), // bottom
      Bodies.rectangle(-5, height / 2, 10, height, { isStatic: true }), // left
      Bodies.rectangle(width + 5, height / 2, 10, height, { isStatic: true }), // right
    ];
    World.add(world, walls);

    const buttonWidth = 360;
    const buttonHeight = 120;
    const buttonBodies = buttonRefs.current.map((ref, i) => {
      const body = Bodies.rectangle(
        Math.random() * (width - buttonWidth),
        Math.random() * (height - buttonHeight),
        buttonWidth,
        buttonHeight,
        {
          restitution: 0, // no bounce
          friction: 1,
          frictionStatic: 1,
          density: 0.002, // slight increase to help compression
          angle: Math.random() * 0.1,
        }
      );
      World.add(world, body);
      return body;
    });

    const mouse = Mouse.create(box);
    const mouseConstraint = MouseConstraint.create(engine, {
      mouse,
      constraint: {
        stiffness: 0.2,
        render: { visible: false },
      },
    });

    World.add(world, mouseConstraint);

    const update = () => {
      buttonRefs.current.forEach((ref, i) => {
        if (!ref) return;
        const { x, y } = buttonBodies[i].position;
        const angle = buttonBodies[i].angle;
        ref.style.left = `${x - buttonWidth / 2}px`;
        ref.style.top = `${y - buttonHeight / 2}px`;
        ref.style.transform = `rotate(${angle}rad)`;
      });
      requestAnimationFrame(update);
    };
    update();

    const runner = Runner.create();
    Runner.run(runner, engine);

    const updateClock = () => {
      const now = new Date();
      const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const clockElement = document.getElementById('clock');
      if (clockElement) {
        clockElement.textContent = timeString;
      }
    };

    updateClock();
    const intervalId = setInterval(updateClock, 1000);

    return () => {
      Matter.World.clear(world);
      Matter.Engine.clear(engine);
      clearInterval(intervalId);
    };
  }, []);

  const handleMouseDown = (index) => {
    mouseDownIndex.current = index;
    mouseDownTime.current = Date.now();
  };

  const handleMouseUp = (index) => {
    const clickDuration = Date.now() - mouseDownTime.current;
    if (mouseDownIndex.current === index && clickDuration < 150) {
      setPopupMessage(`${buttonsData[index].text}, do better`);
      setShowPopup(true);
    }
    mouseDownIndex.current = null;
    mouseDownTime.current = null;
  };

  return (
    <div
      className="w-full h-screen flex items-center justify-center p-6"
      ref={containerRef}
      style={{ backgroundColor: '#171614' }}
    >
      {showPopup && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70 z-50">
          <div className="bg-white p-10 rounded-2xl shadow-lg text-center">
            <h2 className="text-4xl font-bold text-black mb-6">{popupMessage}</h2>
            <button
              onClick={() => setShowPopup(false)}
              className="mt-4 px-6 py-3 bg-orange-500 text-white rounded-xl text-lg"
            >
              Close
            </button>
          </div>
        </div>
      )}

      <div
        className="relative w-[1200px] h-[600px] mx-auto rounded-2xl shadow-2xl px-8 py-10 overflow-hidden"
        ref={boxRef}
        style={{ border: '2px solid white', position: 'relative' }}
      >
        <div className="flex justify-between w-full text-lg font-medium mb-4 white">
          <span>Melbourne, Australia</span>
          <span id="clock">--:--</span>
        </div>

        <h1
          ref={headingRef}
          className="text-4xl font-bold text-center mb-10 white"
        >
          Our amazing <span style={{ color: '#F77E0D', textDecoration: 'underline' }}>TEAM!</span>
        </h1>

        {buttonsData.map((btn, index) => (
          <div
            key={index}
            ref={(el) => (buttonRefs.current[index] = el)}
            onMouseDown={() => handleMouseDown(index)}
            onMouseUp={() => handleMouseUp(index)}
            className="cursor-pointer px-5 py-9 text-6xl rounded-full shadow-xl font-medium absolute select-none flex items-center justify-center"
            style={{
              backgroundColor: btn.color,
              color: btn.textColor,
              minWidth: '360px',
              maxHeight: '120px',
              border: '1px solid #171614',
              position: 'absolute',
             
              left: '0px',
              top: '0px',
              transform: 'rotate(0deg)',
              transformOrigin: 'center',
            }}
          >
            {btn.text}
          </div>
        ))}
      </div>
    </div>
  );
}
