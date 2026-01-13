const ExplorationSystem = {
    _mapData: null,
    _selectedArea: null,
    
    init() {
        const gameData = GameState.get('gameData');
        this._mapData = gameData?.exploration || null;
    },
    
    render() {
        const container = document.getElementById('map-container');
        if (!container || !this._mapData) return;
        
        container.innerHTML = '';
        
        const areas = this._mapData.areas || this._mapData.区域详细设计 || [];
        const currentLocation = GameState.get('currentLocation');
        const exploredAreas = GameState.get('exploredAreas') || [];
        
        this._renderConnections(container, areas);
        
        areas.forEach((area, index) => {
            const node = this._createMapNode(area, index, currentLocation, exploredAreas);
            container.appendChild(node);
        });
    },
    
    _createMapNode(area, index, currentLocation, exploredAreas) {
        const areaId = area.区域ID || area.area_id;
        const areaName = area.区域名 || area.name;
        const areaType = area.类型 || area.type || 'city';
        
        const node = document.createElement('div');
        node.className = 'map-node';
        
        const isCurrentLocation = areaId === currentLocation;
        const isExplored = exploredAreas.includes(areaId);
        const isLocked = !this._checkUnlockCondition(area);
        
        if (isCurrentLocation) node.classList.add('current');
        if (isLocked) node.classList.add('locked');
        if (!isExplored && !isLocked) node.classList.add('unexplored');
        
        const typeIcons = {
            'city': '🏘️',
            'type_city': '🏘️',
            '城镇': '🏘️',
            'wild': '🌲',
            'type_wild': '🌲',
            '野外': '🌲',
            'dungeon': '⚔️',
            'type_dungeon': '⚔️',
            '副本': '⚔️',
            'special': '✨',
            'type_special': '✨',
            '特殊区域': '✨'
        };
        
        node.textContent = typeIcons[areaType] || '📍';
        
        const row = Math.floor(index / 5);
        const col = index % 5;
        node.style.left = `${50 + col * 150}px`;
        node.style.top = `${50 + row * 120}px`;
        
        if (!isLocked) {
            node.addEventListener('click', () => this._selectArea(area));
        }
        
        const label = document.createElement('div');
        label.className = 'map-node-label';
        label.textContent = areaName;
        label.style.position = 'absolute';
        label.style.left = `${parseInt(node.style.left) - 20}px`;
        label.style.top = `${parseInt(node.style.top) + 70}px`;
        label.style.fontSize = '12px';
        label.style.color = 'var(--text-secondary)';
        label.style.width = '100px';
        label.style.textAlign = 'center';
        
        node.parentElement?.appendChild(label);
        
        return node;
    },
    
    _renderConnections(container, areas) {
        areas.forEach((area, index) => {
            const connections = area.相邻区域 || area.adjacent || [];
            
            connections.forEach(targetId => {
                const targetIndex = areas.findIndex(a => 
                    (a.区域ID || a.area_id) === targetId
                );
                
                if (targetIndex > index) {
                    const line = this._createConnection(index, targetIndex);
                    container.appendChild(line);
                }
            });
        });
    },
    
    _createConnection(fromIndex, toIndex) {
        const fromRow = Math.floor(fromIndex / 5);
        const fromCol = fromIndex % 5;
        const toRow = Math.floor(toIndex / 5);
        const toCol = toIndex % 5;
        
        const x1 = 80 + fromCol * 150;
        const y1 = 80 + fromRow * 120;
        const x2 = 80 + toCol * 150;
        const y2 = 80 + toRow * 120;
        
        const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
        
        const line = document.createElement('div');
        line.className = 'map-connection';
        line.style.width = `${length}px`;
        line.style.left = `${x1}px`;
        line.style.top = `${y1}px`;
        line.style.transform = `rotate(${angle}deg)`;
        
        return line;
    },
    
    _checkUnlockCondition(area) {
        const condition = area.解锁条件 || area.unlock_condition;
        
        if (!condition) return true;
        if (condition.默认开放 || condition.default_open) return true;
        
        if (condition.需要剧情 || condition.needs_chapter) {
            const required = condition.需要剧情 || condition.needs_chapter;
            return true;
        }
        
        if (condition.需要等级 || condition.needs_level) {
            return true;
        }
        
        if (condition.需要物品 || condition.needs_item) {
            const items = condition.需要物品 || condition.needs_item;
            return items.every(itemId => GameState.hasItem(itemId));
        }
        
        return true;
    },
    
    _selectArea(area) {
        this._selectedArea = area;
        this._showAreaDetail(area);
    },
    
    _showAreaDetail(area) {
        const detail = document.getElementById('location-detail');
        if (!detail) return;
        
        const areaId = area.区域ID || area.area_id;
        const areaName = area.区域名 || area.name;
        const description = area.描述 || area.description || 
                           area.基础信息?.描述 || '没有描述';
        
        const currentLocation = GameState.get('currentLocation');
        const isCurrentLocation = areaId === currentLocation;
        
        detail.innerHTML = `
            <h4>${areaName}</h4>
            <p>${description}</p>
            <div class="location-actions">
                ${!isCurrentLocation ? 
                    `<button onclick="ExplorationSystem.travelTo('${areaId}')">前往</button>` : 
                    '<p>当前位置</p>'
                }
                <button onclick="ExplorationSystem.explore('${areaId}')">探索</button>
            </div>
        `;
    },
    
    travelTo(areaId) {
        const area = this._getAreaById(areaId);
        if (!area) return;
        
        const exploredAreas = GameState.get('exploredAreas') || [];
        if (!exploredAreas.includes(areaId)) {
            GameState.update('exploredAreas', (areas) => [...areas, areaId]);
        }
        
        GameState.set('currentLocation', areaId);
        
        GameState.modifyStatus('stamina', -10);
        
        this.render();
        StatsUI.updateStats();
        
        document.getElementById('current-location').textContent = 
            area.区域名 || area.name;
    },
    
    explore(areaId) {
        const area = this._getAreaById(areaId);
        if (!area) return;
        
        const locations = area.地点列表 || area.locations || [];
        
        Utils.log('Exploring area:', areaId, locations);
        
        ModalUI.close('map');
    },
    
    _getAreaById(areaId) {
        if (!this._mapData) return null;
        
        const areas = this._mapData.areas || this._mapData.区域详细设计 || [];
        return areas.find(a => (a.区域ID || a.area_id) === areaId);
    },
    
    getCurrentArea() {
        const currentLocation = GameState.get('currentLocation');
        return this._getAreaById(currentLocation);
    }
};
