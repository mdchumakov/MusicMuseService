document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchForm = document.getElementById('search-form');
    const clearSearch = document.getElementById('clear-search');
    const searchContainer = document.querySelector('.search-container');
    const headerContainer = document.querySelector('.header-container');
    const menuToggle = document.getElementById('menu-toggle');
    let searchTimeout;
    let isMobile = window.innerWidth <= 600;
    let isSearchFocused = false;

    // Создаем контейнер для результатов поиска
    const searchResults = document.createElement('div');
    searchResults.className = 'search-results';
    searchForm.parentNode.appendChild(searchResults);

    // Функция для получения иконки в зависимости от типа результата
    function getEntityIcon(entityType) {
        const icons = {
            'artist': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/></svg>',
            'release': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" fill="currentColor"/></svg>',
            'track': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" fill="currentColor"/></svg>'
        };
        return icons[entityType] || icons['track'];
    }

    // Функция для получения текста типа сущности
    function getEntityTypeText(entityType) {
        const types = {
            'artist': 'Исполнитель',
            'release': 'Альбом',
            'track': 'Трек'
        };
        return types[entityType] || 'Трек';
    }

    // Функция для получения URL в зависимости от типа результата
    function getEntityUrl(entityType, entityId) {
        const urls = {
            'artist': `/music/artist/${entityId}/`,
            'release': `/music/release/${entityId}/`,
            'track': `/music/track/${entityId}/`
        };
        return urls[entityType] || '#';
    }

    // Функция для выполнения поиска
    async function performSearch(query) {
        if (!query.trim()) {
            searchResults.innerHTML = '';
            searchResults.classList.remove('active');
            return;
        }

        try {
            const response = await fetch(`/api/v1/music/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();

            if (results.length === 0) {
                searchResults.innerHTML = '<div class="no-results">Ничего не найдено</div>';
            } else {
                searchResults.innerHTML = results.map(result => `
                    <a href="${getEntityUrl(result.entity, result.entity_id)}" class="search-result-item" data-entity-type="${result.entity}" data-entity-id="${result.entity_id}">
                        <div class="search-result-icon">
                            ${getEntityIcon(result.entity)}
                        </div>
                        <div class="search-result-content">
                            <div class="search-result-name">${result.name}</div>
                            <div class="search-result-type">${getEntityTypeText(result.entity)}</div>
                        </div>
                    </a>
                `).join('');
                
                // Добавляем обработчики для результатов поиска
                const resultItems = searchResults.querySelectorAll('.search-result-item');
                resultItems.forEach(item => {
                    item.addEventListener('click', function(e) {
                        // Предотвращаем стандартное поведение ссылки
                        e.preventDefault();
                        
                        // Получаем URL из атрибута href
                        const url = this.getAttribute('href');
                        
                        // Переходим по URL через небольшую задержку
                        setTimeout(() => {
                            window.location.href = url;
                        }, 100);
                    });
                });
            }

            searchResults.classList.add('active');
        } catch (error) {
            console.error('Ошибка при выполнении поиска:', error);
            searchResults.innerHTML = '<div class="no-results">Произошла ошибка при поиске</div>';
            searchResults.classList.add('active');
        }
    }

    // Обработчик ввода в поле поиска
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => performSearch(query), 300);
        } else {
            searchResults.innerHTML = '';
            searchResults.classList.remove('active');
        }
    });

    // Обработчик очистки поиска
    clearSearch.addEventListener('click', function() {
        searchInput.value = '';
        searchResults.innerHTML = '';
        searchResults.classList.remove('active');
        
        // Снимаем фокус только при нажатии на кнопку очистки
        if (isMobile) {
            searchInput.blur();
            handleBlur();
        }
    });

    // Закрытие результатов поиска при клике вне области
    document.addEventListener('click', function(e) {
        // Проверяем, что клик не на форме поиска и не на результатах
        if (!searchForm.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.classList.remove('active');
        }
    });
    
    // Обработчики для мобильного фокуса
    function handleFocus() {
        if (isMobile) {
            isSearchFocused = true;
            searchContainer.classList.add('focused');
            headerContainer.classList.add('search-focused');
            document.body.style.overflow = 'hidden';

        }
    }
    
    function handleBlur() {
        if (isMobile && !isSearchFocused) {
            searchContainer.classList.remove('focused');
            headerContainer.classList.remove('search-focused');
            document.body.style.overflow = '';
        }
    }
    
    searchInput.addEventListener('focus', handleFocus);
    searchInput.addEventListener('blur', function(e) {
        // Проверяем, не кликнули ли мы на результаты поиска
        const relatedTarget = e.relatedTarget;
        if (relatedTarget && searchResults.contains(relatedTarget)) {
            // Если кликнули на результаты, сохраняем фокус
            e.preventDefault();
            searchInput.focus();
            return;
        }
        
        // Если кликнули не на результаты, снимаем фокус
        isSearchFocused = false;
        handleBlur();
    });
    
    // Обработчик изменения размера окна
    window.addEventListener('resize', function() {
        isMobile = window.innerWidth <= 600;
        if (!isMobile) {
            searchContainer.classList.remove('focused');
            headerContainer.classList.remove('search-focused');
            document.body.style.overflow = '';
            
            // Показываем кнопку menu-toggle
            if (menuToggle) {
                menuToggle.style.opacity = '';
                menuToggle.style.transform = '';
                menuToggle.style.pointerEvents = '';
            }
        }
    });
}); 