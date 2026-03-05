/**
 * 飞书长连接客户端
 * 接收飞书事件并转发给 OpenClaw Gateway
 */

const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 配置
const FEISHU_API = 'https://open.larksuite.com';
const APP_ID = 'cli_a901b7b467b8dccd';
const APP_SECRET = '3f3TQ8Mo7rPrBeL4fT5P0em2Mbjoe34o';
const GATEWAY_URL = 'http://127.0.0.1:18789';
const PING_INTERVAL = 30000; // 30秒心跳

let ws = null;
let reconnectTimer = null;
let tenantAccessToken = null;

// 获取 tenant_access_token
async function getTenantAccessToken() {
  try {
    const response = await fetch(`${FEISHU_API}/open-apis/auth/v3/tenant_access_token/internal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET })
    });
    const data = await response.json();
    if (data.tenant_access_token) {
      tenantAccessToken = data.tenant_access_token;
      console.log('✅ Got tenant_access_token');
      return tenantAccessToken;
    }
    throw new Error('Failed to get token: ' + JSON.stringify(data));
  } catch (err) {
    console.error('❌ Get token error:', err.message);
    return null;
  }
}

// 发送消息给用户
async function sendMessage(receive_id, text) {
  if (!tenantAccessToken) {
    console.error('❌ No token available');
    return false;
  }
  
  try {
    const response = await fetch(`${FEISHU_API}/open-apis/im/v1/messages?receive_id_type=open_id`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${tenantAccessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        receive_id,
        msg_type: 'text',
        content: JSON.stringify({ text })
      })
    });
    const result = await response.json();
    console.log('📤 Send message result:', JSON.stringify(result));
    return result.code === 0;
  } catch (err) {
    console.error('❌ Send message error:', err.message);
    return false;
  }
}

// 连接长连接
async function connect() {
  try {
    // 获取 token
    const token = await getTenantAccessToken();
    if (!token) {
      throw new Error('Failed to get token');
    }
    
    // 建立长连接
    ws = new WebSocket(`${FEISHU_API}/open-apis/im/v1/p2p_messages/subtenant`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    ws.on('open', () => {
      console.log('✅ Connected to Feishu WebSocket');
    });
    
    ws.on('message', async (data) => {
      try {
        const event = JSON.parse(data.toString());
        console.log('📥 Received:', JSON.stringify(event, null, 2));
        
        // 处理心跳
        if (event.type === 'ping') {
          console.log('💓 Received ping');
          return;
        }
        
        // 处理消息事件
        if (event.header?.event_type === 'im.message.message_sent_v1') {
          const message = event.event;
          const senderOpenId = message.sender?.sender_id?.open_id;
          const text = message.message?.content?.text;
          
          if (senderOpenId && text) {
            console.log(`💬 Message from ${senderOpenId}: ${text}`);
            
            // 转发给 OpenClaw Gateway
            try {
              await fetch(`${GATEWAY_URL}/api/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  channel: 'feishu',
                  message_id: message.message_id,
                  from: senderOpenId,
                  text: text
                })
              });
              console.log('✅ Forwarded to Gateway');
            } catch (err) {
              console.error('❌ Forward error:', err.message);
            }
            
            // 回复用户
            await sendMessage(senderOpenId, `收到消息: ${text}`);
          }
        }
      } catch (err) {
        console.error('❌ Handle message error:', err.message);
      }
    });
    
    ws.on('close', (code, reason) => {
      console.log(`🔌 Disconnected (${code}): ${reason}`);
      scheduleReconnect();
    });
    
    ws.on('error', (err) => {
      console.error('❌ WebSocket error:', err.message);
    });
    
  } catch (err) {
    console.error('❌ Connect error:', err.message);
    scheduleReconnect();
  }
}

// 定时重连
function scheduleReconnect() {
  if (reconnectTimer) return;
  
  reconnectTimer = setTimeout(async () => {
    reconnectTimer = null;
    console.log('🔄 Reconnecting...');
    await connect();
  }, 5000);
}

// 启动
console.log('🚀 Starting Feishu Long Connection Client...');
connect();
