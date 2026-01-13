// Quest System Engine
const QuestSystem = {
    quests: [],
    activeQuests: [],
    completedQuests: [],
    questData: null,

    async init() {
        console.log('Initializing Quest System...');
        try {
            const response = await fetch('/data/side_quests.json');
            this.questData = await response.json();
            console.log('Quest system loaded:', this.questData);
        } catch (error) {
            console.error('Failed to load quest system:', error);
        }
    },

    checkQuestUnlock(questId) {
        const quest = this.questData.side_quests.find(q => q.quest_id === questId);
        if (!quest) return false;

        const condition = quest.unlock_condition;
        const state = GameState.get();

        // Check chapter
        if (condition.chapter) {
            const currentChapter = state.currentChapter;
            if (currentChapter !== condition.chapter) return false;
        }

        // Check attributes
        if (condition.cultivation) {
            if ((state.protagonist.attributes.cultivation || 0) < condition.cultivation) return false;
        }

        if (condition.relationship_yaolao) {
            if ((state.relationships.char_yaolao || 0) < condition.relationship_yaolao) return false;
        }

        // Check completed quest
        if (condition.quest_completed) {
            if (!this.completedQuests.includes(condition.quest_completed)) return false;
        }

        // Check item
        if (condition.item) {
            if (!InventorySystem.hasItem(condition.item)) return false;
        }

        return true;
    },

    unlockQuest(questId) {
        if (this.activeQuests.some(q => q.quest_id === questId)) return false;
        if (this.completedQuests.includes(questId)) return false;

        const quest = this.questData.side_quests.find(q => q.quest_id === questId);
        if (!quest) return false;

        if (!this.checkQuestUnlock(questId)) return false;

        this.activeQuests.push({
            ...quest,
            status: 'active',
            progress: {}
        });

        this.showQuestNotification('new', quest);
        return true;
    },

    updateQuestObjective(questId, objectiveId, value) {
        const quest = this.activeQuests.find(q => q.quest_id === questId);
        if (!quest) return;

        const objective = quest.objectives.find(o => o.id === objectiveId);
        if (!objective) return;

        if (objective.type === 'collect') {
            objective.current = value;
            if (objective.current >= objective.required) {
                objective.completed = true;
            }
        } else {
            objective.completed = value;
        }

        // Check if all objectives completed
        const allCompleted = quest.objectives.every(o => o.completed);
        if (allCompleted) {
            this.completeQuest(questId);
        }

        this.updateQuestUI();
    },

    completeQuest(questId) {
        const questIndex = this.activeQuests.findIndex(q => q.quest_id === questId);
        if (questIndex === -1) return;

        const quest = this.activeQuests[questIndex];

        // Grant rewards
        if (quest.rewards) {
            this.grantQuestRewards(quest.rewards);
        }

        // Move to completed
        this.activeQuests.splice(questIndex, 1);
        this.completedQuests.push(questId);

        this.showQuestNotification('completed', quest);

        // Check quest chain
        if (quest.quest_chain) {
            this.unlockQuest(quest.quest_chain);
        }

        // Unlock route
        if (quest.rewards.unlock_route) {
            RouteSystem.unlockRoute(quest.rewards.unlock_route);
        }
    },

    grantQuestRewards(rewards) {
        const protagonist = GameState.get('protagonist');

        if (rewards.experience) {
            GameState.update('protagonist', p => ({
                ...p,
                experience: (p.experience || 0) + rewards.experience
            }));
        }

        if (rewards.gold) {
            GameState.update('protagonist', p => ({
                ...p,
                attributes: {
                    ...p.attributes,
                    wealth: (p.attributes.wealth || 0) + rewards.gold
                }
            }));
        }

        if (rewards.items) {
            rewards.items.forEach(itemId => {
                InventorySystem.addItem(itemId);
            });
        }

        if (rewards.skill) {
            GameState.update('protagonist', p => ({
                ...p,
                skills: [...(p.skills || []), rewards.skill]
            }));
        }

        // Update attributes
        Object.keys(rewards).forEach(key => {
            if (key.startsWith('relationship_')) {
                const charId = key;
                GameState.update('relationships', r => ({
                    ...r,
                    [charId]: (r[charId] || 0) + rewards[key]
                }));
            }
        });
    },

    showQuestNotification(type, quest) {
        const notification = document.createElement('div');
        notification.className = 'quest-notification';

        if (type === 'new') {
            notification.innerHTML = `
                <div class="quest-notif-header">新任务</div>
                <div class="quest-notif-title">${quest.name}</div>
                <div class="quest-notif-desc">${quest.description}</div>
            `;
        } else if (type === 'completed') {
            notification.innerHTML = `
                <div class="quest-notif-header">任务完成</div>
                <div class="quest-notif-title">${quest.name}</div>
            `;
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    updateQuestUI() {
        // Update quest tracker in UI
        const questTracker = document.getElementById('quest-tracker');
        if (!questTracker) return;

        questTracker.innerHTML = this.activeQuests.map(quest => `
            <div class="quest-item">
                <div class="quest-name">${quest.name}</div>
                <div class="quest-objectives">
                    ${quest.objectives.map(obj => `
                        <div class="quest-objective ${obj.completed ? 'completed' : ''}">
                            ${obj.description}
                            ${obj.type === 'collect' ? `(${obj.current}/${obj.required})` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
    },

    checkAllQuestUnlocks() {
        this.questData.side_quests.forEach(quest => {
            if (this.checkQuestUnlock(quest.quest_id)) {
                this.unlockQuest(quest.quest_id);
            }
        });
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => QuestSystem.init());
} else {
    QuestSystem.init();
}
