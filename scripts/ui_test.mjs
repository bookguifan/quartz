import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  const url = 'http://localhost:8080/plugins/index.html';
  console.log(`Navigating to ${url}`);
  await page.goto(url);
  await page.waitForLoadState('networkidle');
  console.log('Page loaded');

  // 1. 截图
  const screenshotPath = 'e:\\Obsidian_notebook\\my-digital-garden\\public\\ui_test_screenshot.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Screenshot saved to ${screenshotPath}`);

  // 2. Body 背景色
  const bgColor = await page.evaluate(() => window.getComputedStyle(document.body).backgroundColor);
  console.log(`Body background color: ${bgColor}`);

  // 3. body::before 纹理
  const beforeStyle = await page.evaluate(() => {
    const style = window.getComputedStyle(document.body, '::before');
    return {
      content: style.content,
      bgImage: style.backgroundImage.substring(0, 80),
      opacity: style.opacity
    };
  });
  console.log(`Body::before - content: ${beforeStyle.content}, bgImage: ${beforeStyle.bgImage}..., opacity: ${beforeStyle.opacity}`);

  // 4. h1 字体
  const h1Font = await page.evaluate(() => {
    const h1 = document.querySelector('h1');
    return h1 ? window.getComputedStyle(h1).fontFamily : 'not found';
  });
  console.log(`H1 font family: ${h1Font}`);

  // 5. 正文字体
  const bodyFont = await page.evaluate(() => {
    const p = document.querySelector('article p');
    return p ? window.getComputedStyle(p).fontFamily : 'not found';
  });
  console.log(`Body font family: ${bodyFont}`);

  // 6. 代码字体
  const codeFont = await page.evaluate(() => {
    const code = document.querySelector('code');
    return code ? window.getComputedStyle(code).fontFamily : 'not found';
  });
  console.log(`Code font family: ${codeFont}`);

  // 7. 链接背景色（highlight）
  const linkBg = await page.evaluate(() => {
    const a = document.querySelector('a.internal');
    return a ? window.getComputedStyle(a).backgroundColor : 'not found';
  });
  console.log(`Link background color: ${linkBg}`);

  // 8. 文章动画
  const articleAnim = await page.evaluate(() => {
    const article = document.querySelector('article');
    return article ? window.getComputedStyle(article).animation : 'not found';
  });
  console.log(`Article animation: ${articleAnim}`);

  // 9. pre 圆角
  const preRadius = await page.evaluate(() => {
    const pre = document.querySelector('pre');
    return pre ? window.getComputedStyle(pre).borderRadius : 'not found';
  });
  console.log(`Pre border radius: ${preRadius}`);

  // 10. pre 阴影
  const preShadow = await page.evaluate(() => {
    const pre = document.querySelector('pre');
    return pre ? window.getComputedStyle(pre).boxShadow : 'not found';
  });
  console.log(`Pre box shadow: ${preShadow}`);

  // 11. 滚动条宽度
  const scrollbarWidth = await page.evaluate(() => {
    const div = document.createElement('div');
    div.style.overflow = 'scroll';
    div.style.width = '100px';
    div.style.height = '100px';
    document.body.appendChild(div);
    const width = div.offsetWidth - div.clientWidth;
    document.body.removeChild(div);
    return width;
  });
  console.log(`Scrollbar width: ${scrollbarWidth}px`);

  // 12. hr 背景
  const hrBg = await page.evaluate(() => {
    const hr = document.querySelector('hr');
    return hr ? window.getComputedStyle(hr).backgroundImage : 'not found';
  });
  console.log(`HR background: ${hrBg.substring(0, 60)}...`);

  await browser.close();
  console.log('\n=== UI Test Complete ===');
})();
