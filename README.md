# evolute-onekeyrun
# 使用Docker部署Evolute本地服务

**环境要求**

Linux   
Python3.6以上   
Nginx

**域名**

**不能直接使用ip地址**，需要提前申请一个域名（支持泛域名），例如：
evolute.netease.com

！注意，如果一个域名不能同时支持http和websocket协议，就需要申请两个域名
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
# WEBSOCKET_DOMAIN 长连接服务的域名（可以和DOMAIN相同）
# EVOLUTE_PORT evolute主站点的端口
# STUDIO_PORT studio服务的端口
# BOARD_PORT EvoluteBoard服务的端口
# WIKI_PORT EvoluteWiki服务的端口
# WEBSOCKET_PORT 长连接服务的端口
# LOGIN_URL 接入登录服务地址
```
**启动服务**
```
python evolute_ctl.py --install 
# 启动完成后，可执行docker-compose ps查看容器是否在正常运行
```
**启动Nginx配置**
```
将evolute_nginx.conf复制到本机的nginx目录下 
执行nginx -s reload
```
直接输入http://$DOMAIN， 即可访问


**数据挂载位置**
```
容器内数据默认挂载路径在./docker
```

**在线更新**

 python evolute_ctl.py --update或
 
 python evolute_ctl.py -u
 
 注：如遇更新失败，系统会自动回退至更新前版本，也可执行“python evolute_ctl.py --rollback”手动回退
 
 其他系统命令
 
 python evolute_ctl.py --help
 
 python evolute_ctl.py --status #查看服务状态
 
 python evolute_ctl.py --restart #重启服务
 
 python evolute_ctl.py --kill #停止服务
 
 python evolute_ctl.py --install #安装服务
  
**离线更新**

 如果在线更新获取安装包失败，可前往https://github.com/EvoluteStudio/evolute-onekeyrun/releases/下载tar.gz压缩包进行离线更新
 下载后放于onekeyrun目录下，执行python evolute_ctl.py --update进行离线更新
  
**log&debug**

 如何查看log?
 
 1、查看docker-compose启动时的log
 
 **docker-compose logs**
 
 2、查看某个容器的log
 
 **docker logs {container-name}**
 
 3、log文件
 
 服务log默认挂载目录为./docker/
 
 四个服务对应的log文件：
 
evolute: ./docker/evertest/volume/logs/

studio: ./docker/studio/volume/logs/

board: ./docker/qaboardvolume/logs/

wiki: ./docker/qawiki/volume/logs/

 4、nginx log
 
 nginx默认log位置为/var/log/nginx/
  
**系统超时**

 1、F12打开浏览器控制台，查看network-->all，找出超时请求地址
 ![image](https://user-images.githubusercontent.com/101565326/168969892-1f793808-ecbc-4b5f-9503-9b59d98deed6.png)
 
 （1）前端资源请求超时，比如.js，.png文件请求超时
 检查服务器是否能连接外网，比如ping evolute.netease.com
 
 （2）后端接口请求超时
 如果超时的请求不是png、js、html等前端静态资源文件，则请查看服务对应的log中是否有trackback
  
**Elasticsearch异常退出**
 启动后如发现elasticsearch Exited，首先查看log
 docker logs evolute_es01或者docker-compose logs
 确认是否有evolute_es01相关的报错；
 例如：
 ![image](https://user-images.githubusercontent.com/101565326/168969910-5b664074-b966-4420-81f3-59c5d3ff578c.png)

 解决方法：从报错信息vm.max_map_count看出内存太小了，所以需要修改vm.max_map_count的内存大小 
 
 （1）切换到root账户：su root
 
 （2）修改sysctl.conf文件， vim /etc/sysctl.conf ：
  ![image](https://user-images.githubusercontent.com/101565326/168969930-36aec0d5-ed67-45cc-aaa6-0ade6f17fe04.png)

 （3）输入命令：sysctl -p
  ![image](https://user-images.githubusercontent.com/101565326/168969946-610250ec-f2b2-45c7-a952-ca55b3fc48c8.png)

 （4）重新启动即可
 python evolute_ctl.py --restart
  
 **无法进入协同编辑**
 
 系统启动后无法进行系统编辑？
 
 （1）首先确认服务容器是否都已成功启动
 
 docker-compose ps
 
 （2）查看log，是否有异常报错
 
 docker logs evolute-wiki-ws
 docker logs evolute-wiki
 
 （3）浏览器查看
 
 （4）在容器内测试连接
 
 为排除nginx配置的干扰，可执行步骤（4）（5）进行检查
 {HOST}:团队域名，比如"team1.evolute.netease.com"
 {COOKIE}: 获取方式可参考步骤（6）
 执行docker exec -it evolute-wiki-ws /bin/bash进入容器，然后执行curl --include --no-buffer --header "Connection: Upgrade" --header "Upgrade: websocket" --header "Host:{HOST}" --header "Origin:http://{HOST}" --header "Sec-WebSocket-Key: PSf47py6tqeN8zMMIA3yyQ==" --header "Sec-WebSocket-Version: 13" --header "Cookie: jwt={COOKIE}" http://evolute-wiki-ws:8000/ws/file/1/
 如果可以连接成功，输出"你是xxx"连接信息，证明websocket服务正常启动；
 
 （5）在宿主机测试连接
 
 {HOST}:团队域名，比如"team1.evolute.netease.com"
 {COOKIE}: 获取方式可参考步骤（6）
 {PORT}: 自己配置的websocket端口
 执行curl --include --no-buffer --header "Connection: Upgrade" --header "Upgrade: websocket" --header "Host:{HOST}" --header "Origin:http://{HOST}" --header "Sec-WebSocket-Key: PSf47py6tqeN8zMMIA3yyQ==" --header "Sec-WebSocket-Version: 13" --header "Cookie: jwt={COOKIE}" http://127.0.0.1:{PORT}/ws/file/1/
 如果（4）（5）都可以连接成功，输出"你是xxx"连接信息，证明websocket服务正常启动，且容器网络正常，可进行下一步尝试；
 
 （6）下载postman工具测试连接：
 
 官网下载地址：https://www.postman.com/
  ![image](https://user-images.githubusercontent.com/101565326/168969976-b6c083e2-e6ba-4efe-bd70-d6a97bed92ac.png)

 1. 进入编辑模式后按f12，重新刷新页面，切到ws标签页，获取ws的链接url
 2. 同时在该页面查看Cookie，复制Cookie内容
 3. 在postman创建新request，选择WebSocket Request，将步骤1获取的ws链接黏贴到地址栏，在headers中创建一条数据，key为Cookie，value为步骤2获取的Cookie内容，然后点击connect
 4、如果（5）、（6）都可以连接，这一步无法使用域名时无法连接，请检查evolute-nginx.conf中的域名配置，也有可能是域名存在某些限制，可咨询一下公司内部网络运维相关同学
