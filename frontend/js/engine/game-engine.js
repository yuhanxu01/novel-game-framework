class GameEngine {
    constructor(config = {}) {
        this.apiBase = config.apiBase || '/api/game';
        this.projectId = config.projectId || null;
        
        this.gameData = null;
        this.playerState = {
            currentChapter: null,
            currentScene: null,
            currentNode: null,
            attributes: {},
            inventory: [],
            flags: [],
            relationships: {},
            exploration: {},
            playTime: 0
        };
        
        this.isRunning = false;
        this.isPaused = false;
        this.startTime = null;
        
        this.eventListeners = {};
        
        this.ui = null;
        this.inventory = null;
        this.attributes = null;
        this.exploration = null;
    }
    
    async init(projectId) {
        this.projectId = projectId;
        
        try {
            const response = await fetch(`${this.apiBase}/project/${projectId}/`);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error);
            }
            
            this.gameData = result.data;
            this._initPlayerState();
            
            this.emit('init', { gameData: this.gameData });
            
            return true;
        } catch (error) {
            console.error('游戏初始化失败:', error);
            this.emit('error', { message: '游戏初始化失败', error });
            return false;
        }
    }
    
    _initPlayerState() {
        const attrs = this.gameData.attributes;
        if (attrs && attrs.基础属性) {
            for (const attr of attrs.基础属性) {
                this.playerState.attributes[attr.属性ID] = attr.初始值 || 10;
            }
        }
        
        if (attrs && attrs.状态属性) {
            for (const attr of attrs.状态属性) {
                const maxValue = this._calculateMaxValue(attr);
                this.playerState.attributes[attr.属性ID] = maxValue;
                this.playerState.attributes[`${attr.属性ID}_max`] = maxValue;
            }
        }
        
        const story = this.gameData.story_tree;
        if (story && story.剧情结构) {
            if (story.剧情结构.序章) {
                this.playerState.currentChapter = story.剧情结构.序章.章节ID;
            } else if (story.剧情结构.章节列表 && story.剧情结构.章节列表.length > 0) {
                this.playerState.currentChapter = story.剧情结构.章节列表[0].章节ID;
            }
        }
    }
    
    _calculateMaxValue(statusAttr) {
        if (statusAttr.最大值计算) {
            return 100;
        }
        return statusAttr.最大值 || 100;
    }
    
    start() {
        if (!this.gameData) {
            console.error('请先初始化游戏');
            return;
        }
        
        this.isRunning = true;
        this.startTime = Date.now();
        
        this._loadFirstScene();
        
        this.emit('start', { playerState: this.playerState });
    }
    
    _loadFirstScene() {
        const story = this.gameData.story_tree;
        if (!story || !story.剧情结构) return;
        
        let firstChapter = null;
        if (story.剧情结构.序章) {
            firstChapter = story.剧情结构.序章;
        } else if (story.剧情结构.章节列表 && story.剧情结构.章节列表.length > 0) {
            firstChapter = story.剧情结构.章节列表[0];
        }
        
        if (firstChapter && firstChapter.场景列表 && firstChapter.场景列表.length > 0) {
            this.playerState.currentScene = firstChapter.场景列表[0].场景ID;
            
            const scene = firstChapter.场景列表[0];
            if (scene.场景流程 && scene.场景流程.length > 0) {
                this.playerState.currentNode = scene.场景流程[0].节点ID;
            }
            
            this.emit('sceneLoad', { chapter: firstChapter, scene: scene });
        }
    }
    
    getCurrentNode() {
        const chapter = this._getCurrentChapter();
        const scene = this._getCurrentScene(chapter);
        
        if (!scene || !scene.场景流程) return null;
        
        return scene.场景流程.find(node => node.节点ID === this.playerState.currentNode);
    }
    
    _getCurrentChapter() {
        const story = this.gameData.story_tree;
        if (!story || !story.剧情结构) return null;
        
        if (story.剧情结构.序章 && story.剧情结构.序章.章节ID === this.playerState.currentChapter) {
            return story.剧情结构.序章;
        }
        
        if (story.剧情结构.章节列表) {
            return story.剧情结构.章节列表.find(ch => ch.章节ID === this.playerState.currentChapter);
        }
        
        return null;
    }
    
    _getCurrentScene(chapter) {
        if (!chapter || !chapter.场景列表) return null;
        return chapter.场景列表.find(sc => sc.场景ID === this.playerState.currentScene);
    }
    
    processNode(node) {
        if (!node) return;
        
        switch (node.节点类型) {
            case '对话':
                this.emit('dialogue', {
                    character: node.角色,
                    content: node.内容,
                    nextNode: node.下一节点
                });
                break;
            
            case '旁白':
                this.emit('narration', {
                    content: node.内容,
                    nextNode: node.下一节点
                });
                break;
            
            case '选择':
                const availableOptions = this._filterOptions(node.选项 || []);
                this.emit('choice', {
                    description: node.选择描述,
                    options: availableOptions,
                    timeLimit: node.时间限制
                });
                break;
            
            case '检定':
                const result = this._performCheck(node);
                this.emit('check', {
                    attribute: node.检定属性,
                    difficulty: node.难度,
                    result: result,
                    nextNode: result.success ? node.成功节点 : node.失败节点
                });
                break;
            
            case '战斗':
                this.emit('battle', {
                    enemies: node.敌人,
                    rewards: node.奖励,
                    nextNode: node.下一节点
                });
                break;
            
            case '获取物品':
                this._addItems(node.物品);
                this.emit('itemGet', {
                    items: node.物品,
                    nextNode: node.下一节点
                });
                break;
            
            case '触发事件':
                this._triggerEvent(node);
                break;
            
            default:
                if (node.下一节点) {
                    this.goToNode(node.下一节点);
                }
        }
    }
    
    _filterOptions(options) {
        return options.filter(opt => {
            if (!opt.条件) return true;
            return this._checkCondition(opt.条件);
        }).map(opt => ({
            ...opt,
            meetsCondition: true,
            conditionDisplay: this._formatCondition(opt.条件)
        }));
    }
    
    _checkCondition(condition) {
        if (!condition) return true;
        
        if (condition.需要属性) {
            for (const [attr, value] of Object.entries(condition.需要属性)) {
                if ((this.playerState.attributes[attr] || 0) < value) {
                    return false;
                }
            }
        }
        
        if (condition.需要物品) {
            for (const itemId of condition.需要物品) {
                if (!this.playerState.inventory.some(item => item.id === itemId)) {
                    return false;
                }
            }
        }
        
        if (condition.需要标记) {
            for (const flag of condition.需要标记) {
                if (!this.playerState.flags.includes(flag)) {
                    return false;
                }
            }
        }
        
        if (condition.需要好感) {
            for (const [charId, value] of Object.entries(condition.需要好感)) {
                if ((this.playerState.relationships[charId] || 0) < value) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    _formatCondition(condition) {
        if (!condition) return '';
        
        const parts = [];
        
        if (condition.需要属性) {
            for (const [attr, value] of Object.entries(condition.需要属性)) {
                const attrName = this._getAttributeName(attr);
                parts.push(`${attrName} ≥ ${value}`);
            }
        }
        
        if (condition.需要物品) {
            parts.push(`需要物品: ${condition.需要物品.join(', ')}`);
        }
        
        return parts.join(' | ');
    }
    
    _getAttributeName(attrId) {
        const attrs = this.gameData.attributes;
        if (attrs && attrs.基础属性) {
            const attr = attrs.基础属性.find(a => a.属性ID === attrId);
            if (attr) return attr.属性名;
        }
        return attrId;
    }
    
    _performCheck(node) {
        const attrValue = this.playerState.attributes[node.检定属性] || 0;
        const difficulty = node.难度 || 50;
        
        const roll = Math.random() * 100;
        const successChance = 50 + (attrValue - difficulty);
        const success = roll < successChance;
        
        return {
            success,
            roll: Math.floor(roll),
            target: Math.floor(successChance),
            attrValue,
            difficulty
        };
    }
    
    selectOption(optionId) {
        const node = this.getCurrentNode();
        if (!node || node.节点类型 !== '选择') return;
        
        const option = node.选项.find(opt => opt.选项ID === optionId);
        if (!option) return;
        
        if (option.效果) {
            this._applyEffects(option.效果);
        }
        
        this.emit('optionSelected', { option });
        
        if (option.导向) {
            this.goToNode(option.导向);
        }
    }
    
    _applyEffects(effects) {
        if (effects.属性变化) {
            for (const [attr, change] of Object.entries(effects.属性变化)) {
                this.playerState.attributes[attr] = (this.playerState.attributes[attr] || 0) + change;
                this.emit('attributeChange', { attribute: attr, change, newValue: this.playerState.attributes[attr] });
            }
        }
        
        if (effects.好感变化) {
            for (const [charId, change] of Object.entries(effects.好感变化)) {
                this.playerState.relationships[charId] = (this.playerState.relationships[charId] || 0) + change;
                this.emit('relationshipChange', { character: charId, change, newValue: this.playerState.relationships[charId] });
            }
        }
        
        if (effects.获得物品) {
            this._addItems(effects.获得物品);
        }
        
        if (effects.设置标记) {
            for (const flag of effects.设置标记) {
                if (!this.playerState.flags.includes(flag)) {
                    this.playerState.flags.push(flag);
                }
            }
        }
        
        if (effects.移除标记) {
            this.playerState.flags = this.playerState.flags.filter(f => !effects.移除标记.includes(f));
        }
    }
    
    _addItems(items) {
        if (!Array.isArray(items)) items = [items];
        
        for (const itemId of items) {
            const itemData = this._getItemData(itemId);
            if (itemData) {
                const existing = this.playerState.inventory.find(i => i.id === itemId);
                if (existing && itemData.可堆叠) {
                    existing.count = (existing.count || 1) + 1;
                } else {
                    this.playerState.inventory.push({
                        id: itemId,
                        count: 1,
                        data: itemData
                    });
                }
            }
        }
        
        this.emit('inventoryChange', { inventory: this.playerState.inventory });
    }
    
    _getItemData(itemId) {
        const items = this.gameData.items;
        if (!items || !items.物品列表) return null;
        return items.物品列表.find(item => item.物品ID === itemId);
    }
    
    _triggerEvent(node) {
        if (node.事件效果) {
            this._applyEffects(node.事件效果);
        }
        
        this.emit('eventTriggered', { event: node });
        
        if (node.下一节点) {
            this.goToNode(node.下一节点);
        }
    }
    
    goToNode(nodeId) {
        this.playerState.currentNode = nodeId;
        
        const node = this.getCurrentNode();
        if (node) {
            this.emit('nodeChange', { node });
            this.processNode(node);
        }
    }
    
    goToScene(sceneId) {
        this.playerState.currentScene = sceneId;
        
        const chapter = this._getCurrentChapter();
        const scene = this._getCurrentScene(chapter);
        
        if (scene) {
            if (scene.场景流程 && scene.场景流程.length > 0) {
                this.playerState.currentNode = scene.场景流程[0].节点ID;
            }
            
            this.emit('sceneChange', { scene });
        }
    }
    
    goToChapter(chapterId) {
        this.playerState.currentChapter = chapterId;
        
        const chapter = this._getCurrentChapter();
        if (chapter && chapter.场景列表 && chapter.场景列表.length > 0) {
            const firstScene = chapter.场景列表[0];
            this.playerState.currentScene = firstScene.场景ID;
            
            if (firstScene.场景流程 && firstScene.场景流程.length > 0) {
                this.playerState.currentNode = firstScene.场景流程[0].节点ID;
            }
            
            this.emit('chapterChange', { chapter });
        }
    }
    
    continue() {
        const node = this.getCurrentNode();
        if (node && node.下一节点) {
            this.goToNode(node.下一节点);
        }
    }
    
    async save(slot = 0, saveName = null) {
        this.playerState.playTime = Math.floor((Date.now() - this.startTime) / 1000) + (this.playerState.playTime || 0);
        
        try {
            const response = await fetch(`${this.apiBase}/project/${this.projectId}/save/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    slot,
                    save_name: saveName || `存档 ${slot}`,
                    current_chapter: this.playerState.currentChapter,
                    current_scene: this.playerState.currentScene,
                    current_node: this.playerState.currentNode,
                    attributes: this.playerState.attributes,
                    inventory: this.playerState.inventory,
                    flags: this.playerState.flags,
                    relationships: this.playerState.relationships,
                    exploration: this.playerState.exploration,
                    play_time: this.playerState.playTime
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.emit('saved', { slot, saveName });
            }
            
            return result;
        } catch (error) {
            console.error('保存失败:', error);
            return { success: false, error: error.message };
        }
    }
    
    async load(slot) {
        try {
            const response = await fetch(`${this.apiBase}/project/${this.projectId}/load/${slot}/`);
            const result = await response.json();
            
            if (result.success) {
                const data = result.data;
                
                this.playerState.currentChapter = data.current_chapter;
                this.playerState.currentScene = data.current_scene;
                this.playerState.currentNode = data.current_node;
                this.playerState.attributes = data.attributes;
                this.playerState.inventory = data.inventory;
                this.playerState.flags = data.flags;
                this.playerState.relationships = data.relationships;
                this.playerState.exploration = data.exploration;
                this.playerState.playTime = data.play_time;
                
                this.startTime = Date.now();
                this.isRunning = true;
                
                this.emit('loaded', { slot, data });
                
                const node = this.getCurrentNode();
                if (node) {
                    this.processNode(node);
                }
            }
            
            return result;
        } catch (error) {
            console.error('加载失败:', error);
            return { success: false, error: error.message };
        }
    }
    
    async listSaves() {
        try {
            const response = await fetch(`${this.apiBase}/project/${this.projectId}/saves/`);
            return await response.json();
        } catch (error) {
            console.error('获取存档列表失败:', error);
            return { success: false, error: error.message };
        }
    }
    
    on(event, callback) {
        if (!this.eventListeners[event]) {
            this.eventListeners[event] = [];
        }
        this.eventListeners[event].push(callback);
    }
    
    off(event, callback) {
        if (!this.eventListeners[event]) return;
        this.eventListeners[event] = this.eventListeners[event].filter(cb => cb !== callback);
    }
    
    emit(event, data) {
        if (!this.eventListeners[event]) return;
        for (const callback of this.eventListeners[event]) {
            callback(data);
        }
    }
    
    pause() {
        this.isPaused = true;
        this.emit('pause', {});
    }
    
    resume() {
        this.isPaused = false;
        this.emit('resume', {});
    }
    
    getPlayerState() {
        return { ...this.playerState };
    }
    
    getGameData() {
        return this.gameData;
    }
}

window.GameEngine = GameEngine;
