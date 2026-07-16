from playwright.sync_api import sync_playwright

def test_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        # 首页 404，测试 plugins 页面
        url = "http://localhost:8080/plugins/index.html"
        print(f"Navigating to {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        print("Page loaded")

        # 1. 截图保存
        screenshot_path = "e:\\Obsidian_notebook\\my-digital-garden\\public\\ui_test_screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        # 2. 检查 body 背景色（应为暖纸张色 #f7f5f0）
        bg_color = page.evaluate("""() => {
            return window.getComputedStyle(document.body).backgroundColor;
        }""")
        print(f"Body background color: {bg_color}")

        # 3. 检查 body 是否有背景纹理（body::before 的 background-image）
        before_content = page.evaluate("""() => {
            const style = window.getComputedStyle(document.body, '::before');
            return {
                content: style.content,
                backgroundImage: style.backgroundImage,
                opacity: style.opacity
            };
        }""")
        print(f"Body::before - content: {before_content['content']}, bgImage: {before_content['backgroundImage'][:80]}..., opacity: {before_content['opacity']}")

        # 4. 检查 h1 字体（应为 Fraunces）
        h1_font = page.evaluate("""() => {
            const h1 = document.querySelector('h1');
            return h1 ? window.getComputedStyle(h1).fontFamily : 'not found';
        }""")
        print(f"H1 font family: {h1_font}")

        # 5. 检查正文字体（应为 Newsreader）
        body_font = page.evaluate("""() => {
            const p = document.querySelector('article p');
            return p ? window.getComputedStyle(p).fontFamily : 'not found';
        }""")
        print(f"Body font family: {body_font}")

        # 6. 检查代码字体（应为 JetBrains Mono）
        code_font = page.evaluate("""() => {
            const code = document.querySelector('code');
            return code ? window.getComputedStyle(code).fontFamily : 'not found';
        }""")
        print(f"Code font family: {code_font}")

        # 7. 检查 secondary 颜色（应为苔藓绿 #3d5a3d）
        secondary_color = page.evaluate("""() => {
            const a = document.querySelector('a.internal');
            return a ? window.getComputedStyle(a).backgroundColor : 'not found';
        }""")
        print(f"Link background color (highlight): {secondary_color}")

        # 8. 检查文章是否有 fadeInUp 动画
        article_animation = page.evaluate("""() => {
            const article = document.querySelector('article');
            return article ? window.getComputedStyle(article).animation : 'not found';
        }""")
        print(f"Article animation: {article_animation}")

        # 9. 检查 pre 圆角（应为 8px）
        pre_radius = page.evaluate("""() => {
            const pre = document.querySelector('pre');
            return pre ? window.getComputedStyle(pre).borderRadius : 'not found';
        }""")
        print(f"Pre border radius: {pre_radius}")

        # 10. 检查 pre 阴影
        pre_shadow = page.evaluate("""() => {
            const pre = document.querySelector('pre');
            return pre ? window.getComputedStyle(pre).boxShadow : 'not found';
        }""")
        print(f"Pre box shadow: {pre_shadow}")

        # 11. 检查自定义滚动条样式（WebKit）
        scrollbar_width = page.evaluate("""() => {
            // 获取滚动条宽度，自定义后应为 8px
            const div = document.createElement('div');
            div.style.overflow = 'scroll';
            div.style.width = '100px';
            div.style.height = '100px';
            document.body.appendChild(div);
            const width = div.offsetWidth - div.clientWidth;
            document.body.removeChild(div);
            return width;
        }""")
        print(f"Scrollbar width: {scrollbar_width}px")

        # 12. 检查 hr 是否为渐变（不是纯色）
        hr_bg = page.evaluate("""() => {
            const hr = document.querySelector('hr');
            return hr ? window.getComputedStyle(hr).backgroundImage : 'not found';
        }""")
        print(f"HR background: {hr_bg[:60] if hr_bg != 'not found' else hr_bg}...")

        browser.close()
        print("\n=== UI Test Complete ===")

if __name__ == "__main__":
    test_ui()
