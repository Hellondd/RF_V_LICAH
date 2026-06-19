const Auth = {
    getToken() {
        return localStorage.getItem('access_token');
    },

    getUser() {
        const raw = localStorage.getItem('user');
        return raw ? JSON.parse(raw) : null;
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    isAdmin() {
        const user = this.getUser();
        return user?.role === 'admin';
    },

    saveSession(token, user) {
        localStorage.setItem('access_token', token);
        localStorage.setItem('user', JSON.stringify(user));
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = 'index.html';
    },

    async fetchMe() {
        const { data } = await api.get('/auth/me');
        localStorage.setItem('user', JSON.stringify(data));
        return data;
    },

    requireAuth(redirectTo = 'login.html') {
        if (!this.isLoggedIn()) {
            window.location.href = redirectTo;
            return false;
        }
        return true;
    },

    requireAdmin(redirectTo = 'index.html') {
        if (!this.requireAuth('login.html')) return false;
        if (!this.isAdmin()) {
            window.location.href = redirectTo;
            return false;
        }
        return true;
    },

    updateNav() {
        const container = document.getElementById('navUserArea');
        if (!container) return;

        const user = this.getUser();

        if (user) {
            // Авторизованный пользователь
            container.innerHTML = `
                <span class="nav-user">${user.name}</span>
                <a href="cabinet.html" class="nav-user-link">Кабинет</a>
                ${user.role === 'admin' ? '<a href="admin.html" class="nav-user-link">Админ</a>' : ''}
                <a href="#" id="logoutBtn" class="nav-user-link logout">Выйти</a>
            `;
            document.getElementById('logoutBtn')?.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        } else {
            // Неавторизованный — две акцентные кнопки
            container.innerHTML = `
                <a href="login.html" class="btn-login">Вход</a>
                <a href="register.html" class="btn-register">Регистрация</a>
            `;
        }
    },
};

window.Auth = Auth;

document.addEventListener('DOMContentLoaded', () => {
    Auth.updateNav();
});