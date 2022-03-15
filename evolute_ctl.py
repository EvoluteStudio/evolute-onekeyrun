# -*- coding: utf-8 -*-
import argparse
import os
import os.path
import shutil

parser = argparse.ArgumentParser(description='customize system args')
parser.add_argument('--run', '-r', help='run system', const=True, nargs='?')
parser.add_argument('--update', '-u', help='update system', const=True, nargs='?')
parser.add_argument('--restart', '-rs', help='restart system', const=True, nargs='?')
parser.add_argument('--kill', '-k', help='kill system', const=True, nargs='?')
parser.add_argument('--status', '-s', help='check system status', const=True, nargs='?')

yml_path = './docker-compose.yml'
github_base = 'https://github.com/EvoluteStudio/evolute-onekeyrun'


def replace_sample():
    # importlib.reload(evolute_params)
    from evolute_params import replace_params
    try:
        status = replace_params()
    except Exception as e:
        print(f'配置文件写入失败，请检查后重新启动： {str(e)}')
        return False
    if status:
        print('配置文件写入完成...')
    return True
    # 修改yml文件里面对应的内容
    # 先检查配置是否齐全

def github_download():
    rets = os.popen(
        f"curl {github_base}/releases/latest | grep -Eo '[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+'")
    new_version = ''
    for value in rets.readlines():
        if value:
            new_version = value.strip()
    if not new_version:
        print(f'未获取到版本内容，请前往{github_base}/releases/，下载压缩包尝试手动安装>(⊙﹏⊙)<')
        print('Bye~')
        return False
    if os.path.exists('./.version'):
        with open('.version', 'r') as f:
            local_version = f.readline()
        if local_version >= new_version:
            print('当前已是最新版本~(￣▽￣)~')
            return False
    print('开始更新...')
    # 下载压缩包、替换模板文件、重启
    DOWNLOAD_URL = f"wget --no-check-certificate {github_base}/archive/refs/tags/" + new_version + ".tar.gz"
    if not os.path.exists(f'{new_version}.tar.gz'):
        os.system(DOWNLOAD_URL)
    if not os.path.exists(f'{new_version}.tar.gz'):
        print(f'下载更新包失败>(⊙﹏⊙)<，可以尝试手动下载tar.gz压缩包后安装更新: {DOWNLOAD_URL}')
        return False
    os.system(f"tar zxvf {new_version}.tar.gz")
    new_version_dir = f'test_version-{new_version[1:]}'
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
            shutil.move(os.path.join(cwd, root, dir), os.path.join(cwd, dir))
    if os.path.exists(f'{new_version}.tar.gz'):
        os.remove(f'{new_version}.tar.gz')
    return new_version



def run_system():
    # 检查一下是否已经有在启动
    install_check = check_system()
    if not install_check:
        print('开始安装...')
        new_version = github_download()
        if not new_version:
            skip_permission = input("获取版本信息失败，是否跳过此次更新直接启动：y/n？")
            if isinstance(skip_permission, str) and skip_permission.startswith('y'):
                print('...')
            else:
                return
        status = replace_sample()
        if not status:
            return
        from evolute_params import restart_system
        restart_system(False)
        with open('.version', 'w') as f:
            f.write(new_version)
        from evolute_params import run_install_scripts
        run_install_scripts()
        print('安装成功~')
    else:
        update_flag = input('检测到您本地已安装相关服务，是否进行更新：y/n?')
        if isinstance(update_flag, str) and update_flag.startswith('y'):
            print('开始更新...')
            update_system()
        print('退出...')
        return


def update_system():
    install_check = check_system()
    if install_check:
        new_version = github_download()
        if not new_version:
            return
        status = replace_sample()
        if not status:
            return
        from evolute_params import restart_system
        restart_system(True)
        with open('.version', 'w') as f:
            f.write(new_version)
        from evolute_params import run_update_scripts
        run_update_scripts()
        print('更新完成~')
    else:
        print('Evolute服务未安装或未启动...')
        install_permission = input("是否进行更新重启：y/n？")
        if isinstance(install_permission, str) and install_permission.startswith('y'):
            run_system()
        else:
            print('退出...')


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
    args = parser.parse_args()
    if args.run:
        run_system()
    if args.status:
        system_status()
    if args.update:
        update_system()
    if args.restart:
        from evolute_params import restart_system, check_system

        restart_system()
    if args.kill:
        kill_system()

