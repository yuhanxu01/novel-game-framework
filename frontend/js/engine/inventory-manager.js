class InventoryManager {
    constructor(engine) {
        this.engine = engine;
        this.itemConfig = null;
        this.container = null;
        this.maxCapacity = 20;
        
        this.currentFilter = 'all';
        this.currentSort = 'default';
        this.selectedItem = null;
        
        this._bindEvents();
    }
    
    _bindEvents() {
        this.engine.on('init', (data) => {
            this.itemConfig = data.gameData.items;
            if (this.itemConfig && this.itemConfig.物品系统设计) {
                this.maxCapacity = this.itemConfig.物品系统设计.背包容量?.默认容量 || 20;
            }
        });
        
        this.engine.on('inventoryChange', () => {
            this._refreshDisplay();
        });
        
        this.engine.on('loaded', () => {
            this._refreshDisplay();
        });
    }
    
    addItem(itemId, count = 1) {
        const inventory = this.engine.playerState.inventory;
        const itemData = this._getItemData(itemId);
        
        if (!itemData) {
            console.warn(`物品不存在: ${itemId}`);
            return false;
        }
        
        const existing = inventory.find(item => item.id === itemId);
        
        if (existing) {
            const stackable = this._isStackable(itemData);
            if (stackable) {
                const maxStack = itemData.堆叠上限 || 99;
                existing.count = Math.min(existing.count + count, maxStack);
            } else {
                if (this._getUsedSlots() >= this.maxCapacity) {
                    this.engine.emit('inventoryFull', {});
                    return false;
                }
                inventory.push({
                    id: itemId,
                    count: 1,
                    data: itemData,
                    uniqueId: Date.now()
                });
            }
        } else {
            if (this._getUsedSlots() >= this.maxCapacity) {
                this.engine.emit('inventoryFull', {});
                return false;
            }
            inventory.push({
                id: itemId,
                count: count,
                data: itemData,
                uniqueId: Date.now()
            });
        }
        
        this.engine.emit('inventoryChange', { inventory });
        this.engine.emit('itemAdded', { itemId, count, itemData });
        
        return true;
    }
    
    removeItem(itemId, count = 1) {
        const inventory = this.engine.playerState.inventory;
        const index = inventory.findIndex(item => item.id === itemId);
        
        if (index === -1) return false;
        
        const item = inventory[index];
        
        if (item.count > count) {
            item.count -= count;
        } else {
            inventory.splice(index, 1);
        }
        
        this.engine.emit('inventoryChange', { inventory });
        this.engine.emit('itemRemoved', { itemId, count });
        
        return true;
    }
    
    useItem(itemId) {
        const inventory = this.engine.playerState.inventory;
        const item = inventory.find(i => i.id === itemId);
        
        if (!item) return false;
        
        const itemData = item.data || this._getItemData(itemId);
        if (!itemData) return false;
        
        if (itemData.分类 !== 'category_consumable') {
            this.engine.emit('notification', {
                type: 'warning',
                message: '该物品不可使用'
            });
            return false;
        }
        
        if (itemData.使用效果) {
            const effect = itemData.使用效果;
            
            if (effect.恢复生命) {
                this.engine.emit('attributeChange', {
                    attribute: 'status_health',
                    change: effect.恢复生命,
                    newValue: Math.min(
                        (this.engine.playerState.attributes.status_health || 0) + effect.恢复生命,
                        this.engine.playerState.attributes.status_health_max || 100
                    )
                });
                this.engine.playerState.attributes.status_health = Math.min(
                    (this.engine.playerState.attributes.status_health || 0) + effect.恢复生命,
                    this.engine.playerState.attributes.status_health_max || 100
                );
            }
            
            if (effect.恢复体力) {
                this.engine.playerState.attributes.status_stamina = Math.min(
                    (this.engine.playerState.attributes.status_stamina || 0) + effect.恢复体力,
                    this.engine.playerState.attributes.status_stamina_max || 100
                );
            }
            
            if (effect.效果详情) {
                for (const [key, value] of Object.entries(effect.效果详情)) {
                    if (key.startsWith('恢复')) {
                        const attr = key.replace('恢复', 'status_').toLowerCase();
                        this.engine.playerState.attributes[attr] = Math.min(
                            (this.engine.playerState.attributes[attr] || 0) + value,
                            this.engine.playerState.attributes[`${attr}_max`] || 100
                        );
                    }
                }
            }
        }
        
        this.removeItem(itemId, 1);
        
        this.engine.emit('itemUsed', { itemId, itemData });
        this.engine.emit('notification', {
            type: 'positive',
            message: `使用了 ${itemData.物品名}`
        });
        
        return true;
    }
    
    hasItem(itemId, count = 1) {
        const item = this.engine.playerState.inventory.find(i => i.id === itemId);
        return item && item.count >= count;
    }
    
    getItemCount(itemId) {
        const item = this.engine.playerState.inventory.find(i => i.id === itemId);
        return item ? item.count : 0;
    }
    
    getInventory() {
        return [...this.engine.playerState.inventory];
    }
    
    _getItemData(itemId) {
        if (!this.itemConfig || !this.itemConfig.物品列表) return null;
        return this.itemConfig.物品列表.find(item => item.物品ID === itemId);
    }
    
    _isStackable(itemData) {
        if (!itemData) return false;
        const nonStackable = ['category_equipment', 'category_key'];
        return !nonStackable.includes(itemData.分类);
    }
    
    _getUsedSlots() {
        return this.engine.playerState.inventory.length;
    }
    
    _refreshDisplay() {
        if (!this.container) return;
        this.render(this.container);
    }
    
    render(container) {
        this.container = container;
        
        const inventory = this.getInventory();
        
        let html = `
            <div class="inventory-panel">
                <div class="inventory-header">
                    <h3>背包 (${this._getUsedSlots()}/${this.maxCapacity})</h3>
                    <div class="inventory-controls">
                        <select class="filter-select" onchange="inventoryManager.setFilter(this.value)">
                            <option value="all">全部</option>
                            <option value="category_consumable">消耗品</option>
                            <option value="category_equipment">装备</option>
                            <option value="category_material">材料</option>
                            <option value="category_key">关键物品</option>
                            <option value="category_quest">任务物品</option>
                        </select>
                        <select class="sort-select" onchange="inventoryManager.setSort(this.value)">
                            <option value="default">默认排序</option>
                            <option value="name">按名称</option>
                            <option value="rarity">按稀有度</option>
                            <option value="type">按类型</option>
                        </select>
                    </div>
                </div>
                <div class="inventory-grid">
        `;
        
        const filteredItems = this._filterItems(inventory);
        const sortedItems = this._sortItems(filteredItems);
        
        for (const item of sortedItems) {
            const itemData = item.data || this._getItemData(item.id);
            if (!itemData) continue;
            
            const rarityClass = itemData.稀有度 || 'rarity_common';
            const isSelected = this.selectedItem === item.id;
            
            html += `
                <div class="inventory-slot ${isSelected ? 'selected' : ''}" 
                     data-item-id="${item.id}"
                     onclick="inventoryManager.selectItem('${item.id}')"
                     ondblclick="inventoryManager.useItem('${item.id}')">
                    <div class="item-icon ${rarityClass}">
                        ${this._getItemIcon(itemData)}
                    </div>
                    ${item.count > 1 ? `<span class="item-count">${item.count}</span>` : ''}
                    <div class="item-tooltip">
                        <div class="tooltip-name ${rarityClass}">${itemData.物品名}</div>
                        <div class="tooltip-type">${this._getCategoryName(itemData.分类)}</div>
                        <div class="tooltip-desc">${itemData.描述 || ''}</div>
                        ${itemData.价格 ? `<div class="tooltip-price">价值: ${itemData.价格.出售 || 0}</div>` : ''}
                    </div>
                </div>
            `;
        }
        
        const emptySlots = this.maxCapacity - sortedItems.length;
        for (let i = 0; i < emptySlots; i++) {
            html += '<div class="inventory-slot empty"></div>';
        }
        
        html += `
                </div>
                <div class="item-detail-panel" id="itemDetailPanel">
                    ${this.selectedItem ? this._renderItemDetail(this.selectedItem) : '<div class="no-selection">选择一个物品查看详情</div>'}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    _filterItems(items) {
        if (this.currentFilter === 'all') return items;
        return items.filter(item => {
            const itemData = item.data || this._getItemData(item.id);
            return itemData && itemData.分类 === this.currentFilter;
        });
    }
    
    _sortItems(items) {
        const sorted = [...items];
        
        switch (this.currentSort) {
            case 'name':
                sorted.sort((a, b) => {
                    const nameA = (a.data || this._getItemData(a.id))?.物品名 || '';
                    const nameB = (b.data || this._getItemData(b.id))?.物品名 || '';
                    return nameA.localeCompare(nameB);
                });
                break;
            case 'rarity':
                const rarityOrder = ['rarity_legendary', 'rarity_epic', 'rarity_rare', 'rarity_uncommon', 'rarity_common'];
                sorted.sort((a, b) => {
                    const rarityA = (a.data || this._getItemData(a.id))?.稀有度 || 'rarity_common';
                    const rarityB = (b.data || this._getItemData(b.id))?.稀有度 || 'rarity_common';
                    return rarityOrder.indexOf(rarityA) - rarityOrder.indexOf(rarityB);
                });
                break;
            case 'type':
                sorted.sort((a, b) => {
                    const typeA = (a.data || this._getItemData(a.id))?.分类 || '';
                    const typeB = (b.data || this._getItemData(b.id))?.分类 || '';
                    return typeA.localeCompare(typeB);
                });
                break;
        }
        
        return sorted;
    }
    
    _getItemIcon(itemData) {
        if (itemData.图标) return itemData.图标;
        
        const categoryIcons = {
            'category_consumable': '🧪',
            'category_equipment': '⚔️',
            'category_material': '💎',
            'category_key': '🔑',
            'category_quest': '📜',
            'category_collectible': '🏆'
        };
        
        return categoryIcons[itemData.分类] || '📦';
    }
    
    _getCategoryName(category) {
        const names = {
            'category_consumable': '消耗品',
            'category_equipment': '装备',
            'category_material': '材料',
            'category_key': '关键物品',
            'category_quest': '任务物品',
            'category_collectible': '收藏品'
        };
        return names[category] || '其他';
    }
    
    _renderItemDetail(itemId) {
        const item = this.engine.playerState.inventory.find(i => i.id === itemId);
        if (!item) return '<div class="no-selection">物品不存在</div>';
        
        const itemData = item.data || this._getItemData(itemId);
        if (!itemData) return '<div class="no-selection">物品数据不存在</div>';
        
        const rarityClass = itemData.稀有度 || 'rarity_common';
        
        let html = `
            <div class="item-detail">
                <div class="detail-header">
                    <span class="detail-icon ${rarityClass}">${this._getItemIcon(itemData)}</span>
                    <div class="detail-title">
                        <span class="detail-name ${rarityClass}">${itemData.物品名}</span>
                        <span class="detail-type">${this._getCategoryName(itemData.分类)}</span>
                    </div>
                </div>
                <div class="detail-desc">${itemData.描述 || '暂无描述'}</div>
        `;
        
        if (itemData.使用效果) {
            html += '<div class="detail-effects"><strong>使用效果:</strong><ul>';
            const effect = itemData.使用效果;
            if (effect.恢复生命) html += `<li>恢复生命 +${effect.恢复生命}</li>`;
            if (effect.恢复体力) html += `<li>恢复体力 +${effect.恢复体力}</li>`;
            if (effect.效果详情) {
                for (const [key, value] of Object.entries(effect.效果详情)) {
                    html += `<li>${key}: ${value}</li>`;
                }
            }
            html += '</ul></div>';
        }
        
        if (itemData.属性加成) {
            html += '<div class="detail-stats"><strong>属性加成:</strong><ul>';
            for (const [attr, value] of Object.entries(itemData.属性加成)) {
                html += `<li>${attr}: +${value}</li>`;
            }
            html += '</ul></div>';
        }
        
        html += `
            <div class="detail-info">
                <span>数量: ${item.count}</span>
                ${itemData.价格 ? `<span>价值: ${itemData.价格.出售 || 0}</span>` : ''}
            </div>
            <div class="detail-actions">
        `;
        
        if (itemData.分类 === 'category_consumable') {
            html += `<button class="btn-use" onclick="inventoryManager.useItem('${itemId}')">使用</button>`;
        }
        
        if (!['category_key', 'category_quest'].includes(itemData.分类)) {
            html += `<button class="btn-drop" onclick="inventoryManager.dropItem('${itemId}')">丢弃</button>`;
        }
        
        html += '</div></div>';
        
        return html;
    }
    
    selectItem(itemId) {
        this.selectedItem = itemId;
        
        const detailPanel = document.getElementById('itemDetailPanel');
        if (detailPanel) {
            detailPanel.innerHTML = this._renderItemDetail(itemId);
        }
        
        document.querySelectorAll('.inventory-slot').forEach(slot => {
            slot.classList.remove('selected');
            if (slot.dataset.itemId === itemId) {
                slot.classList.add('selected');
            }
        });
    }
    
    setFilter(filter) {
        this.currentFilter = filter;
        this._refreshDisplay();
    }
    
    setSort(sort) {
        this.currentSort = sort;
        this._refreshDisplay();
    }
    
    dropItem(itemId) {
        if (confirm('确定要丢弃这个物品吗？')) {
            this.removeItem(itemId, 1);
            this.selectedItem = null;
            this._refreshDisplay();
        }
    }
    
    renderQuickBar(container, slots = 5) {
        const inventory = this.getInventory();
        const consumables = inventory.filter(item => {
            const data = item.data || this._getItemData(item.id);
            return data && data.分类 === 'category_consumable';
        }).slice(0, slots);
        
        let html = '<div class="quick-bar">';
        
        for (let i = 0; i < slots; i++) {
            const item = consumables[i];
            if (item) {
                const itemData = item.data || this._getItemData(item.id);
                html += `
                    <div class="quick-slot" onclick="inventoryManager.useItem('${item.id}')" title="${itemData.物品名}">
                        <span class="quick-icon">${this._getItemIcon(itemData)}</span>
                        <span class="quick-count">${item.count}</span>
                        <span class="quick-key">${i + 1}</span>
                    </div>
                `;
            } else {
                html += `
                    <div class="quick-slot empty">
                        <span class="quick-key">${i + 1}</span>
                    </div>
                `;
            }
        }
        
        html += '</div>';
        container.innerHTML = html;
    }
}

window.InventoryManager = InventoryManager;
