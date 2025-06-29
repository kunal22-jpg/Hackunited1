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
  MessageCircle
} from 'lucide-react';
import CircularGallery from './CircularGallery';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

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
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-4"
      onClick={onClose}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
      
      {/* Profile Modal */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        className="relative bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-2xl max-w-md w-full max-h-[80vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-all"
        >
          <X size={20} className="text-white" />
        </button>

        {/* Profile Header */}
        <div className="text-center mb-6">
          <div className="w-20 h-20 bg-gradient-to-r from-amber-400 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <User size={32} className="text-white" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-1">{user.name}</h2>
          <p className="text-white/70">{user.email}</p>
        </div>

        {/* Profile Details */}
        <div className="space-y-4">
          {/* Basic Info */}
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-white mb-3">Basic Information</h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-white/60">Age:</span>
                <p className="text-white font-medium">{user.age}</p>
              </div>
              <div>
                <span className="text-white/60">Gender:</span>
                <p className="text-white font-medium">{user.gender}</p>
              </div>
              <div>
                <span className="text-white/60">Height:</span>
                <p className="text-white font-medium">{user.height} {user.height_unit || 'cm'}</p>
              </div>
              <div>
                <span className="text-white/60">Weight:</span>
                <p className="text-white font-medium">{user.weight} {user.weight_unit || 'kg'}</p>
              </div>
            </div>
          </div>

          {/* Wellness Goals */}
          {user.goals && user.goals.length > 0 && (
            <div className="bg-white/5 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-3">Wellness Goals</h3>
              <div className="flex flex-wrap gap-2">
                {user.goals.map((goal, index) => (
                  <span key={index} className="px-3 py-1 bg-amber-400/20 text-amber-300 rounded-full text-sm">
                    {goal}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Health Information */}
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-white mb-3">Health & Preferences</h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-white/60">Fitness Level:</span>
                <p className="text-white font-medium">{user.fitness_level || 'Not specified'}</p>
              </div>
              <div>
                <span className="text-white/60">Diet Type:</span>
                <p className="text-white font-medium">{user.diet_type || 'Not specified'}</p>
              </div>
              <div>
                <span className="text-white/60">Skin Type:</span>
                <p className="text-white font-medium">{user.skin_type || 'Not specified'}</p>
              </div>
            </div>
          </div>

          {/* Allergies */}
          {user.allergies && user.allergies.length > 0 && (
            <div className="bg-white/5 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-3">Allergies</h3>
              <div className="flex flex-wrap gap-2">
                {user.allergies.map((allergy, index) => (
                  <span key={index} className="px-3 py-1 bg-red-400/20 text-red-300 rounded-full text-sm">
                    {allergy}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Chronic Conditions */}
          {user.chronic_conditions && user.chronic_conditions.length > 0 && (
            <div className="bg-white/5 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-3">Medical Conditions</h3>
              <div className="flex flex-wrap gap-2">
                {user.chronic_conditions.map((condition, index) => (
                  <span key={index} className="px-3 py-1 bg-blue-400/20 text-blue-300 rounded-full text-sm">
                    {condition}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
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

// Modal Component
const Modal = ({ isOpen, onClose, item, type }) => {
  if (!isOpen || !item) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white/10 backdrop-blur-md rounded-3xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto border border-white/20"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-between items-start mb-6">
            <h3 className="text-2xl font-bold text-white">{item.title}</h3>
            <button 
              onClick={onClose}
              className="p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          <p className="text-white/80 mb-6">{item.description}</p>

          {type === 'workout' && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/10 rounded-lg p-4">
                  <div className="flex items-center space-x-2 text-white">
                    <Clock size={18} />
                    <span>{item.duration} minutes</span>
                  </div>
                </div>
                <div className="bg-white/10 rounded-lg p-4">
                  <div className="flex items-center space-x-2 text-white">
                    <Star size={18} />
                    <span className="capitalize">{item.difficulty}</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Muscle Groups:</h4>
                <div className="flex flex-wrap gap-2">
                  {item.muscle_groups?.map((group, idx) => (
                    <span key={idx} className="bg-orange-500/20 text-orange-200 px-3 py-1 rounded-full text-sm capitalize">
                      {group}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Instructions:</h4>
                <ul className="space-y-2">
                  {item.instructions?.map((instruction, idx) => (
                    <li key={idx} className="text-white/80">• {instruction}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {type === 'skincare' && (
            <div className="space-y-4">
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Skin Type:</h4>
                <span className="bg-pink-500/20 text-pink-200 px-3 py-1 rounded-full text-sm capitalize">
                  {item.skin_type}
                </span>
              </div>
              
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Steps:</h4>
                <ol className="space-y-2">
                  {item.steps?.map((step, idx) => (
                    <li key={idx} className="text-white/80">{idx + 1}. {step}</li>
                  ))}
                </ol>
              </div>
            </div>
          )}

          {type === 'diet' && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/10 rounded-lg p-4">
                  <div className="text-white">
                    <div className="text-2xl font-bold">{item.calories}</div>
                    <div className="text-sm text-white/80">Calories</div>
                  </div>
                </div>
                <div className="bg-white/10 rounded-lg p-4">
                  <div className="text-white">
                    <div className="text-2xl font-bold">{item.prep_time}</div>
                    <div className="text-sm text-white/80">Minutes</div>
                  </div>
                </div>
              </div>

              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Ingredients:</h4>
                <div className="flex flex-wrap gap-2">
                  {item.ingredients?.map((ingredient, idx) => (
                    <span key={idx} className="bg-green-500/20 text-green-200 px-3 py-1 rounded-full text-sm">
                      {ingredient}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {type === 'health' && (
            <div className="space-y-4">
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Daily Routine:</h4>
                <ul className="space-y-2">
                  {item.daily_routine?.map((routine, idx) => (
                    <li key={idx} className="text-white/80">• {routine}</li>
                  ))}
                </ul>
              </div>
              
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">Lifestyle Tips:</h4>
                <ul className="space-y-2">
                  {item.lifestyle_tips?.map((tip, idx) => (
                    <li key={idx} className="text-white/80">• {tip}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div className="mt-6 flex justify-center">
            <button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-3 rounded-full font-semibold hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 flex items-center space-x-2">
              <Play size={18} />
              <span>Watch Demo</span>
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

// New Circular Gallery Component using OGL
const CircularGalleryOGL = ({ items, onItemClick, type }) => {
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

  // Transform items to match the expected format for the new component
  const transformedItems = items.map(item => ({
    image: `https://picsum.photos/seed/${item.id || Math.random()}/800/600?grayscale`,
    text: item.title || item.name || 'Item'
  }));

  // Try to use WebGL gallery, fallback to grid if needed
  try {
    return (
      <div style={{ height: '600px', position: 'relative' }}>
        <CircularGallery 
          items={transformedItems}
          bend={3} 
          textColor="#ffffff" 
          borderRadius={0.05} 
        />
      </div>
    );
  } catch (error) {
    console.error("Error rendering WebGL gallery, falling back to grid view:", error);
    // Fallback to grid view if WebGL fails
    return (
      <div className="h-96 overflow-y-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {items.map((item, index) => (
            <motion.div
              key={item.id || index}
              whileHover={{ scale: 1.05, rotateY: 5 }}
              whileTap={{ scale: 0.95 }}
              className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/20 cursor-pointer card-hover"
              onClick={() => onItemClick(item)}
            >
              <div 
                className="h-24 bg-cover bg-center rounded-lg mb-3 border-2 border-white/20"
                style={{ backgroundImage: `url(${backgrounds[type] || backgrounds.home})` }}
              />
              <h4 className="text-white font-semibold text-sm mb-2 line-clamp-2">{item.title}</h4>
              <p className="text-white/70 text-xs line-clamp-2">{item.description}</p>
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
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [personalizedWorkouts, setPersonalizedWorkouts] = useState([]);
  const [isGeneratingPersonalized, setIsGeneratingPersonalized] = useState(false);
  const [showPersonalized, setShowPersonalized] = useState(false);

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      const response = await axios.get(`${API}/workouts`);
      setWorkouts(response.data);
    } catch (error) {
      console.error('Error fetching workouts:', error);
    }
  };

  const generatePersonalizedRecommendations = async () => {
    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    if (!userData.id) {
      alert('Please login to generate personalized recommendations');
      return;
    }

    setIsGeneratingPersonalized(true);
    try {
      const personalizedRequest = {
        user_id: userData.id,
        weight: userData.weight ? `${userData.weight} ${userData.weight_unit || 'kg'}` : '70 kg',
        allergies: userData.allergies ? userData.allergies.join(', ') : 'none',
        wellness_goals: userData.goals || ['general fitness'],
        health_conditions: userData.chronic_conditions || [],
        age: userData.age || 25,
        gender: userData.gender || 'male',
        fitness_level: userData.fitness_level || 'beginner'
      };

      const response = await axios.post(`${API}/wellness/personalized-recommendations`, personalizedRequest);
      
      if (response.data.success) {
        setPersonalizedWorkouts(response.data.recommendations.workout || []);
        setShowPersonalized(true);
      } else {
        alert('Failed to generate personalized recommendations. Please try again.');
      }
    } catch (error) {
      console.error('Error generating personalized recommendations:', error);
      alert('Error generating recommendations. Please try again.');
    }
    setIsGeneratingPersonalized(false);
  };

  const handleWorkoutClick = (workout) => {
    setSelectedWorkout(workout);
    setIsModalOpen(true);
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
      className="min-h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/workout.mp4" 
        overlay="bg-black/50"
      />
      
      <div className="relative z-10 pt-20 px-6">
        <div className="max-w-screen-2xl mx-auto">
          <div className="text-center mb-3">
            <h1 className="text-3xl font-bold text-white mb-4">Workout Plans</h1>
            <p className="text-lg text-white/80">Personalized fitness routines for every goal</p>
          </div>

          {workouts.length > 0 && (
            <CircularGalleryOGL 
              items={workouts}
              onItemClick={handleWorkoutClick}
              type="workout"
            />
          )}
        </div>
      </div>

      <Modal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        item={selectedWorkout}
        type="workout"
      />
    </div>
  );
};

const SkincarePage = () => {
  const [routines, setRoutines] = useState([]);
  const [selectedRoutine, setSelectedRoutine] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchRoutines();
  }, []);

  const fetchRoutines = async () => {
    try {
      const response = await axios.get(`${API}/skincare`);
      setRoutines(response.data);
    } catch (error) {
      console.error('Error fetching skincare routines:', error);
    }
  };

  const handleRoutineClick = (routine) => {
    setSelectedRoutine(routine);
    setIsModalOpen(true);
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
      className="min-h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/skincare.mp4" 
        overlay="bg-black/40"
      />
      
      <div className="relative z-10 pt-20 px-6">
        <div className="max-w-screen-2xl mx-auto">
          <div className="text-center mb-3">
            <h1 className="text-3xl font-bold text-white mb-4">Skincare Routines</h1>
            <p className="text-lg text-white/80">Glow with science-backed skincare</p>
          </div>

          {routines.length > 0 && (
            <CircularGalleryOGL 
              items={routines}
              onItemClick={handleRoutineClick}
              type="skincare"
            />
          )}
        </div>
      </div>

      <Modal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        item={selectedRoutine}
        type="skincare"
      />
    </div>
  );
};

const DietPage = () => {
  const [meals, setMeals] = useState([]);
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchMeals();
  }, []);

  const fetchMeals = async () => {
    try {
      const response = await axios.get(`${API}/meals`);
      setMeals(response.data);
    } catch (error) {
      console.error('Error fetching meals:', error);
    }
  };

  const handleMealClick = (meal) => {
    setSelectedMeal(meal);
    setIsModalOpen(true);
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
      className="min-h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/diet.mp4" 
        overlay="bg-black/50"
      />
      
      <div className="relative z-10 pt-20 px-6">
        <div className="max-w-screen-2xl mx-auto">
          <div className="text-center mb-3">
            <h1 className="text-3xl font-bold text-white mb-4">Diet Plans</h1>
            <p className="text-lg text-white/80">Nutrition that fuels your potential</p>
          </div>

          {meals.length > 0 && (
            <CircularGalleryOGL 
              items={meals}
              onItemClick={handleMealClick}
              type="diet"
            />
          )}
        </div>
      </div>

      <Modal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        item={selectedMeal}
        type="diet"
      />
    </div>
  );
};

const HealthPage = () => {
  const [conditions, setConditions] = useState([]);
  const [selectedCondition, setSelectedCondition] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchConditions();
  }, []);

  const fetchConditions = async () => {
    try {
      const response = await axios.get(`${API}/health-conditions`);
      setConditions(response.data);
    } catch (error) {
      console.error('Error fetching health conditions:', error);
    }
  };

  const handleConditionClick = (condition) => {
    setSelectedCondition(condition);
    setIsModalOpen(true);
  };

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

  return (
    <div 
      className="min-h-screen relative overflow-hidden"
      onMouseEnter={() => handleSectionHover(true)}
      onMouseLeave={() => handleSectionHover(false)}
    >
      <VideoBackground 
        videoSrc="/video/health.mp4" 
        overlay="bg-black/50"
      />
      
      <div className="relative z-10 pt-20 px-6">
        <div className="max-w-screen-2xl mx-auto">
          <div className="text-center mb-3">
            <h1 className="text-3xl font-bold text-white mb-4">Health Conditions</h1>
            <p className="text-lg text-white/80">Personalized support for your health journey</p>
          </div>

          {conditions.length > 0 && (
            <CircularGalleryOGL 
              items={conditions}
              onItemClick={handleConditionClick}
              type="health"
            />
          )}
        </div>
      </div>

      <Modal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        item={selectedCondition}
        type="health"
      />
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