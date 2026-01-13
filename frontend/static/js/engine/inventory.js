const InventorySystem = {
    _selectedItem: null,
    _currentFilter: 'all',
    
    init() {
        GameState.subscribe('inventory', () => this.render());
    },
    
    render() {
        const inventory = GameState.get('inventory') || [];
        const grid = document.getElementById('inventory-grid');
        
        if (!grid) return;
        
        grid.innerHTML = '';
        
        const filtered = this._filterItems(inventory);
        
        filtered.forEach(item => {
            const slot = this._createItemSlot(item);
            grid.appendChild(slot);
        });
        
        const emptySlots = 24 - filtered.length;
        for (let i = 0; i < emptySlots; i++) {
            const emptySlot = document.createElement('div');
            emptySlot.className = 'inventory-slot empty';
            grid.appendChild(emptySlot);
        }
    },
    
    _filterItems(items) {
        if (this._currentFilter === 'all') {
            return items;
        }
        
        return items.filter(item => {
            const category = item.分类 || item.category || '';
            return category.includes(this._currentFilter);
        });
    },
    
    _createItemSlot(item) {
        const slot = document.createElement('div');
        slot.className = 'inventory-slot';
        
        const rarity = item.稀有度 || item.rarity || 'common';
        slot.classList.add(`rarity-${rarity}`);
        
        if (this._selectedItem === item.item_id) {
            slot.classList.add('selected');
        }
        
        const icon = document.createElement('span');
        icon.className = 'item-icon';
        icon.textContent = this._getItemIcon(item);
        slot.appendChild(icon);
        
        if (item.count > 1) {
            const count = document.createElement('span');
            count.className = 'item-count';
            count.textContent = item.count;
            slot.appendChild(count);
        }
        
        slot.addEventListener('click', () => this._selectItem(item));
        
        return slot;
    },
    
    _getItemIcon(item) {
        const iconMap = {
            'consumable': '🧪',
            'equipment': '⚔️',
            'key': '🔑',
            'material': '💎',
            'quest': '📜'
        };
        
        const category = item.分类 || item.category || 'consumable';
        
        for (const [key, icon] of Object.entries(iconMap)) {
            if (category.includes(key)) {
                return icon;
            }
        }
        
        return '📦';
    },
    
    _selectItem(item) {
        this._selectedItem = item.item_id || item.物品ID;
        this._showItemDetail(item);
        this.render();
    },
    
    _showItemDetail(item) {
        const detail = document.getElementById('item-detail');
        if (!detail) return;
        
        const content = detail.querySelector('.item-detail-content');
        if (!content) return;
        
        const name = item.物品名 || item.name || '未知物品';
        const description = item.描述 || item.description || '没有描述';
        const category = item.分类 || item.category || '未分类';
        const rarity = item.稀有度 || item.rarity || 'common';
        
        const rarityNames = {
            'common': '普通',
            'uncommon': '精良',
            'rare': '稀有',
            'epic': '史诗',
            'legendary': '传说'
        };
        
        content.innerHTML = `
            <h4>${name}</h4>
            <p class="item-rarity rarity-${rarity}">${rarityNames[rarity] || rarity}</p>
            <p class="item-category">${category}</p>
            <p class="item-desc">${description}</p>
            <div class="item-actions">
                ${this._canUseItem(item) ? '<button onclick="InventorySystem.useItem()">使用</button>' : ''}
                ${!this._isKeyItem(item) ? '<button onclick="InventorySystem.dropItem()">丢弃</button>' : ''}
            </div>
        `;
    },
    
    _canUseItem(item) {
        const category = item.分类 || item.category || '';
        return category.includes('consumable');
    },
    
    _isKeyItem(item) {
        const category = item.分类 || item.category || '';
        return category.includes('key');
    },
    
    useItem() {
        if (!this._selectedItem) return;
        
        const inventory = GameState.get('inventory');
        const item = inventory.find(i => (i.item_id || i.物品ID) === this._selectedItem);
        
        if (!item) return;
        
        const effects = item.使用效果 || item.use_effect || {};
        
        if (effects.恢复生命 || effects.heal_health) {
            const amount = effects.恢复生命 || effects.heal_health;
            GameState.modifyStatus('health', amount);
        }
        
        if (effects.恢复体力 || effects.heal_stamina) {
            const amount = effects.恢复体力 || effects.heal_stamina;
            GameState.modifyStatus('stamina', amount);
        }
        
        if (effects.属性增益 || effects.buff) {
            const buff = effects.属性增益 || effects.buff;
            for (const [attr, value] of Object.entries(buff)) {
                GameState.modifyAttribute(attr, value);
            }
        }
        
        GameState.removeItem(this._selectedItem);
        this._selectedItem = null;
        
        StatsUI.updateStats();
        this.render();
    },
    
    dropItem() {
        if (!this._selectedItem) return;
        
        const inventory = GameState.get('inventory');
        const item = inventory.find(i => (i.item_id || i.物品ID) === this._selectedItem);
        
        if (item && !this._isKeyItem(item)) {
            GameState.removeItem(this._selectedItem);
            this._selectedItem = null;
            this.render();
        }
    },
    
    setFilter(filter) {
        this._currentFilter = filter;
        this.render();
    },
    
    getItemById(itemId) {
        const gameData = GameState.get('gameData');
        if (!gameData?.items) return null;
        
        const items = gameData.items.items || gameData.items.物品列表 || [];
        return items.find(i => (i.物品ID || i.item_id) === itemId);
    }
};
