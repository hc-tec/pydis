
from __future__ import division, absolute_import

import os
import sys
import time
import warnings

def shortPythonVersion():
    """
    Returns the Python version as a dot-separated string.
    """
    return "%s.%s.%s" % sys.version_info[:3]



knownPlatforms = {
    'nt': 'win32',
    'ce': 'win32',
    'posix': 'posix',
    'java': 'java',
    'org.python.modules.os': 'java',
    }



_timeFunctions = {
    #'win32': time.clock,
    'win32': time.time,
    }


class Platform:
    """
    Gives us information about the platform we're running on.
    """

    type = knownPlatforms.get(os.name)
    seconds = staticmethod(_timeFunctions.get(type, time.time))
    _platform = sys.platform

    def __init__(self, name=None, platform=None):
        if name is not None:
            self.type = knownPlatforms.get(name)
            self.seconds = _timeFunctions.get(self.type, time.time)
        if platform is not None:
            self._platform = platform


    def isKnown(self):
        """
        Do we know about this platform?

        @return: Boolean indicating whether this is a known platform or not.
        @rtype: C{bool}
        """
        return self.type != None


    def getType(self):
        """
        Get platform type.

        @return: Either 'posix', 'win32' or 'java'
        @rtype: C{str}
        """
        return self.type


    def isMacOSX(self):
        """
        Check if current platform is macOS.

        @return: C{True} if the current platform has been detected as macOS.
        @rtype: C{bool}
        """
        return self._platform == "darwin"


    def isWinNT(self):
        """
        Are we running in Windows NT?

        This is deprecated and always returns C{True} on win32 because
        Twisted only supports Windows NT-derived platforms at this point.

        @return: C{True} if the current platform has been detected as
            Windows NT.
        @rtype: C{bool}
        """
        warnings.warn(
                "twisted.python.runtime.Platform.isWinNT was deprecated in "
                "Twisted 13.0. Use Platform.isWindows instead.",
                DeprecationWarning, stacklevel=2)
        return self.isWindows()


    def isWindows(self):
        """
        Are we running in Windows?

        @return: C{True} if the current platform has been detected as
            Windows.
        @rtype: C{bool}
        """
        return self.getType() == 'win32'


    def isVista(self):
        """
        Check if current platform is Windows Vista or Windows Server 2008.

        @return: C{True} if the current platform has been detected as Vista
        @rtype: C{bool}
        """
        if getattr(sys, "getwindowsversion", None) is not None:
            return sys.getwindowsversion()[0] == 6
        else:
            return False


    def isLinux(self):
        """
        Check if current platform is Linux.

        @return: C{True} if the current platform has been detected as Linux.
        @rtype: C{bool}
        """
        return self._platform.startswith("linux")


    def _supportsSymlinks(self):
        """
        Check for symlink support usable for Twisted's purposes.

        @return: C{True} if symlinks are supported on the current platform,
                 otherwise C{False}.
        @rtype: L{bool}
        """
        if self.isWindows():
            # We do the isWindows() check as newer Pythons support the symlink
            # support in Vista+, but only if you have some obscure permission
            # (SeCreateSymbolicLinkPrivilege), which can only be given on
            # platforms with msc.exe (so, Business/Enterprise editions).
            # This uncommon requirement makes the Twisted test suite test fail
            # in 99.99% of cases as general users don't have permission to do
            # it, even if there is "symlink support".
            return False
        else:
            # If we're not on Windows, check for existence of os.symlink.
            try:
                os.symlink
            except AttributeError:
                return False
            else:
                return True


    def supportsThreads(self):
        """
        Can threads be created?

        @return: C{True} if the threads are supported on the current platform.
        @rtype: C{bool}
        """
        try:
            import threading
            return threading is not None # shh pyflakes
        except ImportError:
            return False


platform = Platform()
platformType = platform.getType()
seconds = platform.seconds
