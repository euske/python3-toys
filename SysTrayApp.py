#!/usr/bin/env python

# Prerequisites:
#   Python 2/3 (https://www.python.org/downloads/)
#   Python for Windows (http://sourceforge.net/projects/pywin32/)

import sys
import logging
import win32con
import win32gui
import win32gui_struct


##  SysTrayApp
##
class SysTrayApp(object):

    WM_NOTIFY = None
    WNDCLASS = None
    CLASS_ATOM = None
    _instance = None

    @classmethod
    def _initialize(klass):
        if klass.CLASS_ATOM is not None: return
        WM_RESTART = win32gui.RegisterWindowMessage('TaskbarCreated')
        klass.WM_NOTIFY = win32con.WM_USER+1
        klass.WNDCLASS = win32gui.WNDCLASS()
        klass.WNDCLASS.hInstance = win32gui.GetModuleHandle(None)
        klass.WNDCLASS.lpszClassName = 'Py_'+klass.__name__
        klass.WNDCLASS.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        klass.WNDCLASS.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        klass.WNDCLASS.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        klass.WNDCLASS.hbrBackground = win32con.COLOR_WINDOW
        klass.WNDCLASS.lpfnWndProc = {
            WM_RESTART: klass._restart,
            klass.WM_NOTIFY: klass._notify,
            win32con.WM_CLOSE: klass._close,
            win32con.WM_DESTROY: klass._destroy,
            win32con.WM_COMMAND: klass._command,
            }
        klass.CLASS_ATOM = win32gui.RegisterClass(klass.WNDCLASS)
        klass._instance = {}
        return

    @classmethod
    def _create(klass, hwnd, instance):
        klass._instance[hwnd] = instance
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_ADD,
            (hwnd, 0,
             (win32gui.NIF_ICON | win32gui.NIF_MESSAGE),
             klass.WM_NOTIFY, klass.WNDCLASS.hIcon))
        instance.open()
        return

    @classmethod
    def _restart(klass, hwnd, msg, wparam, lparam):
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_ADD,
            (hwnd, 0,
             (win32gui.NIF_ICON | win32gui.NIF_MESSAGE),
             klass.WM_NOTIFY, klass.WNDCLASS.hIcon))
        self = klass._instance[hwnd]
        self.open()
        return
        
    @classmethod
    def _notify(klass, hwnd, msg, wparam, lparam):
        self = klass._instance[hwnd]
        if lparam == win32con.WM_LBUTTONDBLCLK:
            menu = self.get_popup()
            wid = win32gui.GetMenuDefaultItem(menu, 0, 0)
            win32gui.PostMessage(hwnd, win32con.WM_COMMAND, wid, 0)
        elif lparam == win32con.WM_RBUTTONUP:
            menu = self.get_popup()
            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(hwnd)
            win32gui.TrackPopupMenu(
                menu, win32con.TPM_LEFTALIGN,
                pos[0], pos[1], 0, hwnd, None)
            win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        return True

    @classmethod
    def _close(klass, hwnd, msg, wparam, lparam):
        win32gui.DestroyWindow(hwnd)
        return

    @classmethod
    def _destroy(klass, hwnd, msg, wparam, lparam):
        del klass._instance[hwnd]
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (hwnd, 0))
        win32gui.PostQuitMessage(0)
        return

    @classmethod
    def _command(klass, hwnd, msg, wparam, lparam):
        wid = win32gui.LOWORD(wparam)
        self = klass._instance[hwnd]
        self.choose(wid)
        return

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self._initialize()
        self._hwnd = win32gui.CreateWindow(
            self.CLASS_ATOM, name,
            (win32con.WS_OVERLAPPED | win32con.WS_SYSMENU),
            0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0,
            self.WNDCLASS.hInstance, None)
        self._create(self._hwnd, self)
        self.logger.info('create: name=%r' % name)
        return

    def open(self):
        self.logger.info('open')
        win32gui.UpdateWindow(self._hwnd)
        return

    def run(self):
        self.logger.info('run')
        win32gui.PumpMessages()
        return

    def idle(self):
        return not win32gui.PumpWaitingMessages()

    def close(self):
        self.logger.info('close')
        win32gui.PostMessage(self._hwnd, win32con.WM_CLOSE, 0, 0)
        return

    def set_icon(self, icon):
        self.logger.info('set_icon: %r' % icon)
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_MODIFY,
            (self._hwnd, 0, win32gui.NIF_ICON,
             0, icon))
        return

    def set_text(self, text):
        self.logger.info('set_text: %r' % text)
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_MODIFY,
            (self._hwnd, 0, win32gui.NIF_TIP,
             0, 0, text))
        return
        
    def show_balloon(self, title, text, timeout=1):
        self.logger.info('show_balloon: %r, %r' % (title, text))
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_MODIFY,
            (self._hwnd, 0, win32gui.NIF_INFO,
             0, 0, '', text, timeout, title, win32gui.NIIF_INFO))
        return

    IDI_QUIT = 100
    
    def get_popup(self):
        menu = win32gui.CreatePopupMenu()
        (item, _) = win32gui_struct.PackMENUITEMINFO(text=u'Quit', wID=self.IDI_QUIT)
        win32gui.InsertMenuItem(menu, 0, 1, item)
        win32gui.SetMenuDefaultItem(menu, 0, self.IDI_QUIT)
        (item, _) = win32gui_struct.PackMENUITEMINFO(text=u'Test', wID=123)
        win32gui.InsertMenuItem(menu, 0, 1, item)
        return menu

    def choose(self, wid):
        self.logger.info('choose: wid=%r' % wid)
        if wid == self.IDI_QUIT:
            self.close()
        elif wid == 123:
            win32gui.MessageBox(self._hwnd, u'testing', u'foo', win32con.MB_OK)
        return


# main
def main(argv):
    app = SysTrayApp('foo')
    app.run()
    return
if __name__ == '__main__': sys.exit(main(sys.argv))
