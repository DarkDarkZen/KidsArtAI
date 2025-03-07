// Инициализация Telegram Mini App
let tg = window.Telegram.WebApp;
tg.expand(); // Расширяем на весь экран

// DOM-элементы
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-upload');
const selectedFileContainer = document.getElementById('selected-file');
const fileName = document.getElementById('file-name');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsModal = document.getElementById('results-modal');
const resultsContainer = document.querySelector('.results-container');
const closeModalBtn = document.querySelector('.close-btn');
const demoBtn = document.querySelector('.demo-btn');

// Переменная для отслеживания демо-режима
let demoMode = false;

// Обработка загрузки изображения
function handleImageUpload(file) {
    if (!file) return;
    
    // Проверка типа файла
    const validTypes = ['image/jpeg', 'image/png', 'image/heic'];
    if (!validTypes.includes(file.type) && !file.name.toLowerCase().endsWith('.heic')) {
        alert('Unsupported file format. Please upload JPEG, PNG, or HEIC files.');
        return;
    }
    
    // Показываем имя выбранного файла
    fileName.textContent = file.name;
    selectedFileContainer.hidden = false;
    
    // Активируем кнопку анализа
    analyzeBtn.disabled = false;
    analyzeBtn.style.backgroundColor = '#8A7CFF';
}

// Функция для отправки изображения на сервер для анализа
async function analyzeImage() {
    // Проверяем, есть ли выбранный файл
    if (analyzeBtn.disabled) return;
    
    // Показываем индикатор загрузки
    const originalText = analyzeBtn.textContent;
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.classList.add('loading');
    analyzeBtn.disabled = true;
    
    try {
        // Получаем файл из input
        const file = fileInput.files[0];
        if (!file) throw new Error('No file selected');
        
        // Создаем FormData для отправки файла
        const formData = new FormData();
        formData.append('image', file);
        
        // Отправляем запрос на сервер
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }
        
        // Получаем результаты анализа
        const results = await response.json();
        
        // Отображаем результаты
        displayResults(results);
    } catch (error) {
        console.error('Error analyzing image:', error);
        
        // Для демонстрации показываем тестовые результаты
        if (demoMode) {
            displayDemoResults();
        } else {
            alert('Error analyzing image. Please try again.');
        }
    } finally {
        // Восстанавливаем кнопку
        analyzeBtn.textContent = originalText;
        analyzeBtn.classList.remove('loading');
        analyzeBtn.disabled = false;
        analyzeBtn.style.backgroundColor = '#8A7CFF';
    }
}

// Функция для отображения результатов анализа
function displayResults(results) {
    // Очищаем контейнер результатов
    resultsContainer.innerHTML = '';
    
    // Создаем HTML для результатов
    let resultsHTML = '';
    
    // Добавляем каждый раздел анализа
    if (results.psychologicalAge) {
        resultsHTML += `<div class="result-item">
            <h4>Psychological Age</h4>
            <p>${results.psychologicalAge}</p>
        </div>`;
    }
    
    if (results.imaginationLevel) {
        resultsHTML += `<div class="result-item">
            <h4>Imagination & Intelligence</h4>
            <p>${results.imaginationLevel}</p>
        </div>`;
    }
    
    if (results.emotionalIntelligence) {
        resultsHTML += `<div class="result-item">
            <h4>Emotional Intelligence</h4>
            <p>${results.emotionalIntelligence}</p>
        </div>`;
    }
    
    if (results.developmentLevel) {
        resultsHTML += `<div class="result-item">
            <h4>Mental & Emotional Development</h4>
            <p>${results.developmentLevel}</p>
        </div>`;
    }
    
    if (results.physicalState) {
        resultsHTML += `<div class="result-item">
            <h4>Physical & Psychological State</h4>
            <p>${results.physicalState}</p>
        </div>`;
    }
    
    if (results.recommendations) {
        resultsHTML += `<div class="result-item recommendations">
            <h4>Recommendations</h4>
            <p>${results.recommendations}</p>
        </div>`;
    }
    
    // Вставляем HTML в контейнер
    resultsContainer.innerHTML = resultsHTML;
    
    // Показываем модальное окно
    resultsModal.hidden = false;
}

// Функция для отображения демо-результатов
function displayDemoResults() {
    const demoResults = {
        psychologicalAge: "The drawing suggests a psychological age of around 5-6 years, which is characterized by the use of basic shapes and simplified representations of figures. The child is in the pre-schematic stage of artistic development.",
        imaginationLevel: "The child demonstrates a moderate level of imagination, shown through the creative use of colors and the inclusion of various elements in the drawing. There's potential for further development with proper stimulation.",
        emotionalIntelligence: "The drawing indicates a developing emotional intelligence. The child appears to understand basic emotions, as shown by the facial expressions in the drawing, but may need support in recognizing more complex emotional states.",
        developmentLevel: "The mental and emotional development appears age-appropriate. The child shows the ability to organize thoughts and represent them visually, which is a positive sign of cognitive development.",
        physicalState: "The drawing suggests normal physical development for the child's age. The pressure applied to the drawing tool and the control shown in creating lines indicate appropriate fine motor skills development.",
        recommendations: "Encourage the child to explain their drawings to develop verbal expression. Provide various art materials to explore different textures and techniques. Consider regular drawing sessions where the child can express daily experiences, which will help develop emotional processing skills."
    };
    
    displayResults(demoResults);
}

// Обработчики событий
document.addEventListener('DOMContentLoaded', () => {
    // Обработчик для области загрузки
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Обработчик изменения файла
    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleImageUpload(e.target.files[0]);
        }
    });
    
    // Обработчик для кнопки анализа
    analyzeBtn.addEventListener('click', analyzeImage);
    
    // Обработчик для закрытия модального окна
    closeModalBtn.addEventListener('click', () => {
        resultsModal.hidden = true;
    });
    
    // Закрытие модального окна при клике вне его содержимого
    resultsModal.addEventListener('click', (e) => {
        if (e.target === resultsModal) {
            resultsModal.hidden = true;
        }
    });
    
    // Обработка Drag and Drop для загрузки изображений
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.classList.add('dragover');
    });
    
    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragover');
    });
    
    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const file = e.dataTransfer.files[0];
            handleImageUpload(file);
            
            // Копируем файл в input
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
        }
    });
    
    // Обработчик для кнопки Demo Mode
    demoBtn.addEventListener('click', () => {
        demoMode = !demoMode;
        
        if (demoMode) {
            demoBtn.style.backgroundColor = 'rgba(138, 124, 255, 0.3)';
            alert('Demo mode activated. Analysis will show sample results.');
        } else {
            demoBtn.style.backgroundColor = 'rgba(138, 124, 255, 0.15)';
            alert('Demo mode deactivated.');
        }
    });
}); 