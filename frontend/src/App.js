import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Home, 
  Dumbbell, 
  Sparkles, 
  Apple, 
  Heart, 
  ShoppingCart,
  Menu,
  X,
  Play,
  Clock,
  Star,
  User,
  MessageCircle,
  Brain,
  Zap
} from 'lucide-react';
import CircularGallery from './CircularGallery';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Custom Zen Symbol Icon Component
const ZenIcon = ({ size = 18, className = "" }) => (
  <svg 
    width={size} 
    height={size} 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round"
    className={className}
  >
    <circle cx="12" cy="12" r="10"/>
    <path d="M12 2a10 10 0 0 0 0 20"/>
    <circle cx="12" cy="12" r="3"/>
  </svg>
);

// Video Background Component
const VideoBackground = ({ videoSrc, overlay = 'bg-black/40', className = '' }) => (
  <div className={`absolute inset-0 ${className}`}>
    <video
      autoPlay
      loop
      muted
      playsInline
      className="absolute inset-0 w-full h-full object-cover"
      style={{ filter: 'brightness(0.7)' }}
    >
      <source src={videoSrc} type="video/mp4" />
    </video>
    <div className={`absolute inset-0 ${overlay}`} />
  </div>
);

// Background images from vision expert
const backgrounds = {
  home: 'https://images.pexels.com/photos/1051838/pexels-photo-1051838.jpeg',
  workout: 'https://images.pexels.com/photos/289586/pexels-photo-289586.jpeg',
  skincare: 'https://images.unsplash.com/photo-1528715471579-d1bcf0ba5e83',
  diet: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773',
  health: 'https://images.unsplash.com/photo-1718086436850-ac77db40dadb',
  orderup: 'https://images.pexels.com/photos/668353/pexels-photo-668353.jpeg'
};

// Profile Popup Component
const ProfilePopup = ({ user, isOpen, onClose }) => {
  if (!isOpen || !user) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed top-0 left-0 w-full h-full z-[9999] p-4"
        style={{ 
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          height: '100vh'
        }}
      >
        {/* Enhanced Backdrop */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute top-0 left-0 w-full h-full bg-black/60 backdrop-blur-md" 
          onClick={onClose}
        />
        
        {/* Profile Modal */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.8, opacity: 0, y: 20 }}
          transition={{ 
            type: "spring", 
            stiffness: 300, 
            damping: 25 
          }}
          className="relative bg-white/15 backdrop-blur-xl rounded-3xl p-8 border border-white/30 shadow-2xl max-w-lg w-full max-h-[85vh] overflow-y-auto"
          style={{
            background: 'linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1)'
          }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Enhanced Close Button */}
          <button
            onClick={onClose}
            className="absolute top-6 right-6 p-3 rounded-full bg-white/20 hover:bg-white/30 transition-all duration-200 backdrop-blur-sm border border-white/20 hover:border-white/40 group"
          >
            <X size={20} className="text-white group-hover:text-white/80 transition-colors" />
          </button>

        {/* Enhanced Profile Header */}
        <div className="text-center mb-8 pt-4">
          <div className="w-24 h-24 bg-gradient-to-br from-amber-400 via-orange-500 to-red-500 rounded-full flex items-center justify-center mx-auto mb-5 shadow-lg ring-4 ring-white/20">
            <User size={36} className="text-white" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">{user.name}</h2>
          <p className="text-white/80 text-lg">{user.email}</p>
        </div>

        {/* Enhanced Profile Details */}
        <div className="space-y-5">
          {/* Basic Info */}
          <div className="bg-white/8 rounded-xl p-5 border border-white/10 backdrop-blur-sm">
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <div className="w-2 h-2 bg-amber-400 rounded-full mr-3"></div>
              Basic Information
            </h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Age</span>
                <p className="text-white font-semibold text-lg">{user.age}</p>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Gender</span>
                <p className="text-white font-semibold text-lg">{user.gender}</p>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Height</span>
                <p className="text-white font-semibold text-lg">{user.height} {user.height_unit || 'cm'}</p>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Weight</span>
                <p className="text-white font-semibold text-lg">{user.weight} {user.weight_unit || 'kg'}</p>
              </div>
            </div>
          </div>

          {/* Wellness Goals */}
          {user.goals && user.goals.length > 0 && (
            <div className="bg-white/8 rounded-xl p-5 border border-white/10 backdrop-blur-sm">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
                Wellness Goals
              </h3>
              <div className="flex flex-wrap gap-3">
                {user.goals.map((goal, index) => (
                  <span key={index} className="px-4 py-2 bg-gradient-to-r from-amber-400/20 to-orange-400/20 text-amber-200 rounded-full text-sm font-medium border border-amber-400/30 backdrop-blur-sm">
                    {goal}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Health Information */}
          <div className="bg-white/8 rounded-xl p-5 border border-white/10 backdrop-blur-sm">
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              Health & Preferences
            </h3>
            <div className="grid grid-cols-1 gap-3 text-sm">
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Fitness Level</span>
                <p className="text-white font-semibold text-lg">{user.fitness_level || 'Not specified'}</p>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Diet Type</span>
                <p className="text-white font-semibold text-lg">{user.diet_type || 'Not specified'}</p>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <span className="text-white/60 text-xs uppercase tracking-wide">Skin Type</span>
                <p className="text-white font-semibold text-lg">{user.skin_type || 'Not specified'}</p>
              </div>
            </div>
          </div>

          {/* Allergies */}
          {user.allergies && user.allergies.length > 0 && (
            <div className="bg-white/8 rounded-xl p-5 border border-white/10 backdrop-blur-sm">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                <div className="w-2 h-2 bg-red-400 rounded-full mr-3"></div>
                Allergies
              </h3>
              <div className="flex flex-wrap gap-3">
                {user.allergies.map((allergy, index) => (
                  <span key={index} className="px-4 py-2 bg-gradient-to-r from-red-400/20 to-pink-400/20 text-red-200 rounded-full text-sm font-medium border border-red-400/30 backdrop-blur-sm">
                    {allergy}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Medical Conditions */}
          {user.chronic_conditions && user.chronic_conditions.length > 0 && (
            <div className="bg-white/8 rounded-xl p-5 border border-white/10 backdrop-blur-sm">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                Medical Conditions
              </h3>
              <div className="flex flex-wrap gap-3">
                {user.chronic_conditions.map((condition, index) => (
                  <span key={index} className="px-4 py-2 bg-gradient-to-r from-purple-400/20 to-blue-400/20 text-purple-200 rounded-full text-sm font-medium border border-purple-400/30 backdrop-blur-sm">
                    {condition}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
    </AnimatePresence>
  );
};

// Header Component
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [showProfilePopup, setShowProfilePopup] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const location = useLocation();

  // Check if user is logged in on component mount and location change
  useEffect(() => {
    const checkUserStatus = () => {
      const user = localStorage.getItem('user');
      const userId = localStorage.getItem('userId');
      
      if (user && userId) {
        setIsLoggedIn(true);
        setCurrentUser(JSON.parse(user));
      } else {
        setIsLoggedIn(false);
        setCurrentUser(null);
      }
    };

    checkUserStatus();
  }, [location]);

  // Close user menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showUserMenu && !event.target.closest('.user-menu-container')) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showUserMenu]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('userId');
    setIsLoggedIn(false);
    setCurrentUser(null);
    setShowUserMenu(false);
    // Dispatch custom event for AuthRoute components
    window.dispatchEvent(new Event('authChange'));
    // Optionally redirect to home page
    window.location.href = '/';
  };

  const navItems = [
    { path: '/', label: 'Home', icon: Home, iconClass: 'header-home-icon' },
    { path: '/workout', label: 'Workout', icon: Dumbbell, iconClass: 'header-workout-icon' },
    { path: '/mind-soul', label: 'Mind & Soul', icon: ZenIcon, iconClass: 'header-mindsoul-icon' },
    { path: '/skincare', label: 'Skincare', icon: Sparkles, iconClass: 'header-skincare-icon' },
    { path: '/diet', label: 'Diet', icon: Apple, iconClass: 'header-diet-icon' },
    { path: '/health', label: 'Health', icon: Heart, iconClass: 'header-health-icon' },
    { path: '/order-up', label: 'Order Up', icon: ShoppingCart, iconClass: 'header-orderup-icon' }
  ];

  return (
    <motion.header 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed top-0 w-full z-50 bg-white/10 backdrop-blur-md border-b border-white/20"
    >
      <div className="max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="flex flex-col">
              <div className="text-3xl font-bold bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent font-['Cinzel_Decorative'] hover:from-yellow-300 hover:via-amber-400 hover:to-orange-600 transition-all duration-500 hover:drop-shadow-[0_0_10px_rgba(251,191,36,0.8)] hover:scale-105 cursor-pointer">
                Nutracía
              </div>
              <div className="text-xs text-white/70 font-light font-['Pacifico'] -mt-1 ml-1">
                Redefine Your Limits
              </div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                    isActive 
                      ? 'bg-white/20 text-white' 
                      : 'text-white/80 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <Icon size={18} className={item.iconClass} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Get Started Button & User Menu & Mobile Menu Button */}
          <div className="flex items-center space-x-3">
            {/* Conditional rendering: Get Started Button or User Menu - Desktop */}
            {!isLoggedIn ? (
              <Link
                to="/get-started"
                className="hidden md:block px-6 py-2 get-started-button text-white font-semibold rounded-full transform transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Get Started
              </Link>
            ) : (
              <div className="hidden md:block relative user-menu-container">
                {/* User Menu Button */}
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center space-x-2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full border border-white/20 hover:bg-white/20 transition-all duration-300"
                >
                  <div className="w-8 h-8 bg-gradient-to-r from-amber-400 to-orange-500 rounded-full flex items-center justify-center">
                    <User size={16} className="text-white" />
                  </div>
                  <span className="text-white font-medium">{currentUser?.name?.split(' ')[0] || 'User'}</span>
                  <motion.div
                    animate={{ rotate: showUserMenu ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="text-white">
                      <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </motion.div>
                </button>

                {/* User Dropdown Menu */}
                <AnimatePresence>
                  {showUserMenu && (
                    <motion.div
                      initial={{ opacity: 0, y: -10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -10, scale: 0.95 }}
                      className="absolute right-0 mt-2 w-48 bg-white/10 backdrop-blur-md rounded-xl border border-white/20 shadow-xl z-50"
                    >
                      <div className="py-1">
                        <button
                          onClick={() => {
                            setShowProfilePopup(true);
                            setShowUserMenu(false);
                          }}
                          className="w-full text-left px-4 py-3 text-white hover:bg-white/10 transition-all duration-200 flex items-center space-x-3"
                        >
                          <User size={16} />
                          <span>Profile</span>
                        </button>
                        <button
                          onClick={handleLogout}
                          className="w-full text-left px-4 py-3 text-white hover:bg-white/10 transition-all duration-200 flex items-center space-x-3"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                            <polyline points="16,17 21,12 16,7"/>
                            <line x1="21" y1="12" x2="9" y2="12"/>
                          </svg>
                          <span>Logout</span>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 rounded-lg bg-white/10 text-white"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white/10 backdrop-blur-md border-t border-white/20"
          >
            <div className="px-4 py-4 space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setIsMenuOpen(false)}
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-all"
                  >
                    <Icon size={20} className={item.iconClass} />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
              
              {/* Conditional rendering: Get Started Button or User Menu - Mobile */}
              {!isLoggedIn ? (
                <Link
                  to="/get-started"
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center justify-center mx-2 mt-4 px-6 py-3 get-started-button text-white font-semibold rounded-full transition-all duration-300 shadow-lg"
                >
                  Get Started
                </Link>
              ) : (
                <div className="mx-2 mt-4 space-y-2">
                  <div className="flex items-center space-x-3 px-4 py-3 bg-white/10 rounded-lg">
                    <div className="w-8 h-8 bg-gradient-to-r from-amber-400 to-orange-500 rounded-full flex items-center justify-center">
                      <User size={16} className="text-white" />
                    </div>
                    <span className="text-white font-medium">{currentUser?.name || 'User'}</span>
                  </div>
                  <button
                    onClick={() => {
                      setShowProfilePopup(true);
                      setIsMenuOpen(false);
                    }}
                    className="w-full flex items-center space-x-3 px-4 py-3 text-white hover:bg-white/10 rounded-lg transition-all"
                  >
                    <User size={20} />
                    <span>Profile</span>
                  </button>
                  <button
                    onClick={() => {
                      handleLogout();
                      setIsMenuOpen(false);
                    }}
                    className="w-full flex items-center space-x-3 px-4 py-3 text-white hover:bg-white/10 rounded-lg transition-all"
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                      <polyline points="16,17 21,12 16,7"/>
                      <line x1="21" y1="12" x2="9" y2="12"/>
                    </svg>
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Profile Popup */}
      <ProfilePopup 
        user={currentUser} 
        isOpen={showProfilePopup} 
        onClose={() => setShowProfilePopup(false)} 
      />
    </motion.header>
  );
};

// Enhanced AI Health Chatbot Component
const EnhancedAIChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState('chat'); // 'chat', 'profile'
  const [userProfile, setUserProfile] = useState({
    weight: '',
    allergies: '',
    skin_concern: ''
  });

  // Predefined options for smart input
  const weightOptions = [
    '45-50kg', '50-55kg', '55-60kg', '60-65kg', '65-70kg', '70-75kg', 
    '75-80kg', '80-85kg', '85-90kg', '90-95kg', '95-100kg', '100kg+'
  ];

  const skinConcernOptions = [
    'Acne', 'Dry Skin', 'Oily Skin', 'Anti-aging', 'Tanning', 'Sensitive Skin',
    'Dark Spots', 'Wrinkles', 'Blackheads', 'Dull Skin', 'General Care'
  ];

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        user_id: 'demo-user',
        message: userMessage,
        user_profile: userProfile.weight ? userProfile : null
      });
      
      const botResponse = response.data;
      
      if (botResponse.requires_profile) {
        setMessages(prev => [...prev, { type: 'ai', content: botResponse.response }]);
        setCurrentStep('profile');
      } else {
        setMessages(prev => [...prev, { type: 'ai', content: botResponse.response }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        type: 'ai', 
        content: 'Sorry, I had trouble processing your message. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const submitProfile = () => {
    if (!userProfile.weight || !userProfile.allergies || !userProfile.skin_concern) {
      alert('Please fill in all fields to get personalized recommendations.');
      return;
    }

    setMessages(prev => [...prev, { 
      type: 'system', 
      content: `Profile updated! Weight: ${userProfile.weight}, Allergies: ${userProfile.allergies}, Skin Concern: ${userProfile.skin_concern}` 
    }]);
    
    setCurrentStep('chat');
    
    // Auto-send a follow-up message for recommendations
    setTimeout(() => {
      setMessages(prev => [...prev, { type: 'user', content: 'Now please give me personalized health recommendations' }]);
      setIsLoading(true);
      
      axios.post(`${API}/chat`, {
        user_id: 'demo-user',
        message: 'Now please give me personalized health recommendations based on my profile',
        user_profile: userProfile
      }).then(response => {
        setMessages(prev => [...prev, { type: 'ai', content: response.data.response }]);
      }).catch(() => {
        setMessages(prev => [...prev, { 
          type: 'ai', 
          content: 'I can help you with personalized workout plans, skincare routines, and diet recommendations!' 
        }]);
      }).finally(() => {
        setIsLoading(false);
      });
    }, 1000);
  };

  const quickQuestions = [
    "💪 Show me a workout plan",
    "✨ Skincare routine for my skin type", 
    "🥗 Healthy diet recommendations",
    "🏃‍♂️ How to start exercising?",
    "🧴 Best products for acne",
    "🍎 Foods to avoid for allergies"
  ];

  return (
    <>
      {/* Footer Chatbot Toggle Button */}
      <div className="fixed bottom-0 right-6 z-50">
        <motion.button
          whileHover={{ 
            scale: 1.1, 
            boxShadow: '0 0 30px rgba(168, 85, 247, 0.6)',
            backgroundColor: 'rgba(168, 85, 247, 0.9)'
          }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsOpen(!isOpen)}
          className="mb-4 w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full shadow-lg flex items-center justify-center text-white hover:from-purple-600 hover:to-pink-600 transition-all duration-300"
          style={{
            background: isOpen ? 'linear-gradient(135deg, #7c3aed, #ec4899)' : 'linear-gradient(135deg, #8b5cf6, #f472b6)'
          }}
        >
          <motion.div
            animate={{ rotate: isOpen ? 180 : 0 }}
            transition={{ duration: 0.3 }}
          >
            <MessageCircle size={24} />
          </motion.div>
        </motion.button>

        {/* Chat Window */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.8 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 50, scale: 0.8 }}
              className="absolute bottom-20 right-0 w-96 h-[500px] bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-xl overflow-hidden"
            >
              {/* Chat Header */}
              <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4 text-white">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">🏃‍♂️ Nutracía Health Coach</h3>
                    <p className="text-sm opacity-90">Your AI wellness companion</p>
                  </div>
                  <button
                    onClick={() => setIsOpen(false)}
                    className="p-1 rounded-full hover:bg-white/20 transition-colors"
                  >
                    <X size={20} />
                  </button>
                </div>
              </div>

              {currentStep === 'chat' && (
                <>
                  {/* Messages */}
                  <div className="h-80 overflow-y-auto p-4 space-y-3">
                    {messages.length === 0 && (
                      <div className="text-white/70 text-sm space-y-3">
                        <div className="bg-purple-500/20 p-3 rounded-lg">
                          Hi! I'm your AI Health Coach! 🤖✨
                        </div>
                        <div className="text-xs text-white/60">
                          I can help with workouts, skincare, nutrition, and wellness advice!
                        </div>
                        
                        {/* Quick Questions */}
                        <div className="space-y-2">
                          <div className="text-xs font-semibold text-white/80">Quick Questions:</div>
                          {quickQuestions.map((question, idx) => (
                            <button
                              key={idx}
                              onClick={() => setInput(question)}
                              className="block w-full text-left text-xs bg-white/10 hover:bg-white/20 p-2 rounded-lg transition-colors"
                            >
                              {question}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {messages.map((msg, idx) => (
                      <div key={idx} className={`${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                        <div className={`inline-block p-3 rounded-lg max-w-xs text-sm ${
                          msg.type === 'user' 
                            ? 'bg-purple-500 text-white' 
                            : msg.type === 'system'
                            ? 'bg-green-500/20 text-green-200 backdrop-blur-sm'
                            : 'bg-white/20 text-white backdrop-blur-sm'
                        }`}>
                          <p>{msg.content}</p>
                        </div>
                      </div>
                    ))}
                    
                    {isLoading && (
                      <div className="text-left">
                        <div className="inline-block p-3 rounded-lg bg-white/20 text-white">
                          <div className="flex items-center space-x-2">
                            <div className="flex space-x-1">
                              <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                            </div>
                            <span className="text-xs">AI is thinking...</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Input */}
                  <div className="p-4 border-t border-white/20">
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Ask about workouts, diet, skincare..."
                        className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                      />
                      <button
                        onClick={sendMessage}
                        disabled={!input.trim() || isLoading}
                        className="px-4 py-2 bg-purple-500 text-white rounded-lg disabled:opacity-50 hover:bg-purple-600 transition-colors text-sm"
                      >
                        Send
                      </button>
                    </div>
                  </div>
                </>
              )}

              {currentStep === 'profile' && (
                <div className="p-4 space-y-4">
                  <div className="text-center text-white mb-4">
                    <h3 className="font-semibold">📋 Your Health Profile</h3>
                    <p className="text-sm text-white/80">Help me personalize your recommendations</p>
                  </div>

                  <div className="space-y-3">
                    {/* Weight Selection */}
                    <div>
                      <label className="block text-sm font-medium text-white/90 mb-1">
                        Weight Range
                      </label>
                      <select
                        value={userProfile.weight}
                        onChange={(e) => setUserProfile(prev => ({...prev, weight: e.target.value}))}
                        className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                      >
                        <option value="" className="bg-gray-800">Select your weight range</option>
                        {weightOptions.map(weight => (
                          <option key={weight} value={weight} className="bg-gray-800">{weight}</option>
                        ))}
                      </select>
                    </div>

                    {/* Allergies Input */}
                    <div>
                      <label className="block text-sm font-medium text-white/90 mb-1">
                        Allergies
                      </label>
                      <input
                        type="text"
                        value={userProfile.allergies}
                        onChange={(e) => setUserProfile(prev => ({...prev, allergies: e.target.value}))}
                        placeholder="e.g., nuts, dairy, shellfish or 'none'"
                        className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                      />
                    </div>

                    {/* Skin Concern Selection */}
                    <div>
                      <label className="block text-sm font-medium text-white/90 mb-1">
                        Main Skin Concern
                      </label>
                      <select
                        value={userProfile.skin_concern}
                        onChange={(e) => setUserProfile(prev => ({...prev, skin_concern: e.target.value}))}
                        className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                      >
                        <option value="" className="bg-gray-800">Select your main concern</option>
                        {skinConcernOptions.map(concern => (
                          <option key={concern} value={concern} className="bg-gray-800">{concern}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="flex space-x-2 mt-4">
                    <button
                      onClick={() => setCurrentStep('chat')}
                      className="flex-1 bg-white/20 text-white py-2 px-3 rounded-lg text-sm hover:bg-white/30 transition-colors"
                    >
                      Back
                    </button>
                    <button
                      onClick={submitProfile}
                      className="flex-1 bg-green-600 text-white py-2 px-3 rounded-lg text-sm hover:bg-green-700 transition-colors"
                    >
                      Save Profile
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
};

// Quote Header Component
const QuoteHeader = ({ quote, background }) => (
  <div className="relative h-32 overflow-hidden rounded-2xl mb-8">
    <div 
      className="absolute inset-0 bg-cover bg-center"
      style={{ backgroundImage: `url(${background})` }}
    />
    <div className="absolute inset-0 bg-black/50" />
    <div className="relative h-full flex items-center justify-center">
      <h2 className="text-3xl md:text-4xl font-['Great_Vibes'] text-white text-center px-6">
        "{quote}"
      </h2>
    </div>
  </div>
);

// Enhanced Modal Component with YouTube Embeds
const Modal = ({ isOpen, onClose, item, type }) => {
  if (!isOpen || !item) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
        onClick={handleBackdropClick}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white/10 backdrop-blur-md rounded-3xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-white/20 relative"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Close Button */}
          <button 
            onClick={onClose}
            className="absolute top-4 right-4 p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors z-10"
          >
            <X size={20} />
          </button>

          {/* Header Section */}
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-white mb-2">{item.title}</h2>
            <p className="text-white/80 text-lg">{item.description}</p>
          </div>

          {type === 'workout' && (
            <div className="space-y-6">
              {/* YouTube Video Embed */}
              {item.videoUrl && (
                <div className="bg-white/5 rounded-2xl p-4">
                  <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
                    <Play size={20} />
                    <span>Tutorial Video</span>
                  </h3>
                  <div className="relative w-full pb-[56.25%] h-0 rounded-lg overflow-hidden">
                    <iframe
                      className="absolute top-0 left-0 w-full h-full"
                      src={item.videoUrl}
                      title={`${item.title} Tutorial`}
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    ></iframe>
                  </div>
                </div>
              )}

              {/* Duration and Level */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <Clock size={20} className="text-blue-400" />
                    <div>
                      <div className="text-lg font-bold">{item.duration}</div>
                      <div className="text-sm text-white/70">Duration</div>
                    </div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <Star size={20} className="text-amber-400" />
                    <div>
                      <div className="text-lg font-bold capitalize">{item.level}</div>
                      <div className="text-sm text-white/70">Level</div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Requirements Section */}
              {item.requirements && item.requirements.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <span className="text-orange-400">🎯</span>
                    <span>Requirements</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {item.requirements.map((req, idx) => (
                      <span key={idx} className="bg-orange-500/20 text-orange-200 px-3 py-1 rounded-full text-sm">
                        {req}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Muscle Groups */}
              {item.muscle_groups && item.muscle_groups.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <span className="text-red-400">💪</span>
                    <span>Target Muscles</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {item.muscle_groups.map((muscle, idx) => (
                      <span key={idx} className="bg-red-500/20 text-red-200 px-3 py-1 rounded-full text-sm">
                        {muscle}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Step-by-Step Instructions */}
              {item.steps && item.steps.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-4 flex items-center space-x-2">
                    <span className="text-green-400">✓</span>
                    <span>Step-by-Step Instructions</span>
                  </h4>
                  <ol className="space-y-3">
                    {item.steps.map((step, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full text-sm flex items-center justify-center font-bold">
                          {idx + 1}
                        </span>
                        <span className="text-white/90 leading-relaxed">{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}

              {/* Requirements Section */}
              {item.requirements && item.requirements.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <span className="text-orange-400">🎯</span>
                    <span>Required Products</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {item.requirements.map((req, idx) => (
                      <span key={idx} className="bg-orange-500/20 text-orange-200 px-3 py-1 rounded-full text-sm">
                        {req}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Button */}
              <div className="flex justify-center pt-4">
                <button 
                  onClick={onClose}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-3 rounded-full font-semibold hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 flex items-center space-x-2"
                >
                  <span>✨</span>
                  <span>Start This Workout</span>
                </button>
              </div>
            </div>
          )}

          {/* Keep original modal content for other types (skincare, diet, health) */}
          {type === 'skincare' && (
            <div className="space-y-6">
              {/* YouTube Video Embed */}
              {item.video && (
                <div className="bg-white/5 rounded-2xl p-4">
                  <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
                    <Play size={20} />
                    <span>Skincare Tutorial</span>
                  </h3>
                  <div className="relative w-full pb-[56.25%] h-0 rounded-lg overflow-hidden">
                    <iframe
                      className="absolute top-0 left-0 w-full h-full"
                      src={item.video}
                      title={`${item.title} Tutorial`}
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    ></iframe>
                  </div>
                </div>
              )}

              {/* Skin Type, Time and Level */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <span className="text-pink-400 text-lg">✨</span>
                    <div>
                      <div className="text-lg font-bold">{item.skinType}</div>
                      <div className="text-sm text-white/70">Skin Type</div>
                    </div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <Clock size={20} className="text-blue-400" />
                    <div>
                      <div className="text-lg font-bold">{item.time}</div>
                      <div className="text-sm text-white/70">Timing</div>
                    </div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <Star size={20} className="text-amber-400" />
                    <div>
                      <div className="text-lg font-bold capitalize">{item.level}</div>
                      <div className="text-sm text-white/70">Level</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Step-by-Step Instructions */}
              {item.steps && item.steps.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-4 flex items-center space-x-2">
                    <span className="text-pink-400">🧴</span>
                    <span>Skincare Steps</span>
                  </h4>
                  <ul className="space-y-3">
                    {item.steps.map((step, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-pink-500 text-white rounded-full text-sm flex items-center justify-center font-bold">
                          {idx + 1}
                        </span>
                        <span className="text-white/90 leading-relaxed">{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Action Button */}
              <div className="flex justify-center pt-4">
                <button 
                  onClick={onClose}
                  className="bg-gradient-to-r from-pink-500 to-purple-500 text-white px-8 py-3 rounded-full font-semibold hover:from-pink-600 hover:to-purple-600 transition-all transform hover:scale-105 flex items-center space-x-2"
                >
                  <span>✨</span>
                  <span>Start This Routine</span>
                </button>
              </div>
            </div>
          )}

          {type === 'diet' && (
            <div className="space-y-6">
              {/* YouTube Video Embed */}
              {item.videoUrl && (
                <div className="bg-white/5 rounded-2xl p-4">
                  <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
                    <Play size={20} />
                    <span>Diet Tutorial</span>
                  </h3>
                  <div className="relative w-full pb-[56.25%] h-0 rounded-lg overflow-hidden">
                    <iframe
                      className="absolute top-0 left-0 w-full h-full"
                      src={item.videoUrl}
                      title={`${item.title} Tutorial`}
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    ></iframe>
                  </div>
                </div>
              )}

              {/* Duration, Level and Calories */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <Clock size={20} className="text-blue-400" />
                    <div>
                      <div className="text-lg font-bold">{item.duration}</div>
                      <div className="text-sm text-white/70">Duration</div>
                    </div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <Star size={20} className="text-amber-400" />
                    <div>
                      <div className="text-lg font-bold capitalize">{item.level}</div>
                      <div className="text-sm text-white/70">Level</div>
                    </div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <div className="flex items-center space-x-3 text-white">
                    <span className="text-orange-400 text-lg">🔥</span>
                    <div>
                      <div className="text-lg font-bold">{item.calories}</div>
                      <div className="text-sm text-white/70">Daily Calories</div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Requirements Section */}
              {item.requirements && item.requirements.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <span className="text-orange-400">🥗</span>
                    <span>Key Foods & Requirements</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {item.requirements.map((req, idx) => (
                      <span key={idx} className="bg-orange-500/20 text-orange-200 px-3 py-1 rounded-full text-sm">
                        {req}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Meal Types */}
              {item.meal_types && item.meal_types.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <span className="text-green-400">🍽️</span>
                    <span>Diet Categories</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {item.meal_types.map((type, idx) => (
                      <span key={idx} className="bg-green-500/20 text-green-200 px-3 py-1 rounded-full text-sm">
                        {type}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Step-by-Step Instructions */}
              {item.steps && item.steps.length > 0 && (
                <div className="bg-white/10 rounded-xl p-4">
                  <h4 className="font-semibold text-white mb-4 flex items-center space-x-2">
                    <span className="text-green-400">✓</span>
                    <span>Diet Plan Steps</span>
                  </h4>
                  <ol className="space-y-3">
                    {item.steps.map((step, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full text-sm flex items-center justify-center font-bold">
                          {idx + 1}
                        </span>
                        <span className="text-white/90 leading-relaxed">{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}

              {/* Action Button */}
              <div className="flex justify-center pt-4">
                <button 
                  onClick={onClose}
                  className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-8 py-3 rounded-full font-semibold hover:from-green-600 hover:to-blue-600 transition-all transform hover:scale-105 flex items-center space-x-2"
                >
                  <span>🥗</span>
                  <span>Start This Diet Plan</span>
                </button>
              </div>
            </div>
          )}

          {type === 'health' && (
            <div className="space-y-4">
              {/* Duration and Level */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/10 rounded-lg p-4">
                  <div className="text-white">
                    <div className="text-lg font-bold">{item.duration || 'Daily'}</div>
                    <div className="text-sm text-white/80">Duration</div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-lg p-4">
                  <div className="text-white">
                    <div className="text-lg font-bold">{item.level || 'Personalized'}</div>
                    <div className="text-sm text-white/80">Level</div>
                  </div>
                </div>
              </div>

              {/* Requirements Section */}
              {item.requirements && (
                <div className="bg-white/10 rounded-lg p-4">
                  <h4 className="font-semibold text-white mb-2">Requirements:</h4>
                  <div className="flex flex-wrap gap-2">
                    {item.requirements.map((req, idx) => (
                      <span key={idx} className="bg-blue-500/20 text-blue-200 px-3 py-1 rounded-full text-sm">
                        {req}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Steps Section (Enhanced for AI content) */}
              {(item.steps || item.daily_routine) && (
                <div className="bg-white/10 rounded-lg p-4">
                  <h4 className="font-semibold text-white mb-2">
                    {item.steps ? 'Daily Steps:' : 'Daily Routine:'}
                  </h4>
                  <ol className="space-y-2">
                    {(item.steps || item.daily_routine)?.map((step, idx) => (
                      <li key={idx} className="text-white/80">
                        {item.steps ? `${idx + 1}. ${step}` : `• ${step}`}
                      </li>
                    ))}
                  </ol>
                </div>
              )}
              
              {/* Lifestyle Tips */}
              {item.lifestyle_tips && (
                <div className="bg-white/10 rounded-lg p-4">
                  <h4 className="font-semibold text-white mb-2">Lifestyle Tips:</h4>
                  <ul className="space-y-2">
                    {item.lifestyle_tips.map((tip, idx) => (
                      <li key={idx} className="text-white/80">• {tip}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Motivational Quote (New for AI content) */}
              {item.motivational_quote && (
                <div className="bg-gradient-to-r from-pink-500/20 to-purple-500/20 rounded-lg p-4 border border-pink-500/30">
                  <h4 className="font-semibold text-white mb-2 flex items-center space-x-2">
                    <span>💪</span>
                    <span>Motivation</span>
                  </h4>
                  <p className="text-white/90 font-medium italic text-center">
                    "{item.motivational_quote}"
                  </p>
                </div>
              )}

              {/* YouTube Video Section */}
              {item.youtube_video && (
                <div className="bg-white/10 rounded-lg p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <Play size={18} />
                    <span>Health Management Guide</span>
                  </h4>
                  <a
                    href={item.youtube_video}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block bg-red-600 hover:bg-red-700 text-white py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
                  >
                    <Play size={16} />
                    <span>Watch on YouTube</span>
                  </a>
                </div>
              )}

              {/* Product Links Section */}
              {item.product_links && item.product_links.length > 0 && (
                <div className="bg-white/10 rounded-lg p-4">
                  <h4 className="font-semibold text-white mb-3 flex items-center space-x-2">
                    <span>🏥</span>
                    <span>Health Products</span>
                  </h4>
                  <div className="space-y-2">
                    {item.product_links.map((link, idx) => (
                      <a
                        key={idx}
                        href={link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block bg-blue-600 hover:bg-blue-700 text-white py-2 px-3 rounded text-sm transition-colors"
                      >
                        {link.includes('amazon') ? '🛍️ Amazon' : '🛒 Flipkart'} - {link.split('q=')[1]?.replace(/\+/g, ' ') || 'Health Products'}
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

// New Circular Gallery Component using OGL
const CircularGalleryOGL = ({ items, onItemClick, type }) => {
  const [clickableItems, setClickableItems] = useState([]);
  
  useEffect(() => {
    if (items && items.length > 0) {
      setClickableItems(items);
    }
  }, [items]);

  if (!items || items.length === 0) {
    return (
      <div className="h-96 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading {type} content...</p>
        </div>
      </div>
    );
  }

  // Generate relevant images based on content type and title - MOVED BEFORE USAGE
  const generateRelevantImage = (type, title, index) => {
    const seed = title ? title.toLowerCase().replace(/\s+/g, '-') : `${type}-${index}`;
    switch (type) {
      case 'workout':
        return `https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop&crop=center&auto=format&q=80`;
      case 'skincare':
        return `https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=600&fit=crop&crop=center&auto=format&q=80`;
      case 'diet':
        return `https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800&h=600&fit=crop&crop=center&auto=format&q=80`;
      case 'health':
        return `https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop&crop=center&auto=format&q=80`;
      default:
        return `https://picsum.photos/seed/${seed}/800/600?grayscale`;
    }
  };

  // Transform items to match the expected format for the new component
  const transformedItems = items.map((item, index) => {
    // For AI-generated content, use provided image_url or generate appropriate placeholder
    let imageUrl;
    if (item.image_url) {
      // Use AI-provided image or generate based on type
      imageUrl = item.image_url.includes('http') ? item.image_url : 
                 generateRelevantImage(type, item.title, index);
    } else {
      imageUrl = generateRelevantImage(type, item.title, index);
    }
    
    return {
      image: imageUrl,
      text: item.title || item.name || 'Item',
      originalItem: item  // Keep reference to original item data
    };
  });

  // Handle click on circular gallery items
  const handleItemClick = (transformedItem) => {
    const originalItem = transformedItem.originalItem || transformedItem;
    if (onItemClick && originalItem) {
      onItemClick(originalItem);
    }
  };

  // Try to use WebGL gallery, fallback to grid if needed
  try {
    return (
      <div style={{ height: '100%', position: 'relative' }}>
        <div 
          id="circular-gallery-container"
          style={{ height: '100%', cursor: 'pointer' }}
          onClick={(e) => {
            // Handle clicks on the circular gallery
            const clickX = e.clientX;
            const containerWidth = e.currentTarget.offsetWidth;
            const centerX = containerWidth / 2;
            const itemWidth = containerWidth / Math.min(transformedItems.length, 7);
            const clickedIndex = Math.floor((clickX - centerX + (itemWidth * transformedItems.length / 2)) / itemWidth);
            const safeIndex = Math.max(0, Math.min(clickedIndex, transformedItems.length - 1));
            
            if (transformedItems[safeIndex]) {
              handleItemClick(transformedItems[safeIndex]);
            }
          }}
        >
          <CircularGallery 
            items={transformedItems}
            bend={3} 
            textColor="#ffffff" 
            borderRadius={0.05} 
          />
        </div>
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
          <p className="text-white/70 text-sm text-center bg-black/50 px-4 py-2 rounded-full">
            Click any item to view details
          </p>
        </div>
      </div>
    );
  } catch (error) {
    console.error("Error rendering WebGL gallery, falling back to grid view:", error);
    // Enhanced fallback grid view
    return (
      <div className="h-full overflow-y-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-h-full">
          {clickableItems.map((item, index) => (
            <motion.div
              key={item.id || index}
              whileHover={{ scale: 1.05, rotateY: 5 }}
              whileTap={{ scale: 0.95 }}
              className="bg-white/10 backdrop-blur-md rounded-2xl p-3 border border-white/20 cursor-pointer card-hover h-fit"
              onClick={() => onItemClick(item)}
            >
              <div 
                className="h-20 bg-cover bg-center rounded-lg mb-2 border-2 border-white/20"
                style={{ 
                  backgroundImage: `url(${item.image_url || generateRelevantImage(type, item.title, index)})` 
                }}
              />
              <h4 className="text-white font-semibold text-xs mb-1 line-clamp-2">{item.title}</h4>
              <p className="text-white/70 text-xs line-clamp-2">{item.description}</p>
              {item.level && (
                <p className="text-amber-300 text-xs mt-1">Level: {item.level}</p>
              )}
              {item.duration && (
                <p className="text-blue-300 text-xs">Duration: {item.duration}</p>
              )}
            </motion.div>
          ))}
        </div>
        <div className="text-center mt-4">
          <p className="text-white/60 text-sm">Click any item to view details</p>
        </div>
      </div>
    );
  }
};

// Page Components
const HomePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <VideoBackground 
      videoSrc="/video/home.mp4" 
      overlay=""
    />
    
    <div className="relative z-10 min-h-screen flex items-center justify-center">
      {/* Content removed as requested - only header remains visible */}
    </div>
    
    <EnhancedAIChatbot />
  </div>
);

const WorkoutPage = () => {
  const [workouts, setWorkouts] = useState([]);
  const [selectedWorkout, setSelectedWorkout] = useState(null);
  const [isWorkoutModalOpen, setWorkoutModalOpen] = useState(false);

  // Enhanced Exercise Dataset - 8 Unique Workouts
  const enhancedExerciseData = [
    {
      id: 1,
      title: "HIIT Cardio",
      description: "Fast-paced high-intensity exercises",
      videoUrl: "https://www.youtube.com/embed/ml6cT4AZdqI",
      duration: "20 minutes",
      level: "Intermediate",
      steps: [
        "Warm-up jog in place for 2 minutes",
        "Jump squats - 30 seconds on, 15 seconds rest",
        "Burpees - 30 seconds on, 15 seconds rest",
        "Plank jacks - 30 seconds on, 15 seconds rest",
        "High knees - 30 seconds on, 15 seconds rest",
        "Mountain climbers - 30 seconds on, 15 seconds rest",
        "Cool down with light stretching"
      ],
      requirements: ["Exercise mat", "Water bottle", "Comfortable clothing"],
      muscle_groups: ["Full body", "Cardiovascular system"]
    },
    {
      id: 2,
      title: "Core Strength",
      description: "Focused on abs and obliques",
      videoUrl: "https://www.youtube.com/embed/Xyd_fa5zoEU",
      duration: "15 minutes",
      level: "Beginner",
      steps: [
        "Basic crunches - 3 sets of 15 reps",
        "Leg raises - 3 sets of 12 reps",
        "Plank hold - 3 sets of 30-45 seconds",
        "Russian twists - 3 sets of 20 reps",
        "Dead bug - 3 sets of 10 each side",
        "Cool down with gentle stretching"
      ],
      requirements: ["Exercise mat", "Comfortable clothing"],
      muscle_groups: ["Core", "Abs", "Obliques"]
    },
    {
      id: 3,
      title: "Glutes & Legs",
      description: "Lower body shaping workout",
      videoUrl: "https://www.youtube.com/embed/1oed-UmAxFs",
      duration: "25 minutes",
      level: "Intermediate",
      steps: [
        "Glute bridges - 3 sets of 15 reps",
        "Walking lunges - 3 sets of 12 each leg",
        "Step-ups on bench - 3 sets of 10 each leg",
        "Wall sits - 3 sets of 30-45 seconds",
        "Calf raises - 3 sets of 20 reps",
        "Cool down with leg stretches"
      ],
      requirements: ["Bench or step", "Exercise mat"],
      muscle_groups: ["Glutes", "Quadriceps", "Hamstrings", "Calves"]
    },
    {
      id: 4,
      title: "Upper Body Strength",
      description: "Dumbbell arm & chest routine",
      videoUrl: "https://www.youtube.com/embed/vthMCtgVtFw",
      duration: "30 minutes",
      level: "Intermediate",
      steps: [
        "Dumbbell chest press - 3 sets of 12 reps",
        "Bicep curls - 3 sets of 15 reps",
        "Shoulder press - 3 sets of 10 reps",
        "Tricep dips - 3 sets of 12 reps",
        "Bent-over rows - 3 sets of 12 reps",
        "Cool down with arm stretches"
      ],
      requirements: ["Dumbbells", "Flat bench", "Exercise mat"],
      muscle_groups: ["Chest", "Arms", "Shoulders", "Back"]
    },
    {
      id: 5,
      title: "Stretch & Recovery",
      description: "For cooldown and muscle release",
      videoUrl: "https://www.youtube.com/embed/QXwz1u0vpy4",
      duration: "15 minutes",
      level: "All Levels",
      steps: [
        "Hamstring stretch - Hold 30 seconds each leg",
        "Cat-cow stretch - 10 slow repetitions",
        "Child's pose - Hold for 45 seconds",
        "Hip flexor stretch - 30 seconds each side",
        "Shoulder rolls and neck stretches",
        "Deep breathing relaxation"
      ],
      requirements: ["Exercise mat", "Comfortable clothing"],
      muscle_groups: ["Full body flexibility", "Stress relief"]
    },
    {
      id: 6,
      title: "Resistance Band Full Body",
      description: "Resistance-based strength training",
      videoUrl: "https://www.youtube.com/embed/Hlj6lgV5wUQ",
      duration: "30 minutes",
      level: "Intermediate",
      steps: [
        "Band chest press - 3 sets of 15 reps",
        "Banded squats - 3 sets of 12 reps",
        "Overhead press with band - 3 sets of 12 reps",
        "Band rows - 3 sets of 15 reps",
        "Lateral band walks - 3 sets of 10 each direction",
        "Cool down with light stretching"
      ],
      requirements: ["Resistance bands", "Anchor point", "Exercise mat"],
      muscle_groups: ["Full body", "Functional strength"]
    },
    {
      id: 7,
      title: "Mobility Flow",
      description: "Joint flexibility & motion",
      videoUrl: "https://www.youtube.com/embed/8BcPHWGQO44",
      duration: "10 minutes",
      level: "Beginner",
      steps: [
        "Arm circles - 30 seconds forward and backward",
        "Hip openers - 10 reps each side",
        "Spinal roll from squat to stand - 5 slow reps",
        "Shoulder shrugs and neck circles - 10 each direction",
        "Deep lunge with twist - 30 seconds per side",
        "Gentle breathing and relaxation"
      ],
      requirements: ["Exercise mat", "Comfortable space"],
      muscle_groups: ["Joints", "Mobility", "Flexibility"]
    },
    {
      id: 8,
      title: "Pilates Core Burn",
      description: "Focused mat Pilates sequence",
      videoUrl: "https://www.youtube.com/embed/lCg_gh_fppI",
      duration: "20 minutes",
      level: "Beginner",
      steps: [
        "The Hundred - 100 pulses with breathing",
        "Leg circles - 8 reps each direction, each leg",
        "Roll-up to Teaser - 5 slow controlled reps",
        "Crisscross abs - 10 reps each side",
        "Spine stretch forward - 5 reps with deep breathing",
        "Final relaxation in child's pose"
      ],
      requirements: ["Exercise mat", "Comfortable clothing"],
      muscle_groups: ["Core", "Pilates fundamentals", "Body control"]
    }
  ];

  // Create 12-card gallery: 8 unique + first 4 repeated
  const workoutGalleryData = [
    ...enhancedExerciseData, // First 8 unique workouts (ids 1-8)
    // Repeat first 4 workouts with unique identifiers to avoid key conflicts
    { ...enhancedExerciseData[0], id: 9, originalId: 1 }, // HIIT Cardio repeat
    { ...enhancedExerciseData[1], id: 10, originalId: 2 }, // Core Strength repeat  
    { ...enhancedExerciseData[2], id: 11, originalId: 3 }, // Glutes & Legs repeat
    { ...enhancedExerciseData[3], id: 12, originalId: 4 }  // Upper Body Strength repeat
  ];

  useEffect(() => {
    setWorkouts(workoutGalleryData);
  }, []);

  const handleWorkoutClick = (workout) => {
    setSelectedWorkout(workout);
    setWorkoutModalOpen(true);
  };

  const handleSectionHover = (isHovering) => {
    const workoutIcon = document.querySelector('.header-workout-icon');
    if (workoutIcon) {
      if (isHovering) {
        workoutIcon.style.animation = 'dumbbellLift 0.8s ease-in-out';
        workoutIcon.style.color = '#000000';
        workoutIcon.style.transform = 'rotate(15deg)';
      } else {
        workoutIcon.style.animation = '';
        workoutIcon.style.color = '';
        workoutIcon.style.transform = '';
      }
    }
  };

  return (
    <div 
      className="h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/workout.mp4" 
        overlay="bg-black/50"
      />
      
      <div className="relative z-10 h-full flex flex-col">
        {/* Header Section with Title */}
        <div className="pt-20 px-6 flex-shrink-0">
          <div className="max-w-screen-2xl mx-auto">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-2">Workout Plans</h1>
              <p className="text-lg text-white/80 mb-4">Personalized fitness routines for every goal</p>
            </div>
          </div>
        </div>

        {/* Gallery Section - Takes remaining space */}
        <div className="flex-1 px-6 mt-4">
          <div className="max-w-screen-2xl mx-auto h-full">
            {/* Display Workouts */}
            {workouts.length > 0 ? (
              <CircularGalleryOGL 
                items={workouts}
                onItemClick={handleWorkoutClick}
                type="workout"
              />
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-white/60">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
                  <p>Loading workout plans...</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Modal 
        isOpen={isWorkoutModalOpen}
        onClose={() => setWorkoutModalOpen(false)}
        item={selectedWorkout}
        type="workout"
      />
    </div>
  );
};

const SkincarePage = () => {
  const [routines, setRoutines] = useState([]);
  const [selectedRoutine, setSelectedRoutine] = useState(null);
  const [isSkincareModalOpen, setSkincareModalOpen] = useState(false);

  // Enhanced Skincare Dataset - 8 Unique Routines with Requirements
  const enhancedSkincareData = [
    {
      id: "hydration_boost",
      title: "Hydration Boost",
      skinType: "Dry Skin",
      time: "Morning & Night",
      level: "Beginner",
      video: "https://www.youtube.com/embed/rXxNGl7YQcA",
      description: "Deep hydration for dry, flaky skin",
      steps: [
        "Cleanse with a gentle hydrating face wash",
        "Apply hyaluronic acid serum",
        "Seal with thick moisturizer",
        "Mist with facial spray"
      ],
      requirements: ["Hydrating Cleanser", "Hyaluronic Serum", "Moisturizer", "Facial Mist"]
    },
    {
      id: "acne_defense",
      title: "Acne Defense Routine",
      skinType: "Oily / Acne-Prone",
      time: "Night Only",
      level: "Intermediate",
      video: "https://www.youtube.com/embed/ml6cT4AZdqI",
      description: "Targeted acne treatment and prevention",
      steps: [
        "Use salicylic acid cleanser",
        "Apply niacinamide serum",
        "Spot treat with benzoyl peroxide",
        "Finish with lightweight gel moisturizer"
      ],
      requirements: ["Salicylic Cleanser", "Niacinamide", "Spot Treatment", "Oil-Free Moisturizer"]
    },
    {
      id: "glow_up",
      title: "Glowing Skin Ritual",
      skinType: "All Types",
      time: "Morning",
      level: "Beginner",
      video: "https://www.youtube.com/embed/VVNNS2MDA00",
      description: "Achieve that natural glow every morning",
      steps: [
        "Vitamin C cleanse",
        "Apply antioxidant serum",
        "Follow up with SPF 50 sunscreen",
        "Dab cream highlighter for glow"
      ],
      requirements: ["Vitamin C Cleanser", "Antioxidant Serum", "Sunscreen", "Highlighter"]
    },
    {
      id: "anti_aging",
      title: "Anti-Aging Protocol",
      skinType: "Mature Skin",
      time: "Night Only",
      level: "Advanced",
      video: "https://www.youtube.com/embed/Sq3lNHgzwzE",
      description: "Advanced anti-aging night routine",
      steps: [
        "Double cleanse (oil then foam)",
        "Apply retinol serum",
        "Moisturize with peptide cream",
        "Neck & under-eye massage"
      ],
      requirements: ["Oil Cleanser", "Retinol", "Peptide Cream", "Eye Serum"]
    },
    {
      id: "sensitive_repair",
      title: "Sensitive Skin Repair",
      skinType: "Sensitive",
      time: "Evening",
      level: "Beginner",
      video: "https://www.youtube.com/embed/hv1zvKZTFnA",
      description: "Gentle care for sensitive, reactive skin",
      steps: [
        "Use micellar water or no-rinse cleanser",
        "Apply calming chamomile mist",
        "Moisturize with ceramide cream",
        "Optional: Overnight barrier balm"
      ],
      requirements: ["Micellar Cleanser", "Calming Mist", "Ceramide Cream", "Barrier Balm"]
    },
    {
      id: "pore_minimizer",
      title: "Pore Minimizer Routine",
      skinType: "Oily / Combo",
      time: "Morning",
      level: "Intermediate",
      video: "https://www.youtube.com/embed/X81ZRHZLkB8",
      description: "Minimize pores and control oil production",
      steps: [
        "Clay mask cleanse",
        "Apply BHA toner",
        "Follow with mattifying primer",
        "Finish with mineral SPF"
      ],
      requirements: ["Clay Cleanser", "BHA Toner", "Mattifying Primer", "Mineral SPF"]
    },
    {
      id: "skin_detox",
      title: "Weekend Skin Detox",
      skinType: "All Types",
      time: "Weekly",
      level: "Intermediate",
      video: "https://www.youtube.com/embed/AoFzAkLDvlM",
      description: "Weekly detox routine for refreshed skin",
      steps: [
        "Steam face for 5 minutes",
        "Apply charcoal or green tea mask",
        "Use jade roller with detox oil",
        "Seal with hydrating sleeping pack"
      ],
      requirements: ["Steam Device", "Detox Mask", "Jade Roller", "Sleeping Pack"]
    },
    {
      id: "brighten_tone",
      title: "Brighten & Tone",
      skinType: "Dull Skin",
      time: "Morning",
      level: "Advanced",
      video: "https://www.youtube.com/embed/UKwmsAhWwN0",
      description: "Brighten complexion and even skin tone",
      steps: [
        "Exfoliate gently with lactic acid toner",
        "Apply brightening niacinamide serum",
        "Layer lightweight moisturizer",
        "Finish with glow SPF cream"
      ],
      requirements: ["Lactic Acid Toner", "Niacinamide", "Light Moisturizer", "Glow SPF"]
    }
  ];

  // Create 12-card gallery: 8 unique + first 4 repeated
  const skincareGalleryData = [
    ...enhancedSkincareData, // First 8 unique routines
    // Repeat first 4 routines with unique identifiers to avoid key conflicts
    { ...enhancedSkincareData[0], id: "hydration_boost_repeat", originalId: "hydration_boost" }, // Hydration Boost repeat
    { ...enhancedSkincareData[1], id: "acne_defense_repeat", originalId: "acne_defense" }, // Acne Defense repeat  
    { ...enhancedSkincareData[2], id: "glow_up_repeat", originalId: "glow_up" }, // Glowing Skin repeat
    { ...enhancedSkincareData[3], id: "anti_aging_repeat", originalId: "anti_aging" }  // Anti-Aging repeat
  ];

  useEffect(() => {
    setRoutines(skincareGalleryData);
  }, []);

  const handleRoutineClick = (routine) => {
    // Handle repeated items by finding original data
    const actualRoutine = routine.originalId ? 
      enhancedSkincareData.find(item => item.id === routine.originalId) : 
      routine;
    setSelectedRoutine(actualRoutine);
    setSkincareModalOpen(true);
  };

  const handleSectionHover = (isHovering) => {
    const skincareIcon = document.querySelector('.header-skincare-icon');
    if (skincareIcon) {
      if (isHovering) {
        skincareIcon.style.animation = 'sparkleGlow 1s ease-in-out infinite';
        skincareIcon.style.color = '#ffd700';
        skincareIcon.style.filter = 'drop-shadow(0 0 8px #ffd700)';
      } else {
        skincareIcon.style.animation = '';
        skincareIcon.style.color = '';
        skincareIcon.style.filter = '';
      }
    }
  };

  return (
    <div 
      className="h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/skincare.mp4" 
        overlay="bg-black/50"
      />
      
      <div className="relative z-10 h-full flex flex-col">
        {/* Header Section with Title */}
        <div className="pt-20 px-6 flex-shrink-0">
          <div className="max-w-screen-2xl mx-auto">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-2">Skincare Routines</h1>
              <p className="text-lg text-white/80 mb-4">Glow with science-backed skincare</p>
            </div>
          </div>
        </div>

        {/* Gallery Section - Takes remaining space */}
        <div className="flex-1 px-6 mt-4">
          <div className="max-w-screen-2xl mx-auto h-full">
            {/* Display Skincare Routines */}
            {routines.length > 0 ? (
              <CircularGalleryOGL 
                items={routines}
                onItemClick={handleRoutineClick}
                type="skincare"
              />
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-white/60">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
                  <p>Loading skincare routines...</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Modal 
        isOpen={isSkincareModalOpen}
        onClose={() => setSkincareModalOpen(false)}
        item={selectedRoutine}
        type="skincare"
      />
    </div>
  );
};

const DietPage = () => {
  const [diets, setDiets] = useState([]);
  const [selectedDiet, setSelectedDiet] = useState(null);
  const [isDietModalOpen, setDietModalOpen] = useState(false);

  // Enhanced Diet Dataset - 8 Unique Diet Plans
  const enhancedDietData = [
    {
      id: 1,
      title: "Mediterranean Diet",
      description: "Heart-healthy nutrition with olive oil, fish, and vegetables",
      videoUrl: "https://www.youtube.com/embed/NP7nHOZPPpw",
      duration: "Lifestyle Plan",
      level: "Beginner",
      steps: [
        "Start your day with Greek yogurt and berries",
        "Include fish 2-3 times per week (salmon, sardines, mackerel)",
        "Use olive oil as your primary cooking fat",
        "Eat plenty of vegetables, fruits, and whole grains",
        "Include nuts, seeds, and legumes daily",
        "Limit red meat to 1-2 times per week",
        "Enjoy moderate amounts of red wine with meals (optional)"
      ],
      requirements: ["Olive oil", "Fresh fish", "Vegetables", "Whole grains", "Nuts"],
      calories: "1,800-2,200 per day",
      meal_types: ["Heart-healthy", "Anti-inflammatory", "Sustainable"]
    },
    {
      id: 2,
      title: "Keto Diet Plan",
      description: "Low-carb, high-fat approach for rapid weight loss",
      videoUrl: "https://www.youtube.com/embed/6qcoWUeqOJ8",
      duration: "4-12 weeks",
      level: "Intermediate",
      steps: [
        "Keep carbs under 20-25g per day",
        "Increase healthy fats to 70-75% of calories",
        "Moderate protein intake (20-25% of calories)",
        "Include avocados, nuts, and MCT oil",
        "Eat leafy greens and low-carb vegetables",
        "Track ketones with test strips",
        "Stay hydrated and supplement electrolytes"
      ],
      requirements: ["Avocados", "MCT oil", "Leafy greens", "Quality proteins", "Electrolytes"],
      calories: "1,500-2,000 per day",
      meal_types: ["Low-carb", "High-fat", "Ketogenic"]
    },
    {
      id: 3,
      title: "Plant-Based Nutrition",
      description: "Complete vegan nutrition for optimal health",
      videoUrl: "https://www.youtube.com/embed/d5wabeFG9pM",
      duration: "Lifestyle Plan",
      level: "Beginner",
      steps: [
        "Focus on whole, unprocessed plant foods",
        "Include protein from beans, lentils, quinoa, and tofu",
        "Eat a rainbow of fruits and vegetables daily",
        "Include B12, vitamin D, and omega-3 supplements",
        "Choose whole grains over refined options",
        "Include nuts and seeds for healthy fats",
        "Meal prep to ensure balanced nutrition"
      ],
      requirements: ["Legumes", "Quinoa", "Nutritional yeast", "B12 supplement", "Nuts"],
      calories: "1,800-2,200 per day",
      meal_types: ["Vegan", "Whole foods", "Nutrient-dense"]
    },
    {
      id: 4,
      title: "DASH Diet",
      description: "Designed to lower blood pressure naturally",
      videoUrl: "https://www.youtube.com/embed/kDwjF8D2OvI",
      duration: "Lifestyle Plan",
      level: "Beginner",
      steps: [
        "Reduce sodium intake to less than 2,300mg daily",
        "Eat 4-5 servings of fruits and vegetables daily",
        "Include low-fat dairy products",
        "Choose lean proteins like poultry and fish",
        "Limit saturated and trans fats",
        "Include whole grains at each meal",
        "Monitor portion sizes carefully"
      ],
      requirements: ["Low-sodium foods", "Fresh produce", "Lean proteins", "Whole grains"],
      calories: "1,600-2,000 per day",
      meal_types: ["Heart-healthy", "Low-sodium", "Balanced"]
    },
    {
      id: 5,
      title: "Intermittent Fasting 16:8",
      description: "Time-restricted eating for metabolic health",
      videoUrl: "https://www.youtube.com/embed/f67_w0lOr0M",
      duration: "Ongoing Protocol",
      level: "Intermediate",
      steps: [
        "Fast for 16 hours, eat within 8-hour window",
        "Start with 12pm-8pm eating window",
        "Break fast with nutrient-dense foods",
        "Stay hydrated during fasting periods",
        "Include protein with each meal",
        "Focus on whole foods during eating window",
        "Listen to your body and adjust as needed"
      ],
      requirements: ["Timer app", "Electrolyte supplements", "Quality whole foods"],
      calories: "Maintain within eating window",
      meal_types: ["Time-restricted", "Metabolic", "Flexible"]
    },
    {
      id: 6,
      title: "High-Protein Diet",
      description: "Muscle building and weight management focus",
      videoUrl: "https://www.youtube.com/embed/bfcxNRgq_54",
      duration: "8-12 weeks",
      level: "Intermediate",
      steps: [
        "Aim for 1.2-1.6g protein per kg body weight",
        "Include protein source at every meal",
        "Eat lean meats, fish, eggs, and dairy",
        "Add protein powder if needed",
        "Time protein intake around workouts",
        "Include complex carbs for energy",
        "Stay hydrated for protein metabolism"
      ],
      requirements: ["Lean meats", "Protein powder", "Eggs", "Greek yogurt"],
      calories: "1,800-2,400 per day",
      meal_types: ["High-protein", "Muscle-building", "Performance"]
    },
    {
      id: 7,
      title: "Anti-Inflammatory Diet",
      description: "Reduce inflammation with healing foods",
      videoUrl: "https://www.youtube.com/embed/ECr8SKS6LJU",
      duration: "Lifestyle Plan",
      level: "Beginner",
      steps: [
        "Include omega-3 rich foods daily",
        "Eat colorful antioxidant-rich fruits and vegetables",
        "Use turmeric, ginger, and other anti-inflammatory spices",
        "Avoid processed foods and added sugars",
        "Include green tea and herbal teas",
        "Choose organic when possible",
        "Limit inflammatory oils and fried foods"
      ],
      requirements: ["Turmeric", "Ginger", "Omega-3 sources", "Colorful produce"],
      calories: "1,800-2,200 per day",
      meal_types: ["Anti-inflammatory", "Healing", "Whole foods"]
    },
    {
      id: 8,
      title: "Balanced Macro Diet",
      description: "Perfect macronutrient balance for sustained energy",
      videoUrl: "https://www.youtube.com/embed/XbpvRbgQZbw",
      duration: "Flexible Timeline",
      level: "Beginner",
      steps: [
        "Follow 40% carbs, 30% protein, 30% fat ratio",
        "Choose complex carbohydrates",
        "Include lean protein sources",
        "Add healthy fats from nuts, oils, and avocados",
        "Eat every 3-4 hours to maintain energy",
        "Track macros with a food app",
        "Adjust portions based on activity level"
      ],
      requirements: ["Food scale", "Macro tracking app", "Variety of whole foods"],
      calories: "Calculated based on goals",
      meal_types: ["Balanced", "Sustainable", "Customizable"]
    }
  ];

  // Create 12-card gallery: 8 unique + first 4 repeated
  const dietGalleryData = [
    ...enhancedDietData, // First 8 unique diets (ids 1-8)
    // Repeat first 4 diets with unique identifiers to avoid key conflicts
    { ...enhancedDietData[0], id: 9, originalId: 1 }, // Mediterranean Diet repeat
    { ...enhancedDietData[1], id: 10, originalId: 2 }, // Keto Diet repeat  
    { ...enhancedDietData[2], id: 11, originalId: 3 }, // Plant-Based repeat
    { ...enhancedDietData[3], id: 12, originalId: 4 }  // DASH Diet repeat
  ];

  useEffect(() => {
    setDiets(dietGalleryData);
  }, []);

  const handleDietClick = (diet) => {
    setSelectedDiet(diet);
    setDietModalOpen(true);
  };

  const handleSectionHover = (isHovering) => {
    const dietIcon = document.querySelector('.header-diet-icon');
    if (dietIcon) {
      if (isHovering) {
        dietIcon.style.animation = 'appleGrow 0.6s ease-in-out';
        dietIcon.style.color = '#22c55e';
        dietIcon.style.filter = 'drop-shadow(2px 2px 4px #16a34a)';
      } else {
        dietIcon.style.animation = '';
        dietIcon.style.color = '';
        dietIcon.style.filter = '';
      }
    }
  };

  return (
    <div 
      className="h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/diet.mp4" 
        overlay="bg-black/50"
      />
      
      <div className="relative z-10 h-full flex flex-col">
        {/* Header Section with Title */}
        <div className="pt-20 px-6 flex-shrink-0">
          <div className="max-w-screen-2xl mx-auto">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-white mb-2">Diet Plans</h1>
              <p className="text-lg text-white/80 mb-4">Nutrition that fuels your potential</p>
            </div>
          </div>
        </div>

        {/* Gallery Section - Takes remaining space */}
        <div className="flex-1 px-6 mt-4">
          <div className="max-w-screen-2xl mx-auto h-full">
            {/* Display Diets */}
            {diets.length > 0 ? (
              <CircularGalleryOGL 
                items={diets}
                onItemClick={handleDietClick}
                type="diet"
              />
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-white/60">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
                  <p>Loading diet plans...</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Modal 
        isOpen={isDietModalOpen}
        onClose={() => setDietModalOpen(false)}
        item={selectedDiet}
        type="diet"
      />
    </div>
  );
};

const HealthPage = () => {
  // State management for all features
  const [activeTab, setActiveTab] = useState('symptoms');
  const [symptomData, setSymptomData] = useState({
    symptoms: [],
    custom_symptoms: '',
    body_parts: [],
    duration: '',
    severity: 'moderate',
    additional_info: ''
  });
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    { type: 'bot', content: 'Hello! I\'m your AI health assistant. How can I help you today?' }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [notifications, setNotifications] = useState([]);

  // Predefined symptom options
  const commonSymptoms = [
    'Fever', 'Headache', 'Cough', 'Sore throat', 'Runny nose', 'Body aches',
    'Fatigue', 'Nausea', 'Vomiting', 'Diarrhea', 'Stomach pain', 'Chest pain',
    'Shortness of breath', 'Dizziness', 'Skin rash', 'Joint pain', 'Back pain',
    'Muscle pain', 'Loss of appetite', 'Difficulty sleeping', 'Anxiety', 'Depression'
  ];

  const bodyParts = [
    'Head', 'Neck', 'Chest', 'Abdomen', 'Back', 'Arms', 'Legs', 'Hands', 'Feet',
    'Eyes', 'Ears', 'Nose', 'Throat', 'Skin', 'Joints', 'Muscles'
  ];

  const handleSectionHover = (isHovering) => {
    const healthIcon = document.querySelector('.header-health-icon');
    if (healthIcon) {
      if (isHovering) {
        healthIcon.style.animation = 'heartBeat 0.8s ease-in-out infinite';
        healthIcon.style.color = '#ef4444';
        healthIcon.style.filter = 'drop-shadow(0 0 6px #ef4444)';
      } else {
        healthIcon.style.animation = '';
        healthIcon.style.color = '';
        healthIcon.style.filter = '';
      }
    }
  };

  // Enhanced Symptom Checker Implementation
  const analyzeSymptoms = async () => {
    if (symptomData.symptoms.length === 0 && !symptomData.custom_symptoms.trim()) {
      alert('Please select at least one symptom or describe your symptoms.');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/symptoms/analyze`, {
        symptoms: symptomData.symptoms,
        custom_symptoms: symptomData.custom_symptoms,
        body_parts: symptomData.body_parts,
        duration: symptomData.duration,
        severity: symptomData.severity,
        additional_info: symptomData.additional_info
      });
      
      setAnalysisResult(response.data);
    } catch (error) {
      console.error('Symptom analysis error:', error);
      // Fallback analysis
      const fallbackAnalysis = {
        urgency_level: symptomData.severity === 'severe' ? 'High' : symptomData.severity === 'moderate' ? 'Medium' : 'Low',
        possible_conditions: [
          { name: 'General Health Concern', probability: '50%', description: 'Symptoms require professional evaluation' }
        ],
        recommendations: [
          'Stay hydrated and get adequate rest',
          'Monitor symptoms for changes',
          'Consult healthcare provider if symptoms persist'
        ],
        when_to_seek_care: 'Consult a doctor if symptoms persist beyond 3 days',
        disclaimer: 'This analysis is for informational purposes only and should not replace professional medical advice.'
      };
      setAnalysisResult(fallbackAnalysis);
    } finally {
      setLoading(false);
    }
  };

  // Enhanced Medical Bot Implementation with Backend API
  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;
    
    const userMessage = chatInput;
    setChatInput('');
    setChatMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setChatLoading(true);
    
    try {
      const response = await axios.post(`${API}/chat`, {
        user_id: localStorage.getItem('userId') || 'demo-user',
        message: userMessage,
        user_profile: null // Can be enhanced to include user profile
      });
      
      setChatMessages(prev => [...prev, { type: 'bot', content: response.data.response }]);
    } catch (error) {
      console.error('Chat error:', error);
      // Fallback responses
      const fallbackResponses = [
        "I understand your concern. Can you provide more details about your symptoms?",
        "Based on what you've described, I recommend consulting with a healthcare professional.",
        "That's a great question! For personalized health advice, please speak with your doctor.",
        "I'm here to provide general health information. For specific medical concerns, please consult a healthcare provider."
      ];
      const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
      setChatMessages(prev => [...prev, { type: 'bot', content: randomResponse }]);
    } finally {
      setChatLoading(false);
    }
  };

  // Toggle symptom selection
  const toggleSymptom = (symptom) => {
    setSymptomData(prev => ({
      ...prev,
      symptoms: prev.symptoms.includes(symptom)
        ? prev.symptoms.filter(s => s !== symptom)
        : [...prev.symptoms, symptom]
    }));
  };

  // Toggle body part selection
  const toggleBodyPart = (bodyPart) => {
    setSymptomData(prev => ({
      ...prev,
      body_parts: prev.body_parts.includes(bodyPart)
        ? prev.body_parts.filter(bp => bp !== bodyPart)
        : [...prev.body_parts, bodyPart]
    }));
  };

  // Health Education Topics
  const educationTopics = [
    { title: 'Heart Health', description: 'Prevention and management of cardiovascular diseases', icon: '❤️' },
    { title: 'Mental Wellness', description: 'Understanding and maintaining mental health', icon: '🧠' },
    { title: 'Nutrition Basics', description: 'Essential nutrition for optimal health', icon: '🥗' },
    { title: 'Exercise & Fitness', description: 'Building and maintaining physical fitness', icon: '💪' },
    { title: 'Preventive Care', description: 'Screenings and preventive measures', icon: '🛡️' },
    { title: 'Sleep Health', description: 'Importance of quality sleep for health', icon: '😴' }
  ];

  // Smart Notifications Mock Data
  const mockNotifications = [
    { id: 1, type: 'medication', message: 'Time to take your morning medication', time: '9:00 AM' },
    { id: 2, type: 'appointment', message: 'Doctor appointment reminder - Tomorrow 2:00 PM', time: 'Tomorrow' },
    { id: 3, type: 'wellness', message: 'Weekly wellness check-in available', time: 'Today' }
  ];

  const navigationTabs = [
    { id: 'symptoms', label: 'Symptom Checker', icon: '🩺' },
    { id: 'chatbot', label: 'Medical Bot', icon: '🤖' },
    { id: 'education', label: 'Health Education', icon: '📚' },
    { id: 'notifications', label: 'Smart Notifications', icon: '🔔' }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'symptoms':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">AI-Powered Symptom Checker</h2>
              <p className="text-white/80">Get personalized health insights based on your symptoms</p>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 md:p-8 border border-white/20">
              <div className="space-y-6">
                {/* Predefined Symptoms Selection */}
                <div>
                  <label className="block text-white font-semibold mb-3">Select Your Symptoms</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {commonSymptoms.map((symptom) => (
                      <button
                        key={symptom}
                        onClick={() => toggleSymptom(symptom)}
                        className={`p-3 rounded-lg text-sm font-medium transition-all ${
                          symptomData.symptoms.includes(symptom)
                            ? 'bg-blue-500 text-white border-2 border-blue-400'
                            : 'bg-white/10 text-white/80 border-2 border-white/20 hover:bg-white/20'
                        }`}
                      >
                        {symptom}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Custom Symptoms Input */}
                <div>
                  <label className="block text-white font-semibold mb-3">
                    Describe Additional Symptoms (Optional)
                  </label>
                  <textarea
                    value={symptomData.custom_symptoms}
                    onChange={(e) => setSymptomData({...symptomData, custom_symptoms: e.target.value})}
                    placeholder="Describe any other symptoms not listed above..."
                    className="w-full p-4 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    rows="3"
                  />
                </div>

                {/* Body Parts Selection */}
                <div>
                  <label className="block text-white font-semibold mb-3">Affected Body Parts (Optional)</label>
                  <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
                    {bodyParts.map((bodyPart) => (
                      <button
                        key={bodyPart}
                        onClick={() => toggleBodyPart(bodyPart)}
                        className={`p-2 rounded-lg text-xs font-medium transition-all ${
                          symptomData.body_parts.includes(bodyPart)
                            ? 'bg-green-500 text-white border-2 border-green-400'
                            : 'bg-white/10 text-white/80 border-2 border-white/20 hover:bg-white/20'
                        }`}
                      >
                        {bodyPart}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-white font-semibold mb-3">Duration</label>
                    <select
                      value={symptomData.duration}
                      onChange={(e) => setSymptomData({...symptomData, duration: e.target.value})}
                      className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="" className="bg-gray-800">Select duration</option>
                      <option value="less-than-1-day" className="bg-gray-800">Less than 1 day</option>
                      <option value="1-3-days" className="bg-gray-800">1-3 days</option>
                      <option value="1-week" className="bg-gray-800">About a week</option>
                      <option value="more-than-week" className="bg-gray-800">More than a week</option>
                      <option value="chronic" className="bg-gray-800">Chronic (ongoing)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-white font-semibold mb-3">Severity Level</label>
                    <select
                      value={symptomData.severity}
                      onChange={(e) => setSymptomData({...symptomData, severity: e.target.value})}
                      className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="mild" className="bg-gray-800">Mild</option>
                      <option value="moderate" className="bg-gray-800">Moderate</option>
                      <option value="severe" className="bg-gray-800">Severe</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-white font-semibold mb-3">Additional Information (Optional)</label>
                  <textarea
                    value={symptomData.additional_info}
                    onChange={(e) => setSymptomData({...symptomData, additional_info: e.target.value})}
                    placeholder="Any other relevant information about your symptoms..."
                    className="w-full p-4 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    rows="3"
                  />
                </div>

                <button
                  onClick={analyzeSymptoms}
                  disabled={loading || (symptomData.symptoms.length === 0 && !symptomData.custom_symptoms.trim())}
                  className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-4 px-6 rounded-lg font-semibold hover:from-blue-600 hover:to-cyan-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing Symptoms...</span>
                    </>
                  ) : (
                    <>
                      <span>🔍</span>
                      <span>Analyze Symptoms</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {analysisResult && (
              <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 md:p-8 border border-white/20">
                <h3 className="text-2xl font-bold text-white mb-6 flex items-center space-x-2">
                  <span>📊</span>
                  <span>Analysis Results</span>
                </h3>
                
                <div className="space-y-6">
                  <div className="bg-white/10 rounded-xl p-4">
                    <h4 className="text-white font-semibold mb-2 flex items-center space-x-2">
                      <span>⚠️</span>
                      <span>Urgency Level</span>
                    </h4>
                    <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                      analysisResult.urgency_level === 'High' ? 'bg-red-500/20 text-red-200 border border-red-500/30' :
                      analysisResult.urgency_level === 'Medium' ? 'bg-yellow-500/20 text-yellow-200 border border-yellow-500/30' :
                      'bg-green-500/20 text-green-200 border border-green-500/30'
                    }`}>
                      {analysisResult.urgency_level}
                    </span>
                  </div>

                  <div className="bg-white/10 rounded-xl p-4">
                    <h4 className="text-white font-semibold mb-3 flex items-center space-x-2">
                      <span>🔍</span>
                      <span>Possible Conditions</span>
                    </h4>
                    <div className="space-y-3">
                      {analysisResult.possible_conditions.map((condition, index) => (
                        <div key={index} className="flex justify-between items-start bg-white/5 rounded-lg p-3">
                          <div className="flex-1">
                            <p className="text-white font-medium">{condition.name}</p>
                            <p className="text-white/70 text-sm mt-1">{condition.description}</p>
                          </div>
                          <span className="text-blue-300 font-semibold ml-4">{condition.probability}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-white/10 rounded-xl p-4">
                    <h4 className="text-white font-semibold mb-3 flex items-center space-x-2">
                      <span>💡</span>
                      <span>Recommendations</span>
                    </h4>
                    <ul className="space-y-2">
                      {analysisResult.recommendations.map((rec, index) => (
                        <li key={index} className="text-white/90 flex items-start">
                          <span className="text-green-400 mr-2 mt-1">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4">
                    <h4 className="text-red-200 font-semibold mb-2 flex items-center space-x-2">
                      <span>🏥</span>
                      <span>When to Seek Care</span>
                    </h4>
                    <p className="text-red-100">{analysisResult.when_to_seek_care}</p>
                  </div>

                  <div className="bg-white/5 rounded-xl p-4">
                    <p className="text-white/60 text-sm italic">{analysisResult.disclaimer}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        );

      case 'chatbot':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Medical AI Assistant</h2>
              <p className="text-white/80">Get instant health guidance and support</p>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-3xl p-4 md:p-6 border border-white/20">
              <div className="h-80 md:h-96 overflow-y-auto mb-4 space-y-4 p-2">
                {chatMessages.map((message, index) => (
                  <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                      message.type === 'user' 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-white/20 text-white'
                    }`}>
                      {message.content}
                    </div>
                  </div>
                ))}
                
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-xs lg:max-w-md px-4 py-3 rounded-lg bg-white/20 text-white">
                      <div className="flex items-center space-x-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                        <span className="text-sm">AI is thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex space-x-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !chatLoading && sendChatMessage()}
                  placeholder="Ask about your health concerns..."
                  className="flex-1 p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={chatLoading}
                />
                <button
                  onClick={sendChatMessage}
                  disabled={!chatInput.trim() || chatLoading}
                  className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {chatLoading ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <>
                      <span>Send</span>
                      <span>💬</span>
                    </>
                  )}
                </button>
              </div>
              
              {/* Quick suggestions */}
              <div className="mt-4 flex flex-wrap gap-2">
                {['💪 Workout advice', '🥗 Nutrition tips', '✨ Skincare help', '🧘 Stress management'].map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => setChatInput(suggestion)}
                    className="px-3 py-1 bg-white/10 hover:bg-white/20 rounded-full text-white/80 text-sm transition-colors"
                    disabled={chatLoading}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        );

      case 'education':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Health Education Center</h2>
              <p className="text-white/80">Learn about health topics and wellness</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {educationTopics.map((topic, index) => (
                <div key={index} className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 hover:bg-white/20 transition-all cursor-pointer">
                  <div className="text-4xl mb-4">{topic.icon}</div>
                  <h3 className="text-white font-semibold text-lg mb-2">{topic.title}</h3>
                  <p className="text-white/70">{topic.description}</p>
                </div>
              ))}
            </div>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Smart Health Notifications</h2>
              <p className="text-white/80">Stay on top of your health with personalized reminders</p>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-3xl p-8 border border-white/20">
              <div className="space-y-4">
                {mockNotifications.map((notification) => (
                  <div key={notification.id} className="bg-white/10 rounded-xl p-4 flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">
                        {notification.type === 'medication' ? '💊' : 
                         notification.type === 'appointment' ? '📅' : '🎯'}
                      </span>
                      <div>
                        <p className="text-white font-medium">{notification.message}</p>
                        <p className="text-white/70 text-sm">{notification.time}</p>
                      </div>
                    </div>
                    <button className="text-blue-400 hover:text-blue-300">Mark as read</button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div 
      className="min-h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/health.mp4" 
        overlay="bg-black/70"
      />
      
      <div className="relative z-10 pt-20 px-6 min-h-screen">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <div className="w-20 h-20 bg-gradient-to-br from-red-400 via-pink-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg ring-4 ring-white/20">
              <span className="text-3xl">🏥</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">
              HealNav - Complete Health Platform
            </h1>
            <p className="text-xl text-white/80 max-w-2xl mx-auto">
              AI-powered health navigation with comprehensive tools for symptom checking, medical assistance, and wellness management
            </p>
          </motion.div>

          {/* Navigation Tabs */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            {navigationTabs.map((tab) => (
              <motion.button
                key={tab.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg'
                    : 'bg-white/10 text-white/80 hover:bg-white/20 border border-white/20'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </motion.button>
            ))}
          </div>

          {/* Content */}
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="mb-8"
          >
            {renderContent()}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

// Enhanced Grocery Agent Component with AI Integration
const GroceryAgent = () => {
  const [query, setQuery] = useState('');
  const [budget, setBudget] = useState(500);
  const [preferredBrands, setPreferredBrands] = useState(['MuscleBlaze', 'Organic India']);
  const [diet, setDiet] = useState('high protein');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [currentStep, setCurrentStep] = useState('input');
  const [aiResponse, setAiResponse] = useState('');

  const handleGetRecommendations = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/grocery/recommendations`, {
        query: query,
        budget: budget,
        preferred_brands: preferredBrands,
        diet: diet
      });
      
      setRecommendations(response.data.recommendations || []);
      setAiResponse(response.data.ai_response || '');
      setCurrentStep('recommendations');
    } catch (error) {
      console.error('Error:', error);
      alert('Error getting recommendations. Please try again.');
    }
    setLoading(false);
  };

  const toggleProductSelection = (index) => {
    const updated = [...recommendations];
    updated[index].selected = !updated[index].selected;
    setRecommendations(updated);
  };

  const createCart = async () => {
    const selectedProducts = recommendations.filter(p => p.selected);
    if (selectedProducts.length === 0) {
      alert('Please select at least one product');
      return;
    }

    try {
      const response = await axios.post(`${API}/grocery/create-cart`, selectedProducts);
      setCart(response.data);
      setCurrentStep('cart');
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating cart. Please try again.');
    }
  };

  const sampleQueries = [
    "I need high protein supplements for my workout",
    "Get me organic vegetables under 300 rupees",
    "Find muscle building supplements from MuscleBlaze",
    "I want healthy snacks for my gym routine",
    "Need protein powder for post-workout recovery",
    "Looking for organic skincare supplements"
  ];

  const brandOptions = [
    'MuscleBlaze', 'Organic India', 'Patanjali', 'Dabur', 'Himalaya', 
    'Amway', 'Herbalife', 'ON (Optimum Nutrition)', 'Dymatize', 'BSN'
  ];

  const dietOptions = [
    'high protein', 'keto', 'vegan', 'vegetarian', 'paleo', 
    'low carb', 'gluten free', 'organic', 'weight loss', 'muscle gain'
  ];

  const handleSectionHover = (isHovering) => {
    const orderupIcon = document.querySelector('.header-orderup-icon');
    if (orderupIcon) {
      if (isHovering) {
        orderupIcon.style.animation = 'cartShake 0.6s ease-in-out';
        orderupIcon.style.color = '#f97316';
        orderupIcon.style.filter = 'drop-shadow(0 0 8px #f97316)';
      } else {
        orderupIcon.style.animation = '';
        orderupIcon.style.color = '';
        orderupIcon.style.filter = '';
      }
    }
  };

  return (
    <div 
      className="min-h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${backgrounds.orderup})` }}
      />
      <div className="absolute inset-0 bg-black/60" />
      
      <div className="relative z-10 pt-32 px-6">
        <div className="max-w-screen-2xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold text-white mb-4">Order Up</h1>
            <p className="text-xl text-white/80">AI-Powered Smart Shopping with NUTRACITY AI</p>
          </div>

          {currentStep === 'input' && (
            <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-xl p-8 border border-white/20">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-white mb-4">🎤 What do you need today?</h2>
                <p className="text-white/80">Tell me what groceries or supplements you are looking for</p>
              </div>

              <div className="mb-6">
                <p className="text-sm font-medium text-white/90 mb-3">💡 Try these examples:</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {sampleQueries.map((sample, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(sample)}
                      className="text-left p-3 bg-white/10 hover:bg-white/20 rounded-lg transition-colors border border-white/20"
                    >
                      <span className="text-white/90 text-sm">"{sample}"</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">
                    🗣️ Your Request
                  </label>
                  <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Type your grocery needs..."
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none text-white placeholder-white/50"
                    rows="3"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">
                    💰 Budget: ₹{budget}
                  </label>
                  <input
                    type="range"
                    min="100"
                    max="5000"
                    step="50"
                    value={budget}
                    onChange={(e) => setBudget(parseInt(e.target.value))}
                    className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-white/60 mt-1">
                    <span>₹100</span>
                    <span>₹5,000</span>
                  </div>
                </div>

                <button
                  onClick={handleGetRecommendations}
                  disabled={loading || !query.trim()}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>🤖 AI is analyzing your request...</span>
                    </div>
                  ) : '🤖 Get AI Recommendations'}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'recommendations' && (
            <div className="space-y-6">
              {aiResponse && (
                <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-lg p-6 border border-white/20">
                  <h3 className="text-xl font-bold text-white mb-4">🧠 AI Analysis</h3>
                  <div className="text-white/80 text-sm max-h-32 overflow-y-auto bg-black/20 p-4 rounded-lg">
                    {aiResponse.substring(0, 300)}...
                  </div>
                </div>
              )}
              
              <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-lg p-6 border border-white/20">
                <h3 className="text-xl font-bold text-white mb-6">🤖 AI Recommendations</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map((product, index) => (
                    <div
                      key={index}
                      className={`border-2 rounded-xl p-4 transition-all cursor-pointer transform hover:scale-105 ${
                        product.selected 
                          ? 'border-green-500 bg-green-500/20 shadow-green-500/30 shadow-lg' 
                          : 'border-white/20 hover:border-purple-300 bg-white/10 hover:bg-white/15'
                      }`}
                      onClick={() => toggleProductSelection(index)}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h4 className="font-bold text-white text-sm line-clamp-2">{product.name}</h4>
                        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                          product.selected ? 'bg-green-500 border-green-500 scale-110' : 'border-white/50'
                        }`}>
                          {product.selected && <span className="text-white text-xs">✓</span>}
                        </div>
                      </div>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between items-center">
                          <span className="text-2xl font-bold text-purple-300">{product.price}</span>
                          <span className="text-yellow-400 flex items-center">
                            <Star size={14} className="mr-1" />
                            {product.rating}
                          </span>
                        </div>
                        
                        {product.protein && (
                          <div className="bg-orange-500/20 text-orange-200 px-2 py-1 rounded-full text-xs inline-block">
                            💪 {product.protein}
                          </div>
                        )}
                        
                        <p className="text-white/80 text-xs line-clamp-2">{product.description}</p>
                        
                        <div className="flex justify-between items-center pt-2 border-t border-white/10">
                          <span className="text-xs text-white/70">🏪 {product.platform}</span>
                          <span className="text-xs text-green-400">✓ In Stock</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex space-x-4 mt-8">
                  <button
                    onClick={() => setCurrentStep('input')}
                    className="flex-1 bg-white/20 text-white py-3 px-6 rounded-xl font-semibold hover:bg-white/30 transition-colors"
                  >
                    ← Back to Search
                  </button>
                  <button
                    onClick={createCart}
                    disabled={recommendations.filter(p => p.selected).length === 0}
                    className="flex-1 bg-green-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    🛒 Add to Cart ({recommendations.filter(p => p.selected).length})
                  </button>
                </div>
              </div>
            </div>
          )}

          {currentStep === 'cart' && (
            <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-xl p-8 border border-white/20">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-white mb-2">🛒 Your Smart Cart</h2>
                <p className="text-white/80">AI-curated products ready for checkout!</p>
              </div>

              <div className="space-y-4 mb-8">
                {cart.cart_items && cart.cart_items.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-4 bg-white/10 rounded-lg border border-white/20">
                    <div className="flex-1">
                      <h4 className="font-semibold text-white">{item.name}</h4>
                      <div className="flex items-center space-x-4 mt-1">
                        <p className="text-sm text-white/70">🏪 {item.platform}</p>
                        {item.protein && (
                          <span className="text-xs bg-orange-500/20 text-orange-200 px-2 py-1 rounded-full">
                            💪 {item.protein}
                          </span>
                        )}
                        <span className="text-xs text-yellow-400">⭐ {item.rating}</span>
                      </div>
                    </div>
                    <div className="text-xl font-bold text-green-400">{item.price}</div>
                  </div>
                ))}
              </div>

              <div className="border-t border-white/20 pt-6 space-y-4">
                <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-xl p-4 border border-purple-500/30">
                  <div className="flex justify-between items-center text-2xl font-bold mb-2">
                    <span className="text-white">Total Amount:</span>
                    <span className="text-green-400">₹{cart.total_cost}</span>
                  </div>
                  <div className="flex justify-between text-sm text-white/70">
                    <span>Items: {cart.item_count}</span>
                    <span>Delivery: Free</span>
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    onClick={() => setCurrentStep('recommendations')}
                    className="flex-1 bg-white/20 text-white py-4 px-6 rounded-xl font-semibold hover:bg-white/30 transition-colors"
                  >
                    ← Modify Selection
                  </button>
                  <button
                    onClick={() => {
                      alert('🎉 Order placed successfully! Your AI-curated groceries will be delivered soon.');
                      setCurrentStep('input');
                      setQuery('');
                      setRecommendations([]);
                      setCart([]);
                    }}
                    className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transition-all transform hover:scale-105"
                  >
                    🎉 Place Order
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Get Started Page - Login/Signup with Feature Showcase
const GetStartedPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('login');
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [formData, setFormData] = useState({
    // Basic Credentials
    email: '',
    password: '',
    name: '',
    confirmPassword: '',
    agreeTerms: false,
    // Vital Stats
    age: '',
    gender: '',
    height: '',
    heightUnit: 'cm',
    weight: '',
    weightUnit: 'kg',
    // Allergies & Medical
    allergies: [],
    customAllergy: '',
    chronicConditions: [],
    customChronicCondition: '',
    // Wellness Goals
    wellnessGoals: [],
    // Lifestyle & Preferences
    fitnessLevel: '',
    dietPreference: '',
    skinType: '',
    smartCartOptIn: false
  });

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleMultiSelect = (name, value) => {
    const currentValues = formData[name];
    const updatedValues = currentValues.includes(value)
      ? currentValues.filter(item => item !== value)
      : [...currentValues, value];
    setFormData({
      ...formData,
      [name]: updatedValues
    });
  };

  const handleGoalsSelect = (goal) => {
    const currentGoals = formData.wellnessGoals;
    if (currentGoals.includes(goal)) {
      setFormData({
        ...formData,
        wellnessGoals: currentGoals.filter(g => g !== goal)
      });
    } else {
      setFormData({
        ...formData,
        wellnessGoals: [...currentGoals, goal]
      });
    }
  };

  const handleAllergyAdd = (allergy) => {
    if (allergy && !formData.allergies.includes(allergy)) {
      setFormData({
        ...formData,
        allergies: [...formData.allergies, allergy]
      });
    }
  };

  const handleAllergyRemove = (allergy) => {
    setFormData({
      ...formData,
      allergies: formData.allergies.filter(a => a !== allergy)
    });
  };

  const handleCustomAllergyAdd = () => {
    if (formData.customAllergy.trim() && !formData.allergies.includes(formData.customAllergy.trim())) {
      setFormData({
        ...formData,
        allergies: [...formData.allergies, formData.customAllergy.trim()],
        customAllergy: ''
      });
    }
  };

  const handleCustomChronicConditionAdd = () => {
    if (formData.customChronicCondition.trim() && !formData.chronicConditions.includes(formData.customChronicCondition.trim())) {
      setFormData({
        ...formData,
        chronicConditions: [...formData.chronicConditions, formData.customChronicCondition.trim()],
        customChronicCondition: ''
      });
    }
  };

  const validateStep = (step) => {
    switch (step) {
      case 1:
        return formData.name && formData.email && formData.password && 
               formData.confirmPassword && formData.agreeTerms &&
               formData.password === formData.confirmPassword;
      case 2:
        return formData.age && formData.gender && formData.height && formData.weight;
      case 3:
        return true; // Optional fields
      case 4:
        return formData.wellnessGoals.length > 0;
      case 5:
        return formData.fitnessLevel && formData.dietPreference && formData.skinType;
      default:
        return false;
    }
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, 5));
    } else {
      alert('Please fill in all required fields');
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    
    try {
      if (activeTab === 'login') {
        // Handle login
        const loginData = {
          email: formData.email,
          password: formData.password
        };

        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(loginData)
        });

        const data = await response.json();

        if (data.success) {
          // Store user data in localStorage
          localStorage.setItem('user', JSON.stringify(data.user));
          localStorage.setItem('userId', data.user_id);
          
          // Dispatch custom event for AuthRoute components
          window.dispatchEvent(new Event('authChange'));
          
          setMessage('Login successful! Redirecting...');
          setTimeout(() => navigate('/'), 1500);
        } else {
          setMessage(data.message);
        }
      } else {
        // Handle signup - validate all steps first
        if (!validateStep(5)) {
          setMessage('Please complete all required fields');
          setIsLoading(false);
          return;
        }

        // Prepare signup data matching backend model
        const signupData = {
          // Basic Credentials
          name: formData.name,
          email: formData.email,
          password: formData.password,
          confirmPassword: formData.confirmPassword,
          agreeTerms: formData.agreeTerms,
          // Vital Stats
          age: parseInt(formData.age),
          gender: formData.gender,
          height: parseFloat(formData.height),
          heightUnit: formData.heightUnit,
          weight: parseFloat(formData.weight),
          weightUnit: formData.weightUnit,
          // Allergies & Medical
          allergies: formData.allergies,
          chronicConditions: formData.chronicConditions,
          // Wellness Goals
          wellnessGoals: formData.wellnessGoals,
          // Lifestyle & Preferences
          fitnessLevel: formData.fitnessLevel,
          dietPreference: formData.dietPreference,
          skinType: formData.skinType,
          smartCartOptIn: formData.smartCartOptIn
        };

        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/signup`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(signupData)
        });

        const data = await response.json();

        if (data.success) {
          // Store user data and redirect
          localStorage.setItem('user', JSON.stringify(data.user));
          localStorage.setItem('userId', data.user_id);
          
          // Dispatch custom event for AuthRoute components
          window.dispatchEvent(new Event('authChange'));
          
          setMessage('Registration successful! Redirecting...');
          setTimeout(() => navigate('/'), 1500);
        } else {
          setMessage(data.message);
          setCurrentStep(1); // Reset to first step on error
        }
      }
    } catch (error) {
      console.error('Authentication error:', error);
      setMessage(activeTab === 'login' ? 'Login failed. Please try again.' : 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const wellnessGoalOptions = [
    { id: 'muscle-gain', label: 'Muscle Gain', icon: '💪' },
    { id: 'fat-loss', label: 'Fat Loss', icon: '🔥' },
    { id: 'glowing-skin', label: 'Glowing Skin', icon: '✨' },
    { id: 'acne-control', label: 'Acne Control', icon: '🎯' },
    { id: 'anti-aging', label: 'Anti-Aging', icon: '🧴' },
    { id: 'boost-immunity', label: 'Boost Immunity', icon: '🛡️' },
    { id: 'manage-diabetes', label: 'Manage Health', icon: '📊' },
    { id: 'improve-flexibility', label: 'Improve Flexibility', icon: '🤸' },
    { id: 'healthy-aging', label: 'Healthy Aging', icon: '🌱' },
    { id: 'general-fitness', label: 'General Fitness', icon: '🏃' }
  ];

  const chronicConditionOptions = [
    'PCOS', 'Diabetes', 'Asthma', 'Hypertension', 'Thyroid', 
    'Arthritis', 'Heart Disease', 'None'
  ];

  const commonAllergies = [
    'Nuts', 'Dairy', 'Gluten', 'Shellfish', 'Eggs', 'Soy', 'Fish', 'Peanuts'
  ];



  const renderSignupStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Basic Credentials</h3>
            
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Full Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                placeholder="Enter your name"
                required
              />
            </div>

            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                placeholder="Enter your email"
                required
              />
            </div>

            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                placeholder="Create a password"
                required
              />
            </div>

            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                placeholder="Confirm your password"
                required
              />
            </div>

            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                name="agreeTerms"
                checked={formData.agreeTerms}
                onChange={handleInputChange}
                className="mt-1 w-4 h-4 text-amber-400 bg-white/10 border-white/20 rounded focus:ring-amber-400"
                required
              />
              <label className="text-white/80 text-sm">
                I agree to the <span className="text-amber-400 hover:text-amber-300 cursor-pointer">Terms and Privacy Policy</span>
              </label>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-8">
            <h3 className="text-xl font-semibold text-white mb-6">Vital Stats</h3>
            
            {/* Age Section */}
            <div className="w-full">
              <label className="block text-white/80 text-sm font-medium mb-3">Age</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                placeholder="Age in years"
                min="1"
                max="120"
                required
              />
            </div>

            {/* Gender Section */}
            <div className="w-full">
              <label className="block text-white/80 text-sm font-medium mb-3">Gender</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                required
              >
                <option value="" className="bg-gray-800">Select gender</option>
                <option value="male" className="bg-gray-800">Male</option>
                <option value="female" className="bg-gray-800">Female</option>
                <option value="other" className="bg-gray-800">Other</option>
                <option value="prefer-not-to-say" className="bg-gray-800">Prefer not to say</option>
              </select>
            </div>

            {/* Height Section */}
            <div className="w-full">
              <label className="block text-white/80 text-sm font-medium mb-3">Height</label>
              <div className="flex space-x-3">
                <input
                  type="number"
                  name="height"
                  value={formData.height}
                  onChange={handleInputChange}
                  className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                  placeholder="Height"
                  step="0.1"
                  required
                />
                <select
                  name="heightUnit"
                  value={formData.heightUnit}
                  onChange={handleInputChange}
                  className="px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-amber-400"
                >
                  <option value="cm" className="bg-gray-800">cm</option>
                  <option value="feet" className="bg-gray-800">feet</option>
                </select>
              </div>
            </div>

            {/* Weight Section */}
            <div className="w-full">
              <label className="block text-white/80 text-sm font-medium mb-3">Weight</label>
              <div className="flex space-x-3">
                <input
                  type="number"
                  name="weight"
                  value={formData.weight}
                  onChange={handleInputChange}
                  className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                  placeholder="Weight"
                  step="0.1"
                  required
                />
                <select
                  name="weightUnit"
                  value={formData.weightUnit}
                  onChange={handleInputChange}
                  className="px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-amber-400"
                >
                  <option value="kg" className="bg-gray-800">kg</option>
                  <option value="lbs" className="bg-gray-800">lbs</option>
                </select>
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-white mb-4">Allergies & Medical</h3>
            
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Allergies</label>
              <div className="flex flex-wrap gap-2 mb-3">
                {commonAllergies.map(allergy => (
                  <button
                    key={allergy}
                    type="button"
                    onClick={() => handleAllergyAdd(allergy)}
                    className={`px-3 py-1 rounded-full text-sm transition-all ${
                      formData.allergies.includes(allergy)
                        ? 'bg-amber-400 text-gray-900'
                        : 'bg-white/10 text-white/80 hover:bg-white/20'
                    }`}
                  >
                    {allergy}
                  </button>
                ))}
              </div>
              
              {/* Custom Allergy Input */}
              <div className="mb-3">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    name="customAllergy"
                    value={formData.customAllergy}
                    onChange={handleInputChange}
                    className="flex-1 px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                    placeholder="Add custom allergy..."
                  />
                  <button
                    type="button"
                    onClick={handleCustomAllergyAdd}
                    className="px-4 py-2 bg-amber-400 text-gray-900 rounded-lg hover:bg-amber-500 transition-all font-medium"
                  >
                    Add
                  </button>
                </div>
              </div>

              {formData.allergies.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.allergies.map(allergy => (
                    <span
                      key={allergy}
                      className="px-3 py-1 bg-amber-400/20 text-amber-300 rounded-full text-sm flex items-center space-x-2"
                    >
                      <span>{allergy}</span>
                      <button
                        type="button"
                        onClick={() => handleAllergyRemove(allergy)}
                        className="text-amber-300 hover:text-white"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Chronic Conditions</label>
              <div className="grid grid-cols-2 gap-2 mb-3">
                {chronicConditionOptions.map(condition => (
                  <label key={condition} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.chronicConditions.includes(condition)}
                      onChange={() => handleMultiSelect('chronicConditions', condition)}
                      className="w-4 h-4 text-amber-400 bg-white/10 border-white/20 rounded focus:ring-amber-400"
                    />
                    <span className="text-white/80 text-sm">{condition}</span>
                  </label>
                ))}
              </div>

              {/* Custom Chronic Condition Input */}
              <div className="mb-3">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    name="customChronicCondition"
                    value={formData.customChronicCondition}
                    onChange={handleInputChange}
                    className="flex-1 px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                    placeholder="Add custom chronic condition..."
                  />
                  <button
                    type="button"
                    onClick={handleCustomChronicConditionAdd}
                    className="px-4 py-2 bg-amber-400 text-gray-900 rounded-lg hover:bg-amber-500 transition-all font-medium"
                  >
                    Add
                  </button>
                </div>
              </div>

              {formData.chronicConditions.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.chronicConditions.map(condition => (
                    <span
                      key={condition}
                      className="px-3 py-1 bg-blue-400/20 text-blue-300 rounded-full text-sm flex items-center space-x-2"
                    >
                      <span>{condition}</span>
                      <button
                        type="button"
                        onClick={() => handleMultiSelect('chronicConditions', condition)}
                        className="text-blue-300 hover:text-white"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Wellness Goals</h3>
            <p className="text-white/60 text-sm mb-4">Select your wellness goals ({formData.wellnessGoals.length} selected)</p>
            
            <div className="grid grid-cols-2 gap-3">
              {wellnessGoalOptions.map(goal => (
                <button
                  key={goal.id}
                  type="button"
                  onClick={() => handleGoalsSelect(goal.id)}
                  className={`p-4 rounded-xl border-2 transition-all text-left cursor-pointer ${
                    formData.wellnessGoals.includes(goal.id)
                      ? 'border-amber-400 bg-amber-400/20 text-white'
                      : 'border-white/20 bg-white/10 text-white/80 hover:bg-white/20'
                  }`}
                >
                  <div className="text-2xl mb-2">{goal.icon}</div>
                  <div className="font-medium text-sm">{goal.label}</div>
                </button>
              ))}
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Lifestyle & Preferences</h3>
            
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Fitness Level</label>
              <div className="grid grid-cols-3 gap-2">
                {['beginner', 'intermediate', 'advanced'].map(level => (
                  <label key={level} className="cursor-pointer">
                    <input
                      type="radio"
                      name="fitnessLevel"
                      value={level}
                      checked={formData.fitnessLevel === level}
                      onChange={handleInputChange}
                      className="sr-only"
                    />
                    <div className={`p-3 rounded-lg border-2 text-center transition-all capitalize ${
                      formData.fitnessLevel === level
                        ? 'border-amber-400 bg-amber-400/20 text-white'
                        : 'border-white/20 bg-white/10 text-white/80 hover:bg-white/20'
                    }`}>
                      {level}
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Diet Preference</label>
              <select
                name="dietPreference"
                value={formData.dietPreference}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                required
              >
                <option value="" className="bg-gray-800">Select diet preference</option>
                <option value="vegetarian" className="bg-gray-800">Vegetarian</option>
                <option value="non-vegetarian" className="bg-gray-800">Non-Vegetarian</option>
                <option value="vegan" className="bg-gray-800">Vegan</option>
                <option value="keto" className="bg-gray-800">Keto</option>
                <option value="jain" className="bg-gray-800">Jain</option>
                <option value="gluten-free" className="bg-gray-800">Gluten-Free</option>
              </select>
            </div>

            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">Skin Type</label>
              <select
                name="skinType"
                value={formData.skinType}
                onChange={handleInputChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                required
              >
                <option value="" className="bg-gray-800">Select skin type</option>
                <option value="dry" className="bg-gray-800">Dry</option>
                <option value="oily" className="bg-gray-800">Oily</option>
                <option value="combination" className="bg-gray-800">Combination</option>
                <option value="sensitive" className="bg-gray-800">Sensitive</option>
                <option value="not-sure" className="bg-gray-800">Not Sure</option>
              </select>
            </div>

            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                name="smartCartOptIn"
                checked={formData.smartCartOptIn}
                onChange={handleInputChange}
                className="mt-1 w-4 h-4 text-amber-400 bg-white/10 border-white/20 rounded focus:ring-amber-400"
              />
              <label className="text-white/80 text-sm">
                Allow Smart Cart to recommend items weekly
              </label>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      <VideoBackground 
        videoSrc="/video/login.mp4" 
        overlay="bg-black/40"
      />
      
      <div className="relative min-h-screen flex items-center justify-center p-4 pt-16">
        {/* Title Section - Moved Higher */}
        <div className="absolute top-20 left-1/2 transform -translate-x-1/2 text-center z-10">
          <h1 className="text-3xl lg:text-4xl font-bold text-white mb-2">
            Welcome to <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">Nutracía</span>
          </h1>
          <p className="text-lg text-white/80">
            Your AI-powered wellness platform
          </p>
        </div>

        <div className="max-w-6xl w-full grid lg:grid-cols-5 gap-6 items-center mt-16">
          {/* Left Bento Boxes - Smaller and Narrower */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="lg:col-span-1 space-y-3"
          >
            {/* AI Chatbot */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="bg-white/10 backdrop-blur-md rounded-lg p-3 border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-blue-400 to-blue-600 flex items-center justify-center mb-2">
                <MessageCircle size={16} className="text-white" />
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">AI Health Chatbot</h3>
              <p className="text-xs text-white/70">OpenAI-powered wellness assistant</p>
            </motion.div>

            {/* Workout Plans */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-white/10 backdrop-blur-md rounded-lg p-3 border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-red-400 to-red-600 flex items-center justify-center mb-2">
                <Dumbbell size={16} className="text-white" />
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">Workout Plans</h3>
              <p className="text-xs text-white/70">Customized fitness routines</p>
            </motion.div>

            {/* Diet Plans */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="bg-white/10 backdrop-blur-md rounded-lg p-3 border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-yellow-400 to-yellow-600 flex items-center justify-center mb-2">
                <Apple size={16} className="text-white" />
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">Diet Plans</h3>
              <p className="text-xs text-white/70">Nutrition guidance & meal plans</p>
            </motion.div>
          </motion.div>

          {/* Center - Auth Form (Hero Section) */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="lg:col-span-3 bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 max-h-[75vh] overflow-y-auto shadow-2xl"
          >
            {/* Tab Switcher */}
            <div className="flex mb-6 bg-white/10 rounded-xl p-1">
              <button
                onClick={() => setActiveTab('login')}
                className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-300 ${
                  activeTab === 'login'
                    ? 'bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-lg'
                    : 'text-white/70 hover:text-white'
                }`}
              >
                Login
              </button>
              <button
                onClick={() => {
                  setActiveTab('signup');
                  setCurrentStep(1);
                }}
                className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-300 ${
                  activeTab === 'signup'
                    ? 'bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-lg'
                    : 'text-white/70 hover:text-white'
                }`}
              >
                Sign Up
              </button>
            </div>

            {/* Progress Bar for Signup */}
            {activeTab === 'signup' && (
              <div className="mb-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-white/60">Step {currentStep} of 5</span>
                  <span className="text-sm text-white/60">{Math.round((currentStep / 5) * 100)}%</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-amber-400 to-orange-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentStep / 5) * 100}%` }}
                  />
                </div>
              </div>
            )}

            {/* Message Display */}
            {message && (
              <div className={`p-3 rounded-lg mb-4 text-center ${
                message.includes('successful') || message.includes('Redirecting')
                  ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
                  : 'bg-red-500/20 text-red-300 border border-red-500/30'
              }`}>
                {message}
              </div>
            )}

            {/* Form Content */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {activeTab === 'login' ? (
                // Login Form (unchanged)
                <>
                  <div>
                    <label className="block text-white/80 text-sm font-medium mb-2">Email Address</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                      placeholder="Enter your email"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-white/80 text-sm font-medium mb-2">Password</label>
                    <input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-amber-400 focus:ring-2 focus:ring-amber-400/20 transition-all"
                      placeholder="Enter your password"
                      required
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-3 px-6 bg-gradient-to-r from-amber-400 to-orange-500 text-white font-semibold rounded-lg hover:from-amber-500 hover:to-orange-600 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? 'Logging in...' : 'Login to Nutracía'}
                  </button>
                </>
              ) : (
                // Multi-step Signup Form
                <>
                  {renderSignupStep()}
                  
                  {/* Navigation Buttons */}
                  <div className="flex justify-between pt-4">
                    {currentStep > 1 && (
                      <button
                        type="button"
                        onClick={prevStep}
                        className="px-6 py-2 bg-white/10 text-white/80 rounded-lg hover:bg-white/20 transition-all"
                      >
                        Previous
                      </button>
                    )}
                    
                    <div className="ml-auto">
                      {currentStep < 5 ? (
                        <button
                          type="button"
                          onClick={nextStep}
                          className="px-6 py-2 bg-gradient-to-r from-amber-400 to-orange-500 text-white font-semibold rounded-lg hover:from-amber-500 hover:to-orange-600 transition-all"
                        >
                          Next
                        </button>
                      ) : (
                        <button
                          type="submit"
                          disabled={isLoading}
                          className="px-6 py-2 bg-gradient-to-r from-amber-400 to-orange-500 text-white font-semibold rounded-lg hover:from-amber-500 hover:to-orange-600 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {isLoading ? 'Creating Account...' : 'Join Nutracía'}
                        </button>
                      )}
                    </div>
                  </div>
                </>
              )}
            </form>

            <div className="mt-6 text-center">
              <p className="text-white/60 text-sm">
                {activeTab === 'login' ? "Don't have an account? " : "Already have an account? "}
                <button
                  onClick={() => {
                    setActiveTab(activeTab === 'login' ? 'signup' : 'login');
                    setCurrentStep(1);
                  }}
                  className="text-amber-400 hover:text-amber-300 font-medium"
                >
                  {activeTab === 'login' ? 'Sign up' : 'Login'}
                </button>
              </p>
            </div>
          </motion.div>

          {/* Right Bento Boxes - Smaller and Narrower */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="lg:col-span-1 space-y-3"
          >
            {/* Smart Grocery Shopping */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="bg-white/10 backdrop-blur-md rounded-lg p-3 border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-green-400 to-green-600 flex items-center justify-center mb-2">
                <ShoppingCart size={16} className="text-white" />
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">Smart Grocery Shopping</h3>
              <p className="text-xs text-white/70">AI-powered recommendations</p>
            </motion.div>

            {/* Skincare Routines */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-white/10 backdrop-blur-md rounded-lg p-3 border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-pink-400 to-pink-600 flex items-center justify-center mb-2">
                <Sparkles size={16} className="text-white" />
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">Skincare Routines</h3>
              <p className="text-xs text-white/70">Personalized beauty advice</p>
            </motion.div>

            {/* Health Management */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="bg-white/10 backdrop-blur-md rounded-lg p-3 border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-purple-400 to-purple-600 flex items-center justify-center mb-2">
                <Heart size={16} className="text-white" />
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">Health Management</h3>
              <p className="text-xs text-white/70">Comprehensive health tracking</p>
            </motion.div>
          </motion.div>
        </div>
      </div>
      <EnhancedAIChatbot />
    </div>
  );
};

// Mind & Soul Page Component - Unique Dashboard Layout
const MindSoulPage = () => {
  // State management for all Mind & Soul features
  const [currentUser, setCurrentUser] = useState(null);
  const [meditationContent, setMeditationContent] = useState([]);
  const [moodHistory, setMoodHistory] = useState([]);
  const [meditationProgress, setMeditationProgress] = useState({});
  const [userHabits, setUserHabits] = useState([]);
  
  // Modal and UI states
  const [selectedMeditation, setSelectedMeditation] = useState(null);
  const [isMeditationModalOpen, setMeditationModalOpen] = useState(false);
  const [showMoodTracker, setShowMoodTracker] = useState(false);
  const [isTimerActive, setIsTimerActive] = useState(false);
  const [timerDuration, setTimerDuration] = useState(10); // minutes
  const [timeRemaining, setTimeRemaining] = useState(0);
  
  // Mood tracking states
  const [todayMood, setTodayMood] = useState({
    mood: 3,
    energy: 3,
    stress: 3,
    notes: ''
  });

  // Timer functionality
  useEffect(() => {
    let interval = null;
    if (isTimerActive && timeRemaining > 0) {
      interval = setInterval(() => {
        setTimeRemaining(time => {
          if (time <= 1) {
            setIsTimerActive(false);
            // Log meditation session
            logMeditationSession();
            return 0;
          }
          return time - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTimerActive, timeRemaining]);

  // Load user and data on component mount
  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user) {
      setCurrentUser(JSON.parse(user));
    }
    loadMeditationContent();
    if (user) {
      loadUserData(JSON.parse(user).id);
    }
  }, []);

  const loadMeditationContent = async () => {
    try {
      const response = await axios.get(`${API}/mind-soul/meditation-content`);
      setMeditationContent(response.data.content);
    } catch (error) {
      console.error('Error loading meditation content:', error);
    }
  };

  const loadUserData = async (userId) => {
    try {
      // Load mood history
      const moodResponse = await axios.get(`${API}/mind-soul/mood-history/${userId}`);
      setMoodHistory(moodResponse.data.mood_history);
      
      // Load meditation progress
      const progressResponse = await axios.get(`${API}/mind-soul/meditation-progress/${userId}`);
      setMeditationProgress(progressResponse.data.progress);
      
      // Load user habits
      const habitsResponse = await axios.get(`${API}/mind-soul/habits/${userId}`);
      setUserHabits(habitsResponse.data.habits);
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const logMoodEntry = async () => {
    if (!currentUser) return;
    
    const today = new Date().toISOString().split('T')[0];
    const moodLabels = ['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy'];
    
    try {
      await axios.post(`${API}/mind-soul/mood-tracker`, {
        user_id: currentUser.id,
        date: today,
        mood: todayMood.mood,
        mood_label: moodLabels[todayMood.mood - 1],
        energy: todayMood.energy,
        stress: todayMood.stress,
        notes: todayMood.notes
      });
      setShowMoodTracker(false);
      loadUserData(currentUser.id);
    } catch (error) {
      console.error('Error logging mood:', error);
    }
  };

  const logMeditationSession = async () => {
    if (!currentUser) return;
    
    const today = new Date().toISOString().split('T')[0];
    try {
      await axios.post(`${API}/mind-soul/meditation-session`, {
        user_id: currentUser.id,
        session_type: selectedMeditation?.type || 'general',
        duration_minutes: timerDuration,
        completed: true,
        date: today,
        session_id: `session_${Date.now()}`
      });
      loadUserData(currentUser.id);
    } catch (error) {
      console.error('Error logging meditation session:', error);
    }
  };

  const startTimer = (duration) => {
    setTimerDuration(duration);
    setTimeRemaining(duration * 60); // Convert to seconds
    setIsTimerActive(true);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getMoodEmoji = (mood) => {
    const emojis = ['😢', '😔', '😐', '😊', '😄'];
    return emojis[mood - 1] || '😐';
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background */}
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{ 
          backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          filter: 'brightness(0.8)'
        }}
      />
      <div className="absolute inset-0 bg-black/30" />
      
      <div className="relative z-10 pt-24 px-4">
        <div className="max-w-7xl mx-auto">
          
          {/* Header */}
          <motion.div
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="text-center mb-8"
          >
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
              Mind & Soul
            </h1>
            <p className="text-xl text-white/80 max-w-2xl mx-auto">
              Nurture your inner peace through meditation, mindfulness, and emotional wellness
            </p>
          </motion.div>

          {/* Dashboard Grid Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            
            {/* Left Column - Mood Tracker & Progress */}
            <motion.div
              initial={{ x: -50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="space-y-6"
            >
              
              {/* Today's Mood Tracker */}
              <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 border border-white/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-white flex items-center">
                    <span className="text-2xl mr-2">🎭</span>
                    Today's Mood
                  </h3>
                  <button
                    onClick={() => setShowMoodTracker(!showMoodTracker)}
                    className="text-amber-400 hover:text-amber-300 transition-colors"
                  >
                    {showMoodTracker ? 'Cancel' : 'Track'}
                  </button>
                </div>
                
                {showMoodTracker ? (
                  <div className="space-y-4">
                    <div>
                      <label className="text-white/80 text-sm mb-2 block">Mood: {getMoodEmoji(todayMood.mood)}</label>
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={todayMood.mood}
                        onChange={(e) => setTodayMood(prev => ({...prev, mood: parseInt(e.target.value)}))}
                        className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                    
                    <div>
                      <label className="text-white/80 text-sm mb-2 block">Energy: ⚡</label>
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={todayMood.energy}
                        onChange={(e) => setTodayMood(prev => ({...prev, energy: parseInt(e.target.value)}))}
                        className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                    
                    <div>
                      <label className="text-white/80 text-sm mb-2 block">Stress: 😰</label>
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={todayMood.stress}
                        onChange={(e) => setTodayMood(prev => ({...prev, stress: parseInt(e.target.value)}))}
                        className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                    
                    <textarea
                      placeholder="Optional notes..."
                      value={todayMood.notes}
                      onChange={(e) => setTodayMood(prev => ({...prev, notes: e.target.value}))}
                      className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 resize-none"
                      rows="2"
                    />
                    
                    <button
                      onClick={logMoodEntry}
                      className="w-full py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all"
                    >
                      Save Today's Mood
                    </button>
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <div className="text-4xl mb-2">
                      {moodHistory.length > 0 ? getMoodEmoji(moodHistory[0]?.mood || 3) : '😐'}
                    </div>
                    <p className="text-white/70">
                      {moodHistory.length > 0 ? 'Last tracked mood' : 'Track your mood today'}
                    </p>
                  </div>
                )}
              </div>

              {/* Progress Summary */}
              <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                  <span className="text-2xl mr-2">📊</span>
                  Progress Summary
                </h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Total Sessions</span>
                    <span className="text-white font-semibold">{meditationProgress.total_sessions || 0}</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Total Minutes</span>
                    <span className="text-white font-semibold">{meditationProgress.total_minutes || 0}m</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">Current Streak</span>
                    <span className="text-amber-400 font-semibold">🔥 {meditationProgress.current_streak || 0} days</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-white/80">This Week</span>
                    <span className="text-green-400 font-semibold">{meditationProgress.this_week_sessions || 0} sessions</span>
                  </div>
                </div>
              </div>

            </motion.div>

            {/* Center Column - Meditation Content */}
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="lg:col-span-2"
            >
              
              {/* Meditation Timer */}
              <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 border border-white/20 mb-6">
                <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                  <span className="text-2xl mr-2">⏱️</span>
                  Meditation Timer
                </h3>
                
                <div className="flex items-center justify-center space-x-6">
                  {!isTimerActive ? (
                    <>
                      <button
                        onClick={() => startTimer(5)}
                        className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                      >
                        5 min
                      </button>
                      <button
                        onClick={() => startTimer(10)}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                      >
                        10 min
                      </button>
                      <button
                        onClick={() => startTimer(15)}
                        className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
                      >
                        15 min
                      </button>
                      <button
                        onClick={() => startTimer(20)}
                        className="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors"
                      >
                        20 min
                      </button>
                    </>
                  ) : (
                    <div className="text-center">
                      <div className="text-6xl font-mono text-white mb-4">
                        {formatTime(timeRemaining)}
                      </div>
                      <button
                        onClick={() => setIsTimerActive(false)}
                        className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                      >
                        Stop Timer
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Meditation Content Grid */}
              <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                  <span className="text-2xl mr-2">🧘‍♀️</span>
                  Meditation & Mindfulness
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {meditationContent.map((content) => (
                    <motion.div
                      key={content.id}
                      whileHover={{ y: -5, scale: 1.02 }}
                      onClick={() => {
                        setSelectedMeditation(content);
                        setMeditationModalOpen(true);
                      }}
                      className="bg-white/10 rounded-xl p-4 border border-white/20 cursor-pointer hover:bg-white/20 transition-all duration-300"
                    >
                      <div className="flex items-start space-x-3">
                        <div className="w-12 h-12 rounded-full bg-gradient-to-r from-purple-400 to-pink-400 flex items-center justify-center flex-shrink-0">
                          <span className="text-xl">
                            {content.type === 'breathing_exercise' ? '🫁' :
                             content.type === 'guided_meditation' ? '🧘‍♀️' :
                             content.type === 'mindfulness' ? '🧠' :
                             content.type === 'stress_relief' ? '😌' :
                             content.type === 'sleep_meditation' ? '🌙' : '✨'}
                          </span>
                        </div>
                        
                        <div className="flex-1">
                          <h4 className="text-white font-semibold mb-1">{content.title}</h4>
                          <p className="text-white/70 text-sm mb-2 line-clamp-2">{content.description}</p>
                          
                          <div className="flex items-center space-x-4 text-xs text-white/60">
                            <span>⏱️ {content.duration}</span>
                            <span>📊 {content.difficulty}</span>
                          </div>
                          
                          <div className="flex flex-wrap gap-1 mt-2">
                            {content.benefits.slice(0, 2).map((benefit, idx) => (
                              <span key={idx} className="px-2 py-1 bg-white/10 text-white/80 text-xs rounded-full">
                                {benefit}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

            </motion.div>
          </div>

        </div>
      </div>

      {/* Meditation Modal */}
      <Modal
        isOpen={isMeditationModalOpen}
        onClose={() => setMeditationModalOpen(false)}
        item={selectedMeditation}
        type="meditation"
      />

      <EnhancedAIChatbot />
    </div>
  );
};

// Quote-Only Page Components for Non-Authenticated Users

// Login Call-to-Action Component
const LoginCallToAction = ({ sectionName }) => (
  <motion.div 
    initial={{ y: 30, opacity: 0 }}
    animate={{ y: 0, opacity: 1 }}
    transition={{ duration: 0.8, delay: 0.3 }}
    className="text-center mt-12"
  >
    <div className="bg-white/10 backdrop-blur-md rounded-3xl p-8 border border-white/20 max-w-md mx-auto">
      <motion.div
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5, delay: 0.5 }}
        className="mb-6"
      >
        <h3 className="text-2xl font-bold text-white mb-3">Unlock Your {sectionName} Journey</h3>
        <p className="text-white/80 mb-6">
          Get personalized {sectionName.toLowerCase()} plans, expert guidance, and exclusive content.
        </p>
      </motion.div>
      
      <Link to="/get-started">
        <motion.button
          whileHover={{ 
            scale: 1.05,
            boxShadow: '0 0 30px rgba(251, 191, 36, 0.6)',
            backgroundColor: 'rgba(251, 191, 36, 0.9)'
          }}
          whileTap={{ scale: 0.95 }}
          className="w-full py-4 px-8 bg-gradient-to-r from-amber-400 to-orange-500 text-white font-bold rounded-full text-lg shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <span className="flex items-center justify-center space-x-2">
            <span>Login to Access More Features</span>
            <motion.svg 
              className="w-5 h-5" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              whileHover={{ x: 3 }}
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </motion.svg>
          </span>
        </motion.button>
      </Link>
    </div>
  </motion.div>
);

// Quote-Only Pages
const WorkoutQuotePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <VideoBackground 
      videoSrc="/video/workout.mp4" 
      overlay="bg-black/60"
    />
    
    <div className="relative z-10 pt-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20 mb-8">
            <h1 className="text-6xl md:text-7xl font-['Great_Vibes'] text-white mb-8 leading-tight">
              "Push beyond yesterday, embrace tomorrow's strength."
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-amber-400 to-orange-500 mx-auto rounded-full"></div>
          </div>
        </motion.div>
        
        <LoginCallToAction sectionName="Workout" />
      </div>
    </div>
  </div>
);

const SkincareQuotePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <VideoBackground 
      videoSrc="/video/skincare.mp4" 
      overlay="bg-black/50"
    />
    
    <div className="relative z-10 pt-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20 mb-8">
            <h1 className="text-6xl md:text-7xl font-['Great_Vibes'] text-white mb-8 leading-tight">
              "Radiance is your right, glow is your gift."
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-pink-400 to-purple-500 mx-auto rounded-full"></div>
          </div>
        </motion.div>
        
        <LoginCallToAction sectionName="Skincare" />
      </div>
    </div>
  </div>
);

const MindSoulQuotePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <div 
      className="absolute inset-0 bg-cover bg-center"
      style={{ 
        backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        filter: 'brightness(0.6)'
      }}
    />
    <div className="absolute inset-0 bg-black/40" />
    
    <div className="relative z-10 pt-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20 mb-8">
            <h1 className="text-6xl md:text-7xl font-['Great_Vibes'] text-white mb-8 leading-tight">
              "Peace comes from within, mindfulness is the key."
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-purple-400 to-pink-500 mx-auto rounded-full"></div>
          </div>
        </motion.div>
        
        <LoginCallToAction sectionName="Mind & Soul" />
      </div>
    </div>
  </div>
);

const DietQuotePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <VideoBackground 
      videoSrc="/video/diet.mp4" 
      overlay="bg-black/55"
    />
    
    <div className="relative z-10 pt-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20 mb-8">
            <h1 className="text-6xl md:text-7xl font-['Great_Vibes'] text-white mb-8 leading-tight">
              "Eat vibrant, live radiant, nourish your soul."
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-green-400 to-blue-500 mx-auto rounded-full"></div>
          </div>
        </motion.div>
        
        <LoginCallToAction sectionName="Nutrition" />
      </div>
    </div>
  </div>
);

const HealthQuotePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <VideoBackground 
      videoSrc="/video/health.mp4" 
      overlay="bg-black/60"
    />
    
    <div className="relative z-10 pt-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20 mb-8">
            <h1 className="text-6xl md:text-7xl font-['Great_Vibes'] text-white mb-8 leading-tight">
              "Wellness is wealth, health is your treasure."
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-red-400 to-pink-500 mx-auto rounded-full"></div>
          </div>
        </motion.div>
        
        <LoginCallToAction sectionName="Health" />
      </div>
    </div>
  </div>
);

const OrderUpQuotePage = () => (
  <div className="min-h-screen relative overflow-hidden">
    <div 
      className="absolute inset-0 bg-cover bg-center"
      style={{ backgroundImage: `url(${backgrounds.orderup})` }}
    />
    <div className="absolute inset-0 bg-black/65" />
    
    <div className="relative z-10 pt-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20 mb-8">
            <h1 className="text-6xl md:text-7xl font-['Great_Vibes'] text-white mb-8 leading-tight">
              "Smart shopping starts with understanding you."
            </h1>
            <div className="w-24 h-1 bg-gradient-to-r from-blue-400 to-cyan-500 mx-auto rounded-full"></div>
          </div>
        </motion.div>
        
        <LoginCallToAction sectionName="Smart Shopping" />
      </div>
    </div>
  </div>
);

// Authentication-aware Route Component
const AuthRoute = ({ children, quotePage }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null); // null means loading
  
  useEffect(() => {
    const checkAuth = () => {
      try {
        const user = localStorage.getItem('user');
        const userId = localStorage.getItem('userId');
        const isAuth = !!(user && userId);
        console.log('AuthRoute check:', { user: !!user, userId: !!userId, isAuth }); // Debug log
        setIsAuthenticated(isAuth);
      } catch (error) {
        console.error('Auth check error:', error);
        setIsAuthenticated(false);
      }
    };
    
    // Check immediately
    checkAuth();
    
    // Listen for custom auth events
    const handleAuthChange = () => {
      console.log('Auth change event received'); // Debug log
      checkAuth();
    };
    
    window.addEventListener('authChange', handleAuthChange);
    
    return () => {
      window.removeEventListener('authChange', handleAuthChange);
    };
  }, []);
  
  // Show loading state while determining auth status
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-amber-400 mx-auto mb-4"></div>
          <p className="text-white/70">Loading...</p>
        </div>
      </div>
    );
  }
  
  console.log('AuthRoute rendering:', { isAuthenticated, showingQuote: !isAuthenticated }); // Debug log
  return isAuthenticated ? children : quotePage;
};

// Main App Component
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route 
            path="/workout" 
            element={
              <AuthRoute quotePage={<WorkoutQuotePage />}>
                <WorkoutPage />
              </AuthRoute>
            } 
          />
          <Route 
            path="/mind-soul" 
            element={
              <AuthRoute quotePage={<MindSoulQuotePage />}>
                <MindSoulPage />
              </AuthRoute>
            } 
          />
          <Route 
            path="/skincare" 
            element={
              <AuthRoute quotePage={<SkincareQuotePage />}>
                <SkincarePage />
              </AuthRoute>
            } 
          />
          <Route 
            path="/diet" 
            element={
              <AuthRoute quotePage={<DietQuotePage />}>
                <DietPage />
              </AuthRoute>
            } 
          />
          <Route 
            path="/health" 
            element={
              <AuthRoute quotePage={<HealthQuotePage />}>
                <HealthPage />
              </AuthRoute>
            } 
          />
          <Route 
            path="/order-up" 
            element={
              <AuthRoute quotePage={<OrderUpQuotePage />}>
                <GroceryAgent />
              </AuthRoute>
            } 
          />
          <Route path="/get-started" element={<GetStartedPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;