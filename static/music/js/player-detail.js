document.addEventListener('DOMContentLoaded', function() {
    // Элементы интерфейса плеера
    const miniPlayer = document.getElementById('miniPlayer');
    const fullPlayer = document.getElementById('fullPlayer');
    const audioElement = document.getElementById('audioPlayer');
    const videoElement = document.getElementById('videoPlayer');
    const canvas = document.getElementById('audioVisualizer');
    const coverImage = document.getElementById('trackCover');
    const trackTitle = document.getElementById('trackTitle');
    const trackArtist = document.getElementById('trackArtist');
    const miniPlayerTitle = document.querySelector('.mini-player-title');
    const miniPlayerArtist = document.querySelector('.mini-player-artist');
    const miniPlayerCover = document.querySelector('.mini-player-cover');
    const currentTimeDisplay = document.getElementById('currentTime');
    const totalTimeDisplay = document.getElementById('totalTime');
    const progressBarFill = document.getElementById('progressBarFill');
    const miniProgressBarFill = document.getElementById('miniProgressBarFill');
    const progressHandle = document.getElementById('progressHandle');
    const progressBarContainer = document.querySelector('.player-progress-bar-container');
    const volumeSlider = document.getElementById('volumeSlider');
    const volumeButton = document.getElementById('volumeButton');
    const playPauseButton = document.getElementById('playPauseButton');
    const miniPlayButton = document.querySelector('.mini-player-control.play-button');
    const expandButton = document.querySelector('.expand-button');
    const closeButton = document.getElementById('closePlayer');
    
    // Элементы со страницы деталей трека
    const mainPlayButton = document.getElementById('mainPlayButton');
    const trackItems = document.querySelectorAll('.detail-track-item');
    
    // Добавим новую переменную для хранения всех кнопок воспроизведения треков
    const trackPlayButtons = document.querySelectorAll('.detail-track-play-button');
    
    // Состояние плеера
    let isPlaying = false;
    let isFirstPlay = true;
    let currentTrackId = null;
    let currentPlaylist = [];
    let audioContext = null;
    let analyser = null;
    let visualizer = null;
    
    // Инициализация плеера
    function initPlayer() {
        // Скрываем мини-плеер изначально
        miniPlayer.style.transform = 'translateY(100%)';
        
        // Создаем список воспроизведения из треков на странице
        trackItems.forEach(item => {
            currentPlaylist.push({
                id: item.dataset.trackId,
                name: item.dataset.trackName,
                artist: item.dataset.artistName,
                coverUrl: item.dataset.coverUrl,
                audioUrl: item.dataset.audioUrl,
                videoUrl: item.dataset.videoUrl || null
            });
        });
        
        // Настраиваем события для аудио и видео
        setupAudioEvents();
        
        // Настраиваем обработчики для элементов управления плеера
        setupPlayerControls();
    }
    
    // Настройка событий для аудио/видео
    function setupAudioEvents() {
        // Обновление прогресса воспроизведения
        audioElement.addEventListener('timeupdate', updateProgress);
        
        // Обновление длительности после загрузки метаданных
        audioElement.addEventListener('loadedmetadata', function() {
            const duration = audioElement.duration;
            totalTimeDisplay.textContent = formatTime(duration);
        });
        
        // События завершения воспроизведения
        audioElement.addEventListener('ended', function() {
            playNextTrack();
        });
        
        // Обновление состояния проигрывания
        audioElement.addEventListener('play', function() {
            isPlaying = true;
            
            // Обновляем состояние всех кнопок
            playPauseButton.classList.add('playing');
            miniPlayButton.classList.add('playing');
            mainPlayButton.classList.add('playing');
            
            // Обновляем состояние кнопки воспроизведения трека
            if (currentTrackId) {
                const activeTrack = document.querySelector(`.detail-track-item[data-track-id="${currentTrackId}"]`);
                if (activeTrack) {
                    activeTrack.classList.add('playing');
                    const playButton = activeTrack.querySelector('.detail-track-play-button');
                    if (playButton) {
                        playButton.classList.add('playing');
                    }
                }
            }
            
            // Запуск визуализации
            if (!videoElement.src) {
                startVisualization();
            }
        });
        
        audioElement.addEventListener('pause', function() {
            isPlaying = false;
            
            // Обновляем состояние всех кнопок
            playPauseButton.classList.remove('playing');
            miniPlayButton.classList.remove('playing');
            mainPlayButton.classList.remove('playing');
            
            // Обновляем состояние кнопки воспроизведения трека
            if (currentTrackId) {
                const activeTrack = document.querySelector(`.detail-track-item[data-track-id="${currentTrackId}"]`);
                if (activeTrack) {
                    activeTrack.classList.remove('playing');
                    const playButton = activeTrack.querySelector('.detail-track-play-button');
                    if (playButton) {
                        playButton.classList.remove('playing');
                    }
                }
            }
            
            // Остановка визуализации
            stopVisualization();
        });
    }
    
    // Настройка элементов управления плеера
    function setupPlayerControls() {
        // Основные кнопки воспроизведения
        if (mainPlayButton) {
            mainPlayButton.addEventListener('click', function() {
                // Проверяем, воспроизводится ли уже этот трек
                if (!mainPlayButton.dataset.trackId) {
                    // Если нет, воспроизводим первый трек в списке
                    mainPlayButton.dataset.trackId = currentPlaylist[0].id
                }

                if (currentTrackId === mainPlayButton.dataset.trackId) {
                    // Если трек уже воспроизводится, ставим на паузу
                    togglePlayPause();
                } else {
                    // Иначе воспроизводим новый трек
                    playTrack(mainPlayButton.dataset.trackId);
                }
            });
        }
        
        // Обработчики для кнопок воспроизведения треков
        trackPlayButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const trackItem = button.closest('.detail-track-item');
                const trackId = trackItem.dataset.trackId;

                // Меняем активный трек в mainPlayButton
                mainPlayButton.dataset.trackId = trackId

                if (currentTrackId === trackId) {
                    togglePlayPause();
                } else {
                    playTrack(trackId);
                }
            });
        });
        
        // Воспроизведение при клике на трек
        trackItems.forEach(item => {
            item.addEventListener('click', function(e) {
                // Проверяем, не является ли целевой элемент кнопкой скачивания или её потомком
                if (e.target.closest('.detail-track-actions')) {
                    return; // Прерываем выполнение функции, если клик был по кнопке скачивания
                }
                // Меняем активный трек в mainPlayButton
                mainPlayButton.dataset.trackId = item.dataset.trackId

                playTrack(item.dataset.trackId);
            });
        });
        
        // Управление плеером (Play/Pause)
        playPauseButton.addEventListener('click', togglePlayPause);
        miniPlayButton.addEventListener('click', togglePlayPause);
        
        // Кнопки мини-плеера
        expandButton.addEventListener('click', function() {
            showFullPlayer();
        });
        
        // Кнопка закрытия полноэкранного плеера
        closeButton.addEventListener('click', function() {
            hideFullPlayer();
        });
        
        // Кнопки переключения треков
        const nextButtons = document.querySelectorAll('.next-button');
        const prevButtons = document.querySelectorAll('.prev-button');
        
        nextButtons.forEach(button => {
            button.addEventListener('click', playNextTrack);
        });
        
        prevButtons.forEach(button => {
            button.addEventListener('click', playPrevTrack);
        });
        
        // Прогресс-бар
        progressBarContainer.addEventListener('click', seekTrack);
        
        // Громкость
        volumeSlider.addEventListener('input', function() {
            setVolume(this.value / 100);
        });
        
        volumeButton.addEventListener('click', toggleMute);
        
        // Загружаем сохраненную громкость из localStorage
        const savedVolume = localStorage.getItem('playerVolume');
        if (savedVolume !== null) {
            volumeSlider.value = savedVolume * 100;
            setVolume(savedVolume);
        }
    }
    
    // Функция воспроизведения трека
    function playTrack(trackId) {
        // Находим трек в плейлисте
        const track = currentPlaylist.find(t => t.id === trackId);
        
        if (!track) return;
        
        // Обновляем активный трек в UI
        updateActiveTrack(trackId);
        
        // Обновляем информацию о треке в плеере
        updatePlayerInfo(track);
        
        // Загружаем аудио
        audioElement.src = track.audioUrl;
        
        // Загружаем видео, если есть
        if (track.videoUrl) {
            videoElement.src = track.videoUrl;
            videoElement.style.display = 'block';
            canvas.style.display = 'none';
            coverImage.style.display = 'none';
        } else {
            videoElement.src = '';
            videoElement.style.display = 'none';
            canvas.style.display = 'block';
            coverImage.style.display = 'block';
        }
        
        // Запускаем воспроизведение
        audioElement.play().then(() => {
            isPlaying = true;
            
            // Обновляем состояние всех кнопок
            playPauseButton.classList.add('playing');
            miniPlayButton.classList.add('playing');
            mainPlayButton.classList.add('playing');
            
            // Обновляем состояние кнопки воспроизведения трека
            const activeTrack = document.querySelector(`.detail-track-item[data-track-id="${trackId}"]`);
            if (activeTrack) {
                activeTrack.classList.add('playing');
                const playButton = activeTrack.querySelector('.detail-track-play-button');
                if (playButton) {
                    playButton.classList.add('playing');
                }
            }
            
            // Показываем мини-плеер
            miniPlayer.style.transform = 'translateY(0)';
        }).catch(error => {
            console.error('Error playing audio:', error);
        });
        
        // Сохраняем текущий ID трека
        currentTrackId = trackId;
    }
    
    // Обновление активного трека в UI
    function updateActiveTrack(trackId) {
        // Снимаем классы active и playing со всех треков и их кнопок
        trackItems.forEach(item => {
            item.classList.remove('active', 'playing');
            const playButton = item.querySelector('.detail-track-play-button');
            if (playButton) {
                playButton.classList.remove('playing');
            }
        });
        
        // Добавляем классы к активному треку
        const activeTrack = document.querySelector(`.detail-track-item[data-track-id="${trackId}"]`);
        if (activeTrack) {
            activeTrack.classList.add('active');
            if (isPlaying) {
                activeTrack.classList.add('playing');
            }
            
            // Обновляем состояние кнопки воспроизведения трека
            const playButton = activeTrack.querySelector('.detail-track-play-button');
            if (playButton && isPlaying) {
                playButton.classList.add('playing');
            }
        }
        
        // Обновляем состояние mainPlayButton
        if (mainPlayButton) {
            if (trackId === mainPlayButton.dataset.trackId) {
                if (isPlaying) {
                    mainPlayButton.classList.add('playing');
                } else {
                    mainPlayButton.classList.remove('playing');
                }
            } else {
                mainPlayButton.classList.remove('playing');
            }
        }
    }
    
    // Обновление информации о треке в плеере
    function updatePlayerInfo(track) {
        // Обновляем информацию в полноэкранном плеере
        trackTitle.textContent = track.name;
        trackArtist.textContent = track.artist;
        coverImage.src = track.coverUrl;
        
        // Обновляем информацию в мини-плеере
        miniPlayerTitle.textContent = track.name;
        miniPlayerArtist.textContent = track.artist;
        miniPlayerCover.src = track.coverUrl;
    }
    
    // Переключение Play/Pause
    function togglePlayPause() {
        if (isPlaying) {
            audioElement.pause();
            isPlaying = false;
            
            // Обновляем состояние всех кнопок
            playPauseButton.classList.remove('playing');
            miniPlayButton.classList.remove('playing');
            mainPlayButton.classList.remove('playing');
            
            if (currentTrackId) {
                const activeTrack = document.querySelector(`.detail-track-item[data-track-id="${currentTrackId}"]`);
                if (activeTrack) {
                    activeTrack.classList.remove('playing');
                    const playButton = activeTrack.querySelector('.detail-track-play-button');
                    if (playButton) {
                        playButton.classList.remove('playing');
                    }
                }
            }
        } else {
            audioElement.play().then(() => {
                isPlaying = true;
                
                // Обновляем состояние всех кнопок
                playPauseButton.classList.add('playing');
                miniPlayButton.classList.add('playing');
                mainPlayButton.classList.add('playing');

                if (currentTrackId) {
                    const activeTrack = document.querySelector(`.detail-track-item[data-track-id="${currentTrackId}"]`);
                    if (activeTrack) {
                        activeTrack.classList.add('playing');
                        const playButton = activeTrack.querySelector('.detail-track-play-button');
                        if (playButton) {
                            playButton.classList.add('playing');
                        }
                    }
                }
                
                // Обновляем состояние mainPlayButton
                if (mainPlayButton && currentTrackId === mainPlayButton.dataset.trackId) {
                    mainPlayButton.classList.add('playing');
                }
            }).catch(error => {
                console.error('Error playing audio:', error);
            });
        }
    }
    
    // Обновление прогресса воспроизведения
    function updateProgress() {
        const currentTime = audioElement.currentTime;
        const duration = audioElement.duration || 0;
        
        if (duration > 0) {
            // Обновляем прогресс-бар в полном плеере
            const progressPercent = (currentTime / duration) * 100;
            progressBarFill.style.width = `${progressPercent}%`;
            progressHandle.style.left = `${progressPercent}%`;
            
            // Обновляем прогресс-бар в мини-плеере
            miniProgressBarFill.style.width = `${progressPercent}%`;
            
            // Обновляем отображение времени
            currentTimeDisplay.textContent = formatTime(currentTime);
        }
    }
    
    // Перемотка трека
    function seekTrack(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const width = rect.width;
        const clickPercent = x / width;
        
        // Устанавливаем новую позицию воспроизведения
        if (audioElement.duration) {
            audioElement.currentTime = clickPercent * audioElement.duration;
        }
    }
    
    // Установка громкости
    function setVolume(volume) {
        audioElement.volume = volume;
        
        // Обновляем классы для иконок громкости
        if (volume === 0) {
            volumeButton.classList.add('volume-muted');
            volumeButton.classList.remove('volume-medium');
        } else if (volume < 0.5) {
            volumeButton.classList.add('volume-medium');
            volumeButton.classList.remove('volume-muted');
        } else {
            volumeButton.classList.remove('volume-medium');
            volumeButton.classList.remove('volume-muted');
        }
        
        // Сохраняем в localStorage
        localStorage.setItem('playerVolume', volume);
    }
    
    // Переключение звука
    function toggleMute() {
        if (audioElement.volume > 0) {
            // Сохраняем текущую громкость
            localStorage.setItem('previousVolume', audioElement.volume);
            setVolume(0);
            volumeSlider.value = 0;
        } else {
            // Восстанавливаем предыдущую громкость
            const previousVolume = parseFloat(localStorage.getItem('previousVolume') || 0.8);
            setVolume(previousVolume);
            volumeSlider.value = previousVolume * 100;
        }
    }
    
    // Показать полноэкранный плеер
    function showFullPlayer() {
        fullPlayer.classList.add('active');
    }
    
    // Скрыть полноэкранный плеер
    function hideFullPlayer() {
        fullPlayer.classList.remove('active');
    }
    
    // Воспроизведение следующего трека
    function playNextTrack() {
        if (!currentTrackId) return;
        
        // Находим индекс текущего трека
        const currentIndex = currentPlaylist.findIndex(t => t.id === currentTrackId);
        
        if (currentIndex !== -1 && currentIndex < currentPlaylist.length - 1) {
            // Воспроизводим следующий трек
            playTrack(currentPlaylist[currentIndex + 1].id);
        } else if (currentPlaylist.length > 0) {
            // Воспроизводим первый трек, если достигли конца
            playTrack(currentPlaylist[0].id);
        }
    }
    
    // Воспроизведение предыдущего трека
    function playPrevTrack() {
        if (!currentTrackId) return;
        
        // Находим индекс текущего трека
        const currentIndex = currentPlaylist.findIndex(t => t.id === currentTrackId);
        
        if (currentIndex > 0) {
            // Воспроизводим предыдущий трек
            playTrack(currentPlaylist[currentIndex - 1].id);
        } else if (currentPlaylist.length > 0) {
            // Воспроизводим последний трек, если достигли начала
            playTrack(currentPlaylist[currentPlaylist.length - 1].id);
        }
    }
    
    // Форматирование времени
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    }
    
    // Визуализация аудио
    function startVisualization() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            
            // Подключаем аудиоэлемент к анализатору
            const source = audioContext.createMediaElementSource(audioElement);
            source.connect(analyser);
            analyser.connect(audioContext.destination);
            
            // Настройка анализатора
            analyser.fftSize = 256;
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            // Настройка канваса
            const ctx = canvas.getContext('2d');
            canvas.width = canvas.clientWidth;
            canvas.height = canvas.clientHeight;
            
            // Функция отрисовки визуализации
            function draw() {
                if (!isPlaying) return;
                
                visualizer = requestAnimationFrame(draw);
                
                analyser.getByteFrequencyData(dataArray);
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                const barWidth = (canvas.width / bufferLength) * 2.5;
                let barHeight;
                let x = 0;
                
                // Рисуем визуализацию
                for (let i = 0; i < bufferLength; i++) {
                    barHeight = dataArray[i] * 1.5;
                    
                    // Градиент от оранжевого к красному
                    const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
                    gradient.addColorStop(0, 'rgba(255, 165, 0, 0.8)');  // Оранжевый
                    gradient.addColorStop(1, 'rgba(255, 87, 34, 0.8)');  // Красный
                    
                    ctx.fillStyle = gradient;
                    ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
                    
                    x += barWidth + 1;
                }
            }
            
            draw();
        } else {
            if (audioContext.state === 'suspended') {
                audioContext.resume();
            }
            visualizer = requestAnimationFrame(startVisualization);
        }
    }
    
    // Остановка визуализации
    function stopVisualization() {
        if (visualizer) {
            cancelAnimationFrame(visualizer);
            visualizer = null;
        }
    }
    
    // Добавляем обработчик для прогресс-бара в мини-плеере
    const miniProgressBar = document.querySelector('.mini-player-progress');
    miniProgressBar.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const width = rect.width;
        const clickPercent = x / width;
        
        // Устанавливаем новую позицию воспроизведения
        if (audioElement.duration) {
            audioElement.currentTime = clickPercent * audioElement.duration;
        }
    });
    
    // Инициализация плеера
    initPlayer();
    
    // Экспортируем функции для использования другими скриптами
    window.playerFunctions = {
        playTrack,
        togglePlayPause,
        showFullPlayer,
        hideFullPlayer
    };
}); 