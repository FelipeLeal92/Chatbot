(function() {
    // Configuração
    // Detecta automaticamente a origem de onde este script (loader.js) foi carregado
    // Assim funciona tanto em localhost quanto em produção sem mudar código
    const scriptTag = document.currentScript || document.querySelector('script[src*="loader.js"]');
    const scriptUrl = new URL(scriptTag.src);
    const WIDGET_URL = scriptUrl.origin + "/index.html";
    
    // Criar container do Iframe
    const container = document.createElement('div');
    container.id = "lealverse-widget-container";
    container.style.position = "fixed";
    container.style.bottom = "20px";
    container.style.right = "20px";
    container.style.zIndex = "999999";
    container.style.border = "none";
    container.style.width = "60px"; // Tamanho inicial (só o botão)
    container.style.height = "60px";
    container.style.transition = "all 0.3s ease";
    container.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
    container.style.borderRadius = "30px"; // Redondo inicialmente
    container.style.overflow = "hidden";

    // Criar Iframe
    const iframe = document.createElement('iframe');
    iframe.src = WIDGET_URL;
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "none";
    iframe.allowTransparency = "true";

    container.appendChild(iframe);
    document.body.appendChild(container);

    // Ouvir mensagens do React (Filho) para redimensionar o Iframe (Pai)
    window.addEventListener('message', function(event) {
        // Segurança: verificar origem se necessário
        if (event.data.type === 'LEALVERSE_RESIZE') {
            if (event.data.isOpen) {
                // Estado Aberto
                container.style.width = "350px";
                container.style.height = "550px";
                container.style.borderRadius = "12px";
            } else {
                // Estado Fechado (apenas botão)
                container.style.width = "60px";
                container.style.height = "60px";
                container.style.borderRadius = "30px";
            }
        }
    });
})();