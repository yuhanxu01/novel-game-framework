const ChoicesUI = {
    _container: null,
    _callback: null,
    
    init() {
        this._container = document.getElementById('choices-container');
    },
    
    showChoices(options, callback) {
        if (!this._container) return;
        
        this._callback = callback;
        this._container.innerHTML = '';
        
        options.forEach((option, index) => {
            const btn = this._createChoiceButton(option, index);
            this._container.appendChild(btn);
        });
    },
    
    _createChoiceButton(option, index) {
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        
        const text = option.选项文本 || option.text || option.option_text || `选项 ${index + 1}`;
        btn.textContent = text;
        
        if (option.enabled === false) {
            btn.disabled = true;
            
            if (option.requirementText) {
                const req = document.createElement('span');
                req.className = 'requirement';
                req.textContent = option.requirementText;
                btn.appendChild(req);
            }
        }
        
        btn.addEventListener('click', () => {
            if (!btn.disabled) {
                this._selectChoice(option);
            }
        });
        
        return btn;
    },
    
    _selectChoice(option) {
        this._container.innerHTML = '';
        
        if (this._callback) {
            this._callback(option);
        }
    },
    
    clearChoices() {
        if (this._container) {
            this._container.innerHTML = '';
        }
    },
    
    hasActiveChoices() {
        return this._container && this._container.children.length > 0;
    }
};
