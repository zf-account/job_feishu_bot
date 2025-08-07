# 一、项目介绍

项目应用场景为每天在飞书群中关注24h内更新的校招职位，辅助及时关注新开放的校招职位，提高投递效率。同时，在飞书群中推送未来24h内截止投递的公司，提醒及时投递。

项目主要实现以下功能：
1. 爬取[牛客网](https://www.nowcoder.com)每天更新的校招职位
2. 使用webhook创建飞书机器人，将24h内更新的职位推送到飞书群中
3. 每日定时运行项目，实现定时推送
PS: 本项目爬取信息只为交流学习，fork项目使用请遵守相关法律规定

# 二、使用教程

## 2.1 Install

```sh
pip install -r requirements.txt      
```

## 2.2 设置参数
- 在configs文件夹下，创建文件`config.py`，`config.py`文件中需要包含的内容参考`config_sample.py`

- 关于飞书机器人的创建，参考API文档[自定义机器人使用指南](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN#5a997364)
- 关于`cookies`和`headers`的获取
    - 使用`Chrome`访问牛客网，找到校招日程
    - 使用`F12`快捷键唤出开发者工具
    - 在`Network`界面找到`list_card`，在`Headers`下即可找到
- 添加相关目录，添加完成后这个项目结构如下所示：
```test
├── configs
│   ├── config.py
│   └── config_sampe.py
├── daily_job_notifier.py
├── daily_logs
├── daily_run.sh
├── fetchers
│   ├── hot_recommend_fetcher.py
│   └── job_fetcher.py
├── jobs_data
├── README.md
├── requirements.txt
├── senders
│   ├── apply_deadline_remind_sender.py
│   ├── feishu_sender.py
│   └── tools.py
└── test.py
```
## 2.3 执行
```sh
python daily_job_notifier.py  
```

命令执行完成后，在飞书群中可以看到如下信息：

- 24h内更新的职位推送
![](https://aitotra-picture01-1323869857.cos.ap-beijing.myqcloud.com/typora_img/%E6%88%AA%E5%B1%8F2025-07-26%2019.34.30.png)

- 未来24h截止投递的公司推送
![](https://aitotra-picture01-1323869857.cos.ap-beijing.myqcloud.com/typora_img/%E6%88%AA%E5%B1%8F2025-07-28%2000.54.21.png)

# 三、周期调用
使用 Linux crontab（Linux or MacOS）
1. 编辑 crontab：

```sh
crontab -e
```

2. 添加以下内容（每天上午 10 点定时执行）：
```sh
0 10 * * * /usr/bin/python3 /your/path/daily_job_notifier.py >> /tmp/job_notifier.log 2>&1
```
- 将 /usr/bin/python3 和 /your/path/to/... 替换为你实际的 Python 路径和脚本路径