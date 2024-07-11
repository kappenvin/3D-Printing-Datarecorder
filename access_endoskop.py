import cv2

cap = cv2.VideoCapture(0)
    
if not cap.isOpened():
    print("Error: Could not open camera.")
        
        # Set camera properties (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1294)

focus_value = 100  # Example value, you may need to experiment with this
cap.set(cv2.CAP_PROP_FOCUS, focus_value)



while True:
            # Capture frame-by-frame
    ret, frame = cap.read()
            
    if not ret:
        print("Error: Could not read frame.")
        break
            
    # Display the resulting frame
    cv2.imshow('USB Camera', frame)
            
            # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break