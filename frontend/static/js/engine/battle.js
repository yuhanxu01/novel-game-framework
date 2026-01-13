// Battle System Engine
const BattleSystem = {
    currentBattle: null,
    battleData: null,

    async init() {
        console.log('Initializing Battle System...');
        try {
            const response = await fetch('/data/battle_system.json');
            this.battleData = await response.json();
            console.log('Battle system loaded:', this.battleData);
        } catch (error) {
            console.error('Failed to load battle system:', error);
        }
    },

    startBattle(enemyId, config = {}) {
        const enemy = this.battleData.enemies.find(e => e.enemy_id === enemyId);
        if (!enemy) {
            console.error('Enemy not found:', enemyId);
            return null;
        }

        const player = GameState.get('protagonist');

        this.currentBattle = {
            turn: 1,
            phase: 'player',
            player: {
                hp: player.attributes.health || 100,
                maxHp: player.attributes.max_health || 100,
                stamina: player.attributes.stamina || 100,
                maxStamina: player.attributes.max_stamina || 100,
                attack: player.attributes.strength || 50,
                defense: player.attributes.defense || 30,
                cultivation: player.attributes.cultivation || 5,
                skills: player.skills || [],
                statusEffects: []
            },
            enemy: {
                id: enemy.enemy_id,
                name: enemy.name,
                hp: enemy.stats.max_hp,
                maxHp: enemy.stats.max_hp,
                stamina: enemy.stats.max_stamina,
                maxStamina: enemy.stats.max_stamina,
                attack: enemy.stats.attack,
                defense: enemy.stats.defense,
                cultivation: enemy.stats.cultivation,
                skills: enemy.skills,
                statusEffects: [],
                aiPattern: enemy.ai_pattern
            },
            battleLog: [],
            config: config,
            round: 0
        };

        this.renderBattleUI();
        this.addBattleLog(`战斗开始！你遭遇了${enemy.name}！`);

        if (enemy.special_dialogue && enemy.special_dialogue.battle_start) {
            this.addBattleLog(`${enemy.name}: ${enemy.special_dialogue.battle_start}`);
        }

        return this.currentBattle;
    },

    renderBattleUI() {
        // Create battle UI overlay
        const battleUI = document.createElement('div');
        battleUI.id = 'battle-screen';
        battleUI.className = 'battle-screen';
        battleUI.innerHTML = `
            <div class="battle-container">
                <div class="battle-header">
                    <div class="battle-player">
                        <div class="battle-name">萧炎</div>
                        <div class="battle-hp-bar">
                            <div class="battle-hp-fill" id="player-battle-hp"></div>
                            <span class="battle-hp-text" id="player-battle-hp-text">100/100</span>
                        </div>
                        <div class="battle-stamina-bar">
                            <div class="battle-stamina-fill" id="player-battle-stamina"></div>
                            <span class="battle-stamina-text" id="player-battle-stamina-text">100/100</span>
                        </div>
                    </div>
                    <div class="battle-vs">VS</div>
                    <div class="battle-enemy">
                        <div class="battle-name" id="enemy-name">敌人</div>
                        <div class="battle-hp-bar">
                            <div class="battle-hp-fill enemy" id="enemy-battle-hp"></div>
                            <span class="battle-hp-text" id="enemy-battle-hp-text">100/100</span>
                        </div>
                    </div>
                </div>

                <div class="battle-main">
                    <div class="battle-scene">
                        <div class="battle-player-sprite">🧑</div>
                        <div class="battle-enemy-sprite">👹</div>
                    </div>
                    <div class="battle-log" id="battle-log"></div>
                </div>

                <div class="battle-actions">
                    <button class="battle-btn" data-action="attack">普通攻击</button>
                    <button class="battle-btn" data-action="skill">使用斗技</button>
                    <button class="battle-btn" data-action="defend">防御</button>
                    <button class="battle-btn" data-action="item">使用物品</button>
                    <button class="battle-btn" data-action="flee">逃跑</button>
                </div>

                <div class="battle-skills" id="battle-skills" style="display: none;"></div>
            </div>
        `;

        document.body.appendChild(battleUI);
        this.bindBattleEvents();
        this.updateBattleUI();
    },

    bindBattleEvents() {
        const buttons = document.querySelectorAll('.battle-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                this.handlePlayerAction(action);
            });
        });
    },

    handlePlayerAction(action) {
        if (this.currentBattle.phase !== 'player') return;

        switch (action) {
            case 'attack':
                this.playerAttack();
                break;
            case 'skill':
                this.showSkillList();
                break;
            case 'defend':
                this.playerDefend();
                break;
            case 'item':
                this.showItemList();
                break;
            case 'flee':
                this.attemptFlee();
                break;
        }
    },

    playerAttack() {
        const damage = this.calculateDamage(
            this.currentBattle.player,
            this.currentBattle.enemy,
            1.0
        );

        this.currentBattle.enemy.hp -= damage;
        this.addBattleLog(`你对${this.currentBattle.enemy.name}造成了${damage}点伤害！`);

        this.updateBattleUI();
        this.checkBattleEnd();

        if (this.currentBattle) {
            this.endPlayerTurn();
        }
    },

    playerUseSkill(skillId) {
        const skill = this.battleData.skills.find(s => s.skill_id === skillId);
        if (!skill) return;

        if (this.currentBattle.player.stamina < skill.stamina_cost) {
            this.addBattleLog('斗气不足！');
            return;
        }

        this.currentBattle.player.stamina -= skill.stamina_cost;

        this.addBattleLog(skill.animation_text);

        const damage = this.calculateDamage(
            this.currentBattle.player,
            this.currentBattle.enemy,
            skill.damage_multiplier
        );

        this.currentBattle.enemy.hp -= damage;
        this.addBattleLog(`造成了${damage}点伤害！`);

        // Apply skill effects
        if (skill.effects) {
            skill.effects.forEach(effect => {
                this.applyEffect(effect, 'enemy');
            });
        }

        this.updateBattleUI();
        document.getElementById('battle-skills').style.display = 'none';

        this.checkBattleEnd();

        if (this.currentBattle) {
            this.endPlayerTurn();
        }
    },

    playerDefend() {
        this.currentBattle.player.statusEffects.push({
            type: 'defending',
            duration: 1
        });
        this.addBattleLog('你进入了防御姿态！');
        this.endPlayerTurn();
    },

    attemptFlee() {
        const escapeChance = this.battleData.battle_system.combat_mechanics.escape_chance_base;
        const roll = Math.random();

        if (roll < escapeChance) {
            this.addBattleLog('你成功逃脱了！');
            setTimeout(() => {
                this.endBattle('flee');
            }, 1000);
        } else {
            this.addBattleLog('逃跑失败！');
            this.endPlayerTurn();
        }
    },

    endPlayerTurn() {
        this.currentBattle.phase = 'enemy';
        setTimeout(() => {
            this.enemyTurn();
        }, 1000);
    },

    enemyTurn() {
        if (!this.currentBattle) return;

        const enemy = this.currentBattle.enemy;

        // Simple AI: random attack or skill
        const roll = Math.random();

        if (roll < 0.3 && enemy.skills.length > 0) {
            // Use skill
            const skill = enemy.skills[Math.floor(Math.random() * enemy.skills.length)];
            if (enemy.stamina >= skill.stamina_cost) {
                this.enemyUseSkill(skill);
            } else {
                this.enemyBasicAttack();
            }
        } else {
            this.enemyBasicAttack();
        }

        this.updateBattleUI();
        this.checkBattleEnd();

        if (this.currentBattle) {
            this.currentBattle.phase = 'player';
            this.currentBattle.round++;
        }
    },

    enemyBasicAttack() {
        const damage = this.calculateDamage(
            this.currentBattle.enemy,
            this.currentBattle.player,
            1.0
        );

        this.currentBattle.player.hp -= damage;
        this.addBattleLog(`${this.currentBattle.enemy.name}对你造成了${damage}点伤害！`);
    },

    enemyUseSkill(skill) {
        this.currentBattle.enemy.stamina -= skill.stamina_cost;
        this.addBattleLog(`${this.currentBattle.enemy.name}使用了${skill.name}！`);

        const damage = this.calculateDamage(
            this.currentBattle.enemy,
            this.currentBattle.player,
            skill.damage / 50
        );

        this.currentBattle.player.hp -= damage;
        this.addBattleLog(`你受到了${damage}点伤害！`);
    },

    calculateDamage(attacker, defender, multiplier) {
        const baseDamage = attacker.attack * multiplier;
        const defense = defender.defense;
        const finalDamage = Math.max(
            1,
            Math.floor(baseDamage * (1 + (attacker.attack - defense) / 100) * (Math.random() * 0.2 + 0.9))
        );

        // Check for defending status
        const isDefending = defender.statusEffects.some(e => e.type === 'defending');
        if (isDefending) {
            return Math.floor(finalDamage * 0.5);
        }

        return finalDamage;
    },

    applyEffect(effect, target) {
        const targetObj = target === 'enemy' ? this.currentBattle.enemy : this.currentBattle.player;

        switch (effect.type) {
            case 'burn':
                targetObj.statusEffects.push({
                    type: 'burn',
                    duration: effect.duration,
                    damagePerTurn: effect.damage_per_turn
                });
                this.addBattleLog(`${target === 'enemy' ? this.currentBattle.enemy.name : '你'}陷入了灼烧状态！`);
                break;
            case 'control':
                this.addBattleLog(`${target === 'enemy' ? this.currentBattle.enemy.name : '你'}被控制了！`);
                break;
        }
    },

    checkBattleEnd() {
        if (this.currentBattle.player.hp <= 0) {
            this.endBattle('defeat');
        } else if (this.currentBattle.enemy.hp <= 0) {
            this.endBattle('victory');
        }
    },

    endBattle(result) {
        if (result === 'victory') {
            this.addBattleLog('战斗胜利！');

            // Grant rewards
            const enemy = this.battleData.enemies.find(e => e.enemy_id === this.currentBattle.enemy.id);
            if (enemy && enemy.drop_rewards) {
                this.grantRewards(enemy.drop_rewards);
            }
        } else if (result === 'defeat') {
            this.addBattleLog('战斗失败...');
        }

        setTimeout(() => {
            const battleScreen = document.getElementById('battle-screen');
            if (battleScreen) {
                battleScreen.remove();
            }
            this.currentBattle = null;
        }, 2000);
    },

    grantRewards(rewards) {
        if (rewards.experience) {
            GameState.update('protagonist', p => ({
                ...p,
                experience: (p.experience || 0) + rewards.experience
            }));
            this.addBattleLog(`获得${rewards.experience}点经验！`);
        }

        if (rewards.gold) {
            GameState.update('protagonist', p => ({
                ...p,
                attributes: {
                    ...p.attributes,
                    wealth: (p.attributes.wealth || 0) + rewards.gold
                }
            }));
            this.addBattleLog(`获得${rewards.gold}金币！`);
        }

        if (rewards.items) {
            rewards.items.forEach(itemDrop => {
                if (Math.random() < itemDrop.chance) {
                    InventorySystem.addItem(itemDrop.item_id);
                    this.addBattleLog(`获得物品：${itemDrop.item_id}！`);
                }
            });
        }
    },

    showSkillList() {
        const skillsDiv = document.getElementById('battle-skills');
        const playerSkills = this.currentBattle.player.skills;

        const availableSkills = this.battleData.skills.filter(s =>
            playerSkills.includes(s.skill_id)
        );

        skillsDiv.innerHTML = availableSkills.map(skill => `
            <button class="skill-btn" data-skill="${skill.skill_id}">
                ${skill.name} (消耗: ${skill.stamina_cost})
                <div class="skill-desc">${skill.description}</div>
            </button>
        `).join('');

        skillsDiv.style.display = 'block';

        // Bind skill buttons
        skillsDiv.querySelectorAll('.skill-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const skillId = e.currentTarget.dataset.skill;
                this.playerUseSkill(skillId);
            });
        });
    },

    showItemList() {
        // TODO: Implement item usage in battle
        this.addBattleLog('物品系统开发中...');
    },

    updateBattleUI() {
        if (!this.currentBattle) return;

        // Update player HP
        const playerHpPercent = (this.currentBattle.player.hp / this.currentBattle.player.maxHp) * 100;
        document.getElementById('player-battle-hp').style.width = `${playerHpPercent}%`;
        document.getElementById('player-battle-hp-text').textContent =
            `${Math.max(0, this.currentBattle.player.hp)}/${this.currentBattle.player.maxHp}`;

        // Update player stamina
        const playerStaminaPercent = (this.currentBattle.player.stamina / this.currentBattle.player.maxStamina) * 100;
        document.getElementById('player-battle-stamina').style.width = `${playerStaminaPercent}%`;
        document.getElementById('player-battle-stamina-text').textContent =
            `${this.currentBattle.player.stamina}/${this.currentBattle.player.maxStamina}`;

        // Update enemy HP
        const enemyHpPercent = (this.currentBattle.enemy.hp / this.currentBattle.enemy.maxHp) * 100;
        document.getElementById('enemy-battle-hp').style.width = `${enemyHpPercent}%`;
        document.getElementById('enemy-battle-hp-text').textContent =
            `${Math.max(0, this.currentBattle.enemy.hp)}/${this.currentBattle.enemy.maxHp}`;

        document.getElementById('enemy-name').textContent = this.currentBattle.enemy.name;
    },

    addBattleLog(message) {
        if (!this.currentBattle) return;

        this.currentBattle.battleLog.push(message);

        const logDiv = document.getElementById('battle-log');
        if (logDiv) {
            const logEntry = document.createElement('div');
            logEntry.className = 'battle-log-entry';
            logEntry.textContent = message;
            logDiv.appendChild(logEntry);
            logDiv.scrollTop = logDiv.scrollHeight;
        }
    }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => BattleSystem.init());
} else {
    BattleSystem.init();
}
