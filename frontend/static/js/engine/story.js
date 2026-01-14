const StoryEngine = {
    _currentChapterData: null,
    _currentSceneData: null,
    _nodeHistory: [],

    async loadChapter(chapterId) {
        try {
            const response = await Utils.get(APIEndpoints.getChapter(chapterId));

            if (response.success) {
                this._currentChapterData = response.data;
                GameState.set('currentChapter', chapterId);
                Utils.log('Chapter loaded:', chapterId);
                return response.data;
            }
        } catch (error) {
            // Convert to warning if local data exists, otherwise error
            const localData = this._getLocalChapter(chapterId);
            if (localData) {
                Utils.log('Using local chapter data:', chapterId);
                this._currentChapterData = localData; // Essential to set this for local mode
                return localData;
            }

            Utils.error('Failed to load chapter:', error);
            return null;
        }
    },

    async loadScene(sceneId) {
        try {
            const response = await Utils.get(APIEndpoints.getScene(sceneId));

            if (response.success) {
                this._currentSceneData = response.data;
                GameState.set('currentScene', sceneId);
                Utils.log('Scene loaded:', sceneId);
                return response.data;
            }
        } catch (error) {
            const localData = this._getLocalScene(sceneId);
            if (localData) {
                Utils.log('Using local scene data:', sceneId);
                this._currentSceneData = localData; // Essential to set this for local mode
                return localData;
            }

            Utils.error('Failed to load scene:', error);
            return null;
        }
    },

    _getLocalChapter(chapterId) {
        const gameData = GameState.get('gameData');
        if (!gameData?.story_tree?.chapters) return null;

        return gameData.story_tree.chapters.find(c => c.chapter_id === chapterId);
    },

    _getLocalScene(sceneId) {
        if (!this._currentChapterData?.scenes) return null;

        return this._currentChapterData.scenes.find(s => s.scene_id === sceneId);
    },

    async startChapter(chapterId) {
        const chapter = await this.loadChapter(chapterId);

        if (chapter && chapter.scenes && chapter.scenes.length > 0) {
            const firstScene = chapter.scenes[0];
            await this.startScene(firstScene.scene_id);
        }
    },

    async startScene(sceneId) {
        const scene = await this.loadScene(sceneId);

        if (scene && scene.content) {
            const nodes = scene.content.nodes || scene.content.场景流程 || [];

            if (nodes.length > 0) {
                this._nodeHistory = [];
                await this.processNode(nodes[0]);
            }
        }
    },

    async processNode(node) {
        if (!node) {
            Utils.warn('No node to process');
            return;
        }

        GameState.set('currentNode', node.节点ID || node.node_id);
        this._nodeHistory.push(node);

        const nodeType = node.节点类型 || node.node_type;

        switch (nodeType) {
            case '对话':
            case 'dialogue':
                await this._handleDialogue(node);
                break;

            case '旁白':
            case 'narration':
                await this._handleNarration(node);
                break;

            case '选择':
            case 'choice':
                await this._handleChoice(node);
                break;

            case '检定':
            case 'check':
                await this._handleCheck(node);
                break;

            case '获取物品':
            case 'get_item':
                await this._handleGetItem(node);
                break;

            case '触发事件':
            case 'event':
                await this._handleEvent(node);
                break;

            default:
                await this._handleDefault(node);
        }
    },

    async _handleDialogue(node) {
        const speaker = node.角色 || node.speaker;
        const content = node.内容 || node.content;

        await NarrativeUI.showDialogue(speaker, content);

        await this._autoAdvance(node);
    },

    async _handleNarration(node) {
        const content = node.内容 || node.content;

        await NarrativeUI.showNarration(content);

        await this._autoAdvance(node);
    },

    async _handleChoice(node) {
        const description = node.选择描述 || node.description;
        const options = node.选项 || node.options || [];

        if (description) {
            await NarrativeUI.showNarration(description);
        }

        const validOptions = await this._filterOptions(options);

        ChoicesUI.showChoices(validOptions, async (selectedOption) => {
            await this._applyChoiceEffects(selectedOption);

            const nextNodeId = selectedOption.导向 || selectedOption.next;
            if (nextNodeId) {
                const nextNode = this._findNode(nextNodeId);
                if (nextNode) {
                    await this.processNode(nextNode);
                }
            }
        });
    },

    async _filterOptions(options) {
        const playerState = GameState.getPlayerState();
        const validOptions = [];

        for (const option of options) {
            const condition = option.条件 || option.condition;
            const checkResult = await ConditionChecker.check(condition, playerState);

            validOptions.push({
                ...option,
                enabled: checkResult.passed,
                requirementText: checkResult.requirementText
            });
        }

        return validOptions;
    },

    async _applyChoiceEffects(option) {
        const effects = option.效果 || option.effects || {};

        if (effects.属性变化 || effects.attribute_change) {
            const changes = effects.属性变化 || effects.attribute_change;
            for (const [attr, value] of Object.entries(changes)) {
                GameState.modifyAttribute(attr, value);
            }
        }

        if (effects.好感变化 || effects.relationship_change) {
            const changes = effects.好感变化 || effects.relationship_change;
            for (const [char, value] of Object.entries(changes)) {
                GameState.modifyRelationship(char, value);
            }
        }

        if (effects.获得物品 || effects.get_items) {
            const items = effects.获得物品 || effects.get_items;
            for (const itemId of items) {
                const item = this._getItemData(itemId);
                if (item) {
                    GameState.addItem(item);
                    await NarrativeUI.showSystemMessage(`获得物品：${item.name}`);
                }
            }
        }

        if (effects.设置标记 || effects.set_flags) {
            const flags = effects.设置标记 || effects.set_flags;
            for (const flag of flags) {
                GameState.addFlag(flag);
            }
        }

        if (effects.移除标记 || effects.remove_flags) {
            const flags = effects.移除标记 || effects.remove_flags;
            for (const flag of flags) {
                GameState.removeFlag(flag);
            }
        }

        StatsUI.updateStats();
    },

    async _handleCheck(node) {
        const attribute = node.检定属性 || node.attribute;
        const difficulty = node.难度 || node.difficulty || 50;

        const playerState = GameState.getPlayerState();
        const attrValue = playerState.attributes[attribute]?.value || 0;

        const baseChance = Math.min(100, Math.max(0, 50 + (attrValue - difficulty)));
        const roll = Utils.randomInt(1, 100);
        const success = roll <= baseChance;

        await NarrativeUI.showSystemMessage(
            `${success ? '✓ 检定成功' : '✗ 检定失败'} (${roll}/${baseChance}%)`
        );

        const nextNodeId = success
            ? (node.成功导向 || node.success_next)
            : (node.失败导向 || node.fail_next);

        if (nextNodeId) {
            const nextNode = this._findNode(nextNodeId);
            if (nextNode) {
                await this.processNode(nextNode);
            }
        }
    },

    async _handleGetItem(node) {
        const itemId = node.物品ID || node.item_id;
        const item = this._getItemData(itemId);

        if (item) {
            GameState.addItem(item);
            await NarrativeUI.showSystemMessage(`获得物品：${item.name}`);
        }

        await this._autoAdvance(node);
    },

    async _handleEvent(node) {
        const eventType = node.事件类型 || node.event_type;

        Utils.log('Event triggered:', eventType);

        await this._autoAdvance(node);
    },

    async _handleDefault(node) {
        const content = node.内容 || node.content;

        if (content) {
            await NarrativeUI.showNarration(content);
        }

        await this._autoAdvance(node);
    },

    async _autoAdvance(node) {
        const nextNodeId = node.下一节点 || node.next;

        if (nextNodeId) {
            await new Promise(resolve => setTimeout(resolve, 500));

            const nextNode = this._findNode(nextNodeId);
            if (nextNode) {
                await this.processNode(nextNode);
            }
        } else {
            await this._checkSceneEnd();
        }
    },

    _findNode(nodeId) {
        if (!this._currentSceneData?.content) return null;

        const nodes = this._currentSceneData.content.nodes ||
            this._currentSceneData.content.场景流程 || [];

        return nodes.find(n => (n.节点ID || n.node_id) === nodeId);
    },

    _getItemData(itemId) {
        const gameData = GameState.get('gameData');
        if (!gameData?.items) return null;

        const items = gameData.items.items || gameData.items.物品列表 || [];
        return items.find(i => (i.物品ID || i.item_id) === itemId);
    },

    async _checkSceneEnd() {
        Utils.log('Scene ended');

        const chapter = this._currentChapterData;
        if (!chapter?.scenes) return;

        const currentIndex = chapter.scenes.findIndex(
            s => s.scene_id === GameState.get('currentScene')
        );

        if (currentIndex >= 0 && currentIndex < chapter.scenes.length - 1) {
            const nextScene = chapter.scenes[currentIndex + 1];

            ChoicesUI.showChoices([{
                选项文本: '继续',
                选项ID: 'continue'
            }], async () => {
                await this.startScene(nextScene.scene_id);
            });
        } else {
            await this._checkChapterEnd();
        }
    },

    async _checkChapterEnd() {
        Utils.log('Chapter ended');

        const gameData = GameState.get('gameData');
        if (!gameData?.story_tree?.chapters) return;

        const chapters = gameData.story_tree.chapters;
        const currentIndex = chapters.findIndex(
            c => c.chapter_id === GameState.get('currentChapter')
        );

        if (currentIndex >= 0 && currentIndex < chapters.length - 1) {
            const nextChapter = chapters[currentIndex + 1];

            // Removed explicit chapter header as per user request for seamless narrative
            // await NarrativeUI.showNarration(`\n\n— 第${currentIndex + 2}章 —\n\n`);

            ChoicesUI.showChoices([{
                选项文本: '继续',
                选项ID: 'continue'
            }], async () => {
                await this.startChapter(nextChapter.chapter_id);
            });
        } else {
            await NarrativeUI.showNarration('\n\n— 游戏结束 —\n\n感谢您的游玩！');
        }
    }
};
