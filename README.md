# 青年大学习(广东)工具
![Views](https://views.whatilearened.today/views/github/Chenghow/youthstudy-tool.svg)
[![stars](https://img.shields.io/github/stars/Chenghow/youthstudy-tool.svg?label=Stars)](https://github.com/Chenghow/youthstudy-tool/stargazers)
[![forks](https://img.shields.io/github/forks/Chenghow/youthstudy-tool.svg?label=Forks)](https://github.com/Chenghow/youthstudy-tool/network/members)
[![GitHub contributors](https://img.shields.io/github/contributors/Chenghow/youthstudy-tool?label=Contributors)](https://github.com/Chenghow/youthstudy-tool/graphs/contributors)
[![LICENSE](https://img.shields.io/github/license/Chenghow/youthstudy-tool?label=License)](https://github.com/Chenghow/youthstudy-tool/blob/master/LICENSE)
## 支持
仅支持广东共青团智慧团建系统
## 目前支持的功能
- 青年大学习(广东)每日签到
- 青年大学习视频团课学习签到
- 青年大学习往期视频团课学习签到(需要手动在actions页面运行)
- 学习频道薅羊毛
  - 自动答题赢积分(Beta)
  - 学习频道-广东共青团原创专区(Beta)
  - 学习频道-我们爱学习(Beta)
  - 学习频道-团务小百科(Beta)
- 推送执行结果(默认为微信)
- 多用户批量执行(Beta)
## 使用方法
#### 注：以下所提到的“仓库”皆为你自己Fork的仓库
1. Fork本仓库（更加建议使用[import](https://github.com/new/import)导入本仓库）
2. 在仓库的Settings-Secrets-Actions中分别添加以下两个Secrets并按实际情况填写
    - PUSHTOKEN（pushplus的token，如使用其他推送的话请修改为```推送方法-特定参数```，比如telegram推送的token设置为```telegram-botToken```。**如不需要推送请将`config.ini`中的`push = yes`字段改为`push = no`**）
    - mid 【兼容X-Litemall-Token（可混用），多个请以|隔开】（智慧团建-认证资料-生成电子团员证，点击最下方生成按钮。上传照片页面复制链接 应为：`https://tuan.12355.net/wechat/view/information/member_certification_photo.html?mid=XXXXXXX` 其中XXXXXXX即为mid，X-Litemall-Token需抓包获取，不推荐使用）
      - 举个栗子
        - `8888888|dfajkhdfkjalsdhfalkd.akdjfhalksjdhfalksdfh|1234567`（共三人，二者混用）
        - `1234567|7654321`（共两人，仅使用mid）
        - `dfajkhdfkjalsdhfalkd.akdjfhalksjdhfalksdfh|adfkjahsdkfjlhsld.adsfasdfasdf`（共两人，仅使用X-Litemall-Token）
3. 点击仓库的Actions，再点击“I understand my workflows, go ahead and enable them”的绿色按钮启用actions
4. 在侧边栏找到“GitHub Actions Youthstudy Bot”并点击，再点击右侧的“Enable workflow”启用此action
- 如本地使用请在main.py中手动指定xLitemallToken或mid
- 默认每天中午12点(UTC+8)执行定时任务（由于github action的特性，可能会延迟20分钟左右），如需修改请手动更改`- cron: '0 4 * * *'`字段，生成表达式可以用[https://crontab.guru/](https://crontab.guru/)
- 若想仅在学习签到成功后进行推送，请将`config.ini`中`push`节的`time`值设置为`Success`
## ⚠安全性警告
- 使用mid或者XLITEMALLTOKEN可以通过api获取大量个人信息，请不要在任何地方公开（包括但不限于commit至公开仓库、发表在issue中等等）
- 因此，**请不要在公开仓库的secret以外的任何位置输入您的mid或者XLITEMALLTOKEN**
- 本项目使用了Github Actions，可能违反TOS以导致不可预计的结果（封禁仓库、Github帐号等），使用本项目带来的一切结果由您自己承担
- 建议使用[Github的import功能](https://github.com/new/import)而不是fork以减小风险

## 未来支持的功能
- ~~学习频道薅羊毛~~
  - ~~我们爱学习~~
  - ~~团务小百科~~
- ~~微信登录API获取~~

## 特别感谢
[RnJ4/qndxx_batch_study](https://github.com/RnJ4/qndxx_batch_study)
