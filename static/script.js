function applySettings() {
    const theme = localStorage.getItem('theme') || 'light';
    const fontSize = localStorage.getItem('fontSize') || '16px';
    const fontFam = localStorage.getItem('fontFam') || 'system-ui';

    document.documentElement.setAttribute('data-theme', theme);
    document.body.style.fontSize = fontSize;
    document.body.style.fontFamily = fontFam;

    // Адекватная работа прогресс-бара
    const fill = document.getElementById('progress-bar-fill');
    if (fill) {
        const percent = fill.getAttribute('data-percent');
        setTimeout(() => {
            fill.style.width = percent + "%";
        }, 100);
    }
}

function setTheme(t) { localStorage.setItem('theme', t); applySettings(); }
function setFontSize(s) { localStorage.setItem('fontSize', s); applySettings(); }
function setFontFamily(f) { localStorage.setItem('fontFam', f); applySettings(); }

document.addEventListener('DOMContentLoaded', applySettings);
