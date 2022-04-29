# 青年大学习工具
## 支持
仅支持广东共青团青年大学习系统
## 目前支持的功能
青年大学习(广东)**每日签到**
**与青年大学习视频团课学习签到无关**
## 使用须知
- 如使用github actions，请在你自己fork的仓库的Settings-Secrets-Actions中创建一个名为`XLITEMALLTOKEN`的Secret，并填写你自己的xLitemallToken (**请不要在公开仓库中的main.py中直接设定xLitemallToken，这将不安全**)
- 如本地部署，请在main.py中设定xLitemallToken
## 未来支持的功能
- 青年大学习视频团课学习签到
- 学习频道薅羊毛
  - 刷课赢积分
  - 自动答题赢积分
- ~~微信登录API获取~~