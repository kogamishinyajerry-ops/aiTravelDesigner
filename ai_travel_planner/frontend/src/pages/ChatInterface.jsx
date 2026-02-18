import React, { useState, useEffect, useRef } from 'react';
import { 
  Container, 
  Paper, 
  TextField, 
  IconButton, 
  Box, 
  Typography, 
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import { apiService } from '../services/apiService';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [clarificationQuestions, setClarificationQuestions] = useState([]);
  const [isComplete, setIsComplete] = useState(false);
  const [needsPlanning, setNeedsPlanning] = useState(false);
  const [error, setError] = useState(null);
  
  const messagesEndRef = useRef(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 初始化对话
  useEffect(() => {
    initializeConversation();
  }, []);

  const initializeConversation = async () => {
    try {
      const response = await apiService.createConversation();
      if (response.success) {
        setConversationId(response.conversation_id);
        addMessage({
          role: 'assistant',
          content: response.message,
          timestamp: new Date().toISOString()
        });
      }
    } catch (err) {
      console.error('Failed to initialize conversation:', err);
    }
  };

  const addMessage = (message) => {
    setMessages(prev => [...prev, message]);
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setError(null);
    
    // 添加用户消息
    addMessage({
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    });

    setLoading(true);

    try {
      const response = await apiService.sendMessage({
        message: userMessage,
        conversation_id: conversationId
      });

      if (response.success) {
        // 添加AI回复
        addMessage({
          role: 'assistant',
          content: response.message,
          timestamp: new Date().toISOString()
        });

        // 更新状态
        setClarificationQuestions(response.clarification_questions || []);
        setIsComplete(response.is_complete || false);
        setNeedsPlanning(response.needs_planning || false);
        
        // 显示提取的信息
        if (response.extracted_info) {
          console.log('提取的信息:', response.extracted_info);
        }
      }
    } catch (err) {
      console.error('发送消息失败:', err);
      setError('发送消息失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickQuestion = (question) => {
    setInput(question);
    setTimeout(() => handleSend(), 100);
  };

  const renderMessage = (message, index) => {
    const isUser = message.role === 'user';
    
    return (
      <Box
        key={index}
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          mb: 2
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            maxWidth: '70%',
            flexDirection: isUser ? 'row-reverse' : 'row'
          }}
        >
          <Box
            sx={{
              width: 36,
              height: 36,
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: isUser ? 'primary.main' : 'secondary.main',
              color: 'white',
              ml: isUser ? 0 : 1,
              mr: isUser ? 1 : 0
            }}
          >
            {isUser ? <PersonIcon /> : <SmartToyIcon />}
          </Box>
          
          <Paper
            elevation={1}
            sx={{
              p: 2,
              bgcolor: isUser ? 'primary.light' : 'grey.100',
              borderRadius: 2,
              whiteSpace: 'pre-wrap'
            }}
          >
            <Typography variant="body1">{message.content}</Typography>
          </Paper>
        </Box>
      </Box>
    );
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        AI 旅行规划师
      </Typography>
      <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
        告诉我你想去哪里，我来帮你规划完美的旅程
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {needsPlanning && (
        <Alert severity="success" sx={{ mb: 2 }}>
          我已经了解了您的需求！现在可以开始规划行程了。
        </Alert>
      )}

      {/* 澄清问题 */}
      {clarificationQuestions.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            帮助我更好地了解您：
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {clarificationQuestions.map((q, idx) => (
              <Chip
                key={idx}
                label={q.question}
                onClick={() => handleQuickQuestion(q.question)}
                clickable
                color="primary"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>
      )}

      {/* 消息列表 */}
      <Paper
        elevation={3}
        sx={{
          p: 3,
          height: 500,
          overflowY: 'auto',
          mb: 2,
          bgcolor: 'grey.50'
        }}
      >
        {messages.length === 0 && (
          <Box sx={{ textAlign: 'center', mt: 20, color: 'text.secondary' }}>
            <SmartToyIcon sx={{ fontSize: 60, mb: 2 }} />
            <Typography>开始对话吧！</Typography>
          </Box>
        )}
        
        {messages.map(renderMessage)}
        
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <CircularProgress size={24} />
          </Box>
        )}
        
        <div ref={messagesEndRef} />
      </Paper>

      {/* 输入框 */}
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="告诉我你想去哪里旅行，比如：我想去日本京都玩7天，预算2万..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
          variant="outlined"
        />
        <IconButton
          onClick={handleSend}
          disabled={!input.trim() || loading}
          color="primary"
          sx={{ 
            bgcolor: 'primary.main',
            color: 'white',
            '&:hover': { bgcolor: 'primary.dark' },
            '&:disabled': { bgcolor: 'grey.300' }
          }}
        >
          <SendIcon />
        </IconButton>
      </Box>

      {/* 快捷选项 */}
      {messages.length <= 2 && (
        <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {[
            "我想去日本旅游",
            "计划去泰国普吉岛度假",
            "想体验欧洲文化之旅",
            "国内游推荐一下"
          ].map((suggestion, idx) => (
            <Chip
              key={idx}
              label={suggestion}
              onClick={() => handleQuickQuestion(suggestion)}
              clickable
              size="small"
              color="default"
            />
          ))}
        </Box>
      )}
    </Container>
  );
};

export default ChatInterface;
