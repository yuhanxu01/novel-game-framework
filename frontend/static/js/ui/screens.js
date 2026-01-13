const ScreenManager = {
    _currentScreen: 'loading',
    _screens: ['loading', 'title', 'game', 'creative'],
    
    init() {
        this._screens.forEach(screen => {
            const el = document.getElementById(`${screen}-screen`);
            if (el) {
                el.classList.remove('active');
            }
        });
        
        this.showScreen('loading');
    },
    
    showScreen(screenName) {
        if (!this._screens.includes(screenName)) {
            Utils.warn('Unknown screen:', screenName);
            return;
        }
        
        this._screens.forEach(screen => {
            const el = document.getElementById(`${screen}-screen`);
            if (el) {
                if (screen === screenName) {
                    el.classList.add('active');
                } else {
                    el.classList.remove('active');
                }
            }
        });
        
        this._currentScreen = screenName;
        GameState.set('currentScreen', screenName);
        
        Utils.log('Screen changed to:', screenName);
    },
    
    getCurrentScreen() {
        return this._currentScreen;
    },
    
    async transitionTo(screenName, duration = 300) {
        const currentEl = document.getElementById(`${this._currentScreen}-screen`);
        const targetEl = document.getElementById(`${screenName}-screen`);
        
        if (currentEl) {
            currentEl.style.opacity = '0';
            await new Promise(r => setTimeout(r, duration));
            currentEl.classList.remove('active');
            currentEl.style.opacity = '';
        }
        
        if (targetEl) {
            targetEl.style.opacity = '0';
            targetEl.classList.add('active');
            await new Promise(r => setTimeout(r, 50));
            targetEl.style.opacity = '1';
        }
        
        this._currentScreen = screenName;
        GameState.set('currentScreen', screenName);
    }
};
