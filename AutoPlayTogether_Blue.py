import cv2
import argparse
import imutils
import os
import pyautogui
import time
import numpy as np
from PIL import ImageGrab
import win32gui
import win32ui
import win32con
from win32gui import CreateWindowEx, DragDetect, EnableWindow, FindWindowEx, GetDC, GetDesktopWindow, GetWindowLong, GetWindowRect, Rectangle, SelectObject, SetActiveWindow, SetCapture, SetForegroundWindow, SetWindowLong, SetWindowPos,CreateWindow, UpdateWindow,SendMessage
from win32gui import PostMessage
import threading


#tk.Frame(tk.Tk()).mainloop()
# Cái này là tọa độ nút nhảy, lấy thủ công 1 lần, resize sẽ bị thay đổi tọa độ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


"""
Test Size blue = 791x460
"""

#x=695
#y=346
#position = x | y<<16 
 # Lấy handle của 

Y_Rect = 0

phwnd = FindWindowEx(0, 0,0,"BlueStacks")
hwndInput = FindWindowEx(phwnd, 0, 0, "plrNativeInputWindow")   #Handle Chup man
hwndDraw = FindWindowEx(hwndInput, 0, 0, None)  #handle chup man
# w = 60 # set màn hình 60
# h = 140 # set màn hình 120
#bmpfilenamename = "out.bmp" #lưu file bmp
g_bFindlock = threading.Lock()
g_lockCapture = threading.Lock()
g_EventLock = threading.Event()
def WindowCapture(w=60,h=120,posX=373,posY=Y_Rect):
    g_lockCapture.acquire()
    wDC = win32gui.GetWindowDC(hwndInput)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)  #Định cỡ bitmap cần lấy

    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (posX,posY), win32con.SRCCOPY) #370,63
   # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    #Tối ưu hiệu suất cho OpenCV
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)

    #if loop==100:
    ## Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwndInput, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    g_lockCapture.release()
    #    loop=0
    #2 Chiếc xử lý lỗi 
    #img = img[...,:3]
    #img = np.ascontiguousarray(img) 
    return img

loop_time=time.time()

#g_PosBaoquan = 0
g_bFindMoney = False
#g_bBaoquan=0
# Vòng lặp so sánh --------------------------------------------
def Find_baoquan():
    img_sosanh = cv2.imread('resource\\baoquan.jpg')
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    PosBaoquan=0
    #global g_bBaoquan
    #lock.acquire()
    screenshot = WindowCapture(762-485,429-273,485,273)
    #lock.release()
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Chỉnh kích thước để so sánh
    for scale in np.linspace(0.3, 1, 30)[::-1]:
        resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
        (tH, tW) = resized.shape[:2]
        # So sánh
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxPos) = cv2.minMaxLoc(result)
        locations = np.where(result >= 0.75) # tham số tương đối hình ảnh
        locations = list(zip(*locations[::-1]))
        #print(locations)
        for loc in locations :
            if loc[0] >=0 and loc[1]>=0: #Nếu có locations
                PosBaoquan=maxPos
                return PosBaoquan
    return PosBaoquan
# Load ảnh cần so sánh------------------------------------



def Check_Menu(): 
    img_sosanh = cv2.imread('resource\\menucan.jpg') # 34x64
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    #global g_bFindMoney
    #lock.acquire()
    screenshot = WindowCapture(758-393,65,393,5)
    #lock.release()
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Chỉnh kích thước để so sánh
    for scale in np.linspace(0.4, 1, 30)[::-1]:
        resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
        # So sánh
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.8) # tham số tương đối hình ảnh
        locations = list(zip(*locations[::-1]))
        if locations:
            return True
    return False

def Check_nutsuacan():
    img_sosanh = cv2.imread('resource\\nutsuacan.jpg') # 34x64
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    #global g_bFindMoney
    screenshot = WindowCapture(760-392,428-63,392,63)
    #lock.acquire()
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    #lock.release()
    # Chỉnh kích thước để so sánh
    for scale in np.linspace(0.4, 1, 30)[::-1]:
        resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
        # So sánh
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.75) # tham số tương đối hình ảnh
        locations = list(zip(*locations[::-1]))
        if locations:
            return True
    return False

def Check_cosuacan(): 
    img_sosanh = cv2.imread('resource\\cosuacan.jpg') # 34x64
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    #global g_bFindMoney
    #lock.acquire()
    screenshot = WindowCapture(576-175,358-68,175,68)
    #lock.release
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Chỉnh kích thước để so sánh
    for scale in np.linspace(0.4, 1, 30)[::-1]:
        resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
        # So sánh
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.75) # tham số tương đối hình ảnh
        locations = list(zip(*locations[::-1]))
        if locations:
            return True
    return False

def Check_tiensuacan(): 
    img_sosanh = cv2.imread('resource\\tiensuacan.jpg') # 34x64
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    #global g_bFindMoney
    #lock.acquire()
    screenshot = WindowCapture(576-175,358-68,175,68)
    #lock.release()
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Chỉnh kích thước để so sánh
    for scale in np.linspace(0.4, 1, 30)[::-1]:
        resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
        # So sánh
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.75) # tham số tương đối hình ảnh
        locations = list(zip(*locations[::-1]))
        if locations:
            return True
    return False

def Check_Money():
    img_sosanh = cv2.imread('resource\\money.jpg')
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    PosBaoquan=0
    #global g_bFindMoney
    #lock.acquire()
    screenshot = WindowCapture(769-541,80,541,20)
    #lock.release
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Chỉnh kích thước để so sánh
    for scale in np.linspace(0.3, 1, 30)[::-1]:
        resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
        # So sánh
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.75) # tham số tương đối hình ảnh
        locations = list(zip(*locations[::-1]))
        for loc in locations :
            if loc[0] >=0 and loc[1]>=0: #Nếu có locations
                return True
    return False
def Find_Money_Thread():
    img_sosanh = cv2.imread('resource\\money.jpg')
    img_sosanh = cv2.cvtColor(img_sosanh, cv2.COLOR_BGR2GRAY)
    global g_bFindMoney
    while 1:
        locations=[]
        outscale=False
        #lock.acquire()
        screenshot = WindowCapture(769-541,80,541,20)
        #lock.release()
        #sceenshot = WindowCapture(769-541,80,541,20)
        #prnt(g_bFindMoney)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Capture",screenshot)
        # Chỉnh kích thước để so sánh
        dem=0
        for scale in np.linspace(0.3, 1, 30)[::-1]:
            dem+=1
            resized = imutils.resize(img_sosanh, width = int(img_sosanh.shape[1] * scale))
            (tH, tW) = resized.shape[:2]
            # So sánh
            result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
            #(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            locations = np.where(result >= 0.8) # tham số tương đối hình ảnh
            #print(maxVal,maxLoc)
            locations = list(zip(*locations[::-1]))
            #print(locations)
            if locations:
                for loc in locations :
                    if loc: 
                        
                        #cv2.waitKey()
                        #lock.acquire()
                        g_EventLock.wait()
                        #g_bFindlock.acquire()
                        g_bFindMoney=True
                        #g_bFindlock.release()
                        outscale=True
                        print("TIEN DAY NE")
                        break
                        #return 0   
            else:
                
                #g_bFindlock.acquire() 
                if dem==30:
                    g_EventLock.wait()
                    g_bFindMoney = False
                #g_bFindlock.release()
            #    print("KHONG THE THAY TIEN")

                    
            if outscale: break #out vong for
                #else:
                #cv2.imshow("Capture",screenshot)
                # if cv2.waitKey(1) == ord('q'):
                #     cv2.destroyAllWindows()
                #     break
        time.sleep(0.5)

    return True
# Start Money Find thread
def DrawRect():
    hDC = win32gui.GetDC(hwndDraw)
    win32gui.SelectObject(hDC,win32gui.GetStockObject(win32con.HOLLOW_BRUSH))
    while 1:
        win32gui.Rectangle(hDC,373,Y_Rect,373+60,Y_Rect+120)  # y=63
        time.sleep(0.02)
def Main():
    Canso = g_xSuacan=g_ySuacan=0
    while Canso<1 or Canso >6:
        try:
            Canso = int(input("Chon can so 1-6 : "))
        except:
            print("Nhap so nguyen tu 1-6 dum tao")
    if Canso ==1:
        g_xSuacan=460
        g_ySuacan=206
    elif Canso==2:
        g_xSuacan=577
        g_ySuacan=206
    elif Canso==3:
        g_xSuacan=695
        g_ySuacan=206
    elif Canso==4:
        g_xSuacan=459
        g_ySuacan=354
    elif Canso==5:
        g_xSuacan=577
        g_ySuacan=354
    elif Canso==6:
        g_xSuacan=694
        g_ySuacan=354

    win32gui.MoveWindow(phwnd,300,200,791,460,0)
    threading.Thread(target= DrawRect).start()
    threading.Thread(target = Find_Money_Thread).start()
    global g_bFindMoney
    global loop_time
    g_imgsosanh = cv2.imread('resource\\chamthan.jpg')
    #g_imgsosanh = cv2.cvtColor(g_imgsosanh, cv2.COLOR_BGR2HSV)
    g_imgsosanh = cv2.cvtColor(g_imgsosanh, cv2.COLOR_BGR2GRAY)
    #g_imgsosanh = cv2.Canny(g_imgsosanh, 100, 150)
    while True:
            bsuacan=True
            g_EventLock.set()
            if g_bFindMoney:    # else: # Khi thấy tiền g_bFindMoney == True
                try:
                    # Click Vào túi đồ
                    PostMessage(hwndInput, 513, 1, 729 | (227<<16))
                    PostMessage(hwndInput, 514, 0, 0)
                    # Check Menu
                    for i in range(0,10): #check menu trong 5s
                        if Check_Menu():
                            # Click zô menu
                            PostMessage(hwndInput, 513, 1, 547 | (35<<16))
                            PostMessage(hwndInput, 514, 0, 0)
                            time.sleep(2)
                            #    break
                            #time.sleep(1)
                            #Click xong tìm nút sửa cần
                            #time.sleep(1)
                            while 1:
                                # Tìm nút sửa cần
                                if Check_nutsuacan():
                                    # Click nút sửa cần
                                    PostMessage(hwndInput, 513, 1, g_xSuacan | (g_ySuacan<<16))
                                    PostMessage(hwndInput, 514, 0, 0)
                                    time.sleep(2)
                                    # tim nut tien sua can
                                    if Check_tiensuacan():
                                        # Có chữ tiền sửa cần thì nhấn
                                        PostMessage(hwndInput, 513, 1, 379 | (322<<16))
                                        PostMessage(hwndInput, 514, 0, 0)
                                        time.sleep(3)
                                        # Check Nếu không thấy nút có sửa cẩn
                                        if Check_cosuacan() == False:
                                            # nhấn lại nút sửa cần
                                            continue
                                        else : # Nếu thấy nút có sửa cẩn
                                            # click có sửa cần
                                            PostMessage(hwndInput, 513, 1, 379 | (322<<16))
                                            PostMessage(hwndInput, 514, 0, 0)
                                            time.sleep(2.5)
                                            # click ra bên ngoài
                                            PostMessage(hwndInput, 513, 1, 180 | (200<<16)) # Cần 4
                                            PostMessage(hwndInput, 514, 0, 0)
                                            time.sleep(2)
                                            bsuacan=False
                                            break
                                else: # Nếu không có nút sửa cần
                                    # click ra bên ngoài
                                    PostMessage(hwndInput, 513, 1, 180 | (200<<16)) # Cần 4
                                    PostMessage(hwndInput, 514, 0, 0)
                                    time.sleep(2)
                                    bsuacan=False
                                    break
                        if bsuacan == False: break
                        time.sleep(0.5)
                    if not Check_Menu():
                    # nhấn nút ném cần
                        PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                        PostMessage(hwndInput, 514, 0, 0)
                        time.sleep(0.5)
                        # ném phát nữa cho chắc
                        PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                        PostMessage(hwndInput, 514, 0, 0)
                        time.sleep(3)
                finally:
                    g_EventLock.clear()
                
                #g_EventLock.clear()

            else:
                try:
                    #g_EventLock.set()
                    #g_EventLock.clear()
                    #lock.acquire()
                    g_screenshot = WindowCapture()    #Ảnh đã chụp được từ ứng dụng
                    #lock.release() # Giải phóng lock WindowCapture
                    #print('FPS {}'.format(1/(time.time() - loop_time)))
                    #print(time.time()-loop_time)
                    loop_time=time.time()
                    # Chuyển ảnh đã chụp sang dạng line đen trắng
                    #g_screenshot = cv2.cvtColor(g_screenshot, cv2.COLOR_BGR2HSV)
                    g_screenshot = cv2.cvtColor(g_screenshot, cv2.COLOR_BGR2GRAY)
                    #g_screenshot = cv2.Canny(g_screenshot, 100, 150)
                    #Lặp để  So sánh
                    loc = (0,0)
                    bGiatcan=False
                    # Lặp các kích thước của ảnh chấm than
                    for scale in np.linspace(0.5, 1.5, 30)[::-1]:
                        resized = imutils.resize(g_imgsosanh, width = int(g_imgsosanh.shape[1] * scale))
                        (tH, tW) = resized.shape[:2]
                        # So sánh
                        result = cv2.matchTemplate(g_screenshot, resized, cv2.TM_CCOEFF_NORMED)
                        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
                        locations = np.where(result >= 0.72) # tham số tương đối hình ảnh
                        locations = list(zip(*locations[::-1]))
                        
                    # Nếu có chấm than thì : -----------------------------------------------------------
                        if maxVal >=0.75:
                            #for loc in locations :  #Nếu có locations ( Đã tìm được chấm than)
                            # Send vào nút giật cần
                            print(f'locations: {maxVal}')
                            print(f'locations: {locations}')
                            PostMessage(hwndInput, 513, 1, 670 | (340<<16))
                            PostMessage(hwndInput, 514, 0, 0)
                            time.sleep(0.5)
                            PostMessage(hwndInput, 513, 1, 670 | (340<<16))
                            PostMessage(hwndInput, 514, 0, 0)
                            # Vẽ chữ nhật vào vật tìm đc
                            #cv2.rectangle(g_screenshot, loc,(loc[0] + tW, loc[1] + tH), (255, 255, 255), 2)
                            #cv2.imshow("Capture",g_screenshot)
                            #if cv2.waitKey(1) == ord('q'):
                            #    cv2.destroyAllWindows()
                            # Tìm kiếm nút bảo quản
                            while True:
                            #for i in range (0,12): # nếu 5 giây không thấy thì tiếp tục ném cần
                                if Check_Money(): # check money xem co khong, neu co thi nem can
                                    PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                                    PostMessage(hwndInput, 514, 0, 0)
                                    time.sleep(0.5)
                                    PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                                    PostMessage(hwndInput, 514, 0, 0)
                                    time.sleep(3) # Ném xong đợi 3s cho mất tiền
                                    break
                                if Find_baoquan(): # ttifmn út bảo quản
                                    #while 1:
                                    #posBaoquan = Find_baoquan()
                                    #if posBaoquan: # nếu có nút bảo quản thì
                                    print(f'Thay nut bao quan roi')
                                    # Nhấn nút bao quan
                                    PostMessage(hwndInput, 513, 1, 560 | (335<<16))
                                    PostMessage(hwndInput, 514, 0, 0)
                                    #a=False
                                    # nhấn nút ném cần
                                    #for i in range(0,6): # check trong khoảng 3 s
                                        #g_EventLock.set()
                                        #g_EventLock.clear()
                                        #if g_bFindMoney:
                                    while True:
                                        if Check_Money():
                                            #time.sleep(2)
                                            #Nem can
                                            PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                                            PostMessage(hwndInput, 514, 0, 0)
                                            # Nhấn phát nữa cho chuẩn
                                            time.sleep(0.5)
                                            PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                                            PostMessage(hwndInput, 514, 0, 0)
                                            time.sleep(3)
                                            g_EventLock.set()
                                            g_EventLock.clear()
                                            time.sleep(0.5)
                                            g_bFindMoney = False
                                            bGiatcan=True
                                            break
                                        else: 
                                            print("Nhan bao quan")
                                            
                                                                                    # Nhấn nút bao quan
                                            PostMessage(hwndInput, 513, 1, 560 | (335<<16))
                                            PostMessage(hwndInput, 514, 0, 0)
                                            time.sleep(1)
                                            #break # brick khoi vong tim tien
                                        #time.sleep(0.5)
                                        #if Find_baoquan():
                                        #
                                    if bGiatcan: break # Break While lớn
                                        #    continue
                                else: # else cua FindBaoquan
                                    print("ko thay nut bao quan, tim tiep") 
                                time.sleep(0.5)
                            #----------Hết vòng for
                            # Không thấy bảo quản, nhấn ném cần
                            #print("nhấn ném cần khi thoát khỏi vòng lần nữa")
                            # PostMessage(hwndInput, 513, 1, 612 | (264<<16))
                            # PostMessage(hwndInput, 514, 0, 0)
                            # time.sleep(3) # Ném xong đợi 3s cho mất tiền
                            #cv2.imshow("Capture",screenshot)
                            bGiatcan = True
                            break # break lap locations
                        if bGiatcan: break # Break Scale
                    # Không có chấm than sẽ trở về đầu vòng lặp check hình tiền
                #    cv2.imshow("Capture",g_screenshot)
                #    if cv2.waitKey(1) == ord('q'):
                #        cv2.destroyAllWindows()
                    #break
                        #print(maxVal,maxLoc)
                finally:
                    g_EventLock.clear()

            time.sleep(0.03) # delay 1 chut


Main()

"""
    # ------------ Tìm kiếm all vật thể
    # detector = HomogeneousBgDetector()
    # contours = detector.detect_objects(screenshot)
    # for cnt in contours:
    #     rect = cv2.minAreaRect(cnt)
    #     (xRect, yRect), (wRect, hRect), angle = rect
    #     box = cv2.boxPoints(rect)
    #     box = np.int0(box)
    #     cv2.circle(screenshot, (int(xRect), int(yRect)), 5, (0, 0, 255), -1)
    #     cv2.polylines(screenshot, [box], True, (255, 0, 0), 1)
    # -------------- End
"""

# Cuối chương trình giải phóng DC
# dcObj.DeleteDC()
# cDC.DeleteDC()
# win32gui.ReleaseDC(phwnd, wDC)
# win32gui.DeleteObject(dataBitMap.GetHandle())
#SetForegroundWindow(hwndInput)

#SetActiveWindow(hwndInput)
#PostMessage(phwnd,win32con.WM_ACTIVATE , win32con.WA_ACTIVE,hwndInput)

#PostMessage(0x29035E,win32con.WM_KEYDOWN,win32con.VK_SPACE,0)
#PostMessage(hwndInput,win32con.WM_CHAR,32,0)
#PostMessage(0x29035E,win32con.WM_KEYUP,win32con.VK_SPACE,0)

# hDC = GetDC(hwndDraw)
# SelectObject(hDC,win32gui.GetStockObject(win32con.HOLLOW_BRUSH))
# while 1:
#     Rectangle(hDC,100,100,200,200)  # 



#style = GetWindowLong(hwnd, win32con.GWL_STYLE)
#style = win32con.WS_BORDER | win32con.WS_SIZEBOX
#style = style &~ win32con.WS_CAPTION #style |~ win32con.WS_BORDER #(style &~ win32con.WS_CAPTION) |
#SetWindowLong(hwnd, win32con.GWL_STYLE, style)
#CreateWindow("Classauto","deocotittle",win32con.WS_BORDER|win32con.WS_SIZEBOX,0,0,200,200,0,0,0,None)
#UpdateWindow(hwnd)
#SetWindowPos(phwnd,win32con.HWND_BOTTOM,0,0,800,300,64) 
# 2 cái này phải đi liền nhau
#PostMessage(hwnd, 513, 1, position)
#PostMessage(hwnd, 514, 0, 0)
#-----------------end-----------