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
import { Carousel as CircularCarousel } from 'react-circular-carousel-ts';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Background images from vision expert
const backgrounds = {
  home: 'https://images.pexels.com/photos/1051838/pexels-photo-1051838.jpeg',
  workout: 'https://images.pexels.com/photos/289586/pexels-photo-289586.jpeg',
  skincare: 'https://images.unsplash.com/photo-1528715471579-d1bcf0ba5e83',
  diet: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773',
  health: 'https://images.unsplash.com/photo-1718086436850-ac77db40dadb',
  orderup: 'https://images.pexels.com/photos/668353/pexels-photo-668353.jpeg'
};

// Header Component
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Home, iconClass: '' },
    { path: '/workout', label: 'Workout', icon: Dumbbell, iconClass: 'header-workout-icon' },
    { path: '/skincare', label: 'Skincare', icon: Sparkles, iconClass: 'header-skincare-icon' },
    { path: '/diet', label: 'Diet', icon: Apple, iconClass: 'header-diet-icon' },
    { path: '/health', label: 'Health', icon: Heart, iconClass: 'header-health-icon' },
    { path: '/order-up', label: 'Order Up', icon: ShoppingCart, iconClass: '' }
  ];

  return (
    <motion.header 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed top-0 w-full z-50 bg-white/10 backdrop-blur-md border-b border-white/20"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="text-3xl font-bold bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent font-['Cinzel_Decorative']">
              Nutracía
            </div>
            <div className="text-sm text-white/80 font-light font-['Pacifico']">
              Redefine Your Limits
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

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg bg-white/10 text-white"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
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
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
};

// AI Chatbot Component
const AIChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        user_id: 'demo-user',
        message: userMessage
      });
      
      setMessages(prev => [...prev, { type: 'ai', content: response.data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'ai', content: 'Sorry, I had trouble processing your message. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat Toggle Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsOpen(!isOpen)}
        className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full shadow-lg flex items-center justify-center text-white"
      >
        <MessageCircle size={24} />
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className="absolute bottom-20 right-0 w-80 h-96 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-xl overflow-hidden"
          >
            {/* Chat Header */}
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4 text-white">
              <h3 className="font-semibold">Nutracía AI Assistant</h3>
              <p className="text-sm opacity-90">Your wellness companion</p>
            </div>

            {/* Messages */}
            <div className="h-64 overflow-y-auto p-4 space-y-3">
              {messages.length === 0 && (
                <div className="text-white/70 text-sm">
                  Hi! I'm here to help with your wellness journey. Ask me about workouts, nutrition, skincare, or health advice!
                </div>
              )}
              {messages.map((msg, idx) => (
                <div key={idx} className={`${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-3 rounded-lg max-w-xs ${
                    msg.type === 'user' 
                      ? 'bg-purple-500 text-white' 
                      : 'bg-white/20 text-white backdrop-blur-sm'
                  }`}>
                    <p className="text-sm">{msg.content}</p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="text-left">
                  <div className="inline-block p-3 rounded-lg bg-white/20 text-white">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
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
                  placeholder="Ask me anything..."
                  className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                  onClick={sendMessage}
                  disabled={!input.trim() || isLoading}
                  className="px-4 py-2 bg-purple-500 text-white rounded-lg disabled:opacity-50 hover:bg-purple-600 transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
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

// Circular Gallery Component
const CircularGallery = ({ items, onItemClick, type }) => {
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

  // Create a custom slide component for each item
  const SlideComponent = ({ content, onClick }) => (
    <div className="text-center cursor-pointer w-full h-full" onClick={onClick}>
      <div 
        className="w-20 h-20 bg-cover bg-center rounded-full border-4 border-white/30 hover:border-white/80 transition-all duration-300 transform hover:scale-110 shadow-lg mx-auto"
        style={{ 
          backgroundImage: `url(${backgrounds[type] || backgrounds.home})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />
      <h4 className="text-white font-semibold text-xs mt-2 max-w-20 mx-auto truncate bg-black/50 px-2 py-1 rounded backdrop-blur-sm">
        {content.title}
      </h4>
    </div>
  );

  // Create media pool for the carousel
  const mediaPool = items.map((item, index) => ({
    id: item.id || index,
    content: item,
    onClick: () => onItemClick(item)
  }));

  try {
    return (
      <div className="h-96 flex items-center justify-center">
        <div className="relative w-full max-w-md">
          <CircularCarousel
            type="standard-2d"
            mediaPool={mediaPool}
            slideComponent={({ content, onClick }) => <SlideComponent content={content} onClick={onClick} />}
            slideWidth={100}
            slideGap={10}
            aspectRatio="1/1"
            customControls={false}
            className="circular-gallery"
          />
          
          {/* Center instructions */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center">
              <h3 className="text-white text-sm font-semibold bg-black/60 px-3 py-2 rounded-lg backdrop-blur-sm">
                Click any item to explore
              </h3>
            </div>
          </div>
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error rendering CircularCarousel:', error);
    // Enhanced fallback grid view
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
    <div 
      className="absolute inset-0 bg-cover bg-center bg-fixed"
      style={{ backgroundImage: `url(${backgrounds.home})` }}
    />
    <div className="absolute inset-0 bg-black/40" />
    
    <div className="relative z-10 min-h-screen flex items-center justify-center">
      <div className="text-center px-6 max-w-4xl mx-auto">
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-6xl md:text-8xl font-bold bg-gradient-to-r from-amber-400 via-orange-500 to-red-500 bg-clip-text text-transparent mb-6 font-['Cinzel_Decorative']">
            Nutracía
          </h1>
          <p className="text-2xl md:text-3xl text-white/90 mb-8 font-light">
            Redefine Your Limits with AI-Powered Wellness
          </p>
          <p className="text-lg text-white/80 mb-12 max-w-2xl mx-auto">
            Experience the future of health with our glassmorphic AI platform that personalizes your workout, skincare, diet, and wellness journey.
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
            {[
              { path: '/workout', label: 'Workouts', icon: Dumbbell, color: 'from-red-500 to-orange-500', animation: 'icon-bounce' },
              { path: '/skincare', label: 'Skincare', icon: Sparkles, color: 'from-pink-500 to-purple-500', animation: 'icon-shake' },
              { path: '/diet', label: 'Diet Plans', icon: Apple, color: 'from-green-500 to-emerald-500', animation: 'icon-spin' },
              { path: '/health', label: 'Health', icon: Heart, color: 'from-blue-500 to-cyan-500', animation: 'icon-pulse' }
            ].map((item) => {
              const Icon = item.icon;
              return (
                <Link key={item.path} to={item.path}>
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`bg-gradient-to-br ${item.color} p-6 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 hover:bg-white/20 transition-all duration-300`}
                  >
                    <Icon size={32} className={`text-white mx-auto mb-3 ${item.animation}`} />
                    <p className="text-white font-semibold">{item.label}</p>
                  </motion.div>
                </Link>
              );
            })}
          </div>
        </motion.div>
      </div>
    </div>
    
    <AIChatbot />
  </div>
);

const WorkoutPage = () => {
  const [workouts, setWorkouts] = useState([]);
  const [selectedWorkout, setSelectedWorkout] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

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

  const handleWorkoutClick = (workout) => {
    setSelectedWorkout(workout);
    setIsModalOpen(true);
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${backgrounds.workout})` }}
      />
      <div className="absolute inset-0 bg-black/50" />
      
      <div className="relative z-10 pt-32 px-6">
        <div className="max-w-6xl mx-auto">
          <QuoteHeader 
            quote="Push beyond yesterday." 
            background={backgrounds.workout}
          />
          
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Workout Plans</h1>
            <p className="text-xl text-white/80">Personalized fitness routines for every goal</p>
          </div>

          {workouts.length > 0 && (
            <CircularGallery 
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

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${backgrounds.skincare})` }}
      />
      <div className="absolute inset-0 bg-black/40" />
      
      <div className="relative z-10 pt-32 px-6">
        <div className="max-w-6xl mx-auto">
          <QuoteHeader 
            quote="Radiance is your right." 
            background={backgrounds.skincare}
          />
          
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Skincare Routines</h1>
            <p className="text-xl text-white/80">Glow with science-backed skincare</p>
          </div>

          {routines.length > 0 && (
            <CircularGallery 
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

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${backgrounds.diet})` }}
      />
      <div className="absolute inset-0 bg-black/50" />
      
      <div className="relative z-10 pt-32 px-6">
        <div className="max-w-6xl mx-auto">
          <QuoteHeader 
            quote="Eat vibrant, live radiant." 
            background={backgrounds.diet}
          />
          
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Diet Plans</h1>
            <p className="text-xl text-white/80">Nutrition that fuels your potential</p>
          </div>

          {meals.length > 0 && (
            <CircularGallery 
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

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${backgrounds.health})` }}
      />
      <div className="absolute inset-0 bg-black/50" />
      
      <div className="relative z-10 pt-32 px-6">
        <div className="max-w-6xl mx-auto">
          <QuoteHeader 
            quote="Wellness is the new wealth." 
            background={backgrounds.health}
          />
          
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Health Conditions</h1>
            <p className="text-xl text-white/80">Personalized support for your health journey</p>
          </div>

          {conditions.length > 0 && (
            <CircularGallery 
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

// Grocery Agent Component (embedded from cloned repo)
const GroceryAgent = () => {
  const [query, setQuery] = useState('');
  const [budget, setBudget] = useState(500);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [currentStep, setCurrentStep] = useState('input');

  const handleGetRecommendations = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/grocery/recommendations`, {
        query: query,
        budget: budget,
        preferred_brands: ['MuscleBlaze', 'Organic India'],
        diet: 'high protein'
      });
      
      setRecommendations(response.data.recommendations);
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
    "I want healthy snacks for my gym routine"
  ];

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-fixed"
        style={{ backgroundImage: `url(${backgrounds.orderup})` }}
      />
      <div className="absolute inset-0 bg-black/60" />
      
      <div className="relative z-10 pt-32 px-6">
        <div className="max-w-6xl mx-auto">
          <QuoteHeader 
            quote="Your AI shopper understands you." 
            background={backgrounds.orderup}
          />

          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold text-white mb-4">Order Up</h1>
            <p className="text-xl text-white/80">AI-Powered Smart Shopping</p>
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
                    max="2000"
                    value={budget}
                    onChange={(e) => setBudget(parseInt(e.target.value))}
                    className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                <button
                  onClick={handleGetRecommendations}
                  disabled={loading || !query.trim()}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 disabled:opacity-50"
                >
                  {loading ? 'AI is analyzing...' : '🤖 Get AI Recommendations'}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'recommendations' && (
            <div className="space-y-6">
              <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-lg p-6 border border-white/20">
                <h3 className="text-xl font-bold text-white mb-6">🤖 AI Recommendations</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map((product, index) => (
                    <div
                      key={index}
                      className={`border-2 rounded-xl p-4 transition-all cursor-pointer ${
                        product.selected 
                          ? 'border-green-500 bg-green-500/20' 
                          : 'border-white/20 hover:border-purple-300 bg-white/10'
                      }`}
                      onClick={() => toggleProductSelection(index)}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h4 className="font-bold text-white text-sm">{product.name}</h4>
                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                          product.selected ? 'bg-green-500 border-green-500' : 'border-white/50'
                        }`}>
                          {product.selected && <span className="text-white text-xs">✓</span>}
                        </div>
                      </div>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-2xl font-bold text-purple-300">{product.price}</span>
                          <span className="text-yellow-400">⭐ {product.rating}</span>
                        </div>
                        
                        <p className="text-white/80 text-xs">{product.description}</p>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-white/70">🏪 {product.platform}</span>
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
                    ← Back
                  </button>
                  <button
                    onClick={createCart}
                    className="flex-1 bg-green-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-green-700 transition-all"
                  >
                    Add to Cart ({recommendations.filter(p => p.selected).length})
                  </button>
                </div>
              </div>
            </div>
          )}

          {currentStep === 'cart' && (
            <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-xl p-8 border border-white/20">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-white mb-2">🛒 Your Cart</h2>
                <p className="text-white/80">Ready for checkout!</p>
              </div>

              <div className="space-y-4 mb-8">
                {cart.cart_items && cart.cart_items.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-4 bg-white/10 rounded-lg">
                    <div>
                      <h4 className="font-semibold text-white">{item.name}</h4>
                      <p className="text-sm text-white/70">{item.platform}</p>
                    </div>
                    <div className="text-xl font-bold text-green-400">{item.price}</div>
                  </div>
                ))}
              </div>

              <div className="border-t border-white/20 pt-6">
                <div className="flex justify-between items-center text-2xl font-bold mb-6">
                  <span className="text-white">Total:</span>
                  <span className="text-green-400">₹{cart.total_cost}</span>
                </div>

                <div className="flex space-x-4">
                  <button
                    onClick={() => setCurrentStep('recommendations')}
                    className="flex-1 bg-white/20 text-white py-4 px-6 rounded-xl font-semibold hover:bg-white/30 transition-colors"
                  >
                    ← Modify
                  </button>
                  <button
                    onClick={() => {
                      alert('🎉 Order placed successfully!');
                      setCurrentStep('input');
                      setQuery('');
                      setRecommendations([]);
                      setCart([]);
                    }}
                    className="flex-1 bg-green-600 text-white py-4 px-6 rounded-xl font-semibold hover:bg-green-700 transition-all"
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

// Main App Component
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/workout" element={<WorkoutPage />} />
          <Route path="/skincare" element={<SkincarePage />} />
          <Route path="/diet" element={<DietPage />} />
          <Route path="/health" element={<HealthPage />} />
          <Route path="/order-up" element={<GroceryAgent />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;