// JavaScript para o Sistema de Placar da Igreja

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização
    initializeApp();
    
    // Auto-dismiss alerts após 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

function initializeApp() {
    // Adicionar classes de animação aos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Melhorar a experiência do usuário com tooltips
    initializeTooltips();
    
    // Adicionar confirmação para ações importantes
    addConfirmationDialogs();
    
    // Melhorar a navegação
    improveNavigation();
}

function initializeTooltips() {
    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function addConfirmationDialogs() {
    // Adicionar confirmação para formulários importantes
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner"></span> Processando...';
                submitBtn.disabled = true;
            }
        });
    });
}

function improveNavigation() {
    // Destacar item ativo no menu
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Função para calcular pontuação em tempo real (usado no formulário de atividades)
function calcularPontuacaoTempo() {
    const pontuacaoConfig = {
        pessoas_novas: 10,
        elite_novos: 15,
        celulas_novas: 5,
        arena_participacao: 20,
        domingo_participacao: 10,
        parceiro_deus_novos: 25
    };
    
    let total = 0;
    
    // Calcular baseado nos inputs
    Object.keys(pontuacaoConfig).forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento) {
            if (elemento.type === 'checkbox') {
                if (elemento.checked) {
                    total += pontuacaoConfig[campo];
                }
            } else if (elemento.type === 'number') {
                const valor = parseInt(elemento.value) || 0;
                total += valor * pontuacaoConfig[campo];
            }
        }
    });
    
    return total;
}

// Função para animar números (contador)
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        element.textContent = Math.round(current);
        
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = end;
            clearInterval(timer);
        }
    }, 16);
}

// Função para mostrar notificações toast
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover o toast após ser ocultado
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Função para validar formulários
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Função para formatar números
function formatNumber(num) {
    return new Intl.NumberFormat('pt-BR').format(num);
}

// Função para salvar dados no localStorage
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
        console.warn('Não foi possível salvar no localStorage:', e);
    }
}

// Função para carregar dados do localStorage
function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.warn('Não foi possível carregar do localStorage:', e);
        return null;
    }
}

// Função para debounce (evitar muitas chamadas seguidas)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Exportar funções para uso global
window.PlacarApp = {
    calcularPontuacaoTempo,
    animateNumber,
    showToast,
    validateForm,
    formatNumber,
    saveToLocalStorage,
    loadFromLocalStorage,
    debounce
};
