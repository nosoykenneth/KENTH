import React from 'react';
import logoMain from '../../assets/logo-main.png';
import logoMainBlack from '../../assets/logo-main-black.png';

export default function Logo({ className = "h-8 md:h-12" }) {
  return (
    <div className={`kenth-logo-container ${className}`}>
      <img 
        src={logoMain} 
        alt="KENTH Logo" 
        className="h-full w-auto object-contain kenth-logo-dark" 
      />
      <img 
        src={logoMainBlack} 
        alt="KENTH Logo" 
        className="h-full w-auto object-contain kenth-logo-light" 
      />
    </div>
  );
}
