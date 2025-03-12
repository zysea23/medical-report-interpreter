//static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const reportFileInput = document.getElementById('report-file');
    const uploadButton = document.getElementById('upload-button');
    const loadingIndicator = document.getElementById('loading');
    const resultsContainer = document.getElementById('results');
    const originalContent = document.getElementById('original-content');
    const explanationContent = document.getElementById('explanation-content');
    const translatedContent = document.getElementById('translated-content');
    const translationLoading = document.getElementById('translation-loading');
    const languageTabs = document.querySelectorAll('.language-tab');
    
    // Q&A elements
    const questionInput = document.getElementById('question-input');
    const askButton = document.getElementById('ask-button');
    const qaHistory = document.getElementById('qa-history');
    const qaLoading = document.getElementById('qa-loading');

    // Store content for translation and Q&A
    let explanationText = '';
    let reportContentText = '';
    let isTranslated = false;

    // Display file selection status
    reportFileInput.addEventListener('change', function() {
        const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
        this.nextElementSibling.textContent = fileName;
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Check if a file is selected
        if (!reportFileInput.files[0]) {
            alert('Please select a medical report image');
            return;
        }

        // Show loading state
        uploadButton.disabled = true;
        loadingIndicator.classList.remove('hidden');
        resultsContainer.classList.add('hidden');

        // Reset translation status and Q&A history
        isTranslated = false;
        translatedContent.textContent = '';
        explanationContent.classList.add('active-content');
        translatedContent.classList.remove('active-content');
        setActiveLanguageTab('original');
        qaHistory.innerHTML = '';

        // Prepare form data
        const formData = new FormData();
        formData.append('file', reportFileInput.files[0]);

        try {
            // Send request
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            // Process response
            const result = await response.json();

            if (result.success) {
                // Store content for later use
                explanationText = result.explanation;
                reportContentText = result.original_content;
                
                // Display results
                originalContent.textContent = result.original_content;
                explanationContent.textContent = result.explanation;
                // Ensure explanation content is visible initially
                explanationContent.classList.add('active-content');
                resultsContainer.classList.remove('hidden');
            } else {
                alert('Processing failed: ' + result.message);
            }
        } catch (error) {
            alert('Request Failed: ' + error.message);
        } finally {
            // Restore state
            uploadButton.disabled = false;
            loadingIndicator.classList.add('hidden');
        }
    });

    // Handle language tab switching
    languageTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const language = this.getAttribute('data-language');
            
            if (language === 'chinese' && !isTranslated) {
                translateExplanation();
            } else {
                setActiveLanguageTab(language);
            }
        });
    });

    // Handle Q&A submission
    askButton.addEventListener('click', async function() {
        handleQuestionSubmission();
    });

    // Handle Enter key press in question input
    questionInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleQuestionSubmission();
        }
    });

    // Function to handle question submission
    async function handleQuestionSubmission() {
        const question = questionInput.value.trim();
        
        // Validate input
        if (!question) {
            alert('Please enter a question');
            return;
        }
        
        if (!reportContentText) {
            alert('Please upload a medical report first');
            return;
        }
        
        // Show loading indicator
        askButton.disabled = true;
        qaLoading.classList.remove('hidden');
        
        try {
            // Add question to history
            addQuestionToHistory(question);
            
            // Clear input field
            questionInput.value = '';
            
            // Send question to API
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    report_content: reportContentText,
                    question: question
                })
            });
            
            // Process response
            const result = await response.json();
            
            if (result.success) {
                // Add answer to history
                addAnswerToHistory(result.answer);
            } else {
                // Add error message to history
                addAnswerToHistory(`Error: ${result.message}`);
            }
        } catch (error) {
            // Add error message to history
            addAnswerToHistory(`Error: ${error.message}`);
        } finally {
            // Restore state
            askButton.disabled = false;
            qaLoading.classList.add('hidden');
        }
    }

    // Function to add question to history
    function addQuestionToHistory(question) {
        // Create question container if no answer exists yet
        const existingPair = qaHistory.querySelector('.qa-pair:last-child:not(.complete)');
        
        if (existingPair) {
            // Update existing pair
            const questionElement = existingPair.querySelector('.qa-question');
            questionElement.textContent = question;
        } else {
            // Create new pair
            const pair = document.createElement('div');
            pair.className = 'qa-pair';
            
            const questionElement = document.createElement('div');
            questionElement.className = 'qa-question';
            questionElement.textContent = question;
            
            pair.appendChild(questionElement);
            qaHistory.appendChild(pair);
        }
        
        // Scroll to bottom
        qaHistory.scrollTop = qaHistory.scrollHeight;
    }

    // Function to add answer to history
    function addAnswerToHistory(answer) {
        const existingPair = qaHistory.querySelector('.qa-pair:last-child:not(.complete)');
        
        if (existingPair) {
            // Add answer to existing pair
            const answerElement = document.createElement('div');
            answerElement.className = 'qa-answer';
            answerElement.textContent = answer;
            
            existingPair.appendChild(answerElement);
            existingPair.classList.add('complete');
        } else {
            // Create new pair (shouldn't happen but just in case)
            const pair = document.createElement('div');
            pair.className = 'qa-pair complete';
            
            const questionElement = document.createElement('div');
            questionElement.className = 'qa-question';
            questionElement.textContent = 'Unknown question';
            
            const answerElement = document.createElement('div');
            answerElement.className = 'qa-answer';
            answerElement.textContent = answer;
            
            pair.appendChild(questionElement);
            pair.appendChild(answerElement);
            qaHistory.appendChild(pair);
        }
        
        // Scroll to bottom
        qaHistory.scrollTop = qaHistory.scrollHeight;
    }

    // Function to set active language tab and content
    function setActiveLanguageTab(language) {
        // Update tab active state
        languageTabs.forEach(tab => {
            if (tab.getAttribute('data-language') === language) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });

        // Update content visibility
        if (language === 'original') {
            explanationContent.classList.add('active-content');
            translatedContent.classList.remove('active-content');
        } else {
            explanationContent.classList.remove('active-content');
            translatedContent.classList.add('active-content');
        }
    }

    // Function to handle translation
    async function translateExplanation() {
        // Check if there's text to translate
        if (!explanationText) {
            alert('No explanation content to translate');
            return;
        }

        // Show loading indicator
        translationLoading.classList.remove('hidden');

        try {
            // Send translation request
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: explanationText,
                    language: 'Chinese'
                })
            });

            // Process response
            const result = await response.json();

            if (result.success) {
                // Display translated content
                translatedContent.textContent = result.translated_text;
                isTranslated = true;
                
                // Switch to translated view
                setActiveLanguageTab('chinese');
            } else {
                alert('Translation failed: ' + result.message);
                setActiveLanguageTab('original');
            }
        } catch (error) {
            alert('Translation Request Failed: ' + error.message);
            setActiveLanguageTab('original');
        } finally {
            // Hide loading indicator
            translationLoading.classList.add('hidden');
        }
    }
});