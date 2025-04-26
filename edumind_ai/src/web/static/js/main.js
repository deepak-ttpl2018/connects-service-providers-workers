/**
 * EduMind AI - Main JavaScript file
 */

// Global state
let currentDocument = null;
let currentChapter = 0;
let chapters = [];
let isReading = false;
let audioElement = null;

// DOM elements
const uploadForm = document.getElementById('upload-form');
const uploadSection = document.getElementById('upload-section');
const readerSection = document.getElementById('reader-section');
const chatSection = document.getElementById('chat-section');
const contentArea = document.getElementById('content-area');
const prevButton = document.getElementById('prev-btn');
const nextButton = document.getElementById('next-btn');
const readButton = document.getElementById('read-btn');
const pauseButton = document.getElementById('pause-btn');
const chatMessages = document.getElementById('chat-messages');
const questionInput = document.getElementById('question-input');
const sendButton = document.getElementById('send-btn');
const micButton = document.getElementById('mic-btn');

// Initialize the application
function init() {
    // Add event listeners
    uploadForm.addEventListener('submit', handleFileUpload);
    prevButton.addEventListener('click', showPreviousChapter);
    nextButton.addEventListener('click', showNextChapter);
    readButton.addEventListener('click', startReading);
    pauseButton.addEventListener('click', pauseReading);
    sendButton.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendQuestion();
        }
    });
    micButton.addEventListener('click', toggleSpeechRecognition);
}

// Handle file upload
async function handleFileUpload(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('pdf-upload');
    if (fileInput.files.length === 0) {
        showError('Please select a PDF file');
        return;
    }
    
    const file = fileInput.files[0];
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }
    
    // Show loading state
    showLoading('Uploading and processing document...');
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        // Upload the file
        const uploadResponse = await fetch('/api/upload', {
            method: 'POST',
            body