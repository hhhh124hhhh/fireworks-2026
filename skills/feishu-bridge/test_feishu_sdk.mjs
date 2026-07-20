import * as Lark from '@larksuiteoapi/node-sdk';

console.log('Lark version:', Lark.version);
console.log('Available WSClient:', typeof Lark.WSClient);
console.log('WSClient:', Lark.WSClient);

const testConfig = {
  appId: 'test',
  appSecret: 'test',
  domain: Lark.Domain.Feishu,
  appType: Lark.AppType.SelfBuild,
  loggerLevel: Lark.LoggerLevel.info
};

console.log('Test config:', testConfig);

try {
  const wsClient = new Lark.WSClient(testConfig);
  console.log('WSClient created successfully:', wsClient);
} catch (err) {
  console.error('Failed to create WSClient:', err.message);
  console.error('Error:', err);
}
