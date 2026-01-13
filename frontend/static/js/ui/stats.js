const StatsUI = {
    init() {
        GameState.subscribe('statusAttributes', () => this.updateStats());
        GameState.subscribe('attributes', () => this.updateStats());
    },
    
    updateStats() {
        this._updateQuickStats();
        this._updateLocationInfo();
    },
    
    _updateQuickStats() {
        const status = GameState.get('statusAttributes') || {};
        
        if (status.health) {
            const healthBar = document.getElementById('health-bar');
            const healthValue = document.getElementById('health-value');
            
            if (healthBar) {
                const percent = (status.health.current / status.health.max) * 100;
                healthBar.style.width = `${percent}%`;
            }
            
            if (healthValue) {
                healthValue.textContent = `${status.health.current}/${status.health.max}`;
            }
        }
        
        if (status.stamina) {
            const staminaBar = document.getElementById('stamina-bar');
            const staminaValue = document.getElementById('stamina-value');
            
            if (staminaBar) {
                const percent = (status.stamina.current / status.stamina.max) * 100;
                staminaBar.style.width = `${percent}%`;
            }
            
            if (staminaValue) {
                staminaValue.textContent = `${status.stamina.current}/${status.stamina.max}`;
            }
        }
    },
    
    _updateLocationInfo() {
        const locationEl = document.getElementById('current-location');
        const timeEl = document.getElementById('current-time');
        
        if (locationEl) {
            const currentLocation = GameState.get('currentLocation');
            const gameData = GameState.get('gameData');
            
            if (currentLocation && gameData?.exploration) {
                const areas = gameData.exploration.areas || 
                              gameData.exploration.区域详细设计 || [];
                const area = areas.find(a => 
                    (a.区域ID || a.area_id) === currentLocation
                );
                
                locationEl.textContent = area?.区域名 || area?.name || currentLocation;
            } else {
                locationEl.textContent = '未知位置';
            }
        }
        
        if (timeEl) {
            const now = new Date();
            const hours = now.getHours();
            
            let timeOfDay = '白天';
            if (hours >= 6 && hours < 12) timeOfDay = '上午';
            else if (hours >= 12 && hours < 18) timeOfDay = '下午';
            else if (hours >= 18 && hours < 22) timeOfDay = '傍晚';
            else timeOfDay = '夜晚';
            
            timeEl.textContent = timeOfDay;
        }
    },
    
    renderStatusModal() {
        const attributes = GameState.get('attributes') || {};
        const status = GameState.get('statusAttributes') || {};
        const flags = GameState.get('flags') || [];
        
        const gameData = GameState.get('gameData');
        const characterName = gameData?.meta?.protagonist_name || '主角';
        
        const nameEl = document.getElementById('character-name');
        if (nameEl) {
            nameEl.textContent = characterName;
        }
        
        const avatarEl = document.getElementById('character-avatar');
        if (avatarEl) {
            avatarEl.textContent = '👤';
        }
        
        const attrList = document.getElementById('attributes-list');
        if (attrList) {
            attrList.innerHTML = '';
            
            Object.entries(attributes).forEach(([key, attr]) => {
                const item = document.createElement('div');
                item.className = 'attribute-item';
                item.innerHTML = `
                    <span class="attr-name">
                        <span>${attr.icon || '📊'}</span>
                        ${attr.name}
                    </span>
                    <span class="attr-value">${attr.value}</span>
                `;
                attrList.appendChild(item);
            });
        }
        
        const effectsList = document.getElementById('effects-list');
        if (effectsList) {
            effectsList.innerHTML = '';
            
            if (flags.length === 0) {
                effectsList.innerHTML = '<span class="no-effects">无特殊状态</span>';
            } else {
                flags.forEach(flag => {
                    const tag = document.createElement('span');
                    tag.className = 'effect-tag';
                    
                    if (flag.includes('buff') || flag.includes('增益')) {
                        tag.classList.add('positive');
                    } else if (flag.includes('debuff') || flag.includes('减益')) {
                        tag.classList.add('negative');
                    }
                    
                    tag.textContent = flag;
                    effectsList.appendChild(tag);
                });
            }
        }
    },
    
    showAttributeChange(attrName, delta) {
        const changeEl = document.createElement('div');
        changeEl.className = 'attribute-change';
        changeEl.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 1rem 2rem;
            background: rgba(0,0,0,0.8);
            border-radius: 8px;
            z-index: 9999;
            animation: fadeInOut 1.5s ease forwards;
        `;
        
        const sign = delta > 0 ? '+' : '';
        const color = delta > 0 ? '#27ae60' : '#e74c3c';
        
        changeEl.innerHTML = `
            <span style="color: ${color}">${attrName} ${sign}${delta}</span>
        `;
        
        document.body.appendChild(changeEl);
        
        setTimeout(() => changeEl.remove(), 1500);
    }
};
