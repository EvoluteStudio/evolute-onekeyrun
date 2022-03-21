# -*- coding: utf-8 -*-
import argparse
import json
import yaml
import os
import os.path
import shutil

BACKUP_DB = True
BACKUP_MEDIA = True
BACKUP_ES = False

parser = argparse.ArgumentParser(description='customize system args')
parser.add_argument('--domain', '-d', help='set domain')
parser.add_argument('--login', '-l', help='set login')
parser.add_argument('--evertest_port', '-ep', help='set evertest_port')
parser.add_argument('--studio_port', '-sp', help='set studio_port')
parser.add_argument('--wiki_port', '-wp', help='set wiki_port')
parser.add_argument('--board_port', '-bp', help='set board_port')
parser.add_argument('--run', '-r', help='run system', const=True, nargs='?')
parser.add_argument('--kill', '-k', help='kill system', const=True, nargs='?')
parser.add_argument('--check', '-c', help='check system', const=True, nargs='?')
parser.add_argument('--websocket_domain', '-wd', help='set websocket_domain')
parser.add_argument('--websocket_port', '-op', help='set websocket_port')
parser.add_argument('--gunicorn_worker', '-gw', help='set gunicoren worker')
parser.add_argument('--celery_worker', '-cw', help='set celery worker')
success_path = './docker/qawiki/volume/logs/success.txt'

#
sample_settings_path = './sample_customize_settings.json'
sample_yml_path = './sample_docker-compose.yml'
sample_nginx_path = './sample_nginx_demo.conf'

settings_path = './customize_settings.json'
yml_path = './docker-compose.yml'
nginx_path = './evolute_nginx.conf'
success_path = './docker/qawiki/volume/logs/success.txt'


def set_domain(domain):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_EVERTEST_DOMAIN'] = domain
        json.dump(old_settings, new_settings)


def set_login(login):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_LOGIN_URL'] = login
        json.dump(old_settings, new_settings)


def set_sp(sp):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_STUDIO_PORT'] = sp
        json.dump(old_settings, new_settings)


def set_wd(wd):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_WEBSOCKET_DOMAIN'] = wd
        json.dump(old_settings, new_settings)


def set_ep(ep):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_EVERTEST_PORT'] = ep
        json.dump(old_settings, new_settings)


def set_bp(bp):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_BOARD_PORT'] = bp
        json.dump(old_settings, new_settings)


def set_wp(wp):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_WIKI_PORT'] = wp
        json.dump(old_settings, new_settings)


def set_op(op):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_WEBSOCKET_PORT'] = op
        json.dump(old_settings, new_settings)


def set_gw(gw):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        # old_settings['GUNICORN_WORKER'] = gw
        old_settings.update({'GUNICORN_WORKER': gw})
        json.dump(old_settings, new_settings)


def set_cw(cw):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings.update({'CELERY_WORKER': cw})
        json.dump(old_settings, new_settings)


def replace_params(image_tag):
    local_version = '20200202'
    if os.path.exists('.version'):
        with open('.version', 'r') as f:
            local_version = f.readline()
    with open(settings_path, 'r', encoding='utf8') as settings_content:
        settings = json.load(settings_content)
    check_field = ['EVOLUTE_EVERTEST_DOMAIN', 'EVOLUTE_LOGIN_URL', 'EVOLUTE_EVERTEST_PORT', 'EVOLUTE_STUDIO_PORT',
                   'EVOLUTE_WIKI_PORT', 'EVOLUTE_BOARD_PORT', 'EVOLUTE_WEBSOCKET_PORT', 'EVOLUTE_WEBSOCKET_DOMAIN']
    remain_settings = []
    for cf in check_field:
        if not settings.get(cf, ''):
            remain_settings.append(cf)
    if remain_settings:
        res = 'some settings should be seted:'
        for rs in remain_settings:
            res = res + f' {rs},'

        print(res)
        return False

    # 检查通过，根据实际情况修改yml文件
    with open(sample_yml_path, 'r', encoding='utf-8') as yml_settings_content:
        yml_settings = yaml.full_load(yml_settings_content)
        print(yml_settings)

    with open(yml_path, 'w', encoding='utf-8') as yml_settings_content:
        # 替换镜像tag
        yml_settings['services']['evolute']['image'] = 'ncr-partner.nie.netease.com/evolute/evolute-deploy:' + image_tag
        yml_settings['services']['evolute-studio'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-studio:' + image_tag
        yml_settings['services']['celery-board'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-board:' + image_tag
        yml_settings['services']['evolute-board'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-board:' + image_tag
        yml_settings['services']['celery-board-beat'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-board:' + image_tag
        yml_settings['services']['evolute-wiki'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-wiki:' + image_tag
        yml_settings['services']['evolute-wiki-ws'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-wiki:' + image_tag
        yml_settings['services']['celery-wiki-beat'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-wiki:' + image_tag
        yml_settings['services']['celery-wiki'][
            'image'] = 'ncr-partner.nie.netease.com/evolute/evolute-wiki:' + image_tag

        # 修改对应域名和端口
        yml_settings['services']['celery-board']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-board']['environment']['LOCAL_VERSION'] = local_version
        yml_settings['services']['celery-board-beat']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['celery-wiki']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki']['environment']['LOCAL_VERSION'] = local_version
        yml_settings['services']['evolute-wiki']['environment']['WS_DOMAIN'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki-ws']['environment']['WS_DOMAIN'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        # yml_settings['services']['celery-wiki-beat']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute']['environment']['LOCAL_VERSION'] = local_version
        yml_settings['services']['evolute-board']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-studio']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-studio']['environment']['LOCAL_VERSION'] = local_version
        yml_settings['services']['evolute-wiki']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki-ws']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        # yml_settings['services']['db']['environment']['DOMAIN'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute']['ports'] = [f'{settings["EVOLUTE_EVERTEST_PORT"]}:8000']
        yml_settings['services']['evolute-board']['ports'] = [f'{settings["EVOLUTE_BOARD_PORT"]}:8002']
        yml_settings['services']['evolute-studio']['ports'] = [f'{settings["EVOLUTE_STUDIO_PORT"]}:8001']
        yml_settings['services']['evolute-wiki']['ports'] = [f'{settings["EVOLUTE_WIKI_PORT"]}:8003']
        yml_settings['services']['evolute-wiki-ws']['ports'] = [f'{settings["EVOLUTE_WEBSOCKET_PORT"]}:8000']

        # 修改两个celery的worker数
        worker_amount = settings['CELERY_WORKER']
        board_command = yml_settings['services']['celery-board']['command'].split('info')[
                            0] + f'info --concurrency={worker_amount}"'
        yml_settings['services']['celery-board']['command'] = board_command

        wiki_command = yml_settings['services']['celery-wiki']['command'].split('info')[
                           0] + f'info --concurrency={worker_amount}"'
        yml_settings['services']['celery-wiki']['command'] = wiki_command

        # 修改gunicorn的worker数量
        gunicorn_worker = settings['GUNICORN_WORKER']
        yml_settings['services']['evolute-board']['environment']['SERVER_WORKER'] = gunicorn_worker
        yml_settings['services']['evolute-wiki']['environment']['SERVER_WORKER'] = gunicorn_worker

        try:
            # replace_tag
            replace_tag = 'need_replace_evolute_login_url'
            login_url = f'http://{settings["EVOLUTE_EVERTEST_DOMAIN"]}/auth/login_complete/'
            LOGIN_URL = settings["EVOLUTE_LOGIN_URL"]
            yml_settings['services']['evolute']['environment']['LOGIN_URL'] = LOGIN_URL
        except:
            print('set login_url error')
            return False

        yaml.dump(yml_settings, yml_settings_content)

    with open(sample_nginx_path, 'r', encoding='utf-8') as nginx_content:
        nginx_settings = nginx_content.read()
    with open(nginx_path, 'w', encoding='utf-8') as nginx_content:
        nginx_settings = nginx_settings.replace('EVOLUTE_EVERTEST_PORT', str(settings['EVOLUTE_EVERTEST_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_BOARD_PORT', str(settings['EVOLUTE_BOARD_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_WIKI_PORT', str(settings['EVOLUTE_WIKI_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_STUDIO_PORT', str(settings['EVOLUTE_STUDIO_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_DOMAIN', str(settings['EVOLUTE_EVERTEST_DOMAIN']))
        nginx_settings = nginx_settings.replace('EVOLUTE_WEBSOCKET_PORT', str(settings['EVOLUTE_WEBSOCKET_PORT']))
        nginx_content.write(nginx_settings)
    return True


def restart_system(update=False):
    if update:
        try:
            # os.system(f'docker-compose -f {yml_path} down')
            print('docker rm ...')
            os.system(
                f'docker rm -f evolute evolute-board evolute-studio evolute-wiki evolute-wiki-ws wiki_celery board_celery board_celery_beat')
            os.remove(success_path)
        except Exception as e:
            pass
        print('start to update docker images ...')
        os.system('docker-compose pull')
    os.system(f'docker-compose -f {yml_path} up -d --build')
    # res = os.popen('docker-compose ps')
    # for line in res.readlines():
    #     print(line)
    # if 'evolute' in line or 'board' in line or 'wiki' in line:
    #     print(line)

    flag = True
    print('服务启动中，请稍等 ...')
    while flag:
        if not os.path.exists(success_path):
            pass
        else:
            flag = False


def backup_data(version):
    # 备份数据库
    if BACKUP_DB:
        if os.path.exists('./docker/mysql-base'):
            shutil.rmtree('./docker/mysql-base')
        if os.path.exists('./docker/mysql'):
            shutil.copytree('./docker/mysql', f'./docker/mysql-base')
    # 备份文件
    if BACKUP_MEDIA:
        if os.path.exists('./docker/evolute-studio-base'):
            shutil.rmtree('./docker/evolute-studio-base')
        if os.path.exists('./docker/evolute-studio'):
            shutil.copytree('./docker/evolute-studio', f'./docker/evolute-studio-base')
    if BACKUP_ES:
        os.system("docker exec -it evolute-wiki /bin/bash -c './backup_es.sh'")
        # res = os.popen(
        #     "docker exec -it evolute-wiki /bin/bash -c 'curl -XGET  evolute_es01:9200/_snapshot/evolute_backup'")
        # backup_json = '{"type": "fs","settings": {"location": "/usr/share/elasticsearch/backup"}}'
        # backup_cmd = """curl -H 'Content-Type: application/json' -s -XPUT  evolute_es01:9200/_snapshot/evolute_backup -d '{"type": "fs","settings": {"location": "/usr/share/elasticsearch/backup"}}'"""
        # os.system(backup_cmd)
        # os.system(
        #     f"docker exec -it evolute-wiki /bin/bash -c 'curl -XPUT evolute_es01:9200/_snapshot/evolute_backup/snapshot_{version}?wait_for_completion=true'")
    if os.path.exists('./docker-compose.yml.backup'):
        os.remove('./docker-compose.yml.backup')
    shutil.copy('./docker-compose.yml', './docker-compose.yml.backup')
    print('备份完成')
    return True
    # 备份es


def restore_data(version):
    # 恢复数据库
    print('即将回退到上个版本...')
    if os.path.exists('./docker-compose.yml.backup'):
        os.system('docker-compose down')
        if os.path.exists('./docker-compose.yml'):
            os.remove('./docker-compose.yml')
        os.rename('docker-compose.yml.backup', 'docker-compose.yml')
    else:
        print('无法回退至上一个版本')
    if BACKUP_DB:
        if os.path.exists(f'./docker/mysql-base'):
            shutil.rmtree('./docker/mysql')
            os.rename(f'./docker/mysql-base', f'./docker/mysql')
    # 恢复media文件
    if BACKUP_MEDIA:
        if os.path.exists(f'./docker/evolute-studio-base'):
            shutil.rmtree('./docker/evolute-studio')
            os.rename(f'./docker/evolute-studio-base', f'./docker/evolute-studio')
    # 恢复es数据
    if BACKUP_ES and version:
        os.system(
            f"docker exec -it evolute-wiki /bin/bash -c 'curl -XPOST evolute_es01:9200/_snapshot/evolute_backup/snapshot_{version}/_restore?wait_for_completion=true'")


def check_system():
    install_check = False
    res = os.popen('docker ps -a')
    for line in res.readlines():
        if 'evolute-studio' in line:
            install_check = True
            return install_check
    return install_check


def run_install_scripts():
    return


def remove_images(version=''):
    cmd = f"docker images|grep ncr-partner.nie.netease.com|grep {version}|" + "awk '{print $3}'|xargs docker rmi"
    os.system(cmd)


def run_update_scripts():
    result = os.system("docker exec -it evolute /bin/bash -c './run_scripts.sh'")
    if result != 0:
        print('脚本执行失败，可以在./docker/evertest/volume/logs/run_scripts.log中查看详情')
        return False
    result = os.system("docker exec -it evolute-studio /bin/bash -c './run_scripts.sh'")
    if result != 0:
        print('脚本执行失败，可以在./docker/studio/volume/logs/run_scripts.log中查看详情')
        return False
    result = os.system("docker exec -it evolute-board /bin/bash -c './run_scripts.sh'")
    if result != 0:
        print('脚本执行失败，可以在./docker/qaboard/volume/logs/run_scripts.log中查看详情')
        return False
    result = os.system("docker exec -it evolute-wiki /bin/bash -c './run_scripts.sh'")
    if result != 0:
        print('脚本执行失败，可以在./docker/qawiki/volume/logs/run_scripts.log中查看详情')
        return False
    return True


def replace_sample(version):
    try:
        status = replace_params(version)
    except Exception as e:
        print(f'配置文件写入失败，请检查后重新启动： {str(e)}')
        return False
    if status:
        print('配置文件写入完成...')
    return True


def update_system(local_version, new_version):
    if not new_version:
        return
    print('开始备份数据...')
    try:
        backup_flag = backup_data(local_version)
    except Exception as e:
        print(e)
        backup_flag = False
    if not backup_flag:
        skip_backup = input('备份数据失败，是否跳过备份直接更新：y/n?')
        if isinstance(skip_backup, str) and skip_backup.startswith('y'):
            print('开始更新...')
        else:
            return
    status = replace_sample(new_version)
    if not status:
        return
    restart_system(True)
    result = run_update_scripts()
    install_check = check_system()
    if not result or not install_check:
        restore_data(local_version)
        restart_system()
    else:
        with open('.version', 'w') as f:
            f.write(new_version)
        print('更新完成~')
        remove_images(local_version)
    # if install_check:
    #     local_version, new_version = github_download()
    #
    # else:
    #     print('Evolute服务未安装或未启动...')
    #     install_permission = input("是否进行更新重启：y/n？")
    #     if isinstance(install_permission, str) and install_permission.startswith('y'):
    #         run_system()
    #     else:
    #         print('退出...')


def run_system(local_version, new_version):
    run_install_scripts()
    print('开始启动...')
    if not new_version:
        skip_permission = input("获取版本信息失败，是否跳过此次更新直接启动：y/n？")
        if isinstance(skip_permission, str) and skip_permission.startswith('y'):
            print('...')
        else:
            return
    status = replace_sample(new_version)
    if not status:
        return
    restart_system(False)
    with open('.version', 'w') as f:
        f.write(new_version)
    print('启动成功~')

    # # 检查一下是否已经有在启动
    # install_check = check_system()
    # if not install_check:
    #     run_install_scripts()
    #     print('开始启动...')
    #     local_version, new_version = github_download()
    #     if not new_version:
    #         skip_permission = input("获取版本信息失败，是否跳过此次更新直接启动：y/n？")
    #         if isinstance(skip_permission, str) and skip_permission.startswith('y'):
    #             print('...')
    #         else:
    #             return
    #     status = replace_sample(new_version)
    #     if not status:
    #         return
    #     importlib.reload(evolute_params)
    #     evolute_params.restart_system(False)
    #     with open('.version', 'w') as f:
    #         f.write(new_version)
    #     print('启动成功~')
    # else:
    #     update_flag = input('检测到您本地已安装相关服务，是否进行更新：y/n?')
    #     if isinstance(update_flag, str) and update_flag.startswith('y'):
    #         print('开始更新...')
    #         update_system()
    #     print('退出...')
    #     return


def rollback_system():
    local_version = ''
    if os.path.exists('./.version'):
        with open('.version', 'r') as f:
            local_version = f.readline()
    restore_data(local_version)
    print('回退到上个版本...')
    restart_system()


def kill_system():
    os.system(f'docker-compose down')


def system_status():
    res = os.popen('docker-compose ps')
    if not res:
        print('服务未启动~')
        return
    for line in res.readlines():
        print(line)


if __name__ == '__main__':
    # 先检查是否有配置好的文件

    sample_settings_path = './sample_customize_settings.json'
    sample_yml_path = './sample_docker-compose.yml'
    sample_nginx_path = './sample_nginx_demo.conf'

    settings_path = './customize_settings.json'
    yml_path = './docker-compose.yml'
    nginx_path = './evolute_nginx.conf'
    try:
        if os.path.exists(settings_path):
            pass
        else:
            shutil.copy(sample_settings_path, settings_path)

        if os.path.exists(yml_path):
            pass
        else:
            shutil.copy(sample_yml_path, yml_path)

        if os.path.exists(nginx_path):
            pass
        else:
            shutil.copy(sample_nginx_path, nginx_path)
    except:
        pass
    args = parser.parse_args()
    if args.domain:
        set_domain(args.domain)
    if args.login:
        set_login(args.login)
    if args.evertest_port:
        set_ep(args.evertest_port)
    if args.studio_port:
        set_sp(args.studio_port)
    if args.wiki_port:
        set_wp(args.wiki_port)
    if args.board_port:
        set_bp(args.board_port)
    if args.websocket_domain:
        set_wd(args.websocket_domain)
    if args.websocket_port:
        set_op(args.websocket_port)
    if args.gunicorn_worker:
        set_gw(args.gunicorn_worker)
    if args.celery_worker:
        set_cw(args.celery_worker)
