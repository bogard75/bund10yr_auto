from pywinauto import Desktop
import ctypes
import time
import pygetwindow as pw


# 윈도우 열거 함수 정의
def enum_windows_proc(hwnd, lparam):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)

    # 클래스 이름 가져오기
    class_name_buff = ctypes.create_unicode_buffer(256)
    ctypes.windll.user32.GetClassNameW(hwnd, class_name_buff, 256)
    
    # 클래스 이름이 "_FNSSClass"인 윈도우 찾기
    if class_name_buff.value == "_FNSSClass":
        # 컨트롤 열거 함수 정의
        def enum_controls_proc(hwnd, lparam):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)

            # 컨트롤 텍스트 출력
            if buff.value:
                print(f"Control handle: {hwnd}, text: {buff.value}")
            return True

        # 컨트롤 중 버튼 컨트롤만 가져오도록
        def enum_button_controls_proc(hwnd, lparam):
            # 클래스 이름 가져오기
            class_name_buff = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, class_name_buff, 256)

            # 클래스 이름이 "Button"인 컨트롤 찾기
            if class_name_buff.value == "Button":
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)

                # 컨트롤 텍스트 출력
                if buff.value:
                    print(f"Button control handle: {hwnd}, text: {buff.value}")
            return True

        # 차일드 윈도우 열거 함수 정의
        def enum_child_windows_proc(hwnd, lparam):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            
            # 창 제목이 "[9502]"로 시작하는 차일드 윈도우 찾기
            if buff.value.startswith("[9502]"):
                print(f"Window handle: {hwnd}, text: {buff.value}")
        
                # 컨트롤 열거 함수 포인터 생성
                EnumChildWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
                enum_controls_proc_ptr = EnumChildWindowsProc(enum_controls_proc)
                
                # 차일드 창 핸들로 컨트롤 열거
                ctypes.windll.user32.EnumChildWindows(hwnd, enum_controls_proc_ptr, 0)
            return True

        # 차일드 윈도우 열거 함수 포인터 생성
        EnumChildWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        enum_child_windows_proc_ptr = EnumChildWindowsProc(enum_child_windows_proc)

        # 차일드 윈도우 열거
        ctypes.windll.user32.EnumChildWindows(hwnd, enum_child_windows_proc_ptr, 0)
    return True


# 윈도우 열거 함수 포인터 생성
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
enum_windows_proc_ptr = EnumWindowsProc(enum_windows_proc)

# 모든 윈도우 열거
ctypes.windll.user32.EnumWindows(enum_windows_proc_ptr, 0)

#find_and_handle_windows()
