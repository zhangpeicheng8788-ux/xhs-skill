#!/usr/bin/env node
/**
 * 小红书扫码登录脚本 (Node.js 版本)
 * 弹出浏览器窗口，扫码登录后自动保存 Cookie
 * 
 * 使用方法:
 *     node login_xhs.js
 * 
 * 功能:
 *     1. 弹出小红书登录页面
 *     2. 用户扫码登录
 *     3. 自动保存 Cookie 到 .env 文件
 *     4. 下次发布时自动使用保存的 Cookie
 * 
 * 依赖安装:
 *     npm install playwright dotenv
 *     npx playwright install chromium
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// 获取脚本所在目录
const SCRIPT_DIR = path.join(__dirname, '..');
const ENV_FILE = path.join(SCRIPT_DIR, '.env');

/**
 * 加载现有的 Cookie
 */
function loadExistingCookie() {
    if (fs.existsSync(ENV_FILE)) {
        const content = fs.readFileSync(ENV_FILE, 'utf-8');
        const match = content.match(/XHS_COOKIE=(.+)/);
        return match ? match[1].trim() : null;
    }
    return null;
}

/**
 * 保存 Cookie 到 .env 文件
 */
function saveCookie(cookieStr) {
    try {
        let content = '';
        
        // 如果文件已存在，读取现有内容
        if (fs.existsSync(ENV_FILE)) {
            content = fs.readFileSync(ENV_FILE, 'utf-8');
            
            // 移除旧的 XHS_COOKIE 行
            content = content.split('\n')
                .filter(line => !line.startsWith('XHS_COOKIE=') && !line.includes('Cookie 更新时间'))
                .join('\n');
        }
        
        // 添加新的 Cookie
        const timestamp = new Date().toLocaleString('zh-CN');
        const newContent = content.trim() + '\n' +
            `XHS_COOKIE=${cookieStr}\n` +
            `# Cookie 更新时间: ${timestamp}\n`;
        
        fs.writeFileSync(ENV_FILE, newContent, 'utf-8');
        console.log(`✅ Cookie 已保存到: ${ENV_FILE}`);
        
        return true;
    } catch (error) {
        console.error(`❌ 保存 Cookie 失败: ${error.message}`);
        return false;
    }
}

/**
 * 等待用户登录完成
 */
async function waitForLogin(page) {
    console.log('\n📱 请使用小红书 APP 扫码登录...');
    console.log('⏳ 等待登录中...');
    
    try {
        // 方法1: 等待跳转到首页或创作者中心
        await page.waitForURL('**/explore**', { timeout: 120000 }).catch(() => {});
        return true;
    } catch {
        try {
            // 方法2: 等待用户头像出现
            await page.waitForSelector('.avatar, .user-avatar, [class*="avatar"]', { timeout: 120000 });
            return true;
        } catch {
            try {
                // 方法3: 检查是否有用户相关的 Cookie
                const cookies = await page.context().cookies();
                const hasUserCookie = cookies.some(c => 
                    ['web_session', 'a1', 'webId'].includes(c.name)
                );
                return hasUserCookie;
            } catch {
                return false;
            }
        }
    }
}

/**
 * 格式化 Cookie
 */
function formatCookie(cookies) {
    return cookies.map(c => `${c.name}=${c.value}`).join('; ');
}

/**
 * 使用二维码登录小红书
 */
async function loginWithQRCode() {
    const browser = await chromium.launch({
        headless: false,
        args: [
            '--window-size=800,900',
            '--window-position=400,100'
        ]
    });
    
    const context = await browser.newContext({
        viewport: { width: 800, height: 900 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    
    const page = await context.newPage();
    
    try {
        // 访问小红书创作者平台登录页
        console.log('📄 正在打开小红书登录页面...');
        await page.goto('https://creator.xiaohongshu.com/login', { 
            waitUntil: 'networkidle' 
        });
        
        // 等待二维码加载
        await page.waitForTimeout(2000);
        
        // 等待用户登录
        const loginSuccess = await waitForLogin(page);
        
        if (!loginSuccess) {
            console.log('❌ 登录超时或失败');
            await browser.close();
            return false;
        }
        
        console.log('✅ 登录成功！');
        
        // 等待一下确保 Cookie 完全设置
        await page.waitForTimeout(2000);
        
        // 获取所有 Cookie
        const cookies = await context.cookies();
        
        if (!cookies || cookies.length === 0) {
            console.log('❌ 未能获取 Cookie');
            await browser.close();
            return false;
        }
        
        // 格式化并保存 Cookie
        const cookieStr = formatCookie(cookies);
        
        console.log(`\n📋 获取到 ${cookies.length} 个 Cookie`);
        
        // 显示关键 Cookie
        const keyCookies = ['web_session', 'a1', 'webId'];
        const foundKeys = cookies
            .filter(c => keyCookies.includes(c.name))
            .map(c => c.name);
        
        if (foundKeys.length > 0) {
            console.log(`🔑 关键 Cookie: ${foundKeys.join(', ')}`);
        }
        
        // 保存 Cookie
        if (saveCookie(cookieStr)) {
            console.log('\n🎉 登录配置完成！');
            console.log('💡 现在可以使用 publish_xhs.py 或 publish_xhs.js 发布笔记了');
            
            // 等待几秒让用户看到成功消息
            await page.waitForTimeout(3000);
            await browser.close();
            return true;
        } else {
            await browser.close();
            return false;
        }
        
    } catch (error) {
        console.error(`❌ 登录过程出错: ${error.message}`);
        await browser.close();
        return false;
    }
}

/**
 * 验证现有 Cookie 是否有效
 */
async function verifyCookie() {
    const existingCookie = loadExistingCookie();
    
    if (!existingCookie) {
        return false;
    }
    
    console.log('🔍 检测到现有 Cookie，正在验证...');
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    
    // 设置 Cookie
    const cookies = existingCookie.split(';').map(item => {
        const [name, value] = item.trim().split('=');
        return {
            name: name.trim(),
            value: value.trim(),
            domain: '.xiaohongshu.com',
            path: '/'
        };
    }).filter(c => c.name && c.value);
    
    await context.addCookies(cookies);
    
    const page = await context.newPage();
    
    try {
        // 访问创作者中心
        await page.goto('https://creator.xiaohongshu.com/', { timeout: 10000 });
        await page.waitForTimeout(2000);
        
        // 检查是否登录成功（没有跳转到登录页）
        const currentUrl = page.url();
        const isValid = !currentUrl.includes('login');
        
        await browser.close();
        
        if (isValid) {
            console.log('✅ 现有 Cookie 有效');
        } else {
            console.log('⚠️ 现有 Cookie 已失效');
        }
        
        return isValid;
        
    } catch (error) {
        console.log(`⚠️ Cookie 验证失败: ${error.message}`);
        await browser.close();
        return false;
    }
}

/**
 * 询问用户输入
 */
function askQuestion(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    return new Promise(resolve => {
        rl.question(question, answer => {
            rl.close();
            resolve(answer.trim().toLowerCase());
        });
    });
}

/**
 * 主函数
 */
async function main() {
    console.log('='.repeat(60));
    console.log('🔐 小红书扫码登录工具 (Node.js)');
    console.log('='.repeat(60));
    
    try {
        // 检查现有 Cookie
        if (fs.existsSync(ENV_FILE)) {
            const cookieValid = await verifyCookie();
            
            if (cookieValid) {
                console.log('\n✨ 您已经登录，Cookie 仍然有效');
                console.log('💡 如需重新登录，请删除 .env 文件后再运行此脚本');
                
                const response = await askQuestion('\n是否要重新登录？(y/N): ');
                if (response !== 'y') {
                    console.log('👋 保持现有登录状态');
                    return;
                }
                
                console.log('\n🔄 开始重新登录...');
            }
        }
        
        // 执行登录
        const success = await loginWithQRCode();
        
        if (success) {
            console.log('\n' + '='.repeat(60));
            console.log('✅ 登录成功！');
            console.log('='.repeat(60));
            console.log('\n📝 使用方法:');
            console.log('   python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png card_1.png');
            console.log('   或');
            console.log('   node scripts/publish_xhs.js --title "标题" --desc "描述" --images cover.png card_1.png');
        } else {
            console.log('\n' + '='.repeat(60));
            console.log('❌ 登录失败');
            console.log('='.repeat(60));
            process.exit(1);
        }
        
    } catch (error) {
        console.error(`\n❌ 程序异常: ${error.message}`);
        process.exit(1);
    }
}

// 运行主函数
if (require.main === module) {
    main().catch(error => {
        console.error(`\n❌ 未处理的错误: ${error.message}`);
        process.exit(1);
    });
}
