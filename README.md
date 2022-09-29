# AutoFishTogether
Tự động câu cá trong play together dùng thư viện nhận dạng hình ảnh và winapi

Vào include thiếu thư viện gì thì pip install về =))

Hô trợ blue stack, cần trình giả lập khác thì nghiên cứu handle cửa sổ và sửa cái code này

phwnd = FindWindowEx(0, 0,0,"BlueStacks")
hwndInput = FindWindowEx(phwnd, 0, 0, "plrNativeInputWindow")   #Handle Chup man
hwndDraw = FindWindowEx(hwndInput, 0, 0, None)  #handle chup man
