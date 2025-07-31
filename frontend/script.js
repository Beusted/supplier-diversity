// PDF.js configuration
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

// Global variables
let pdfDoc = null;
let pageNum = 1;
let pageRendering = false;
let pageNumPending = null;
let scale = 1.0;
let canvas = document.getElementById('pdf-canvas');
let ctx = canvas.getContext('2d');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updatePageInfo();
    updateZoomLevel();
});

// File handling functions
function openFile() {
    document.getElementById('file-input').click();
}

function loadPDF(event) {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        const fileReader = new FileReader();
        fileReader.onload = function() {
            const typedarray = new Uint8Array(this.result);
            loadPDFDocument(typedarray);
        };
        fileReader.readAsArrayBuffer(file);
    } else {
        alert('Please select a valid PDF file.');
    }
}

function loadPDFDocument(data) {
    pdfjsLib.getDocument(data).promise.then(function(pdfDoc_) {
        pdfDoc = pdfDoc_;
        pageNum = 1;
        
        // Hide placeholder and show canvas
        document.getElementById('pdf-placeholder').style.display = 'none';
        canvas.style.display = 'block';
        
        // Update UI
        updatePageInfo();
        renderPage(pageNum);
        
        // Enable navigation buttons
        updateNavigationButtons();
    }).catch(function(error) {
        console.error('Error loading PDF:', error);
        alert('Error loading PDF file. Please try another file.');
    });
}

// PDF rendering functions
function renderPage(num) {
    pageRendering = true;
    
    pdfDoc.getPage(num).then(function(page) {
        const viewport = page.getViewport({ scale: scale });
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        
        const renderContext = {
            canvasContext: ctx,
            viewport: viewport
        };
        
        const renderTask = page.render(renderContext);
        
        renderTask.promise.then(function() {
            pageRendering = false;
            if (pageNumPending !== null) {
                renderPage(pageNumPending);
                pageNumPending = null;
            }
        });
    });
    
    updatePageInfo();
}

function queueRenderPage(num) {
    if (pageRendering) {
        pageNumPending = num;
    } else {
        renderPage(num);
    }
}

// Navigation functions
function prevPage() {
    if (pageNum <= 1) {
        return;
    }
    pageNum--;
    queueRenderPage(pageNum);
    updateNavigationButtons();
}

function nextPage() {
    if (pageNum >= pdfDoc.numPages) {
        return;
    }
    pageNum++;
    queueRenderPage(pageNum);
    updateNavigationButtons();
}

function updatePageInfo() {
    const pageInfo = document.getElementById('page-info');
    if (pdfDoc) {
        pageInfo.textContent = `Page ${pageNum} of ${pdfDoc.numPages}`;
    } else {
        pageInfo.textContent = 'Page 1 of 1';
    }
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');
    
    if (pdfDoc) {
        prevBtn.disabled = pageNum <= 1;
        nextBtn.disabled = pageNum >= pdfDoc.numPages;
    } else {
        prevBtn.disabled = true;
        nextBtn.disabled = true;
    }
}

// Zoom functions
function zoomIn() {
    scale += 0.25;
    if (scale > 3.0) scale = 3.0;
    updateZoomLevel();
    if (pdfDoc) {
        queueRenderPage(pageNum);
    }
}

function zoomOut() {
    scale -= 0.25;
    if (scale < 0.5) scale = 0.5;
    updateZoomLevel();
    if (pdfDoc) {
        queueRenderPage(pageNum);
    }
}

function updateZoomLevel() {
    document.getElementById('zoom-level').textContent = Math.round(scale * 100) + '%';
}

// Header button functions
function downloadReport() {
    if (!pdfDoc) {
        alert('No PDF loaded to download.');
        return;
    }
    
    // Create a download link for the current PDF
    const fileInput = document.getElementById('file-input');
    if (fileInput.files[0]) {
        const url = URL.createObjectURL(fileInput.files[0]);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileInput.files[0].name || 'report.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

function printReport() {
    if (!pdfDoc) {
        alert('No PDF loaded to print.');
        return;
    }
    
    // Open print dialog for the current page
    window.print();
}

function shareReport() {
    if (!pdfDoc) {
        alert('No PDF loaded to share.');
        return;
    }
    
    // Simple share functionality
    if (navigator.share) {
        const fileInput = document.getElementById('file-input');
        if (fileInput.files[0]) {
            navigator.share({
                title: 'PDF Report',
                text: 'Check out this PDF report',
                files: [fileInput.files[0]]
            }).catch(console.error);
        }
    } else {
        // Fallback: copy current URL to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Page URL copied to clipboard!');
        }).catch(() => {
            alert('Share functionality not supported in this browser.');
        });
    }
}

// Chatbot functions
function toggleChatbot() {
    const modal = document.getElementById('chatbot-modal');
    modal.classList.toggle('active');
    
    if (modal.classList.contains('active')) {
        document.getElementById('chat-input').focus();
    }
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, 'user');
        input.value = '';
        
        // Simulate bot response
        setTimeout(() => {
            const botResponse = generateBotResponse(message);
            addMessage(botResponse, 'bot');
        }, 1000);
    }
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageText = document.createElement('p');
    messageText.textContent = text;
    messageDiv.appendChild(messageText);
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function generateBotResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    // Simple response logic
    if (message.includes('help') || message.includes('how')) {
        return "I can help you navigate the PDF report. You can use the controls to zoom in/out, navigate between pages, or ask me specific questions about the document.";
    } else if (message.includes('page') || message.includes('navigate')) {
        return "Use the Previous/Next buttons to navigate between pages, or ask me to go to a specific page number.";
    } else if (message.includes('zoom')) {
        return "You can zoom in and out using the + and - buttons in the PDF controls, or use your mouse wheel while viewing the document.";
    } else if (message.includes('download') || message.includes('save')) {
        return "Click the 'Download' button in the header to save the current PDF report to your device.";
    } else if (message.includes('print')) {
        return "Use the 'Print' button in the header to print the current PDF document.";
    } else if (message.includes('share')) {
        return "Click the 'Share' button to share this report with others.";
    } else {
        return "I'm here to help you with the PDF report viewer. You can ask me about navigation, zooming, downloading, printing, or any other features.";
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    if (!pdfDoc) return;
    
    switch(event.key) {
        case 'ArrowLeft':
            if (!event.target.matches('input')) {
                prevPage();
                event.preventDefault();
            }
            break;
        case 'ArrowRight':
            if (!event.target.matches('input')) {
                nextPage();
                event.preventDefault();
            }
            break;
        case '+':
        case '=':
            if (event.ctrlKey || event.metaKey) {
                zoomIn();
                event.preventDefault();
            }
            break;
        case '-':
            if (event.ctrlKey || event.metaKey) {
                zoomOut();
                event.preventDefault();
            }
            break;
        case 'Escape':
            const modal = document.getElementById('chatbot-modal');
            if (modal.classList.contains('active')) {
                toggleChatbot();
            }
            break;
    }
});

// Handle window resize
window.addEventListener('resize', function() {
    if (pdfDoc && !pageRendering) {
        queueRenderPage(pageNum);
    }
});

// Initialize navigation buttons state
updateNavigationButtons();
