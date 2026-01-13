// Story Route System Engine
const RouteSystem = {
    routeData: null,
    currentRoute: null,
    routeProgress: {},
    availableRoutes: [],

    async init() {
        console.log('Initializing Route System...');
        try {
            const response = await fetch('/data/story_routes.json');
            this.routeData = await response.json();
            console.log('Route system loaded:', this.routeData);
        } catch (error) {
            console.error('Failed to load route system:', error);
        }
    },

    checkRouteUnlock(routeId) {
        const route = this.routeData.story_routes[routeId];
        if (!route) return false;

        const condition = route.unlock_condition;
        const state = GameState.get();
        const protagonist = state.protagonist;

        // Check attributes
        if (condition.cultivation && (protagonist.attributes.cultivation || 0) < condition.cultivation) {
            return false;
        }

        if (condition.strength && (protagonist.attributes.strength || 0) < condition.strength) {
            return false;
        }

        if (condition.intelligence && (protagonist.attributes.intelligence || 0) < condition.intelligence) {
            return false;
        }

        if (condition.charisma && (protagonist.attributes.charisma || 0) < condition.charisma) {
            return false;
        }

        if (condition.determination && (protagonist.attributes.determination || 0) < condition.determination) {
            return false;
        }

        // Check relationships
        if (condition.relationship_xuner) {
            if ((state.relationships?.char_xuner || 0) < condition.relationship_xuner) {
                return false;
            }
        }

        if (condition.relationship_xiaozhan) {
            if ((state.relationships?.char_xiaozhan || 0) < condition.relationship_xiaozhan) {
                return false;
            }
        }

        if (condition.relationship_yaolao) {
            if ((state.relationships?.char_yaolao || 0) < condition.relationship_yaolao) {
                return false;
            }
        }

        // Check flags
        if (condition.hidden_strength_flag && !state.flags?.hidden_strength) {
            return false;
        }

        // Check other conditions
        if (condition.family_contribution && (state.family_contribution || 0) < condition.family_contribution) {
            return false;
        }

        if (condition.alchemy_skill && (state.alchemy_skill || 0) < condition.alchemy_skill) {
            return false;
        }

        return true;
    },

    unlockRoute(routeId) {
        if (this.availableRoutes.includes(routeId)) return false;

        if (!this.checkRouteUnlock(routeId)) return false;

        this.availableRoutes.push(routeId);
        this.showRouteNotification(routeId);

        return true;
    },

    selectRoute(routeId) {
        if (!this.availableRoutes.includes(routeId)) return false;

        const route = this.routeData.story_routes[routeId];
        if (!route) return false;

        this.currentRoute = routeId;
        GameState.update('currentRoute', routeId);

        this.showRouteSelectedNotification(route);

        return true;
    },

    checkRouteDetection() {
        // Check all detection points
        const detectionPoints = this.routeData.route_detection.detection_points;
        const currentChapter = GameState.get('currentChapter');

        detectionPoints.forEach(point => {
            if (point.chapter === currentChapter) {
                // Check all routes for unlock conditions
                Object.keys(this.routeData.story_routes).forEach(routeId => {
                    if (this.checkRouteUnlock(routeId)) {
                        this.unlockRoute(routeId);
                    }
                });

                // Show route hint
                if (!this.currentRoute) {
                    this.showRouteHint();
                }
            }

            // Final route selection point
            if (point.final_route_selection && point.chapter === currentChapter) {
                if (!this.currentRoute && this.availableRoutes.length > 0) {
                    this.showRouteSelectionUI();
                }
            }
        });
    },

    showRouteHint() {
        const hints = this.routeData.route_hints;
        const state = GameState.get();
        const protagonist = state.protagonist;

        // Determine which hint to show based on current attributes
        let hintKey = 'hint_balance';

        if (protagonist.attributes.strength >= 60 && protagonist.attributes.determination >= 10) {
            hintKey = 'hint_power';
        } else if (protagonist.attributes.intelligence >= 75) {
            hintKey = 'hint_wisdom';
        } else if (state.relationships?.char_xuner >= 25) {
            hintKey = 'hint_love';
        } else if (state.alchemy_skill >= 5) {
            hintKey = 'hint_alchemy';
        } else if (protagonist.attributes.determination >= 15) {
            hintKey = 'hint_revenge';
        } else if (state.relationships?.char_xiaozhan >= 25) {
            hintKey = 'hint_family';
        }

        const hint = hints[hintKey];
        if (hint) {
            this.showHintNotification(hint);
        }
    },

    showRouteNotification(routeId) {
        const route = this.routeData.story_routes[routeId];
        if (!route) return;

        const notification = document.createElement('div');
        notification.className = 'route-notification';
        notification.innerHTML = `
            <div class="route-notif-header">新路线解锁</div>
            <div class="route-notif-title">${route.name}</div>
            <div class="route-notif-desc">${route.description}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    },

    showRouteSelectedNotification(route) {
        const notification = document.createElement('div');
        notification.className = 'route-selected-notification';
        notification.innerHTML = `
            <div class="route-selected-header">已选择路线</div>
            <div class="route-selected-title">${route.name}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    showHintNotification(hint) {
        const notification = document.createElement('div');
        notification.className = 'route-hint-notification';
        notification.innerHTML = `
            <div class="hint-icon">💡</div>
            <div class="hint-text">${hint}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    },

    showRouteSelectionUI() {
        const modal = document.createElement('div');
        modal.id = 'route-selection-modal';
        modal.className = 'route-selection-modal';

        const routes = this.availableRoutes.map(routeId => this.routeData.story_routes[routeId]);

        modal.innerHTML = `
            <div class="route-selection-content">
                <h2>选择你的道路</h2>
                <p class="route-selection-desc">你的选择将决定未来的发展方向</p>
                <div class="route-list">
                    ${routes.map(route => `
                        <div class="route-option" data-route="${route.id}">
                            <div class="route-option-name">${route.name}</div>
                            <div class="route-option-desc">${route.description}</div>
                            <div class="route-option-ending">
                                <strong>结局称号：</strong>${route.ending.title}
                            </div>
                            <button class="route-select-btn" data-route="${route.id}">
                                选择此路线
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Bind selection buttons
        modal.querySelectorAll('.route-select-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const routeId = e.target.dataset.route;
                this.selectRoute(routeId);
                modal.remove();
            });
        });
    },

    getCurrentRouteChapters() {
        if (!this.currentRoute) return [];

        const route = this.routeData.story_routes[this.currentRoute];
        return route ? route.route_chapters : [];
    },

    getRouteEnding() {
        if (!this.currentRoute) return null;

        const route = this.routeData.story_routes[this.currentRoute];
        return route ? route.ending : null;
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => RouteSystem.init());
} else {
    RouteSystem.init();
}
