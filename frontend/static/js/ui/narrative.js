const NarrativeUI = {
    _container: null,
    _isTyping: false,
    _skipRequested: false,
    
    init() {
        this._container = document.getElementById('narrative-content');
        
        if (this._container) {
            this._container.addEventListener('click', () => {
                if (this._isTyping) {
                    this._skipRequested = true;
                }
            });
        }
    },
    
    clear() {
        if (this._container) {
            this._container.innerHTML = '';
        }
    },
    
    async showDialogue(speaker, content) {
        const dialogueEl = document.createElement('div');
        dialogueEl.className = 'dialogue';
        
        if (speaker) {
            const speakerEl = document.createElement('div');
            speakerEl.className = 'speaker';
            speakerEl.textContent = this._getSpeakerName(speaker);
            dialogueEl.appendChild(speakerEl);
        }
        
        const textEl = document.createElement('div');
        textEl.className = 'text';
        dialogueEl.appendChild(textEl);
        
        this._container.appendChild(dialogueEl);
        this._scrollToBottom();
        
        await this._typeText(textEl, content);
    },
    
    async showNarration(content) {
        const narrationEl = document.createElement('div');
        narrationEl.className = 'narration';
        
        this._container.appendChild(narrationEl);
        this._scrollToBottom();
        
        await this._typeText(narrationEl, content);
    },
    
    async showAction(content) {
        const actionEl = document.createElement('div');
        actionEl.className = 'action';
        actionEl.textContent = `— ${content} —`;
        
        this._container.appendChild(actionEl);
        this._scrollToBottom();
        
        await new Promise(resolve => setTimeout(resolve, 500));
    },
    
    async showSystemMessage(content) {
        const msgEl = document.createElement('div');
        msgEl.className = 'system-message';
        msgEl.textContent = content;
        
        this._container.appendChild(msgEl);
        this._scrollToBottom();
        
        await new Promise(resolve => setTimeout(resolve, 1000));
    },
    
    appendText(content) {
        const textNode = document.createTextNode(content);
        this._container.appendChild(textNode);
        this._scrollToBottom();
    },
    
    _getSpeakerName(speakerId) {
        if (!speakerId.startsWith('char_')) {
            return speakerId;
        }
        
        const gameData = GameState.get('gameData');
        const character = gameData?.characters?.[speakerId];
        
        return character?.name || character?.姓名 || speakerId;
    },
    
    async _typeText(element, text) {
        this._isTyping = true;
        this._skipRequested = false;
        
        const speed = GameState.get('settings')?.textSpeed || 5;
        const delay = Math.max(10, 60 - speed * 5);
        
        for (let i = 0; i < text.length; i++) {
            if (this._skipRequested) {
                element.textContent = text;
                break;
            }
            
            element.textContent += text[i];
            this._scrollToBottom();
            
            await new Promise(resolve => setTimeout(resolve, delay));
        }
        
        this._isTyping = false;
        this._skipRequested = false;
    },
    
    _scrollToBottom() {
        if (this._container) {
            this._container.scrollTop = this._container.scrollHeight;
        }
    },
    
    isTyping() {
        return this._isTyping;
    },
    
    skipTyping() {
        this._skipRequested = true;
    }
};
