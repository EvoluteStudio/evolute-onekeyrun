# evolute-onekeyrun
# 使用Docker部署Evolute本地服务

**环境要求**

Linux   
Python3.6以上   
Nginx

**域名**
需提前申请两个域名，例如：
- evolute.netease.com (系统域名)
- evolute-websocket.netease.com （websocket长连接域名）

## 快速开始

**安装docker-compose**

```
# for CentOS
yum install docker-compose -y

# for Ubuntu
apt-get install docker-compose -y
```
**下载压缩包**
前往https://github.com/EvoluteStudio/evolute-onekeyrun/releases/
下载onekeyrun.zip压缩包，并将压缩包放到服务器的指定目录，解压
```
unzip onkeyrun.zip
```
**目录结构**
- create_db             # 初始化数据库脚本
- jvm.options.d         #elasticsearch配置项
- README.md             #
- customize_settings.py #配置项模板
- evolute_ctl.py        #启动脚本
- requirements.txt      
- sample_customize_settings.json #配置项模板
- sample_docker-compose.yml #docker-compose模板文件
- sample_nginx_demo.conf    #nginx模板文件

**安装依赖**
```
# 进入onekeyrun目录
pip install -r requirements.txt
```

**查看配置项**
```
python evolute_ctl.py -h 
```

**填写配置项**
```
python evolute_params.py -d $DOMAIN -wd $WEBSOCKET_DOMAIN -ep $EVOLUTE_PORT -sp $STUDIO_PORT -bp $BOARD_PORT -wp $WIKI_PORT -op $WEBSOCKET_PORT -l ${LOGIN_URL}need_replace_evolute_login_url 
# DOMAIN 主系统的域名
# WEBSOCKET_DOMAIN 长连接服务的域名
# EVOLUTE_PORT evolute主站点的端口
# STUDIO_PORT studio服务的端口
# BOARD_PORT EvoluteBoard服务的端口
# WIKI_PORT EvoluteWiki服务的端口
# WEBSOCKET_PORT 长连接服务的端口
# LOGIN_URL 接入登录服务地址
```
**启动服务**
```
python evolute_ctl.py --run 
# 启动完成后，可执行docker-compose ps查看容器是否在正常运行
```
**启动Nginx配置**
```
将evolute_nginx.conf复制到本机的nginx目录下 
执行nginx -s reload
```
直接输入http://$DOMAIN， 即可访问


**如何更新**
```
#执行启动命令，即可拉取最新镜像进行更新
python evolute_ctl.py --run
```
**数据挂载位置**
```
容器内数据默认挂载路径在./docker
```
