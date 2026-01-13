const Game = {
    async init() {
        Utils.log('Initializing game...');
        
        ScreenManager.init();
        NarrativeUI.init();
        ChoicesUI.init();
        ModalUI.init();
        StatsUI.init();
        InventorySystem.init();
        CreativeChat.init();
        CreativeEditor.init();
        
        this._bindEvents();
        
        await this._loadGameData();
    },
    
    _bindEvents() {
        document.getElementById('btn-new-game')?.addEventListener('click', 
            () => this.startNewGame()
        );
        
        document.getElementById('btn-load-game')?.addEventListener('click', 
            () => ModalUI.open('save')
        );
        
        document.getElementById('btn-creative-mode')?.addEventListener('click', 
            () => this.enterCreativeMode()
        );
        
        document.getElementById('btn-settings')?.addEventListener('click', 
            () => ModalUI.open('settings')
        );
        
        document.getElementById('btn-inventory')?.addEventListener('click', 
            () => ModalUI.open('inventory')
        );
        
        document.getElementById('btn-status')?.addEventListener('click', 
            () => ModalUI.open('status')
        );
        
        document.getElementById('btn-map')?.addEventListener('click', 
            () => ModalUI.open('map')
        );
        
        document.getElementById('btn-save')?.addEventListener('click', 
            () => ModalUI.open('save')
        );
        
        document.getElementById('btn-menu')?.addEventListener('click', 
            () => this._showGameMenu()
        );
        
        document.getElementById('btn-exit-creative')?.addEventListener('click', 
            () => this.exitCreativeMode()
        );
        
        this._bindSettingsEvents();
    },
    
    _bindSettingsEvents() {
        document.getElementById('text-speed')?.addEventListener('change', (e) => {
            GameState.update('settings', s => ({ ...s, textSpeed: parseInt(e.target.value) }));
        });
        
        document.getElementById('auto-play')?.addEventListener('change', (e) => {
            GameState.update('settings', s => ({ ...s, autoPlay: e.target.checked }));
        });
        
        document.getElementById('sfx-volume')?.addEventListener('change', (e) => {
            GameState.update('settings', s => ({ ...s, sfxVolume: parseInt(e.target.value) }));
        });
        
        document.getElementById('bgm-volume')?.addEventListener('change', (e) => {
            GameState.update('settings', s => ({ ...s, bgmVolume: parseInt(e.target.value) }));
        });
    },
    
    async _loadGameData() {
        Utils.log('Loading game data...');
        
        try {
            const response = await Utils.get(APIEndpoints.getGameData());
            
            if (response.success && response.data) {
                this._onGameDataLoaded(response.data);
            } else {
                throw new Error('Invalid game data response');
            }
        } catch (error) {
            Utils.warn('Failed to load from API, trying local data:', error);
            
            const localData = await this._loadLocalGameData();
            
            if (localData) {
                this._onGameDataLoaded(localData);
            } else {
                this._showNoDataScreen();
            }
        }
    },
    
    async _loadLocalGameData() {
        try {
            const response = await fetch('data/game_data.json');
            return await response.json();
        } catch (error) {
            Utils.warn('No local game data found');
            return null;
        }
    },
    
    _onGameDataLoaded(gameData) {
        Utils.log('Game data loaded:', gameData);
        
        GameState.set('gameData', gameData);
        
        const title = gameData.meta?.title || gameData.名称 || '文字冒险游戏';
        const description = gameData.meta?.description || gameData.描述 || '';
        
        document.getElementById('game-title').textContent = title;
        document.getElementById('game-description').textContent = description;
        
        ScreenManager.showScreen('title');
    },
    
    _showNoDataScreen() {
        document.getElementById('game-title').textContent = '文字冒险游戏';
        document.getElementById('game-description').textContent = 
            '暂无游戏数据。请在创造模式中上传小说并生成游戏，或导入现有游戏数据。';
        
        document.getElementById('btn-new-game').style.display = 'none';
        document.getElementById('btn-load-game').style.display = 'none';
        
        ScreenManager.showScreen('title');
    },
    
    async startNewGame() {
        Utils.log('Starting new game...');
        
        const gameData = GameState.get('gameData');
        
        if (!gameData) {
            alert('没有游戏数据');
            return;
        }
        
        GameState.initNewGame(gameData);
        
        ScreenManager.showScreen('game');
        
        NarrativeUI.clear();
        StatsUI.updateStats();
        ExplorationSystem.init();
        
        const firstChapter = gameData.story_tree?.chapters?.[0]?.chapter_id || 'chapter_001';
        await StoryEngine.startChapter(firstChapter);
    },
    
    enterCreativeMode() {
        Utils.log('Entering creative mode...');
        ScreenManager.showScreen('creative');
        CreativeEditor.loadHistory();
    },
    
    exitCreativeMode() {
        Utils.log('Exiting creative mode...');
        ScreenManager.showScreen('title');
    },
    
    _showGameMenu() {
        const menu = document.createElement('div');
        menu.className = 'game-menu-overlay';
        menu.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
        `;
        
        menu.innerHTML = `
            <div style="text-align: center;">
                <h2 style="margin-bottom: 2rem;">游戏菜单</h2>
                <button class="menu-btn" onclick="ModalUI.open('save'); this.closest('.game-menu-overlay').remove();">
                    保存/读取
                </button>
                <button class="menu-btn" onclick="ModalUI.open('settings'); this.closest('.game-menu-overlay').remove();">
                    设置
                </button>
                <button class="menu-btn" onclick="Game.returnToTitle(); this.closest('.game-menu-overlay').remove();">
                    返回标题
                </button>
                <button class="menu-btn" onclick="this.closest('.game-menu-overlay').remove();">
                    继续游戏
                </button>
            </div>
        `;
        
        document.body.appendChild(menu);
        
        menu.addEventListener('click', (e) => {
            if (e.target === menu) {
                menu.remove();
            }
        });
    },
    
    returnToTitle() {
        if (confirm('确定要返回标题画面吗？未保存的进度将丢失。')) {
            ScreenManager.showScreen('title');
            NarrativeUI.clear();
            ChoicesUI.clearChoices();
        }
    },
    
    async quickSave() {
        const saveData = GameState.getSaveData();
        
        Utils.saveToLocalStorage('quick_save', {
            ...saveData,
            timestamp: new Date().toISOString()
        });
        
        await NarrativeUI.showSystemMessage('快速存档完成');
    },
    
    async quickLoad() {
        const saveData = Utils.loadFromLocalStorage('quick_save');
        
        if (saveData) {
            GameState.loadSaveData(saveData);
            await NarrativeUI.showSystemMessage('快速读档完成');
            StatsUI.updateStats();
        } else {
            await NarrativeUI.showSystemMessage('没有快速存档');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Game.init().catch(error => {
        console.error('Game initialization failed:', error);
    });
});

document.addEventListener('keydown', (e) => {
    if (GameState.get('currentScreen') === 'game') {
        if (e.key === 'F5') {
            e.preventDefault();
            Game.quickSave();
        }
        
        if (e.key === 'F9') {
            e.preventDefault();
            Game.quickLoad();
        }
        
        if (e.key === 'i' || e.key === 'I') {
            if (!e.ctrlKey && !e.altKey) {
                ModalUI.open('inventory');
            }
        }
        
        if (e.key === 'm' || e.key === 'M') {
            if (!e.ctrlKey && !e.altKey) {
                ModalUI.open('map');
            }
        }
    }
});
