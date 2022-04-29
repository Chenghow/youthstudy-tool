# 青年大学习工具
## 支持
仅支持广东共青团青年大学习系统
## 目前支持的功能
青年大学习(广东)**每日签到**
**与青年大学习视频团课学习签到无关**
## 使用须知
- 如使用github actions，请在你自己fork的仓库的Settings-Secrets-Actions中分别创建两个名为`XLITEMALLTOKEN`和`PUSHTOKEN`的Secret，并填写你自己的xLitemallToken和pushplus的token（如不使用pushplus请在.github/workflow/mark.yml中将`push: true`改为`push: false`）
- 如本地部署，请在main.py中设定xLitemallToken
## 未来支持的功能
- 青年大学习视频团课学习签到
- 学习频道薅羊毛
  - 刷课赢积分
  - 自动答题赢积分
- ~~微信登录API获取~~