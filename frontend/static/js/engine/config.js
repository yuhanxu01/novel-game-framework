const GameConfig = {
    API_BASE_URL: 'http://localhost:8000/api',
    
    PROJECT_ID: 1,
    
    TEXT_SPEED: 30,
    AUTO_PLAY_DELAY: 3000,
    
    DEFAULT_ATTRIBUTES: {
        health: { name: '生命值', max: 100, current: 100, icon: '❤️' },
        stamina: { name: '体力', max: 100, current: 100, icon: '⚡' },
        strength: { name: '力量', value: 10, icon: '💪' },
        intelligence: { name: '智力', value: 10, icon: '🧠' },
        charisma: { name: '魅力', value: 10, icon: '✨' },
        luck: { name: '幸运', value: 10, icon: '🍀' }
    },
    
    SAVE_SLOTS: 10,
    AUTO_SAVE_INTERVAL: 300000,
    
    DEBUG_MODE: true
};

const APIEndpoints = {
    getGameData: () => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/`,
    getChapter: (chapterId) => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/chapter/${chapterId}/`,
    getScene: (sceneId) => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/scene/${sceneId}/`,
    saveGame: () => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/save/`,
    loadGame: (slot) => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/load/${slot}/`,
    listSaves: () => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/saves/`,
    deleteSave: (slot) => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/save/${slot}/delete/`,
    checkCondition: () => `${GameConfig.API_BASE_URL}/game/project/${GameConfig.PROJECT_ID}/check-condition/`,
    
    startCreativeSession: () => `${GameConfig.API_BASE_URL}/creative/project/${GameConfig.PROJECT_ID}/session/start/`,
    creativeChat: (sessionId) => `${GameConfig.API_BASE_URL}/creative/session/${sessionId}/chat/`,
    generateContent: (sessionId) => `${GameConfig.API_BASE_URL}/creative/session/${sessionId}/generate/`,
    applyModification: (sessionId) => `${GameConfig.API_BASE_URL}/creative/session/${sessionId}/apply/`,
    getModificationHistory: () => `${GameConfig.API_BASE_URL}/creative/project/${GameConfig.PROJECT_ID}/history/`,
};
