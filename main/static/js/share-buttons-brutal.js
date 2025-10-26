// ===== БРУТАЛЬНЫЕ КНОПКИ ПОДЕЛИТЬСЯ =====

document.addEventListener('DOMContentLoaded', function() {
    
    // Функция для показа уведомления
    function showNotification(message) {
        // Удаляем предыдущее уведомление если есть
        const existingNotification = document.querySelector('.brutal-copy-notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Создаем новое уведомление
        const notification = document.createElement('div');
        notification.className = 'brutal-copy-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Показываем уведомление
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Скрываем уведомление через 3 секунды
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Обработчик кнопки копирования
    const copyButtons = document.querySelectorAll('.brutal-copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Получаем текст из блока контента
            const contentBlock = document.querySelector('.brutal-service-detail-content');
            let textToCopy = '';
            
            if (contentBlock) {
                // Извлекаем весь текстовый контент из блока
                textToCopy = contentBlock.innerText || contentBlock.textContent;
                
                // Добавляем заголовок страницы и URL
                const pageTitle = document.title;
                const pageUrl = window.location.href;
                
                textToCopy = `${pageTitle}\n\n${textToCopy}\n\n${pageUrl}`;
            } else {
                // Fallback на data-text если блок контента не найден
                textToCopy = this.getAttribute('data-text');
            }
            
            if (navigator.clipboard && window.isSecureContext) {
                // Современный способ копирования
                navigator.clipboard.writeText(textToCopy).then(() => {
                    showNotification('Текст скопирован!');
                }).catch(err => {
                    console.error('Ошибка копирования:', err);
                    fallbackCopyTextToClipboard(textToCopy);
                });
            } else {
                // Fallback для старых браузеров
                fallbackCopyTextToClipboard(textToCopy);
            }
        });
    });
    
    // Fallback функция для копирования
    function fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showNotification('Текст скопирован!');
            } else {
                showNotification('Ошибка копирования');
            }
        } catch (err) {
            console.error('Fallback: Ошибка копирования', err);
            showNotification('Ошибка копирования');
        }
        
        document.body.removeChild(textArea);
    }
    
    // Обработчики кнопок социальных сетей
    const socialLinks = document.querySelectorAll('.brutal-social-link');
    socialLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = this.getAttribute('data-url');
            const platform = this.classList.contains('vk') ? 'vk' : 'telegram';
            
            if (!url) {
                console.error('URL не указан для кнопки социальной сети');
                return;
            }
            
            let shareUrl = '';
            
            if (platform === 'vk') {
                shareUrl = `https://vk.com/share.php?url=${encodeURIComponent(url)}&title=${encodeURIComponent(document.title)}`;
            } else if (platform === 'telegram') {
                shareUrl = `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(document.title)}`;
            }
            
            if (shareUrl) {
                // Открываем в новом окне
                window.open(shareUrl, '_blank', 'width=600,height=400,scrollbars=yes,resizable=yes');
            }
        });
    });
    
    // Добавляем анимацию при загрузке
    const shareBlock = document.querySelector('.brutal-share-block');
    if (shareBlock) {
        shareBlock.style.opacity = '0';
        shareBlock.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            shareBlock.style.transition = 'all 0.5s ease';
            shareBlock.style.opacity = '1';
            shareBlock.style.transform = 'translateY(0)';
        }, 200);
    }
    
    console.log('Брутальные кнопки поделиться загружены!');
});
