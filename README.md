什么是 Selenium 和 webdriver

Selenium 是一个用于自动化浏览器操作的工具，它常用于：

自动化测试（Web UI 测试）

网页数据抓取（爬虫）

自动化日常操作（比如自动登录、表单填写）

webdriver 是 Selenium 的核心组件，它充当浏览器和代码之间的桥梁。通过 webdriver，Python 代码可以控制浏览器行为：打开网页、点击按钮、输入内容、获取信息等。

2️⃣ 安装 Selenium

在 Python 中使用 Selenium，需要先安装 Selenium 库：

pip install selenium


从 Selenium 4 开始，不再需要单独下载 chromedriver，可以通过 Selenium Manager 自动管理驱动，但也可以手动下载浏览器驱动（ChromeDriver、GeckoDriver 等）。

3️⃣ Selenium 支持的浏览器

常见浏览器和对应的 webdriver 类：

浏览器	WebDriver 类
Chrome	webdriver.Chrome
Firefox	webdriver.Firefox
Edge	webdriver.Edge
Safari	webdriver.Safari
Opera	webdriver.Opera

使用方式类似，区别主要在初始化时使用的浏览器类不同。

4️⃣ 基本用法示例
4.1 打开网页
from selenium import webdriver

# 启动 Chrome 浏览器
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.example.com")

# 获取网页标题
print(driver.title)

# 关闭浏览器
driver.quit()

4.2 查找元素

Selenium 支持多种查找元素的方法：

from selenium.webdriver.common.by import By

# 通过 ID 查找
element = driver.find_element(By.ID, "username")

# 通过 CSS Selector 查找
element = driver.find_element(By.CSS_SELECTOR, ".login-button")

# 通过 XPath 查找
element = driver.find_element(By.XPATH, "//input[@name='password']")


备注：Selenium 4 以后，find_element_by_* 系列方法已废弃，推荐使用 find_element(By, "value")。

4.3 元素操作
# 输入文本
element.send_keys("hello")

# 点击按钮
element.click()

# 获取文本
text = element.text

4.4 浏览器控制
# 前进后退
driver.back()
driver.forward()

# 刷新页面
driver.refresh()

# 获取当前 URL
url = driver.current_url

5️⃣ 高级功能

等待元素出现
Selenium 提供显示等待和隐式等待，解决元素加载慢的问题。

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 显示等待
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)


处理弹窗、iframe、选项卡

执行 JavaScript

driver.execute_script("alert('Hello')")


无头模式（Headless）
浏览器不显示界面，适合后台任务：

from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

6️⃣ 总结

selenium.webdriver 是 Selenium 中的核心模块，它让 Python 代码能像人操作浏览器一样执行动作。基本流程：

启动浏览器

打开网页

查找元素

对元素操作（输入、点击、获取信息）

关闭浏览器

通过 webdriver 可以实现自动化测试、爬虫、数据采集等多种用途。

如果你需要，我可以帮你画一张 webdriver 与浏览器、元素之间的关系图，让整个流程一目了然。
