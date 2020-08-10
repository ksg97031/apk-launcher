import click
import os
import shutil
import sys
import time
from adb import adb_commands, usb_exceptions
from androguard.core.bytecodes.apk import APK

import builtins as __builtin__
def print(*args, **kwargs):
    sys.stdout.write('[apk-launcher] ')
    return __builtin__.print(*args, **kwargs)

@click.command()
@click.argument('apk_path')
@click.option('-n', '--nolog', required=False, default=False, is_flag=True)
def run(apk_path, nolog):
    try:
        from adb import sign_m2crypto

        rsa_signer = sign_m2crypto.M2CryptoSigner
    except ImportError:
        try:
            from adb import sign_pythonrsa

            rsa_signer = sign_pythonrsa.PythonRSASigner.FromRSAKeyPath
        except ImportError:
            try:
                from adb import sign_pycryptodome

                rsa_signer = sign_pycryptodome.PycryptodomeAuthSigner
            except ImportError:
                rsa_signer = None

    default = os.path.expanduser('~/.android/adbkey')
    if os.path.isfile(default):
        rsa_key_path = [default]

    adb = adb_commands.AdbCommands()
    devices = list(adb.Devices())
    if len(devices) == 0:
        print("No device")
        return
    elif len(devices) == 1:
        device = devices[0]
    else:
        for idx, device in enumerate(devices):
            print('%d: %s\tdevice' % (idx, device.serial_number))
        device = devices[int(input("Select device: "))-1]

    try:
        adb.ConnectDevice(port_path=device.port_path, rsa_keys=[rsa_signer(path) for path in rsa_key_path])
    except usb_exceptions.ReadFailedError:
        print(f"is your device offline? reconnect your device to pc.")
        sys.exit(-1)
    except Exception as e:
        print(f"kill the current adb session(error msg: {str(e)})")
        os.system("adb kill-server")
        try:
            adb.ConnectDevice(port_path=device.port_path, rsa_keys=[rsa_signer(path) for path in rsa_key_path]) # try again
        except:
            print(f"something wrong.. try reconnect your device to pc and run again.")
            sys.exit(-1)

    apk = APK(apk_path)
    print(f"uninstall {apk.package} package")
    adb.Uninstall(apk.package)

    print(f"reinstall {apk_path} file")
    adb.Install(apk_path, timeout_ms=1000000)
    print(f"start {apk.package} on {apk.get_main_activity()}")
    adb.Shell("am start -n %s/%s" % (apk.package, apk.get_main_activity()))
    if not nolog:
        adb.Logcat('clean')
        time.sleep(1) # wait for activity
        pid = adb.Shell("ps -ef | grep %s | tr -s [:space:] ' ' | cut -d' ' -f2" % apk.package)
        pid = pid.strip()

        print(f"\n\n[ Logcat - {apk.package}({pid}) ]\n") # recommand to use pidcat
        for i in adb.Logcat('| grep -F "%s"' % (pid), 1000000):
            __builtin__.print(i)

if __name__ == '__main__':
    if not shutil.which('adb'):
        print('You need to install adb. (reference, https://stackoverflow.com/a/32314718)')
        sys.exit(-1)
    
    run()
