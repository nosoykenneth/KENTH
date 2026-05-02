import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Logo from '../ui/Logo';
import ThemeToggle from '../ui/ThemeToggle';
import UserMenu from './UserMenu';

export default function Navbar() {
  const location = useLocation();
  const token = localStorage.getItem('moodle_token');
  
  const navLinks = [
    { name: 'Inicio', path: '/' },
    { name: 'Cursos', path: '/courses' },
    { name: 'Precios', path: '/pricing' },
  ];

  return (
    <header className="fixed top-0 w-full z-50 flex justify-between items-center p-4 md:p-6 bg-kenth-bg/80 backdrop-blur-md border-b border-kenth-border transition-all duration-500">
      <Link to="/" className="flex items-center">
        <Logo className="h-8 md:h-12" />
      </Link>
      
      <nav className="flex gap-4 md:gap-8 font-bold items-center text-[10px] md:text-sm uppercase tracking-widest">
        {navLinks.map((link) => (
          <Link 
            key={link.path}
            to={link.path} 
            className={`transition-colors hover:text-kenth-brightred ${location.pathname === link.path ? 'text-kenth-brightred' : 'text-kenth-subtext'}`}
          >
            {link.name}
          </Link>
        ))}
        
        <div className="h-4 w-px bg-kenth-border mx-2 hidden md:block"></div>
        
        <ThemeToggle />
        
        {token ? (
          <div className="flex items-center gap-4">
            <UserMenu />
            <Link to="/dashboard" className="bg-kenth-text text-kenth-bg px-5 py-2 md:px-6 md:py-2.5 rounded-full transition shadow-lg hover:bg-kenth-brightred hover:text-white font-black italic tracking-tighter">
              Mi Estudio
            </Link>
          </div>
        ) : (
          <Link to="/login" className="bg-kenth-brightred text-white px-5 py-2 md:px-6 md:py-2.5 rounded-full transition shadow-lg shadow-kenth-brightred/20 hover:bg-white hover:text-kenth-bg font-black italic tracking-tighter">
            Acceder
          </Link>
        )}
      </nav>
    </header>
  );
}
