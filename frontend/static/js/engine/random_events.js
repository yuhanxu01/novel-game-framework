// Random Event System Engine
const RandomEventSystem = {
    eventData: null,
    triggeredEvents: [],
    eventCooldowns: {},

    async init() {
        console.log('Initializing Random Event System...');
        try {
            const response = await fetch('/data/random_events.json');
            this.eventData = await response.json();
            console.log('Random event system loaded:', this.eventData);
        } catch (error) {
            console.error('Failed to load random event system:', error);
        }
    },

    checkEventTrigger(location, action = null) {
        if (!this.eventData) return null;

        const settings = this.eventData.event_system_settings;
        const currentDay = GameState.get('currentDay') || 0;

        // Check max events per day
        const todayEvents = this.triggeredEvents.filter(e => e.day === currentDay);
        if (todayEvents.length >= settings.max_events_per_day) {
            return null;
        }

        // Find eligible events
        const eligibleEvents = this.eventData.random_events.filter(event => {
            // Check cooldown
            if (this.eventCooldowns[event.event_id]) {
                const cooldownEnd = this.eventCooldowns[event.event_id];
                if (currentDay < cooldownEnd) return false;
            }

            // Check location
            if (Array.isArray(event.trigger_location)) {
                if (!event.trigger_location.includes(location)) return false;
            } else if (event.trigger_location !== location && event.trigger_location !== 'location_anywhere') {
                return false;
            }

            // Check trigger conditions
            if (!this.checkTriggerCondition(event.trigger_condition)) {
                return false;
            }

            // Random chance
            if (Math.random() > event.trigger_chance) {
                return false;
            }

            return true;
        });

        if (eligibleEvents.length === 0) return null;

        // Pick random event from eligible ones
        const event = eligibleEvents[Math.floor(Math.random() * eligibleEvents.length)];

        this.triggeredEvents.push({
            event_id: event.event_id,
            day: currentDay
        });

        this.eventCooldowns[event.event_id] = currentDay + this.eventData.event_system_settings.event_cooldown;

        return event;
    },

    checkTriggerCondition(condition) {
        if (!condition) return true;

        const state = GameState.get();

        // Check chapter range
        if (condition.chapter_range) {
            const currentChapter = state.currentChapter;
            const [minChapter, maxChapter] = condition.chapter_range;
            // Simple string comparison - might need more sophisticated logic
            if (currentChapter < minChapter || currentChapter > maxChapter) {
                return false;
            }
        }

        // Check specific chapter
        if (condition.chapter) {
            if (state.currentChapter !== condition.chapter) return false;
        }

        // Check relationship
        if (condition.relationship_xuner) {
            const relationship = state.relationships?.char_xuner || 0;
            if (relationship < condition.relationship_xuner) return false;
        }

        // Check attributes
        if (condition.cultivation_range) {
            const cultivation = state.protagonist?.attributes?.cultivation || 0;
            const [min, max] = condition.cultivation_range;
            if (cultivation < min || cultivation > max) return false;
        }

        // Check flags
        if (condition.flag) {
            if (!state.flags?.[condition.flag]) return false;
        }

        // Check wealth
        if (condition.wealth) {
            const wealth = state.protagonist?.attributes?.wealth || 0;
            if (wealth < condition.wealth) return false;
        }

        return true;
    },

    triggerEvent(event) {
        if (!event) return;

        // Create event UI
        const eventUI = document.createElement('div');
        eventUI.id = 'random-event-modal';
        eventUI.className = 'random-event-modal';

        eventUI.innerHTML = `
            <div class="random-event-content">
                <div class="random-event-header">
                    <h3 class="random-event-title">${event.name}</h3>
                    <span class="random-event-type">[${event.type}]</span>
                </div>
                <div class="random-event-description">${event.description}</div>
                ${event.dialogue ? `
                    <div class="random-event-dialogue">
                        <div class="dialogue-speaker">${this.getSpeakerName(event.dialogue.speaker)}</div>
                        <div class="dialogue-content">"${event.dialogue.content}"</div>
                    </div>
                ` : ''}
                <div class="random-event-choices">
                    ${event.choices.map((choice, index) => `
                        <button class="random-event-choice-btn" data-choice="${index}"
                                ${this.checkChoiceCondition(choice.condition) ? '' : 'disabled'}>
                            ${choice.text}
                            ${choice.condition ? '<span class="choice-requirement">(需求未满足)</span>' : ''}
                            ${choice.time_cost ? `<span class="choice-time">耗时: ${choice.time_cost}小时</span>` : ''}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(eventUI);

        // Bind choice buttons
        eventUI.querySelectorAll('.random-event-choice-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => {
                this.handleEventChoice(event, event.choices[index]);
                eventUI.remove();
            });
        });
    },

    checkChoiceCondition(condition) {
        if (!condition) return true;

        const state = GameState.get();
        const protagonist = state.protagonist;

        if (condition.intelligence) {
            if ((protagonist.attributes.intelligence || 0) < condition.intelligence) return false;
        }

        if (condition.cultivation) {
            if ((protagonist.attributes.cultivation || 0) < condition.cultivation) return false;
        }

        if (condition.strength) {
            if ((protagonist.attributes.strength || 0) < condition.strength) return false;
        }

        if (condition.charisma) {
            if ((protagonist.attributes.charisma || 0) < condition.charisma) return false;
        }

        if (condition.item) {
            if (!InventorySystem.hasItem(condition.item)) return false;
        }

        return true;
    },

    handleEventChoice(event, choice) {
        // Apply effects
        if (choice.effects) {
            this.applyEventEffects(choice.effects);
        }

        // Show outcome
        if (choice.outcome) {
            this.showEventOutcome(choice.outcome);
        }

        // Trigger battle
        if (choice.battle) {
            const battle = BattleSystem.startBattle(choice.battle.enemy);
            if (battle) {
                // Handle win/lose effects after battle
                // This would need integration with battle system callbacks
            }
        }

        // Unlock quest
        if (choice.unlock_quest) {
            QuestSystem.unlockQuest(choice.unlock_quest);
        }

        // Set flag
        if (choice.flag) {
            GameState.update('flags', f => ({
                ...f,
                [choice.flag]: true
            }));
        }

        // Time cost
        if (choice.time_cost) {
            GameState.update('time', t => (t || 0) + choice.time_cost);
        }
    },

    applyEventEffects(effects) {
        const protagonist = GameState.get('protagonist');

        Object.keys(effects).forEach(key => {
            if (key.startsWith('relationship_')) {
                GameState.update('relationships', r => ({
                    ...r,
                    [key]: (r[key] || 0) + effects[key]
                }));
            } else if (['intelligence', 'strength', 'charisma', 'cultivation', 'wealth', 'determination'].includes(key)) {
                GameState.update('protagonist', p => ({
                    ...p,
                    attributes: {
                        ...p.attributes,
                        [key]: (p.attributes[key] || 0) + effects[key]
                    }
                }));
            } else if (key === 'reputation') {
                GameState.update('reputation', r => (r || 0) + effects[key]);
            } else if (key === 'health') {
                GameState.update('protagonist', p => ({
                    ...p,
                    attributes: {
                        ...p.attributes,
                        health: Math.max(0, (p.attributes.health || 100) + effects[key])
                    }
                }));
            }
        });
    },

    showEventOutcome(outcome) {
        const outcomeDiv = document.createElement('div');
        outcomeDiv.className = 'event-outcome-notification';
        outcomeDiv.textContent = outcome;

        document.body.appendChild(outcomeDiv);

        setTimeout(() => {
            outcomeDiv.classList.add('show');
        }, 100);

        setTimeout(() => {
            outcomeDiv.classList.remove('show');
            setTimeout(() => outcomeDiv.remove(), 300);
        }, 3000);
    },

    getSpeakerName(speakerId) {
        const characterData = GameState.get('gameData')?.characters;
        if (characterData && characterData[speakerId]) {
            return characterData[speakerId].name;
        }
        return speakerId;
    },

    // Call this when player moves to a new location
    checkLocationEvents(location) {
        const event = this.checkEventTrigger(location);
        if (event) {
            // Delay to make it feel more natural
            setTimeout(() => {
                this.triggerEvent(event);
            }, 500);
        }
    },

    // Call this when player performs an action
    checkActionEvents(action, location) {
        const event = this.checkEventTrigger(location, action);
        if (event) {
            setTimeout(() => {
                this.triggerEvent(event);
            }, 500);
        }
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => RandomEventSystem.init());
} else {
    RandomEventSystem.init();
}
