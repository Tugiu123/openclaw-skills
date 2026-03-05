/**
 * 飞书云函数 - 消息事件处理
 * 部署到飞书开放平台 → 云函数
 */

// 配置
const APP_ID = process.env.APP_ID || 'cli_a901b7b467b8dccd';
const APP_SECRET = process.env.APP_SECRET || '3f3TQ8Mo7rPrBeL4fT5P0em2Mbjoe34o';
const GATEWAY_URL = process.env.GATEWAY_URL || 'http://127.0.0.1:18789';

/**
 * 获取 tenant_access_token
 */
async function getTenantAccessToken() {
  const response = await fetch('https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET })
  });
  return response.json();
}

/**
 * 发送消息给用户
 */
async function sendMessage(receive_id, text) {
  const { tenant_access_token } = await getTenantAccessToken();
  
  await fetch(`https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${tenant_access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      receive_id,
      msg_type: 'text',
      content: JSON.stringify({ text })
    })
  });
}

/**
 * 云函数入口
 */
exports.handler = async (event) => {
  const { verify_token, type } = event.queryStringParameters || {};
  
  // URL 验证（飞书配置回调时触发）
  if (type === 'url_verification') {
    return {
      challenge: verify_token
    };
  }
  
  // 消息事件
  try {
    const body = JSON.parse(event.body || '{}');
    const { header, event } = body;
    
    console.log('收到事件:', JSON.stringify(body));
    
    // 处理消息事件
    if (header?.event_type === 'im.message.message_sent_v1') {
      const { message } = event || {};
      const receive_id = message?.sender?.open_id;
      const text = message?.message?.content?.text;
      
      if (receive_id && text) {
        console.log(`收到消息 from ${receive_id}: ${text}`);
        
        // 转发给 OpenClaw Gateway
        try {
          await fetch(`${GATEWAY_URL}/feishu/webhook`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              message_id: message?.message_id,
              receive_id,
              text,
              sender_id: receive_id
            })
          });
          console.log('转发到 Gateway 成功');
        } catch (err) {
          console.error('转发失败:', err.message);
        }
      }
    }
    
    return { success: true };
  } catch (err) {
    console.error('处理失败:', err);
    return { success: false, error: err.message };
  }
};
