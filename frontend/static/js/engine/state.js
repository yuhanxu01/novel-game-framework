const GameState = {
    _state: {
        isLoaded: false,
        currentScreen: 'loading',
        
        gameData: null,
        
        currentChapter: null,
        currentScene: null,
        currentNode: null,
        
        attributes: {},
        statusAttributes: {},
        inventory: [],
        flags: [],
        relationships: {},
        
        exploredAreas: [],
        currentLocation: null,
        
        playTime: 0,
        startTime: null,
        
        settings: {
            textSpeed: 5,
            autoPlay: false,
            sfxVolume: 80,
            bgmVolume: 50
        }
    },
    
    _listeners: {},
    
    get(key) {
        return this._state[key];
    },
    
    set(key, value) {
        const oldValue = this._state[key];
        this._state[key] = value;
        this._notify(key, value, oldValue);
    },
    
    update(key, updater) {
        const oldValue = this._state[key];
        const newValue = updater(Utils.deepClone(oldValue));
        this._state[key] = newValue;
        this._notify(key, newValue, oldValue);
    },
    
    subscribe(key, callback) {
        if (!this._listeners[key]) {
            this._listeners[key] = [];
        }
        this._listeners[key].push(callback);
        
        return () => {
            this._listeners[key] = this._listeners[key].filter(cb => cb !== callback);
        };
    },
    
    _notify(key, newValue, oldValue) {
        if (this._listeners[key]) {
            this._listeners[key].forEach(callback => callback(newValue, oldValue));
        }
    },
    
    initNewGame(gameData) {
        this._state = {
            ...this._state,
            isLoaded: true,
            gameData: gameData,
            
            currentChapter: gameData.story_tree?.chapters?.[0]?.chapter_id || 'chapter_001',
            currentScene: null,
            currentNode: null,
            
            attributes: this._initAttributes(gameData.attributes),
            statusAttributes: this._initStatusAttributes(gameData.attributes),
            inventory: [],
            flags: [],
            relationships: this._initRelationships(gameData.characters),
            
            exploredAreas: [],
            currentLocation: gameData.exploration?.areas?.[0]?.area_id || 'area_001',
            
            playTime: 0,
            startTime: Date.now()
        };
        
        Utils.log('New game initialized', this._state);
    },
    
    _initAttributes(attributeConfig) {
        const attributes = {};
        
        if (attributeConfig?.基础属性) {
            attributeConfig.基础属性.forEach(attr => {
                attributes[attr.属性ID] = {
                    name: attr.属性名,
                    value: attr.初始值 || 10,
                    max: attr.最大值 || 100,
                    icon: attr.图标建议 || '📊'
                };
            });
        } else {
            Object.entries(GameConfig.DEFAULT_ATTRIBUTES).forEach(([key, attr]) => {
                if (attr.value !== undefined) {
                    attributes[key] = {
                        name: attr.name,
                        value: attr.value,
                        max: 100,
                        icon: attr.icon
                    };
                }
            });
        }
        
        return attributes;
    },
    
    _initStatusAttributes(attributeConfig) {
        const status = {};
        
        if (attributeConfig?.状态属性?.属性列表) {
            attributeConfig.状态属性.属性列表.forEach(attr => {
                status[attr.属性ID] = {
                    name: attr.属性名,
                    current: 100,
                    max: 100,
                    icon: '❤️'
                };
            });
        } else {
            status.health = { name: '生命值', current: 100, max: 100, icon: '❤️' };
            status.stamina = { name: '体力', current: 100, max: 100, icon: '⚡' };
        }
        
        return status;
    },
    
    _initRelationships(characters) {
        const relationships = {};
        
        if (characters) {
            Object.keys(characters).forEach(charId => {
                relationships[charId] = 0;
            });
        }
        
        return relationships;
    },
    
    loadSaveData(saveData) {
        this._state = {
            ...this._state,
            isLoaded: true,
            
            currentChapter: saveData.current_chapter,
            currentScene: saveData.current_scene,
            currentNode: saveData.current_node,
            
            attributes: saveData.attributes?.basic || this._state.attributes,
            statusAttributes: saveData.attributes?.status || this._state.statusAttributes,
            inventory: saveData.inventory || [],
            flags: saveData.flags || [],
            relationships: saveData.relationships || {},
            
            exploredAreas: saveData.exploration?.explored || [],
            currentLocation: saveData.exploration?.current || null,
            
            playTime: saveData.play_time || 0,
            startTime: Date.now()
        };
        
        Utils.log('Save data loaded', this._state);
    },
    
    getSaveData() {
        return {
            current_chapter: this._state.currentChapter,
            current_scene: this._state.currentScene,
            current_node: this._state.currentNode,
            
            attributes: {
                basic: this._state.attributes,
                status: this._state.statusAttributes
            },
            inventory: this._state.inventory,
            flags: this._state.flags,
            relationships: this._state.relationships,
            
            exploration: {
                explored: this._state.exploredAreas,
                current: this._state.currentLocation
            },
            
            play_time: this.getPlayTime()
        };
    },
    
    getPlayTime() {
        if (!this._state.startTime) return this._state.playTime;
        
        const sessionTime = Math.floor((Date.now() - this._state.startTime) / 1000);
        return this._state.playTime + sessionTime;
    },
    
    modifyAttribute(attrId, delta) {
        if (this._state.attributes[attrId]) {
            const attr = this._state.attributes[attrId];
            attr.value = Utils.clamp(attr.value + delta, 0, attr.max);
            this._notify('attributes', this._state.attributes);
        }
    },
    
    modifyStatus(statusId, delta) {
        if (this._state.statusAttributes[statusId]) {
            const status = this._state.statusAttributes[statusId];
            status.current = Utils.clamp(status.current + delta, 0, status.max);
            this._notify('statusAttributes', this._state.statusAttributes);
        }
    },
    
    addItem(item) {
        const existing = this._state.inventory.find(i => i.item_id === item.item_id);
        
        if (existing && item.stackable !== false) {
            existing.count = (existing.count || 1) + (item.count || 1);
        } else {
            this._state.inventory.push({ ...item, count: item.count || 1 });
        }
        
        this._notify('inventory', this._state.inventory);
    },
    
    removeItem(itemId, count = 1) {
        const index = this._state.inventory.findIndex(i => i.item_id === itemId);
        
        if (index !== -1) {
            const item = this._state.inventory[index];
            item.count -= count;
            
            if (item.count <= 0) {
                this._state.inventory.splice(index, 1);
            }
            
            this._notify('inventory', this._state.inventory);
            return true;
        }
        
        return false;
    },
    
    hasItem(itemId, count = 1) {
        const item = this._state.inventory.find(i => i.item_id === itemId);
        return item && (item.count || 1) >= count;
    },
    
    addFlag(flag) {
        if (!this._state.flags.includes(flag)) {
            this._state.flags.push(flag);
            this._notify('flags', this._state.flags);
        }
    },
    
    removeFlag(flag) {
        const index = this._state.flags.indexOf(flag);
        if (index !== -1) {
            this._state.flags.splice(index, 1);
            this._notify('flags', this._state.flags);
        }
    },
    
    hasFlag(flag) {
        return this._state.flags.includes(flag);
    },
    
    modifyRelationship(charId, delta) {
        if (this._state.relationships[charId] === undefined) {
            this._state.relationships[charId] = 0;
        }
        
        this._state.relationships[charId] = Utils.clamp(
            this._state.relationships[charId] + delta,
            -100,
            100
        );
        
        this._notify('relationships', this._state.relationships);
    },
    
    getRelationship(charId) {
        return this._state.relationships[charId] || 0;
    },
    
    getPlayerState() {
        return {
            attributes: this._state.attributes,
            status: this._state.statusAttributes,
            inventory: this._state.inventory,
            flags: this._state.flags,
            relationships: this._state.relationships
        };
    }
};
