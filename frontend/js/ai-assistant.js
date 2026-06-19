const AI_RESPONSES = {
    'день россии': 'День России отмечается 12 июня. Это государственный праздник, установленный в 1992 году в честь принятия Декларации о государственном суверенитете РСФСР.',
    'регионы': 'На сайте вы найдёте карточки регионов России с описанием, фактами и культурой. Перейдите в раздел «Карта регионов».',
    'поздравление': 'Для создания поздравительной открытки перейдите в раздел «Открытка», выберите шаблон и введите текст. С Днём России!',
    'викторина': 'Пройдите викторину в соответствующем разделе! Вопросы о Дне России, истории и географии. Результаты сохраняются в личном кабинете.',
    'помощь': 'Я могу рассказать о Дне России, регионах, помочь с открыткой или викториной. Выберите вопрос ниже или напишите свой.',
    'default': 'Спасибо за вопрос! Я — ИИ-помощник проекта «Россия в лицах». Спросите о Дне России, регионах, викторине или открытках.',
};

function getAiResponse(text) {
    const lower = text.toLowerCase();
    for (const [key, answer] of Object.entries(AI_RESPONSES)) {
        if (key !== 'default' && lower.includes(key)) return answer;
    }
    return AI_RESPONSES.default;
}

document.addEventListener('DOMContentLoaded', () => {
    const fab = document.getElementById('aiFab');
    const modal = document.getElementById('aiModal');
    const body = document.getElementById('aiBody');
    if (!fab || !modal || !body) return;

    fab.addEventListener('click', () => modal.classList.toggle('open'));

    document.querySelectorAll('.ai-quick-btns button').forEach((btn) => {
        btn.addEventListener('click', () => addMessage(btn.textContent, 'user'));
    });

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = `ai-message ${type}`;
        div.textContent = text;
        body.appendChild(div);

        if (type === 'user') {
            setTimeout(() => {
                const reply = document.createElement('div');
                reply.className = 'ai-message bot';
                reply.textContent = getAiResponse(text);
                body.appendChild(reply);
                body.scrollTop = body.scrollHeight;
            }, 400);
        }
        body.scrollTop = body.scrollHeight;
    }

    if (!body.querySelector('.ai-message')) {
        const welcome = document.createElement('div');
        welcome.className = 'ai-message bot';
        welcome.textContent = 'Здравствуйте! Я помогу узнать о Дне России. Выберите вопрос или задайте свой.';
        body.appendChild(welcome);
    }
});
