const ConditionChecker = {
    async check(condition, playerState) {
        if (!condition || Object.keys(condition).length === 0) {
            return { passed: true, requirementText: null };
        }
        
        const requirements = [];
        let allPassed = true;
        
        if (condition.需要属性 || condition.needs_attribute) {
            const attrReq = condition.需要属性 || condition.needs_attribute;
            for (const [attr, value] of Object.entries(attrReq)) {
                const playerValue = playerState.attributes?.[attr]?.value || 0;
                const passed = playerValue >= value;
                
                if (!passed) allPassed = false;
                
                const attrName = playerState.attributes?.[attr]?.name || attr;
                requirements.push({
                    text: `${attrName} ≥ ${value}`,
                    passed: passed,
                    current: playerValue
                });
            }
        }
        
        if (condition.需要物品 || condition.needs_item) {
            const itemReq = condition.需要物品 || condition.needs_item;
            for (const itemId of itemReq) {
                const hasItem = GameState.hasItem(itemId);
                
                if (!hasItem) allPassed = false;
                
                requirements.push({
                    text: `需要物品: ${itemId}`,
                    passed: hasItem
                });
            }
        }
        
        if (condition.需要好感 || condition.needs_relationship) {
            const relReq = condition.需要好感 || condition.needs_relationship;
            for (const [charId, value] of Object.entries(relReq)) {
                const currentRel = GameState.getRelationship(charId);
                const passed = currentRel >= value;
                
                if (!passed) allPassed = false;
                
                const gameData = GameState.get('gameData');
                const charName = gameData?.characters?.[charId]?.name || charId;
                
                requirements.push({
                    text: `${charName}好感度 ≥ ${value}`,
                    passed: passed,
                    current: currentRel
                });
            }
        }
        
        if (condition.需要标记 || condition.needs_flag) {
            const flagReq = condition.需要标记 || condition.needs_flag;
            for (const flag of flagReq) {
                const hasFlag = GameState.hasFlag(flag);
                
                if (!hasFlag) allPassed = false;
                
                requirements.push({
                    text: `需要: ${flag}`,
                    passed: hasFlag
                });
            }
        }
        
        if (condition.禁止标记 || condition.forbid_flag) {
            const flagReq = condition.禁止标记 || condition.forbid_flag;
            for (const flag of flagReq) {
                const hasFlag = GameState.hasFlag(flag);
                
                if (hasFlag) allPassed = false;
                
                requirements.push({
                    text: `不能有: ${flag}`,
                    passed: !hasFlag
                });
            }
        }
        
        const requirementText = requirements.length > 0
            ? requirements.map(r => `${r.passed ? '✓' : '✗'} ${r.text}`).join('\n')
            : null;
        
        return {
            passed: allPassed,
            requirements: requirements,
            requirementText: requirementText
        };
    },
    
    async checkRemote(condition, playerState) {
        try {
            const response = await Utils.post(APIEndpoints.checkCondition(), {
                condition: condition,
                player_state: playerState
            });
            
            return { passed: response.result, requirementText: null };
        } catch (error) {
            Utils.error('Remote condition check failed:', error);
            return this.check(condition, playerState);
        }
    },
    
    evaluateExpression(expression, playerState) {
        const safeContext = {
            attr: (name) => playerState.attributes?.[name]?.value || 0,
            item: (id) => GameState.hasItem(id),
            flag: (name) => GameState.hasFlag(name),
            rel: (id) => GameState.getRelationship(id),
            random: () => Math.random(),
            roll: (max) => Utils.randomInt(1, max)
        };
        
        try {
            const func = new Function(...Object.keys(safeContext), `return ${expression}`);
            return func(...Object.values(safeContext));
        } catch (error) {
            Utils.error('Expression evaluation failed:', error);
            return false;
        }
    }
};
