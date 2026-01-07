import cv2

print("🔍 Testing cameras with DirectShow...")

for index in [0, 1, 2, 3]:
    # Force DirectShow backend
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ Index {index} WORKS! (Resolution: {frame.shape[1]}x{frame.shape[0]})")
            cv2.imshow(f"Camera {index}", frame)
            cv2.waitKey(1000)  # Show for 1 second
            cv2.destroyAllWindows()
        else:
            print(f"❌ Index {index} opens but returns no video (Likely audio-device).")
    else:
        print(f"❌ Index {index} could not be opened.")
    
    cap.release()