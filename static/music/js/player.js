document.addEventListener('DOMContentLoaded', function() {
    // Находим все кнопки воспроизведения
    const playButtons = document.querySelectorAll('.play-button');
    
    // Добавляем обработчик события для каждой кнопки
    playButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Получаем ID элемента (трек, исполнитель или альбом)
            const card = this.closest('[data-track-id]');
            const itemId = card.dataset.id;
            const itemType = card.classList.contains('track-card') ? 'track' : 
                            card.classList.contains('artist-card') ? 'artist' : 'album';
            
            // Здесь будет логика воспроизведения в зависимости от типа элемента
            console.log(`Воспроизведение ${itemType} с ID: ${itemId}`);
            
            // Функция для воспроизведения будет реализована в зависимости от вашего API
            playItem(itemType, itemId);
        });
    });
    
    // Функция для воспроизведения элемента
    function playItem(type, id) {
        // Здесь будет логика воспроизведения
        // Например, вызов API для получения URL аудио и создание плеера
        // Это шаблон, который нужно заполнить вашей логикой
        
        switch(type) {
            case 'track':
                // Логика воспроизведения трека
                console.log(`Воспроизведение трека ${id}`);
                break;
            case 'artist':
                // Логика воспроизведения популярных треков исполнителя
                console.log(`Воспроизведение треков исполнителя ${id}`);
                break;
            case 'album':
                // Логика воспроизведения альбома
                console.log(`Воспроизведение альбома ${id}`);
                break;
        }
    }
    
    // Обработка воспроизведения на странице деталей трека
    const trackItems = document.querySelectorAll('.track-item');
    const playLargeButton = document.querySelector('.play-large-button');
    
    // Обработчик для основной кнопки воспроизведения
    if (playLargeButton) {
        playLargeButton.addEventListener('click', function() {
            const activeTrack = document.querySelector('.track-item.active');
            if (activeTrack) {
                const trackId = activeTrack.dataset.id;
                playItem('track', trackId);
            }
        });
    }
    
    // Обработчик для отдельных треков в списке
    trackItems.forEach(item => {
        const playButton = item.querySelector('.play-button-small');
        
        if (playButton) {
            playButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Устанавливаем активный трек
                trackItems.forEach(t => t.classList.remove('active'));
                item.classList.add('active');
                
                // Воспроизводим
                const trackId = item.dataset.id;
                playItem('track', trackId);
            });
        }
        
        // Воспроизведение при клике на строку
        item.addEventListener('click', function() {
            // Устанавливаем активный трек
            trackItems.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Воспроизводим
            const trackId = this.dataset.id;
            playItem('track', trackId);
        });
    });
}); 