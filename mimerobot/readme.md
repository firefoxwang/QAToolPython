
##米么微信机器人
通过微信删除米么数据 查询米么测试环境数据 ，比如手机验证码 


##米么微信机器人有哪些功能？
* 用户A登录后，给A发送微信，可以'删除'，'查询'米么数据
* 用户A登录后，在群组里@A，可以'删除'，查询'米么数据
* 直接运行deletealiuat2.1 输入手机号码 删除用户数据，可选是否删除redis，是否删除用户user数据


##如何使用？

* 安装python库 : pymysql, pyodbc,logging,redis,itchat（最新包）, re
* 运行wechatrobot.py
* A用户扫码登录微信，登录完成，路径下的登录二维码自动删除
* B给A微信发送手机号码，查询aliuat手机短信；发送删除信息删除用户数据 
   *  发送：15151863768 查询手机号码
   *  发送：1515186376811 删除所有用户数据  1515186376810 删除redis跟钱包数据 1515186376800 不删除redis只删除钱包数据

##如何配置

* deletealiuat2.1删除 用户数据 可以自己加入sql 跟需要删除的redis，可'单独运行' 
* mimedata 配置查询/删除米么数据的话术



##问题反馈与优化
在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流

* QQ:1228137800

##感激
感谢以下的项目或个人,排名不分先后

* [王永骏]()
* [itchat](https://github.com/littlecodersh/ItChat)
