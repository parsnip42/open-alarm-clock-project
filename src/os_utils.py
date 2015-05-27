import subprocess

class OSUtils:
    @staticmethod
    def shutdown():
        subprocess.Popen("/sbin/halt")

    @staticmethod
    def reboot():
        subprocess.Popen("/sbin/reboot")
















