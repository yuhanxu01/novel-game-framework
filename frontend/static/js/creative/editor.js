const CreativeEditor = {
    _currentPreview: null,
    _modificationHistory: [],
    
    init() {
        document.querySelectorAll('.tool-btn').forEach(btn => {
            btn.addEventListener('click', () => this._handleToolClick(btn.dataset.tool));
        });
        
        document.getElementById('btn-apply-changes')?.addEventListener('click', 
            () => this.applyChanges()
        );
        
        document.getElementById('btn-discard-changes')?.addEventListener('click', 
            () => this.discardChanges()
        );
    },
    
    _handleToolClick(toolType) {
        if (!CreativeChat.isConnected()) {
            alert('请先连接API');
            return;
        }
        
        const prompts = {
            'character': '我想添加一个新角色。请告诉我角色的基本信息（姓名、身份、性格等）：',
            'scene': '我想创建一个新场景。请描述场景的内容：',
            'item': '我想添加一个新物品。请告诉我物品的信息：',
            'branch': '我想在某个地方添加剧情分支。请告诉我分支的位置和选项：',
            'quest': '我想添加一个新任务/支线。请描述任务内容：'
        };
        
        const prompt = prompts[toolType];
        if (prompt) {
            const input = document.getElementById('creative-input');
            if (input) {
                input.value = prompt;
                input.focus();
            }
        }
    },
    
    showPreview(data) {
        this._currentPreview = data;
        
        const container = document.getElementById('creative-preview-content');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (data.type === 'character' || data.角色) {
            this._renderCharacterPreview(container, data);
        } else if (data.type === 'scene' || data.场景) {
            this._renderScenePreview(container, data);
        } else if (data.type === 'item' || data.物品) {
            this._renderItemPreview(container, data);
        } else if (data.type === 'branch' || data.分支) {
            this._renderBranchPreview(container, data);
        } else {
            this._renderGenericPreview(container, data);
        }
    },
    
    _renderCharacterPreview(container, data) {
        const char = data.character || data.角色 || data;
        
        const preview = document.createElement('div');
        preview.className = 'preview-item';
        preview.innerHTML = `
            <h4>👤 新角色</h4>
            <p><strong>姓名:</strong> ${char.name || char.姓名 || '未命名'}</p>
            <p><strong>身份:</strong> ${char.role || char.身份 || '未知'}</p>
            <p><strong>性格:</strong> ${char.personality || char.性格 || '未设定'}</p>
            ${char.description || char.描述 ? 
                `<p><strong>描述:</strong> ${char.description || char.描述}</p>` : ''
            }
        `;
        container.appendChild(preview);
    },
    
    _renderScenePreview(container, data) {
        const scene = data.scene || data.场景 || data;
        
        const preview = document.createElement('div');
        preview.className = 'preview-item';
        preview.innerHTML = `
            <h4>🎬 新场景</h4>
            <p><strong>场景名:</strong> ${scene.name || scene.场景名 || '未命名'}</p>
            <p><strong>位置:</strong> ${scene.location || scene.位置 || '未知'}</p>
            ${scene.description || scene.描述 ? 
                `<p><strong>描述:</strong> ${scene.description || scene.描述}</p>` : ''
            }
        `;
        container.appendChild(preview);
        
        if (scene.dialogues || scene.对话) {
            const dialogues = scene.dialogues || scene.对话;
            dialogues.slice(0, 3).forEach(d => {
                const dialogueEl = document.createElement('div');
                dialogueEl.className = 'preview-item';
                dialogueEl.style.borderLeftColor = 'var(--success-color)';
                dialogueEl.innerHTML = `
                    <p><strong>${d.speaker || d.角色}:</strong></p>
                    <p>${d.content || d.内容}</p>
                `;
                container.appendChild(dialogueEl);
            });
        }
    },
    
    _renderItemPreview(container, data) {
        const item = data.item || data.物品 || data;
        
        const preview = document.createElement('div');
        preview.className = 'preview-item';
        preview.innerHTML = `
            <h4>📦 新物品</h4>
            <p><strong>名称:</strong> ${item.name || item.物品名 || '未命名'}</p>
            <p><strong>类型:</strong> ${item.category || item.分类 || '未分类'}</p>
            <p><strong>稀有度:</strong> ${item.rarity || item.稀有度 || '普通'}</p>
            ${item.description || item.描述 ? 
                `<p><strong>描述:</strong> ${item.description || item.描述}</p>` : ''
            }
            ${item.effect || item.效果 ? 
                `<p><strong>效果:</strong> ${JSON.stringify(item.effect || item.效果)}</p>` : ''
            }
        `;
        container.appendChild(preview);
    },
    
    _renderBranchPreview(container, data) {
        const branch = data.branch || data.分支 || data;
        
        const preview = document.createElement('div');
        preview.className = 'preview-item';
        preview.innerHTML = `
            <h4>🔀 新分支</h4>
            <p><strong>触发位置:</strong> ${branch.location || branch.位置 || '未指定'}</p>
            <p><strong>选项数量:</strong> ${(branch.options || branch.选项 || []).length}</p>
        `;
        container.appendChild(preview);
        
        const options = branch.options || branch.选项 || [];
        options.forEach((opt, i) => {
            const optEl = document.createElement('div');
            optEl.className = 'preview-item';
            optEl.style.borderLeftColor = 'var(--warning-color)';
            optEl.innerHTML = `
                <p><strong>选项 ${i + 1}:</strong> ${opt.text || opt.选项文本}</p>
                ${opt.condition || opt.条件 ? 
                    `<p style="font-size:0.85rem;color:var(--text-secondary)">
                        条件: ${JSON.stringify(opt.condition || opt.条件)}
                    </p>` : ''
                }
            `;
            container.appendChild(optEl);
        });
    },
    
    _renderGenericPreview(container, data) {
        const preview = document.createElement('div');
        preview.className = 'preview-item';
        preview.innerHTML = `
            <h4>📝 预览数据</h4>
            <pre class="json-preview">${Utils.highlightJSON(data)}</pre>
        `;
        container.appendChild(preview);
    },
    
    async applyChanges() {
        if (!this._currentPreview) {
            alert('没有待应用的修改');
            return;
        }
        
        const sessionId = CreativeChat.getSessionId();
        if (!sessionId) {
            alert('请先连接API');
            return;
        }
        
        try {
            const modification = this._buildModification(this._currentPreview);
            
            const response = await Utils.post(
                APIEndpoints.applyModification(sessionId),
                { modification: modification }
            );
            
            if (response.success) {
                this._addToHistory(modification);
                this.discardChanges();
                alert('修改已应用！');
            }
        } catch (error) {
            alert('应用修改失败: ' + error.message);
        }
    },
    
    _buildModification(data) {
        let operationType = 'add';
        let targetPath = '';
        
        if (data.type === 'character' || data.角色) {
            targetPath = 'characters';
        } else if (data.type === 'scene' || data.场景) {
            targetPath = 'story_tree.scenes';
        } else if (data.type === 'item' || data.物品) {
            targetPath = 'items.items';
        } else if (data.type === 'branch' || data.分支) {
            targetPath = 'story_tree.branches';
        }
        
        return {
            operation_type: operationType,
            target_path: targetPath,
            new_value: data,
            description: `添加新${data.type || '内容'}`
        };
    },
    
    discardChanges() {
        this._currentPreview = null;
        
        const container = document.getElementById('creative-preview-content');
        if (container) {
            container.innerHTML = '<p style="color:var(--text-secondary);text-align:center;">无预览内容</p>';
        }
    },
    
    _addToHistory(modification) {
        this._modificationHistory.unshift({
            ...modification,
            timestamp: new Date().toISOString()
        });
        
        this._renderHistory();
    },
    
    _renderHistory() {
        const container = document.getElementById('modification-history');
        if (!container) return;
        
        container.innerHTML = '';
        
        this._modificationHistory.slice(0, 20).forEach(mod => {
            const item = document.createElement('div');
            item.className = 'history-item';
            item.innerHTML = `
                <span class="history-type">${mod.operation_type}</span>
                <span>${mod.description}</span>
                <span class="history-time">${Utils.formatDate(mod.timestamp)}</span>
            `;
            container.appendChild(item);
        });
    },
    
    async loadHistory() {
        try {
            const response = await Utils.get(APIEndpoints.getModificationHistory());
            
            if (response.success && response.data) {
                this._modificationHistory = response.data;
                this._renderHistory();
            }
        } catch (error) {
            Utils.warn('Failed to load modification history:', error);
        }
    }
};
