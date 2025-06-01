import { useEffect, useState } from "react";

export default function GlowyBackground() {
  const [mousePos, setMousePos] = useState({ x: -9999, y: -9999 }); // Hide off-screen initially

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
}
