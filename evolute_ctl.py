# -*- coding: utf-8 -*-
import argparse
import importlib
import os
import os.path
import shutil
import evolute_params
parser = argparse.ArgumentParser(description='customize system args')
parser.add_argument('--run', '-r', help='run system', const=True, nargs='?')
parser.add_argument('--update', '-u', help='update system', const=True, nargs='?')
parser.add_argument('--restart', '-rs', help='restart system', const=True, nargs='?')
parser.add_argument('--kill', '-k', help='kill system', const=True, nargs='?')
parser.add_argument('--status', '-s', help='check system status', const=True, nargs='?')
parser.add_argument('--rollback', '-rb', help='rollback system', const=True, nargs='?')

yml_path = './docker-compose.yml'
github_base = 'https://github.com/EvoluteStudio/evolute-onekeyrun'


def github_download():
    local_version = '20200202'
    rets = os.popen(
        f"curl {github_base}/releases/latest | grep -Eo '[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+'")
    new_version = ''
    for value in rets.readlines():
        if value:
            new_version = value.strip()
    if not new_version:
        print(f'未获取到版本内容，请前往{github_base}/releases/ 查看版本信息>(⊙﹏⊙)<')
        print('Bye~')
        return False, False
    if os.path.exists('./.version'):
        with open('.version', 'r') as f:
            local_version = f.readline()
        if local_version >= new_version:
            print('当前已是最新版本~(￣▽￣)~')
            return False, False
    print('开始更新...')
    # 下载压缩包、替换模板文件、重启
    DOWNLOAD_URL = f"wget --no-check-certificate {github_base}/archive/refs/tags/" + new_version + ".tar.gz"
    if not os.path.exists(f'{new_version}.tar.gz'):
        os.system(DOWNLOAD_URL)
    if not os.path.exists(f'{new_version}.tar.gz'):
        print(f'下载更新包失败>(⊙﹏⊙)<，可以尝试手动下载tar.gz压缩包后安装更新: {DOWNLOAD_URL}')
        return False, False
    os.system(f"tar zxvf {new_version}.tar.gz")
    new_version_dir = f'evolute-onekeyrun-{new_version}'
    cwd = os.getcwd()
    if not os.path.exists(new_version_dir):
        print(f'找不到文件夹: {new_version_dir}')

    for root, dirs, files in os.walk(new_version_dir):
        for file in files:
            if 'evolute_ctl' in file:
                continue
            print(f'update: {file}')
            shutil.move(os.path.join(cwd, root, file), os.path.join(cwd, file))
        for dir in dirs:
            if '.git' in dir:
                continue
            print(f'update: {dir}')
            if os.path.exists(os.path.join(cwd, dir)):
                shutil.rmtree(os.path.join(cwd, dir))
            shutil.move(os.path.join(cwd, root, dir), os.path.join(cwd, dir))
    if os.path.exists(f'{new_version}.tar.gz'):
        os.remove(f'{new_version}.tar.gz')
    if os.path.exists(new_version_dir):
        shutil.rmtree(new_version_dir)
    return local_version, new_version

if __name__ == '__main__':
    # 先检查是否有配置好的文件
    install_check = evolute_params.check_system()
    args = parser.parse_args()
    if args.run:
        if not install_check:
            local_version, new_version = github_download()
            importlib.reload(evolute_params)
            from evolute_params import run_system
            run_system(local_version, new_version)
        else:
            print('检测到您本地已安装相关服务, 退出安装...')
    if args.status:
        from evolute_params import system_status
        system_status()
    if args.update:
        if install_check:
            local_version, new_version = github_download()
            importlib.reload(evolute_params)
            from evolute_params import update_system
            update_system(local_version, new_version)
        else:
            print('Evolute服务未安装或未启动...')
    if args.restart:
        from evolute_params import restart_system
        restart_system()
    if args.kill:
        from evolute_params import kill_system
        kill_system()
    if args.rollback:
        from evolute_params import rollback_system
        rollback_system()

