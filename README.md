### 什么是 Selenium 和 webdriver

Selenium 是一个用于自动化浏览器操作的工具，它常用于：

自动化测试（Web UI 测试）

网页数据抓取（爬虫）

自动化日常操作（比如自动登录、表单填写）

webdriver 是 Selenium 的核心组件，它充当浏览器和代码之间的桥梁。通过 webdriver，Python 代码可以控制浏览器行为：打开网页、点击按钮、输入内容、获取信息等。

### 安装 Selenium

在 Python 中使用 Selenium，需要先安装 Selenium 库：

pip install selenium


从 Selenium 4 开始，不再需要单独下载 chromedriver，可以通过 Selenium Manager 自动管理驱动，但也可以手动下载浏览器驱动（ChromeDriver、GeckoDriver 等）。

### Selenium 支持的浏览器

常见浏览器和对应的 webdriver 类：

浏览器	WebDriver 类
Chrome	webdriver.Chrome
Firefox	webdriver.Firefox
Edge	webdriver.Edge
Safari	webdriver.Safari
Opera	webdriver.Opera

selenium.webdriver 是 Selenium 中的核心模块，它让 Python 代码能像人操作浏览器一样执行动作。

启动浏览器

打开网页

查找元素

对元素操作（输入、点击、获取信息）

关闭浏览器

通过 webdriver 可以实现自动化测试、爬虫、数据采集等多种用途。
