// Simple test script to check authentication behavior
console.log('Testing authentication behavior...');

// Clear localStorage to simulate non-authenticated user
localStorage.clear();

// Check if user and userId exist
const user = localStorage.getItem('user');
const userId = localStorage.getItem('userId');

console.log('Current auth state:');
console.log('user:', user);
console.log('userId:', userId);
console.log('isAuthenticated:', !!(user && userId));

// This would be run in browser console
console.log('To test: Navigate to /workout, /skincare, /diet, /health, /order-up');
console.log('Should show quote-only pages for non-authenticated users');