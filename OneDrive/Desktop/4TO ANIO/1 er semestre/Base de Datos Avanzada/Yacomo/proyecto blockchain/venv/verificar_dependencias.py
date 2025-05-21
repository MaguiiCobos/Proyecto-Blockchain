try:
    import cv2
    import face_recognition as fr
    import os
    import numpy as np
    from datetime import datetime
    import tkinter as tk
    from tkinter import simpledialog, messagebox

    print("✅ Todas las dependencias están instaladas correctamente.")
except ImportError as e:
    print("❌ Faltan dependencias:", e)
