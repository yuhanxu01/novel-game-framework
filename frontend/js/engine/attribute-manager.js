class AttributeManager {
    constructor(engine) {
        this.engine = engine;
        this.attributeConfig = null;
        this.container = null;
        
        this._bindEvents();
    }
    
    _bindEvents() {
        this.engine.on('init', (data) => {
            this.attributeConfig = data.gameData.attributes;
            this._initAttributes();
        });
        
        this.engine.on('attributeChange', (data) => {
            this._onAttributeChange(data);
        });
        
        this.engine.on('loaded', () => {
            this._refreshDisplay();
        });
    }
    
    _initAttributes() {
        if (!this.attributeConfig) return;
        
        const playerState = this.engine.playerState;
        
        if (this.attributeConfig.基础属性) {
            for (const attr of this.attributeConfig.基础属性) {
                if (!(attr.属性ID in playerState.attributes)) {
                    playerState.attributes[attr.属性ID] = attr.初始值 || 10;
                }
            }
        }
        
        if (this.attributeConfig.状态属性) {
            for (const attr of this.attributeConfig.状态属性) {
                if (!(attr.属性ID in playerState.attributes)) {
                    const maxVal = this._calculateMax(attr, playerState.attributes);
                    playerState.attributes[attr.属性ID] = maxVal;
                    playerState.attributes[`${attr.属性ID}_max`] = maxVal;
                }
            }
        }
    }
    
    _calculateMax(statusAttr, currentAttrs) {
        return 100;
    }
    
    _onAttributeChange(data) {
        this._refreshDisplay();
        this._showChangeNotification(data);
        this._checkThresholds(data.attribute, data.newValue);
    }
    
    _showChangeNotification(data) {
        const attrName = this._getAttributeName(data.attribute);
        const changeText = data.change > 0 ? `+${data.change}` : `${data.change}`;
        
        this.engine.emit('notification', {
            type: data.change > 0 ? 'positive' : 'negative',
            message: `${attrName} ${changeText}`
        });
    }
    
    _getAttributeName(attrId) {
        if (!this.attributeConfig) return attrId;
        
        const allAttrs = [
            ...(this.attributeConfig.基础属性 || []),
            ...(this.attributeConfig.状态属性 || []),
            ...(this.attributeConfig.特殊属性?.属性列表 || [])
        ];
        
        const attr = allAttrs.find(a => a.属性ID === attrId);
        return attr ? attr.属性名 : attrId;
    }
    
    _checkThresholds(attrId, value) {
        if (!this.attributeConfig || !this.attributeConfig.基础属性) return;
        
        const attr = this.attributeConfig.基础属性.find(a => a.属性ID === attrId);
        if (!attr || !attr.阈值效果) return;
        
        for (const [threshold, effect] of Object.entries(attr.阈值效果)) {
            const match = threshold.match(/(\d+)(以下|以上|-(\d+))?/);
            if (!match) continue;
            
            const val1 = parseInt(match[1]);
            const val2 = match[3] ? parseInt(match[3]) : null;
            
            let triggered = false;
            if (threshold.includes('以下') && value < val1) {
                triggered = true;
            } else if (threshold.includes('以上') && value >= val1) {
                triggered = true;
            } else if (val2 && value >= val1 && value <= val2) {
                triggered = true;
            }
            
            if (triggered) {
                this.engine.emit('thresholdReached', {
                    attribute: attrId,
                    threshold,
                    effect,
                    value
                });
            }
        }
    }
    
    modifyAttribute(attrId, amount) {
        const playerState = this.engine.playerState;
        const oldValue = playerState.attributes[attrId] || 0;
        
        let newValue = oldValue + amount;
        
        const attr = this._getAttributeConfig(attrId);
        if (attr) {
            const min = 0;
            const max = attr.最大值 || playerState.attributes[`${attrId}_max`] || 100;
            newValue = Math.max(min, Math.min(max, newValue));
        }
        
        playerState.attributes[attrId] = newValue;
        
        this.engine.emit('attributeChange', {
            attribute: attrId,
            change: newValue - oldValue,
            newValue
        });
        
        return newValue;
    }
    
    _getAttributeConfig(attrId) {
        if (!this.attributeConfig) return null;
        
        const allAttrs = [
            ...(this.attributeConfig.基础属性 || []),
            ...(this.attributeConfig.状态属性 || []),
            ...(this.attributeConfig.特殊属性?.属性列表 || [])
        ];
        
        return allAttrs.find(a => a.属性ID === attrId);
    }
    
    getAttribute(attrId) {
        return this.engine.playerState.attributes[attrId] || 0;
    }
    
    getAllAttributes() {
        return { ...this.engine.playerState.attributes };
    }
    
    checkRequirement(requirements) {
        if (!requirements) return true;
        
        for (const [attrId, required] of Object.entries(requirements)) {
            if (this.getAttribute(attrId) < required) {
                return false;
            }
        }
        
        return true;
    }
    
    _refreshDisplay() {
        if (!this.container) return;
        this.render(this.container);
    }
    
    render(container) {
        this.container = container;
        
        if (!this.attributeConfig) {
            container.innerHTML = '<div class="no-data">属性系统未配置</div>';
            return;
        }
        
        const playerState = this.engine.playerState;
        
        let html = '<div class="attribute-panel">';
        
        if (this.attributeConfig.状态属性) {
            html += '<div class="status-attributes">';
            for (const attr of this.attributeConfig.状态属性) {
                const current = playerState.attributes[attr.属性ID] || 0;
                const max = playerState.attributes[`${attr.属性ID}_max`] || 100;
                const percent = (current / max * 100).toFixed(0);
                
                html += `
                    <div class="status-bar" data-attr="${attr.属性ID}">
                        <div class="status-label">
                            <span class="status-icon">${attr.图标 || ''}</span>
                            <span class="status-name">${attr.属性名}</span>
                            <span class="status-value">${current}/${max}</span>
                        </div>
                        <div class="status-bar-bg">
                            <div class="status-bar-fill" style="width: ${percent}%"></div>
                        </div>
                    </div>
                `;
            }
            html += '</div>';
        }
        
        if (this.attributeConfig.基础属性) {
            html += '<div class="base-attributes">';
            html += '<h3>属性</h3>';
            html += '<div class="attribute-grid">';
            
            for (const attr of this.attributeConfig.基础属性) {
                const value = playerState.attributes[attr.属性ID] || 0;
                
                html += `
                    <div class="attribute-item" data-attr="${attr.属性ID}" title="${attr.属性描述 || ''}">
                        <span class="attr-icon">${attr.图标建议 || '📊'}</span>
                        <span class="attr-name">${attr.属性名}</span>
                        <span class="attr-value">${value}</span>
                    </div>
                `;
            }
            
            html += '</div></div>';
        }
        
        if (this.attributeConfig.特殊属性 && this.attributeConfig.特殊属性.属性列表) {
            html += '<div class="special-attributes">';
            html += '<h3>特殊属性</h3>';
            
            for (const attr of this.attributeConfig.特殊属性.属性列表) {
                const value = playerState.attributes[attr.属性ID] || 0;
                
                if (attr.等级列表) {
                    const currentLevel = attr.等级列表.find(l => l.等级 === value) || attr.等级列表[0];
                    html += `
                        <div class="special-attr-item">
                            <span class="attr-name">${attr.属性名}</span>
                            <span class="attr-level">${currentLevel ? currentLevel.名称 : '未知'}</span>
                        </div>
                    `;
                } else {
                    html += `
                        <div class="special-attr-item">
                            <span class="attr-name">${attr.属性名}</span>
                            <span class="attr-value">${value}</span>
                        </div>
                    `;
                }
            }
            
            html += '</div>';
        }
        
        html += '</div>';
        
        container.innerHTML = html;
    }
    
    renderMiniStatus(container) {
        if (!this.attributeConfig || !this.attributeConfig.状态属性) {
            return;
        }
        
        const playerState = this.engine.playerState;
        
        let html = '<div class="mini-status">';
        
        for (const attr of this.attributeConfig.状态属性) {
            const current = playerState.attributes[attr.属性ID] || 0;
            const max = playerState.attributes[`${attr.属性ID}_max`] || 100;
            const percent = (current / max * 100).toFixed(0);
            
            html += `
                <div class="mini-bar" title="${attr.属性名}: ${current}/${max}">
                    <span class="mini-icon">${attr.图标 || ''}</span>
                    <div class="mini-bar-bg">
                        <div class="mini-bar-fill" style="width: ${percent}%"></div>
                    </div>
                </div>
            `;
        }
        
        html += '</div>';
        
        container.innerHTML = html;
    }
}

window.AttributeManager = AttributeManager;
