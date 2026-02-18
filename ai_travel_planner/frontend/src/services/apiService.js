import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败';
    console.error('API Error:', message);
    return Promise.reject(new Error(message));
  }
);

export const apiService = {
  // 创建对话
  createConversation: async (userId = null) => {
    return await api.post('/chat/conversations', { user_id: userId });
  },

  // 发送消息
  sendMessage: async ({ message, conversationId, userId = null, skipClarification = false }) => {
    return await api.post('/chat/message', {
      message,
      conversation_id: conversationId,
      user_id: userId,
      skip_clarification: skipClarification
    });
  },

  // 获取对话历史
  getConversation: async (conversationId) => {
    return await api.get(`/chat/conversations/${conversationId}`);
  },

  // 删除对话
  deleteConversation: async (conversationId) => {
    return await api.delete(`/chat/conversations/${conversationId}`);
  },

  // 生成行程
  generatePlan: async (requirements) => {
    return await api.post('/plan/generate', requirements);
  },

  // 获取行程
  getPlan: async (planId) => {
    return await api.get(`/plan/${planId}`);
  },

  // 健康检查
  healthCheck: async () => {
    return await api.get('/health');
  }
};

export default api;
