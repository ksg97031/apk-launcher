import os
import click
import time

from adb import adb_commands
from androguard.core.bytecodes.apk import APK

@click.command()
@click.argument('apk_path')
def run(apk_path):
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

    adb.ConnectDevice(port_path=device.port_path, rsa_keys=[rsa_signer(path) for path in rsa_key_path])

    apk = APK(apk_path)
    print("Uninstall")
    adb.Uninstall(apk.package)

    print("Install")
    adb.Install(apk_path, timeout_ms=1000000)
    print("Start")

    print(apk.package, apk.get_main_activity())
    adb.Shell("am start -n %s/%s" % (apk.package, apk.get_main_activity()))
    pid = adb.Shell("ps -ef | grep %s | tr -s [:space:] ' ' | cut -d' ' -f2" % apk.package)

    print("Logcat")
    for i in adb.Logcat('| grep -F "%s"' % (pid), 1000000):
        print(i)

if __name__ == '__main__':
    run()
