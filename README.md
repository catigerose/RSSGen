# rssgen

`rssgen` 是一个用于抓取新闻网站并生成 RSS/Atom 种子的 Python 项目。

项目当前的组织方式是：

- 每个新闻源对应一个独立脚本，统一放在 `sources/`
- 公共抓取、旧 feed 读取、RSS 写入逻辑统一放在 `feed_funcs.py`
- 生成出来的 XML 文件统一放在 `feeds/`
- `main.py` 会自动扫描 `sources/` 目录下的站点脚本并批量执行

这个项目适合做两类事情：

- 给自己常看的新闻、快讯、电子报生成可订阅的 RSS
- 把没有 RSS 的站点转成可喂给阅读器的 Atom feed

## 项目特点

- 统一了抓取和写入逻辑，减少重复代码
- 主要脚本都补充了中文注释，便于后续维护
- 支持静态页面抓取，也支持 Selenium 抓取动态页面
- 支持从已有 feed 增量更新，避免重复写入历史内容
- `main.py` 已改为自动发现脚本，无需手工维护默认执行列表

## 目录结构

```text
rssgen/
├─ backup/             # 暂时弃用或保留的旧脚本
├─ feeds/              # 生成出来的 Atom XML 文件
├─ feed_funcs.py       # 公共函数：抓取、解析、写入 feed
├─ main.py             # 项目入口，自动执行 sources/ 下的站点脚本
├─ sources/            # 各新闻源对应的独立脚本
├─ pyproject.toml      # 项目依赖与元数据
└─ README.md
```

## 运行环境

- Python `>= 3.11`
- Windows / Linux 均可
- 部分动态页面依赖 Selenium 和本机可用的 Chrome/Chromium WebDriver

项目依赖定义在 [pyproject.toml](/D:/rssgen/pyproject.toml) 中，当前主要包括：

- `requests`
- `beautifulsoup4`
- `lxml`
- `feedgen`
- `feedparser`
- `selenium`
- `pytz`

## 安装依赖

如果你使用 `uv`：

```bash
uv sync
```

如果你使用 `pip`：

```bash
pip install -e .
```

## 运行方式

### 1. 批量执行全部站点脚本

```bash
python main.py
```

`main.py` 会自动扫描 `sources/` 目录下的 `*.py` 文件，并排除以下非站点脚本：

- `__init__.py`

这意味着：

- 你把脚本移到 `backup/` 后，不需要再改 `main.py`
- 你在 `sources/` 里新增一个站点脚本后，也不需要再手动登记

### 2. 执行单个脚本

```bash
python main.py renmrb
python main.py wallstreet_news.py
```

也可以直接执行某个脚本：

```bash
python main.py renmrb
python -m sources.investing
```

## 当前在用脚本

当前 `sources/` 目录下仍在使用、会被 `main.py` 自动发现的脚本包括：

- `cls_telegraph.py`
- `cls_top.py`
- `cmf.py`
- `futunn.py`
- `futunn_live.py`
- `investing.py`
- `jjrb.py`
- `nbd.py`
- `renmrb.py`
- `sjjd.py`
- `tjj.py`
- `wallstreet_news.py`
- `wallstreetcn_live.py`
- `xinhua_focus.py`
- `xwlb.py`
- `zqrb.py`
- `zqsb.py`
- `ztcj.py`

已移到 `backup/`、暂时弃用的脚本不再由 `main.py` 默认执行。

## feeds 目录说明

所有生成出来的 feed 文件都位于 [feeds](/D:/rssgen/feeds)。

每个脚本通常对应一个 XML 文件，例如：

- `renmrb.py` -> `feeds/renmrb.xml`
- `wallstreet_news.py` -> `feeds/wallstreet_news.xml`
- `investing.py` -> 同时生成多个 XML

判断一个脚本当前是否基本正常，通常可以先看：

- 对应 XML 是否存在
- 文件是否不是空壳
- XML 是否可解析
- 是否有 `entry`

## 公共模块说明

[feed_funcs.py](/D:/rssgen/feed_funcs.py) 是整个项目的核心公共模块，主要负责：

- `get_soup`
  抓取网页并返回 `BeautifulSoup` 对象，支持静态请求和 Selenium 动态加载

- `get_entries`
  读取已有 feed 内容，并返回 `FeedEntry` 列表，方便做增量更新

- `append_entry`
  统一向 `FeedEntry` 列表中追加新条目

- `build_feed`
  根据 `FeedEntry` 列表构建 Atom feed

- `persist_feed`
  将结果写回 XML 文件

- `get_json`
  获取 JSON 接口数据

如果以后继续新增站点脚本，建议优先复用这些公共函数，而不是每个脚本重复写一遍网络请求和 feed 输出逻辑。

## 站点脚本的推荐写法

一个新脚本大致遵循下面的流程：

1. 定义站点名称、feed 名称、网站地址
2. 读取旧 feed
3. 抓取列表页或接口数据
4. 根据链接或自定义 guid 去重
5. 调用 `append_entry(...)` 追加内容
6. 调用 `persist_feed(...)` 写出 XML

推荐结构：

```python
def run():
    ...

if __name__ == "__main__":
    run()
```

这样做的好处是：

- 结构统一
- 更容易排查站点改版
- 注释可以只写站点差异部分
- 后续重构成本更低
- 后面做测试、重试和诊断更方便

## 当前已做过的整理

这一轮主要完成了下面这些整理：

- 重构了 `feed_funcs.py`
- 引入了 `FeedEntry` 数据结构，替代 6 个并行列表
- 将公共命名统一为 `get_entries`、`build_feed` 等更直观的名字
- 补充了项目内主要脚本的中文注释
- 修复了多个脚本中旧的 class 选择器失效问题
- 修复了部分报纸脚本的日期、版面拼接和列表长度问题
- 将 `investing.py` 改为直接消费官方 RSS，绕过页面反爬
- 将 `futunn.py`、`nbd.py`、`wallstreet_news.py` 调整为更稳定的列表页方案
- 将站点脚本统一迁移到 `sources/`
- 将 `main.py` 改为自动发现 `sources/` 下的站点脚本

## 已知注意事项

### 1. 某些站点结构变化较快

新闻站点经常改 class 名、HTML 结构或加载方式。一个脚本如果突然失效，优先检查：

- 列表页选择器是否改了
- 详情页正文容器是否改了
- 是否新增了 Cloudflare、验证码、登录校验
- 是否改成了前端异步接口

### 2. 动态页面抓取更慢

使用 Selenium 的脚本会明显比普通 `requests` 更慢。如果站点已经有稳定接口或 RSS，优先使用接口 / RSS。

### 3. 不是所有脚本都适合抓全文

有些站点详情页非常慢、容易超时，或者正文页反爬更强。这种情况下，先保证“列表页标题 + 摘要 + 时间”能稳定生成 feed，通常比硬抓全文更实用。

### 4. 旧脚本建议移到 backup

如果某个站点暂时弃用，建议把脚本移到 `backup/`，这样：

- `main.py` 不会再默认执行它
- 根目录更干净
- 以后需要恢复时也更容易找回

## 常见维护动作

### 新增一个站点脚本

1. 在 `sources/` 目录新增一个 `xxx.py`
2. 按现有脚本风格复用 `feed_funcs.py`
3. 直接运行 `python main.py xxx` 或 `python -m sources.xxx` 测试
4. 成功后运行 `python main.py`

### 暂停某个站点

1. 把脚本移到 `backup/`
2. 保留原来的 XML 以便日后参考

### 检查哪些 feed 有问题

通常优先看 `feeds/` 目录中的 XML：

- 缺文件：脚本可能运行失败或未执行
- 空文件 / 无 entry：脚本可能抓到了空列表
- XML 解析失败：脚本可能写出了损坏内容

## 后续建议

如果后面继续演进这个项目，比较值得做的方向有：

- 增加统一日志输出
- 增加失败重试与超时策略
- 给每个脚本加简单的健康检查
- 将 feed 生成状态汇总成一个报告
- 给部分站点增加更稳定的 API / RSS 方案

## 说明

本项目主要面向个人订阅与信息聚合使用。抓取新闻站点时请注意目标站点的使用条款、访问频率和 robots / 反爬策略，尽量控制请求频率，避免给站点造成不必要压力。
