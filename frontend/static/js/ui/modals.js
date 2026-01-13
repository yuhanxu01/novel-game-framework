const ModalUI = {
    _activeModals: [],
    
    init() {
        document.querySelectorAll('.modal .close-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                if (modal) {
                    this.close(modal.id.replace('-modal', ''));
                }
            });
        });
        
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.close(modal.id.replace('-modal', ''));
                }
            });
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this._activeModals.length > 0) {
                this.close(this._activeModals[this._activeModals.length - 1]);
            }
        });
        
        this._initInventoryTabs();
        this._initSaveTabs();
    },
    
    open(modalName) {
        const modal = document.getElementById(`${modalName}-modal`);
        if (!modal) return;
        
        modal.classList.add('active');
        this._activeModals.push(modalName);
        
        switch (modalName) {
            case 'inventory':
                InventorySystem.render();
                break;
            case 'status':
                StatsUI.renderStatusModal();
                break;
            case 'map':
                ExplorationSystem.render();
                break;
            case 'save':
                this._renderSaveSlots();
                break;
        }
    },
    
    close(modalName) {
        const modal = document.getElementById(`${modalName}-modal`);
        if (!modal) return;
        
        modal.classList.remove('active');
        this._activeModals = this._activeModals.filter(m => m !== modalName);
    },
    
    closeAll() {
        this._activeModals.forEach(modalName => {
            const modal = document.getElementById(`${modalName}-modal`);
            if (modal) {
                modal.classList.remove('active');
            }
        });
        this._activeModals = [];
    },
    
    isOpen(modalName) {
        return this._activeModals.includes(modalName);
    },
    
    _initInventoryTabs() {
        const tabs = document.querySelectorAll('#inventory-modal .tab-btn');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const filter = tab.dataset.tab;
                InventorySystem.setFilter(filter);
            });
        });
    },
    
    _initSaveTabs() {
        const tabs = document.querySelectorAll('#save-modal .tab-btn');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                this._currentSaveAction = tab.dataset.action;
                this._renderSaveSlots();
            });
        });
        
        this._currentSaveAction = 'save';
    },
    
    async _renderSaveSlots() {
        const container = document.getElementById('save-slots');
        if (!container) return;
        
        container.innerHTML = '<p>加载中...</p>';
        
        try {
            const response = await Utils.get(APIEndpoints.listSaves());
            const saves = response.data || [];
            
            container.innerHTML = '';
            
            for (let i = 1; i <= GameConfig.SAVE_SLOTS; i++) {
                const save = saves.find(s => s.slot === i);
                const slot = this._createSaveSlot(i, save);
                container.appendChild(slot);
            }
        } catch (error) {
            container.innerHTML = '';
            
            for (let i = 1; i <= GameConfig.SAVE_SLOTS; i++) {
                const localSave = Utils.loadFromLocalStorage(`save_slot_${i}`);
                const slot = this._createSaveSlot(i, localSave);
                container.appendChild(slot);
            }
        }
    },
    
    _createSaveSlot(slotNum, saveData) {
        const slot = document.createElement('div');
        slot.className = 'save-slot';
        
        if (saveData) {
            slot.innerHTML = `
                <div class="slot-info">
                    <h4>存档 ${slotNum}</h4>
                    <p>游戏时间: ${Utils.formatTime(saveData.play_time || 0)}</p>
                    <p>保存时间: ${Utils.formatDate(saveData.saved_at || saveData.timestamp)}</p>
                </div>
                <div class="slot-actions">
                    ${this._currentSaveAction === 'save' ? 
                        `<button onclick="ModalUI._saveToSlot(${slotNum})">覆盖</button>` :
                        `<button onclick="ModalUI._loadFromSlot(${slotNum})">读取</button>`
                    }
                    <button class="btn-delete" onclick="ModalUI._deleteSlot(${slotNum})">删除</button>
                </div>
            `;
        } else {
            slot.classList.add('empty');
            
            if (this._currentSaveAction === 'save') {
                slot.innerHTML = `<span>空存档位 ${slotNum}</span>`;
                slot.addEventListener('click', () => this._saveToSlot(slotNum));
            } else {
                slot.innerHTML = `<span>空存档位 ${slotNum}</span>`;
            }
        }
        
        return slot;
    },
    
    async _saveToSlot(slotNum) {
        const saveData = GameState.getSaveData();
        
        try {
            await Utils.post(APIEndpoints.saveGame(), {
                slot: slotNum,
                save_data: saveData
            });
        } catch (error) {
            Utils.saveToLocalStorage(`save_slot_${slotNum}`, {
                ...saveData,
                timestamp: new Date().toISOString()
            });
        }
        
        await NarrativeUI.showSystemMessage(`已保存到存档 ${slotNum}`);
        this._renderSaveSlots();
    },
    
    async _loadFromSlot(slotNum) {
        try {
            const response = await Utils.get(APIEndpoints.loadGame(slotNum));
            
            if (response.success) {
                GameState.loadSaveData(response.data);
                this.close('save');
                
                await StoryEngine.loadChapter(response.data.current_chapter);
                if (response.data.current_scene) {
                    await StoryEngine.loadScene(response.data.current_scene);
                }
                
                StatsUI.updateStats();
            }
        } catch (error) {
            const localSave = Utils.loadFromLocalStorage(`save_slot_${slotNum}`);
            
            if (localSave) {
                GameState.loadSaveData(localSave);
                this.close('save');
                StatsUI.updateStats();
            }
        }
    },
    
    async _deleteSlot(slotNum) {
        if (!confirm(`确定要删除存档 ${slotNum} 吗？`)) return;
        
        try {
            await Utils.delete(APIEndpoints.deleteSave(slotNum));
        } catch (error) {
            localStorage.removeItem(`save_slot_${slotNum}`);
        }
        
        this._renderSaveSlots();
    }
};
