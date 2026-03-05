/**
 * 飞书 Webhook 服务
 * 接收飞书事件回调，转发给 OpenClaw Gateway
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// 配置
const PORT = 18790;
const GATEWAY_URL = 'http://127.0.0.1:18789';
const FEISHU_TOKEN_FILE = path.join(process.env.HOME, '.openclaw', '.feishu_access_token');

// 获取 tenant_access_token
async function getTenantAccessToken() {
  try {
    const token = fs.readFileSync(FEISHU_TOKEN_FILE, 'utf8').trim();
    return token;
  } catch (err) {
    console.error('Failed to read token:', err.message);
    return null;
  }
}

// 发送消息给用户
async function sendMessage(receive_id, text) {
  const token = await getTenantAccessToken();
  if (!token) return false;
  
  try {
    const response = await fetch(`https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=open_id`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        receive_id,
        msg_type: 'text',
        content: JSON.stringify({ text })
      })
    });
    
    const result = await response.json();
    console.log('Send message result:', JSON.stringify(result));
    return result.code === 0;
  } catch (err) {
    console.error('Failed to send message:', err.message);
    return false;
  }
}

// 验证 URL（飞书配置回调时触发）
function handleVerification(url) {
  // 从 URL 字符串中提取 challenge 参数
  const match = url.match(/[?&]challenge=([^&]+)/);
  if (match) {
    return match[1];
  }
  return 'ok';
}

// 处理飞书事件
async function handleEvent(body) {
  try {
    const event = JSON.parse(body);
    console.log('Received event:', JSON.stringify(event, null, 2));
    
    // 处理消息事件
    if (event.event === 'im.message.message_sent_v1' || event.header?.event_type === 'im.message.receive_v1') {
      const message = event.event || event;
      const senderOpenId = message.sender?.sender_id?.open_id || message.sender?.open_id;
      const text = message.message?.content?.text || message.content?.text;
      
      if (senderOpenId && text) {
        console.log(`Received message from ${senderOpenId}: ${text}`);
        
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
          console.log('Forwarded to Gateway');
        } catch (err) {
          console.error('Failed to forward to Gateway:', err.message);
        }
        
        // 立即返回 success 确认收到
        return { success: true };
      }
    }
    
    return { success: true };
  } catch (err) {
    console.error('Error handling event:', err.message);
    return { error: err.message };
  }
}

// HTTP 服务器
const server = http.createServer(async (req, res) => {
  console.log(`${req.method} ${req.url}`);
  
  // 处理飞书 webhook
  if (req.url === '/feishu/webhook' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const result = await handleEvent(body);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }
  
  // URL 验证（飞书配置回调时触发 GET 请求）
  if (req.url.startsWith('/feishu/webhook') && req.method === 'GET') {
    const challenge = handleVerification(req.url);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(challenge);
    return;
  }
  
  // 其他请求
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not Found' }));
});

server.listen(PORT, () => {
  console.log(`🚀 Feishu Webhook Server running on port ${PORT}`);
  console.log(`   Local: http://localhost:${PORT}/feishu/webhook`);
  console.log(`   Gateway: ${GATEWAY_URL}`);
});
