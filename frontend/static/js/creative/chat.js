const CreativeChat = {
    _sessionId: null,
    _isConnected: false,
    _isProcessing: false,
    _messagesContainer: null,
    
    init() {
        this._messagesContainer = document.getElementById('creative-messages');
        
        document.getElementById('btn-connect-api')?.addEventListener('click', 
            () => this.connect()
        );
        
        document.getElementById('btn-send-creative')?.addEventListener('click', 
            () => this.sendMessage()
        );
        
        document.getElementById('creative-input')?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    },
    
    async connect() {
        const apiKey = document.getElementById('api-key-input')?.value;
        const apiProvider = document.getElementById('api-provider')?.value || 'deepseek';
        
        if (!apiKey) {
            alert('请输入API Key');
            return;
        }
        
        const btn = document.getElementById('btn-connect-api');
        btn.textContent = '连接中...';
        btn.disabled = true;
        
        try {
            const response = await Utils.post(
                APIEndpoints.startCreativeSession(),
                { api_key: apiKey, api_provider: apiProvider }
            );
            
            if (response.success) {
                this._sessionId = response.session_id;
                this._isConnected = true;
                
                btn.textContent = '已连接';
                btn.classList.add('connected');
                
                this._enableTools();
                this._addSystemMessage('已连接到AI助手，你可以开始创作了！');
            }
        } catch (error) {
            btn.textContent = '连接';
            btn.disabled = false;
            alert('连接失败: ' + error.message);
        }
    },
    
    _enableTools() {
        document.querySelectorAll('.tool-btn').forEach(btn => {
            btn.disabled = false;
        });
        
        document.getElementById('btn-send-creative').disabled = false;
    },
    
    async sendMessage() {
        if (!this._isConnected || this._isProcessing) return;
        
        const input = document.getElementById('creative-input');
        const message = input?.value.trim();
        
        if (!message) return;
        
        input.value = '';
        this._isProcessing = true;
        
        this._addUserMessage(message);
        this._showTypingIndicator();
        
        try {
            const response = await Utils.post(
                APIEndpoints.creativeChat(this._sessionId),
                { message: message }
            );
            
            this._hideTypingIndicator();
            
            if (response.success) {
                this._addAssistantMessage(response.response);
                
                this._parseAndShowPreview(response.response);
            }
        } catch (error) {
            this._hideTypingIndicator();
            this._addSystemMessage('发送失败: ' + error.message);
        }
        
        this._isProcessing = false;
    },
    
    _addUserMessage(content) {
        const msg = document.createElement('div');
        msg.className = 'chat-message user';
        msg.innerHTML = `
            <div class="message-content">${this._escapeHtml(content)}</div>
            <div class="message-time">${this._getTimeString()}</div>
        `;
        this._messagesContainer.appendChild(msg);
        this._scrollToBottom();
    },
    
    _addAssistantMessage(content) {
        const msg = document.createElement('div');
        msg.className = 'chat-message assistant';
        msg.innerHTML = `
            <div class="message-content">${this._formatMessage(content)}</div>
            <div class="message-time">${this._getTimeString()}</div>
        `;
        this._messagesContainer.appendChild(msg);
        this._scrollToBottom();
    },
    
    _addSystemMessage(content) {
        const msg = document.createElement('div');
        msg.className = 'chat-message system';
        msg.innerHTML = `
            <div class="message-content" style="text-align:center;color:var(--text-secondary);">
                ${content}
            </div>
        `;
        this._messagesContainer.appendChild(msg);
        this._scrollToBottom();
    },
    
    _showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'chat-message assistant';
        indicator.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        this._messagesContainer.appendChild(indicator);
        this._scrollToBottom();
    },
    
    _hideTypingIndicator() {
        document.getElementById('typing-indicator')?.remove();
    },
    
    _formatMessage(content) {
        let formatted = this._escapeHtml(content);
        
        formatted = formatted.replace(/```(\w+)?\n([\s\S]*?)```/g, 
            '<pre><code>$2</code></pre>'
        );
        
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    },
    
    _escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    _getTimeString() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    },
    
    _scrollToBottom() {
        if (this._messagesContainer) {
            this._messagesContainer.scrollTop = this._messagesContainer.scrollHeight;
        }
    },
    
    _parseAndShowPreview(response) {
        const jsonMatch = response.match(/```json\n([\s\S]*?)```/);
        
        if (jsonMatch) {
            try {
                const data = JSON.parse(jsonMatch[1]);
                CreativeEditor.showPreview(data);
            } catch (e) {
                Utils.warn('Failed to parse JSON preview:', e);
            }
        }
    },
    
    getSessionId() {
        return this._sessionId;
    },
    
    isConnected() {
        return this._isConnected;
    }
};
